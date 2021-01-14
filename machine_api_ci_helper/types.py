import json
from functools import wraps


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

def detect_problem(func):
    @wraps(func)
    def wrapper(self, *args, **kw):
        kobj = func(self, *args, **kw)
        if kobj.status == 'problem':
            self.status = 'problem'
        print("procssed: {} status {}".format(kobj.name, kobj.status))
        return kobj
    return wrapper

class Operator:

    assets = set()
    gzipped_assets = set()
    html_template = None
    name = "unknown"

    def __init__(self):
        self.rendered_html = ""
        self.data = dict()
        self.status = 'ok'

    def generate_html(self):
        self.rendered_html = self.html_template.render(data=self.data)

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

    def process_scalable(self, input, hasConditions=False):
        status = 'ok'
        available_found = not hasConditions
        desired_replicas = '-1'
        try:
            desired_replicas = input['spec']['replicas']
        except Exception as e:
            status = 'problem'

        try:
            if desired_replicas > 0 and input['status']['availableReplicas'] != desired_replicas:
                status = 'problem'
        except Exception as e:
            status = 'problem'

        if hasConditions:
            if not self.condition_is_true(input, "Available"):
                status = 'problem'

        return status

    @detect_problem
    def process_pod(self, input):
        name = input['metadata']['name']
        description = 'Important pod'
        status = 'ok'
        if not self.condition_is_true(input, "Ready"):
            status = 'problem'
        return K8Obj(name, input, status, description)
