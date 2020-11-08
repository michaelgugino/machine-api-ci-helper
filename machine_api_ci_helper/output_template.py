from jinja2 import Template

html_template_string = '''<html>
<head>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
    <style>
    .k8sobjstatusok {background-color: #4CAF50;}
    .k8sobjstatusunknown {background-color: #9c9c9c;}
    .k8sobjstatusproblem {background-color: #FA2569;}
    </style>
</head>
<body>
    <div id="main" class="container-fluid">
        <!-- main row -->
        <div class="row">
            <!-- operator column -->
            <div class="col-sm-6">

                <h1>Cluster Operators</h1>
{% for data in operators %}
                <button class="btn btn-primary k8sobjstatus{{ data['status'] }}" type="button" data-toggle="collapse" data-target="#{{ data['name'] }}" aria-expanded="false" aria-controls="{{ data['name'] }}">{{ data['name'] }}</button>
{% endfor %}
{% for data in operators %}
                <!-- begin operator data block -->
                <div class="collapse" id="{{ data['name'] }}">

                    <div class="row-fluid">
                        <h2>Operator, Deployments, ReplicaSets</h2>

                        <button class="btn btn-primary k8sobjstatus{{ data['maoco'].status }}" type="button" data-target="#maoco" aria-expanded="false" aria-controls="maoco">{{ data['maoco'].name }}</button>
                        <div class="d-none" id="maoco">
                            <p>{{ data['maoco'].description }}</p>
                            <div class="k8sraw">
                                <pre>
                                    <code>
{{ data['maoco'].data }}
                                    </code>
                                </pre>
                            </div>
                        </div>

                        <button class="btn btn-primary k8sobjstatus{{ data['maod'].status }}" type="button" data-target="#maod" aria-expanded="false" aria-controls="maod">{{ data['maod'].name }}</button>
                        <div class="d-none" id="maod">
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
                        <button class="btn btn-primary k8sobjstatus{{ item.status }}" type="button" data-target="#{{ item.name }}" aria-expanded="false" aria-controls="{{ item.name }}">{{ item.name }}</button>
                        <div class="d-none" id="{{ item.name }}">
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

                        <button class="btn btn-primary k8sobjstatus{{ data['mapi-controllersd'].status }}" type="button" data-target="#mapi-controllersd" aria-expanded="false" aria-controls="mapi-controllersd">{{ data['mapi-controllersd'].name }}</button>
                        <div class="d-none" id="mapi-controllersd">
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
                        <button class="btn btn-primary k8sobjstatus{{ item.status }}" type="button" data-target="#{{ item.name }}" aria-expanded="false" aria-controls="{{ item.name }}">{{ item.name }}</button>
                        <div class="d-none" id="{{ item.name }}">
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
                    </div> <!-- end of Operator, Deployments, ReplicaSets -->
                    <hr/>

                    <div class="row-fluid">
                        <h2>Pods</h2>

{% for item in data['mapipods'] %}
                        <button class="btn btn-primary k8sobjstatus{{ item.status }}" type="button" data-target="#{{ item.name }}" aria-expanded="false" aria-controls="{{ item.name }}">{{ item.name }}</button>
                        <div class="d-none" id="{{ item.name }}">
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
                    </div> <!-- end of Pods -->
                    <hr/>

                    <div class="row-fluid">
                        <h2>CRD Artifacts</h2>
                        <div class="row-fluid">
                            <h3>Master Machines</h3>
                            <p>Note: If a master machine is owned by a machineset it won't appear here</p>

{% for item in data['msmd']['masters'] %}
                            <button class="btn btn-primary k8sobjstatus{{ item.status }}" type="button" data-target="#{{ item.name }}" aria-expanded="false" aria-controls="{{ item.name }}">{{ item.name }}</button>
                            <div class="d-none" id="{{ item.name }}">
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
                        </div> <!-- end of Master Machines -->

                        <div class="row-fluid">
                            <h3>Un-Owned</h3>
                            <p>These are machines without an ownerReference (machineset, typically)</p>

{% for item in data['msmd']['unowned'] %}
                            <button class="btn btn-primary k8sobjstatus{{ item.status }}" type="button" data-target="#{{ item.name }}" aria-expanded="false" aria-controls="{{ item.name }}">{{ item.name }}</button>
                            <div class="d-none" id="{{ item.name }}">
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
                        </div> <!-- end of Un-Owned -->

                        <div class="row-fluid">
                            <h3>Missing Owner</h3>
                            <p>These are machines with an ownerReference that is either not a machineset or
                            the corresponding machineset was not found.</p>

{% for item in data['msmd']['missing-owner'] %}
                            <button class="btn btn-primary k8sobjstatus{{ item.status }}" type="button" data-target="#{{ item.name }}" aria-expanded="false" aria-controls="{{ item.name }}">{{ item.name }}</button>
                            <div class="d-none" id="{{ item.name }}">
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
                        </div> <!-- end of Missing Owner -->

                        <div class="row-fluid">
                            <h3>Machine Sets</h3>
                            <p>These are machinesets and any corresponding machines we found.</p>

                            <dl>
{% for item in data['machinesets'] %}
                                <dt>MachineSet: {{ item.name }}</dt>
                                <dd>
                                    <button class="btn btn-primary k8sobjstatus{{ item.status }}" type="button" data-target="#{{ item.name }}" aria-expanded="false" aria-controls="{{ item.name }}">{{ item.name }}</button>
                                    <div class="d-none" id="{{ item.name }}">
                                        <p>{{ item.description }}</p>
                                        <div class="k8sraw">
                                            <pre>
                                                <code>
{{ item.data }}
                                                </code>
                                            </pre>
                                        </div>
                                    </div>

                                    <div class="ml-3">Owned Machines
{% for m in data['msmd'][item.name] %}
                                        <button class="btn btn-primary k8sobjstatus{{ m.status }}" type="button" data-target="#{{ m.name }}" aria-expanded="false" aria-controls="{{ m.name }}">{{ m.name }}</button>
                                        <div class="d-none" id="{{ m.name }}">
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
                                    </div>
                                </dd>
{% endfor %}
                            </dl>
                        </div> <!-- end of Machinesets -->
                    </div> <!-- end of CRD Artifacts -->
                </div> <!-- end of operator data block -->
{% endfor %}
            </div> <!-- end of operator column -->

            <div class="col-sm-6" id="codeview"></div>

        </div> <!-- end of main row -->
    </div> <!-- end of main container -->
<script>
function showCode(event) {
    event.preventDefault()
    var target = event.target
    dataid = target.getAttribute('data-target').substr(1)
    datahtml = document.getElementById(dataid).innerHTML
    cvdiv = document.getElementById('codeview')
    if (target.selected == true) {
        target.selected = false
        cvdiv.innerHTML = ''
    } else {
        resetButtons()
        target.selected = true
        cvdiv.innerHTML = datahtml
    }
}

function resetButtons() {
    const buttons = document.getElementsByTagName('button')
    for (i = 0; i < buttons.length; i++) {
        datatoggle = buttons[i].getAttribute('data-toggle')
        if (datatoggle == undefined) {
            buttons[i].selected = false
            buttons[i].onclick = showCode
        }
    }
}

resetButtons()
</script>
</body>
</html>
'''

template = Template(html_template_string)
