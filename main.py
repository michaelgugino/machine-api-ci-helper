import argparse
import hashlib
import json
import requests
import os
import tempfile
import zlib

from machine_api_ci_helper.types import *
from machine_api_ci_helper.mao import *


def create_artifact_pathstring(basedir, url):
    s = hashlib.sha256(url.encode("utf-8")).hexdigest()
    return os.path.join(basedir, s)

def setup_operators():
    return (MAO(),)

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


    op = OperatorProcessor(setup_operators(), artifact_pathstring, artifacts_url, refetch)



if __name__ == '__main__':
    main()
