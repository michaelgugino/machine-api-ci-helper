from machine_api_ci_helper.types import *
import machine_api_ci_helper.templates.mao_template

class MAO(Operator):

    assets = set(["machinesets.json", "machines.json", "csr.json", "nodes.json"])
    html_template = machine_api_ci_helper.templates.mao_template.template
    name = "machine-api"

    def process_artifacts(self, artifacts_dict):
        data = dict()
        data['maoco'] = self.get_item_by_name(artifacts_dict['clusteroperators.json'], "machine-api")
        data['maod'] = self.get_item_by_name(artifacts_dict['deployments.json'], "machine-api-operator")
        data['mao-rs'] = self.get_many_by_ns_and_owner(artifacts_dict['replicasets.json'], 'openshift-machine-api', 'machine-api-operator')
        data['mapi-controllersd'] = self.get_item_by_name(artifacts_dict['deployments.json'], "machine-api-controllers")
        data['mapi-mcrs'] = self.get_many_by_ns_and_owner(artifacts_dict['replicasets.json'], 'openshift-machine-api', 'machine-api-controllers')
        replicaset_names = self.extract_names(data['mapi-mcrs'])
        replicaset_names += self.extract_names(data['mao-rs'])
        mapipods = []
        for name in replicaset_names:
            pods = self.get_many_by_ns_and_owner(artifacts_dict['pods.json'], 'openshift-machine-api', name)
            mapipods += pods
        data['mapipods'] = mapipods

        # CRD Artificats
        # We don't really need to extract anything here, just process later
        data['machinesets'] = artifacts_dict['machinesets.json']['items']
        data['machines'] = artifacts_dict['machines.json']['items']
        data['nodes']  = artifacts_dict['nodes.json']['items']
        data['csr'] = artifacts_dict['csr.json']['items']

        self.generate_output_data(data)
        self.generate_html()

    def generate_output_data(self, data):
        #self.data is the processed data we use to generate our html.
        self.data['maoco'] = self.process_maoco(data['maoco'])
        self.data['maod'] = self.process_maod(data['maod'])
        self.data['mapi-controllersd'] = self.process_mapid(data['mapi-controllersd'])
        self.data['mao-rs'] = list()
        for i in data['mao-rs']:
            self.data['mao-rs'].append(self.process_maors(i))
        self.data['mapi-mcrs'] = list()
        for i in data['mapi-mcrs']:
            self.data['mapi-mcrs'].append(self.process_mapirs(i))
        self.data['mapipods'] = list()
        for p in data['mapipods']:
            self.data['mapipods'].append(self.process_pod(p))
        #machineset/machine dict mapping
        msmd = dict()
        msmd['masters'] = list()
        msmd['unowned'] = list()
        msmd['missing-owner'] = list()
        self.data['machinesets'] = list()
        for ms in data['machinesets']:
            # this will update msmd with each MS name
            self.data['machinesets'].append(self.process_machineset(ms, msmd))
        for m in data['machines']:
            # This will populate populate the corresponding dictlist in msmd
            self.process_machine(m, msmd)
        self.data['msmd'] = msmd
        self.data['csrd'] = self.process_csrs(data['csr'])


    @detect_problem
    def process_csr(self, csr):
        status = 'problem'
        name = "unknown"
        description = 'a CSR'
        try:
            name = csr['metadata']['name']
            del csr['metadata']['managedFields']
        except:
            pass

        try:
            for condition in csr['status']['conditions']:
                if condition['type'] == 'Approved':
                    status = 'ok'
        except Exception as e:
            pass

        return K8Obj(name, csr, status, description)


    def process_csrs(self, input):
        csrd = dict()
        csrd['status'] = 'ok'
        csrd['items'] = list()
        for csr in input:
            kobj = self.process_csr(csr)
            if kobj.status == 'problem':
                csrd['status'] = 'problem'
            csrd['items'].append(kobj)
        return csrd

    @detect_problem
    def process_maoco(self, input):
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


    @detect_problem
    def process_maod(self, input):
        name = "machine-api-operator deployment"
        description = "MAO deployment itself."
        return K8Obj(name, input, self.process_scalable(input, hasConditions=True), description)

    @detect_problem
    def process_maors(self, input):
        name = "machine-api-operator replicaset {}".format(input['metadata']['name'])
        description = "machine-api-operator replicaset"
        return K8Obj(name, input, self.process_scalable(input), description)

    @detect_problem
    def process_mapid(self, input):
        name = "machine-api-controllers deployment"
        description = "machine-api components that do the actual work itself."
        return K8Obj(name, input, self.process_scalable(input, hasConditions=True), description)

    @detect_problem
    def process_mapirs(self, input):
        name = "machine-api-controllers replicaset {}".format(input['metadata']['name'])
        description = "machine-api-controllers replicaset"
        return K8Obj(name, input, self.process_scalable(input), description)

    @detect_problem
    def process_machineset(self, input, msmd):
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

    # Don't wrap this function, it doesn't return a K8Obj instance
    def process_machine(self, input, msmd):
        description = "A machine"
        status = 'ok'
        name = "Broken machine??"

        try:
            name = input['metadata']['name']
            del input['metadata']['managedFields']
        except:
            status = 'problem'
            self.status = 'problem'

        owner = 'unowned'
        # TODO: Determine if master based on role

        try:
            # TODO: account for multiple owner references and grab machineset only.
            owner = input['metadata']['ownerReferences'][0]['name']
        except:
            pass

        try:
            if input['status']['phase'] != "Running":
                status = 'problem'
                self.status = 'problem'
        except:
            status = 'problem'
            self.status = 'problem'

        if owner not in msmd:
            owner = 'missing-owner'

        msmd[owner].append(K8Obj(name, input, status, description))
