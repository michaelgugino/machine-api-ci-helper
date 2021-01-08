from machine_api_ci_helper.types import *
import machine_api_ci_helper.templates.todo_template

class TODO(Operator):

    assets = set(["machinesets.json", "machines.json", "csr.json", "nodes.json"])
    html_template = machine_api_ci_helper.templates.todo_template.template
    name = "should be set externally"

    def process_artifacts(self, artifacts_dict):
        data = dict()
        data['operator'] = self.get_item_by_name(artifacts_dict['clusteroperators.json'], self.name)
        self.generate_output_data(data)
        self.generate_html()

    def generate_output_data(self, data):
        #self.data is the processed data we use to generate our html.
        self.data['operator'] = self.process_operator(data['operator'])

    @detect_problem
    def process_operator(self, input):
        status = 'ok'
        name = "{} cluster operator status".format(self.name)
        description = '''
                      This is a cluster operator and denotes import status'''
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
