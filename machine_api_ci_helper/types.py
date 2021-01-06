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

    def __init__(self, html_template, needed_artifacts):
        self.html_template = html_template
        self.needed_artifacts = needed_artifacts
        self.rendered_html = ""
        self.data = dict()

    def generate_html(self):
        self.rendered_html = self.html_template.template.render(data=self)
