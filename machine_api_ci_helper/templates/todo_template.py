from jinja2 import Template

html_template_string = '''
<h2>Operator, Deployments, ReplicaSets</h2>
    <button class="btn btn-primary k8sobjstatus{{ data['operator'].status }}" type="button" data-toggle="collapse" data-target="#{{ data['operator'].name }}-operator" aria-expanded="false" aria-controls="maoco">{{ data['operator'].name }}</button>
    <div class="collapse" id="{{ data['operator'].name }}-operator">
        <p>{{ data['operator'].description }}</p>
        <div class="k8sraw">
            <pre>
                <code>
{{ data['operator'].data }}
                </code>
            </pre>
        </div>
    </div>
'''

template = Template(html_template_string)
