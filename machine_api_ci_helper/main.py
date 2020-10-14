import argparse
import json
import requests
import os
import tempfile
import zlib

import output_template

ASSETS = ("machines.json", "nodes.json", "csr.json", "pods.json",
          "clusteroperators.json", "machinesets.json")

GZIPPED_ASSETS = ("deployments.json", "replicasets.json")

class K8Obj:
    data = ''
    name = 'unknown'
    status = 'unknown'
    description = 'none'

    def __init__(self, name, data, status, description):
        self.name = name
        self.data = json.dumps(data, indent=4)
        self.status = status
        self.description = description


def gather(artifacts_url):
    artifacts_dict = dict()
    for asset in ASSETS:
        r = requests.get(artifacts_url + asset)
        artifacts_dict[asset] = r.json()

    for asset in GZIPPED_ASSETS:
        r = requests.get(artifacts_url + asset)
        artifacts_dict[asset] = json.loads(zlib.decompress(r.content, zlib.MAX_WBITS|32))
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

def process_maod(input):
    status = 'ok'
    name = "machine-api-operator deployment"
    description = "MAO deployment itself."
    available_found = False
    try:
        if input['status']['availableReplicas'] != 1:
            status = 'problem'
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

def process_mapid(input):
    status = 'ok'
    name = "machine-api-controllers deployment"
    description = "machine-api components that do the actual work itself."
    available_found = False
    try:
        if input['status']['availableReplicas'] != 1:
            status = 'problem'
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
    return output_data

def generate_output_data(data):
    final = dict()
    final['maoco'] = process_maoco(data['maoco'])
    final['maod'] = process_maod(data['maod'])
    final['mapi-controllersd'] = process_mapid(data['mapi-controllersd'])
    return final

def generate_html(data):
    html = output_template.template.render(data=data)
    fd, path = tempfile.mkstemp(suffix=".html")
    with os.fdopen(fd, 'w') as f:
        f.write(html)

    print("file created:", path)

def main():
    parser = argparse.ArgumentParser(
        description='Parse must gather assets from CI run')
    parser.add_argument('artifacts_url', metavar='ARTIFACTS_URL',
                        help='artifacts url with must gather data')
    args = parser.parse_args()

    artifacts_url = args.artifacts_url
    artifacts_dict = gather(artifacts_url)
    filtered_data = process_artifacts(artifacts_dict)
    output_data = generate_output_data(filtered_data)
    generate_html(output_data)



if __name__ == '__main__':
    main()
