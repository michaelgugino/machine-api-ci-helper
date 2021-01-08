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
