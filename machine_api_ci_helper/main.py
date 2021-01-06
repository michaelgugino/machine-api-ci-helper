import argparse
import hashlib
import json
import requests
import os
import tempfile
import zlib

import output_template
from .types import *

ASSETS = ("machines.json", "nodes.json", "csr.json", "pods.json",
          "clusteroperators.json", "machinesets.json")

GZIPPED_ASSETS = ("deployments.json", "replicasets.json")


def create_artifact_pathstring(basedir, url):
    s = hashlib.sha256(url.encode("utf-8")).hexdigest()
    return os.path.join(basedir, s)

def gather(artifacts_url, artifact_pathstring):
    artifacts_dict = dict()
    for asset in ASSETS:
        r = requests.get(artifacts_url + asset)
        artifacts_dict[asset] = r.json()
        with open(os.path.join(artifact_pathstring, asset), 'wb') as f:
            f.write(r.content)

    for asset in GZIPPED_ASSETS:
        r = requests.get(artifacts_url + asset)
        content = zlib.decompress(r.content, zlib.MAX_WBITS|32)
        artifacts_dict[asset] = json.loads(content)
        with open(os.path.join(artifact_pathstring, asset), 'wb') as f:
            f.write(content)
    return artifacts_dict

def read_from_local(artifact_pathstring):
    artifacts_dict = dict()
    for asset in ASSETS + GZIPPED_ASSETS:
        with open(os.path.join(artifact_pathstring, asset), 'rb') as f:
            artifacts_dict[asset] = json.load(f)
    return artifacts_dict

def setup_artifacts(artifact_pathstring, refetch, artifacts_url):
    needs_download = False
    if not os.path.exists(artifact_pathstring):
        os.mkdir(artifact_pathstring)
        needs_download = True
    artifacts_dict = False
    if needs_download or refetch:
        artifacts_dict = gather(artifacts_url, artifact_pathstring)
    else:
        artifacts_dict = read_from_local(artifact_pathstring)
    return artifacts_dict


def get_mao_from_cluster_operators(cojson):
    print("processing cluster operators")
    maoco = dict()
    for item in cojson['items']:
        try:
            if item['metadata']['name'] != "machine-api":
                continue    # print(maoco)
            del item['metadata']['managedFields']
            maoco = item
        except:
            continue
    return maoco

def get_mao_from_deployments(depjson):
    maod = dict()
    for item in depjson['items']:
        try:
            if item['metadata']['name'] != "machine-api-controllers":
                continue
            del item['metadata']['managedFields']
            maod = item
        except:
            continue
    # print(maoco)
    return maod

def get_item_by_name(il, name):
    wanted = dict()
    try:
        items = il['items']
    except:
        return wanted
    for item in items:
        try:
            if item['metadata']['name'] != name:
                continue
            del item['metadata']['managedFields']
            wanted = item
        except:
            continue
    return wanted

def get_many_by_ns_and_owner(il, ns, owner):
    wanted = []
    try:
        items = il['items']
    except:
        return wanted
    for item in items:
        try:
            if item['metadata']['namespace'] != ns:
                continuetempfile.TemporaryFile
            if item['metadata']['ownerReferences'][0]['name'] != owner:
                continue
            del item['metadata']['managedFields']
            wanted.append(item)
        except:
            continue
    return wanted

def extract_names(items):
    names = []
    for item in items:
        names.append(item['metadata']['name'])
    return names

def process_maoco(input):
    status = 'ok'
    name = "machine-api-operator cluster operator status"
    description = '''
                  This operator status will indicate if we have been able to
                  deploy and roll out the MAO'''
    available_found = False
    try:
        for condition in input['status']['conditions']:
            if condition['type'] == "Available":
                available_found = True

                if condition['status'] != "True":
                    status = 'problem'
                break
    except Exception as e:
        status = 'problem'

    if not available_found:
        status = 'problem'

    return K8Obj(name, input, status, description)

def condition_is_true(input, key):
    try:
        for condition in input['status']['conditions']:
            if condition['type'] == key:
                if condition['status'] == "True":
                    return True
                return False
    except Exception as e:
        return False
    return False

def process_scalable(input, hasConditions=False):
    status = 'ok'
    available_found = not hasConditions
    print("available found1:", available_found)

    try:
        if input['status']['availableReplicas'] != 1:
            status = 'problem'
    except Exception as e:
        status = 'problem'

    if hasConditions:
        if not condition_is_true(input, "Available"):
            status = 'problem'

    print("returning status:", status)
    return status

def process_maod(input):
    name = "machine-api-operator deployment"
    description = "MAO deployment itself."
    return K8Obj(name, input, process_scalable(input, hasConditions=True), description)

def process_maors(input):
    name = "machine-api-operator replicaset {}".format(input['metadata']['name'])
    description = "machine-api-operator replicaset"
    return K8Obj(name, input, process_scalable(input), description)

def process_mapid(input):
    name = "machine-api-controllers deployment"
    description = "machine-api components that do the actual work itself."
    return K8Obj(name, input, process_scalable(input, hasConditions=True), description)

def process_mapirs(input):
    name = "machine-api-controllers replicaset {}".format(input['metadata']['name'])
    description = "machine-api-controllers replicaset"
    return K8Obj(name, input, process_scalable(input), description)

def process_pod(input):
    name = input['metadata']['name']
    description = 'Important pod'
    status = 'ok'
    if not condition_is_true(input, "Ready"):
        status = 'problem'
    return K8Obj(name, input, status, description)

def process_machineset(input, msmd):
    description = "A machineset"
    status = 'ok'
    name = "Broken machineset??"
    try:
        name = input['metadata']['name']
        del input['metadata']['managedFields']
    except:
        status = 'problem'

    msmd[name] = list()

    try:
        AvailableReplicas = input['status']['availableReplicas']
        SpecReplicas = input['spec']['replicas']
        StatusReplicas = input['status']['replicas']
        if SpecReplicas != AvailableReplicas or SpecReplicas != StatusReplicas:
            status = 'problem'
    except:
        status = 'problem'

    return K8Obj(name, input, status, description)

def process_machine(input, msmd):
    description = "A machine"
    status = 'ok'
    name = "Broken machine??"

    try:
        name = input['metadata']['name']
        del input['metadata']['managedFields']
    except:
        status = 'problem'

    owner = 'unowned'
    # TODO: Determine if master based on role

    try:
        # TODO: account for multiple owner references and grab machineset only.
        owner = input['metadata']['ownerReferences'][0]['name']
        print(owner)
    except:
        pass

    try:
        if input['status']['phase'] != "Running":
            status = 'problem'
    except:
        status = 'problem'

    if owner not in msmd:
        owner = 'missing-owner'

    msmd[owner].append(K8Obj(name, input, status, description))



def process_artifacts(artifacts_dict):
    output_data = dict()
    output_data['maoco'] = get_item_by_name(artifacts_dict['clusteroperators.json'], "machine-api")
    output_data['maod'] = get_item_by_name(artifacts_dict['deployments.json'], "machine-api-operator")
    output_data['mao-rs'] = get_many_by_ns_and_owner(artifacts_dict['replicasets.json'], 'openshift-machine-api', 'machine-api-operator')
    output_data['mapi-controllersd'] = get_item_by_name(artifacts_dict['deployments.json'], "machine-api-controllers")
    output_data['mapi-mcrs'] = get_many_by_ns_and_owner(artifacts_dict['replicasets.json'], 'openshift-machine-api', 'machine-api-controllers')
    replicaset_names = extract_names(output_data['mapi-mcrs'])
    replicaset_names += extract_names(output_data['mao-rs'])
    mapipods = []
    for name in replicaset_names:
        pods = get_many_by_ns_and_owner(artifacts_dict['pods.json'], 'openshift-machine-api', name)
        mapipods += pods
    output_data['mapipods'] = mapipods

    # CRD Artificats
    # We don't really need to extract anything here, just process later
    output_data['machinesets'] = artifacts_dict['machinesets.json']['items']
    output_data['machines'] = artifacts_dict['machines.json']['items']
    output_data['nodes']  = artifacts_dict['nodes.json']['items']
    output_data['csr'] = artifacts_dict['csr.json']['items']


    return output_data

def generate_output_data(data):
    final = dict()
    final['maoco'] = process_maoco(data['maoco'])
    final['maod'] = process_maod(data['maod'])
    final['mapi-controllersd'] = process_mapid(data['mapi-controllersd'])
    final['mao-rs'] = list()
    for i in data['mao-rs']:
        final['mao-rs'].append(process_maors(i))
    final['mapi-mcrs'] = list()
    for i in data['mapi-mcrs']:
        final['mapi-mcrs'].append(process_mapirs(i))
    final['mapipods'] = list()
    for p in data['mapipods']:
        final['mapipods'].append(process_pod(p))
    #machineset/machine dict mapping
    msmd = dict()
    msmd['masters'] = list()
    msmd['unowned'] = list()
    msmd['missing-owner'] = list()
    final['machinesets'] = list()
    for ms in data['machinesets']:
        # this will update msmd with each MS name
        final['machinesets'].append(process_machineset(ms, msmd))
    for m in data['machines']:
        # This will populate populate the corresponding dictlist in msmd
        process_machine(m, msmd)
    final['msmd'] = msmd


    return final

def generate_html(operators, artifact_pathstring):
    html = output_template.template.render(operators=operators)
    # fd, path = tempfile.mkstemp(suffix=".html")
    # with os.fdopen(fd, 'w') as f:
    path = os.path.join(artifact_pathstring, "results.html")
    with open(path, 'w') as f:
        f.write(html)

    print("file created:", path)

def main():
    parser = argparse.ArgumentParser(
        description='Parse must gather assets from CI run')
    parser.add_argument('artifacts_url', metavar='ARTIFACTS_URL',
                        help='artifacts url with must gather data')
    parser.add_argument('--output-dir', type=str, default="/tmp",
                        help='Base directory to create output artifacts')
    parser.add_argument('--refetch', type=bool, default=False,
                        help='Re-download artifacts for processing')
    args = parser.parse_args()

    artifacts_url = args.artifacts_url
    output_dir = args.output_dir
    refetch = args.refetch

    if not os.path.exists(output_dir) or not os.path.isdir(output_dir):
        print("output-dir invalid, need existing directory. exiting")
        os.Exit(1)

    artifact_pathstring = create_artifact_pathstring(output_dir, artifacts_url)
    print("Using directory {} for artifacts".format(artifact_pathstring))

    artifacts_dict = setup_artifacts(artifact_pathstring, refetch, artifacts_url)
    filtered_data = process_artifacts(artifacts_dict)
    output_data = generate_output_data(filtered_data)
    # TODO: make this an actual list of operators
    output_data['name'] = "machine-api-operator"
    output_data['status'] = "problem"
    od2 = output_data.copy()
    od2['name'] = "other-operator"
    od2['status'] = "ok"
    operators = (output_data, od2)
    generate_html(operators, artifact_pathstring)



if __name__ == '__main__':
    main()
