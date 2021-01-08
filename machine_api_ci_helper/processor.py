import json
import os
import requests
import machine_api_ci_helper.templates.main
import machine_api_ci_helper.todo
import machine_api_ci_helper.types

class OperatorProcessor:

    def __init__(self, artifact_pathstring, artifacts_url, refetch):
        self.artifact_pathstring = artifact_pathstring
        self.artifacts_url = artifacts_url
        self.assets = set(["deployments.json",
            "replicasets.json", "clusteroperators.json", "pods.json"])
        self.gzipped_assets = set()
        self.artifacts_dict = dict()
        self.errors = []
        self.setup_operators()
        self.__setup_assets()
        self.setup_artifacts(refetch)
        self.add_todo_operators()
        self.process_artifacts()
        self.generate_html()

    def setup_operators(self):
        self.operators = [machine_api_ci_helper.mao.MAO()]

    def add_todo_operators(self):
        knownnames = []
        needed = []
        for operator in self.operators:
            knownnames.append(operator.name)

        allops = machine_api_ci_helper.types.Operator.extract_names(self.artifacts_dict['clusteroperators.json']['items'])
        skn = set(knownnames)
        needed = [x for x in allops if x not in skn]
        for n in needed:
            op = machine_api_ci_helper.todo.TODO()
            op.name = n
            self.operators.append(op)


    def __setup_assets(self):
        for operator in self.operators:
            self.assets.update(operator.assets)
            self.gzipped_assets.update(operator.gzipped_assets)

    def generate_html(self):
        html = machine_api_ci_helper.templates.main.template.render(operators=self.operators)
        # fd, path = tempfile.mkstemp(suffix=".html")
        # with os.fdopen(fd, 'w') as f:
        path = os.path.join(self.artifact_pathstring, "results.html")
        with open(path, 'w') as f:
            f.write(html)

        print("file created:", path)

    def gather(self):
        artifacts_dict = dict()
        for asset in self.assets:
            r = requests.get(self.artifacts_url + asset)
            artifacts_dict[asset] = r.json()
            with open(os.path.join(self.artifact_pathstring, asset), 'wb') as f:
                f.write(r.content)

        for asset in self.gzipped_assets:
            r = requests.get(self.artifacts_url + asset)
            content = zlib.decompress(r.content, zlib.MAX_WBITS|32)
            artifacts_dict[asset] = json.loads(content)
            with open(os.path.join(self.artifact_pathstring, asset), 'wb') as f:
                f.write(content)
        self.artifacts_dict = artifacts_dict

    def read_from_local(self):
        for asset in self.assets.union(self.gzipped_assets):
            try:
                path = os.path.join(self.artifact_pathstring, asset)
                with open(path, 'rb') as f:
                    self.artifacts_dict[asset] = json.load(f)
            except Exception as e:
                err = "Unable to process file {}: {}".format(path, e)
                self.errors.append(err)
                print(err)
                continue

    def setup_artifacts(self, refetch):
        needs_download = False
        if not os.path.exists(self.artifact_pathstring):
            os.mkdir(self.artifact_pathstring)
            needs_download = True
        if needs_download or refetch:
            self.gather()
        else:
            self.read_from_local()

    def process_artifacts(self):
        for operator in self.operators:
            operator.process_artifacts(self.artifacts_dict)
