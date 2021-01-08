import json


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

class Operator:

    def __init__(self):
        self.html_template = None
        self.rendered_html = ""
        self.data = dict()
        self.assets = set()
        self.gzipped_assets = set()
        self.status = 'ok'

    def generate_html(self):
        self.rendered_html = self.html_template.template.render(data=self.data)

    def process_artifacts(self, artifacts_dict):
        # define this in child class
        pass

    @staticmethod
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
                try:
                    del item['metadata']['managedFields']
                except:
                    pass
                wanted = item
            except:
                continue
        return wanted

    @staticmethod
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

    @staticmethod
    def extract_names(items):
        names = []
        for item in items:
            names.append(item['metadata']['name'])
        return names

    @staticmethod
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

    @staticmethod
    def process_scalable(input, hasConditions=False):
        status = 'ok'
        available_found = not hasConditions
        print("available found1:", available_found)
        desired_replicas = '-1'
        try:
            desired_replicas = input['spec']['replicas']
        except Exception as e:
            status = 'problem'

        try:
            if input['status']['availableReplicas'] != desired_replicas:
                status = 'problem'
        except Exception as e:
            status = 'problem'

        if hasConditions:
            if not condition_is_true(input, "Available"):
                status = 'problem'

        print("returning status:", status)
        return status

    def process_pod(self, input):
        name = input['metadata']['name']
        description = 'Important pod'
        status = 'ok'
        if not condition_is_true(input, "Ready"):
            status = 'problem'
        return K8Obj(name, input, status, description)

class OperatorProcessor:

    def __init__(self, operators, artifact_pathstring, artifacts_url):
        self.operators = operators
        self.artifact_pathstring = artifact_pathstring
        self.artifacts_url = artifacts_url
        self.assets = set("deployments.json",
            "replicasets.json", "clusteroperators.json", "pods.json")
        self.gzipped_assets = set()
        self.artifacts_dict = dict()
        self.errors = []
        self.__setup_assets()

    def __setup_assets(self):
        for operator in self.operators:
            self.assets.update(operator.assets)
            self.gzipped_assets.update(operator.gzipped_assets)

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
        return artifacts_dict

    def read_from_local(self):
        for asset in self.assets + self.gzipped_assets:
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
        artifacts_dict = False
        if needs_download or refetch:
            self.gather()
        else:
            self.read_from_local()
