from jinja2 import Template

html_template_string = '''
<h2>Operator, Deployments, ReplicaSets</h2>
    <button class="btn btn-primary k8sobjstatus{{ data['maoco'].status }}" type="button" data-toggle="collapse" data-target="#maoco" aria-expanded="false" aria-controls="maoco">{{ data['maoco'].name }}</button>
    <div class="collapse" id="maoco">
        <p>{{ data['maoco'].description }}</p>
        <div class="k8sraw">
            <pre>
                <code>
{{ data['maoco'].data }}
                </code>
            </pre>
        </div>
    </div>
    <button class="btn btn-primary k8sobjstatus{{ data['maod'].status }}" type="button" data-toggle="collapse" data-target="#maod" aria-expanded="false" aria-controls="maod">{{ data['maod'].name }}</button>
    <div class="collapse" id="maod">
        <p>{{ data['maod'].description }}</p>
        <div class="k8sraw">
            <pre>
                <code>
{{ data['maod'].data }}
                </code>
            </pre>
        </div>
    </div>

    {% for item in data['mao-rs'] %}
    <button class="btn btn-primary k8sobjstatus{{ item.status }}" type="button" data-toggle="collapse" data-target="#{{ item.name }}" aria-expanded="false" aria-controls="{{ item.name }}">{{ item.name }}</button>
    <div class="collapse" id="{{ item.name }}">
        <p>{{ item.description }}</p>
        <div class="k8sraw">
            <pre>
                <code>
{{ item.data }}
                </code>
            </pre>
        </div>
    </div>
    {% endfor %}

    <button class="btn btn-primary k8sobjstatus{{ data['mapi-controllersd'].status }}" type="button" data-toggle="collapse" data-target="#mapi-controllersd" aria-expanded="false" aria-controls="mapi-controllersd">{{ data['mapi-controllersd'].name }}</button>
    <div class="collapse" id="mapi-controllersd">
        <p>{{ data['mapi-controllersd'].description }}</p>
        <div class="k8sraw">
            <pre>
                <code>
{{ data['mapi-controllersd'].data }}
                </code>
            </pre>
        </div>
    </div>

    {% for item in data['mapi-mcrs'] %}
    <button class="btn btn-primary k8sobjstatus{{ item.status }}" type="button" data-toggle="collapse" data-target="#{{ item.name }}" aria-expanded="false" aria-controls="{{ item.name }}">{{ item.name }}</button>
    <div class="collapse" id="{{ item.name }}">
        <p>{{ item.description }}</p>
        <div class="k8sraw">
            <pre>
                <code>
{{ item.data }}
                </code>
            </pre>
        </div>
    </div>
    {% endfor %}

<br>
<h2>Pods</h2>
    {% for item in data['mapipods'] %}
    <button class="btn btn-primary k8sobjstatus{{ item.status }}" type="button" data-toggle="collapse" data-target="#{{ item.name }}" aria-expanded="false" aria-controls="{{ item.name }}">{{ item.name }}</button>
    <div class="collapse" id="{{ item.name }}">
        <p>{{ item.description }}</p>
        <div class="k8sraw">
            <pre>
                <code>
{{ item.data }}
                </code>
            </pre>
        </div>
    </div>
    {% endfor %}

<br>
<h2>CSRs</h2>
In a healthy cluster, there should be no unapproved CSRs.
<br>
<button class="btn btn-primary k8sobjstatus{{ data['csrd']['status'] }}" type="button" data-toggle="collapse" data-target="#csrs" aria-expanded="false" aria-controls="csrs">CSRs</button>
<div class="collapse" id="csrs">
    {% for item in data['csrd']['items'] %}
    <button class="btn btn-primary k8sobjstatus{{ item.status }}" type="button" data-toggle="collapse" data-target="#{{ item.name }}" aria-expanded="false" aria-controls="{{ item.name }}">{{ item.name }}</button>
    <div class="collapse" id="{{ item.name }}">
        <p>{{ item.description }}</p>
        <div class="k8sraw">
            <pre>
                <code>
{{ item.data }}
                </code>
            </pre>
        </div>
    </div>
    {% endfor %}
</div>

<h2>CRD Artifacts</h2>
<br>
<h3>Master Machines</h3>
Note: If a master machine is owned by a machineset it won't appear here
<br>
    {% for item in data['msmd']['masters'] %}
    <button class="btn btn-primary k8sobjstatus{{ item.status }}" type="button" data-toggle="collapse" data-target="#{{ item.name }}" aria-expanded="false" aria-controls="{{ item.name }}">{{ item.name }}</button>
    <div class="collapse" id="{{ item.name }}">
        <p>{{ item.description }}</p>
        <div class="k8sraw">
            <pre>
                <code>
{{ item.data }}
                </code>
            </pre>
        </div>
    </div>
    {% endfor %}

<br>
<h3>Un-Owned</h3>
These are machines without an ownerReference (machineset, typically)
<br>

    {% for item in data['msmd']['unowned'] %}
    <button class="btn btn-primary k8sobjstatus{{ item.status }}" type="button" data-toggle="collapse" data-target="#{{ item.name }}" aria-expanded="false" aria-controls="{{ item.name }}">{{ item.name }}</button>
    <div class="collapse" id="{{ item.name }}">
        <p>{{ item.description }}</p>
        <div class="k8sraw">
            <pre>
                <code>
{{ item.data }}
                </code>
            </pre>
        </div>
    </div>
    {% endfor %}

<br>
<h3>Missing Owner</h3>
These are machines with an ownerReference that is either not a machineset or
the corresponding machineset was not found.
<br>

    {% for item in data['msmd']['missing-owner'] %}
    <button class="btn btn-primary k8sobjstatus{{ item.status }}" type="button" data-toggle="collapse" data-target="#{{ item.name }}" aria-expanded="false" aria-controls="{{ item.name }}">{{ item.name }}</button>
    <div class="collapse" id="{{ item.name }}">
        <p>{{ item.description }}</p>
        <div class="k8sraw">
            <pre>
                <code>
{{ item.data }}
                </code>
            </pre>
        </div>
    </div>
    {% endfor %}

<br>
<h3>Machine Sets</h3>
These are machinesets and any corresponding machines we found.
<br>

{% for item in data['machinesets'] %}
<h4>MachineSet: {{ item.name }}</h4>
    <button class="btn btn-primary k8sobjstatus{{ item.status }}" type="button" data-toggle="collapse" data-target="#{{ item.name }}" aria-expanded="false" aria-controls="{{ item.name }}">{{ item.name }}</button>
    <div class="collapse" id="{{ item.name }}">
        <p>{{ item.description }}</p>
        <div class="k8sraw">
            <pre>
                <code>
{{ item.data }}
                </code>
            </pre>
        </div>
    </div>

<br>
<h5>Owned Machines</h5>
{% for m in data['msmd'][item.name] %}
    <button class="btn btn-primary k8sobjstatus{{ m.status }}" type="button" data-toggle="collapse" data-target="#{{ m.name }}" aria-expanded="false" aria-controls="{{ m.name }}">{{ m.name }}</button>
    <div class="collapse" id="{{ m.name }}">
        <p>{{ m.description }}</p>
        <div class="k8sraw">
            <pre>
                <code>
{{ m.data }}
                </code>
            </pre>
        </div>
    </div>
{% endfor %}
<br>
{% endfor %}
'''

template = Template(html_template_string)
