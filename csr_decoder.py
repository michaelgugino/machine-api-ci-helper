import argparse
import base64
import json
import os

from cryptography import x509
from cryptography.hazmat.primitives import hashes



def process(csrjson):

    for csr in csrjson['items']:
        b64 = csr['spec']['request']
        pem = base64.b64decode(b64)
        request = x509.load_pem_x509_csr(pem)

        if csr['spec']['username'] == 'system:serviceaccount:openshift-machine-config-operator:node-bootstrapper':
            for name in request.subject:
                if name.oid.dotted_string == "2.5.4.3":
                    print(csr['metadata']['name'])
                    print("   cn name:", name)
                    print("   approver:", csr['status']['conditions'][0]['reason'])
                    print("   creationTimestamp:", csr['metadata']['creationTimestamp'])
                    print("   approved Timestampe:", csr['status']['conditions'][0]['lastUpdateTime'])

def t1():
        sub_alt_names = []
        try:
            alt_names = request.extensions.get_extension_for_class(
                x509.SubjectAlternativeName
            )
            for alt_name in alt_names.value:
                sub_alt_names.append(
                    {"nameType": type(alt_name).__name__, "value": alt_name.value}
                )
            print(sub_alt_names)
        except x509.ExtensionNotFound:
            pass



def main():
    parser = argparse.ArgumentParser(
        description='Parse must gather assets from CI run')
    parser.add_argument('artifact_pathstring', metavar='ARTIFACT_PATHSTRING',
                        help='dir to list of csrs json')

    args = parser.parse_args()

    path = os.path.join(args.artifact_pathstring, "csr.json")

    with open(path, 'rb') as f:
        d = json.load(f)

    process(d)

if __name__ == '__main__':
    main()
