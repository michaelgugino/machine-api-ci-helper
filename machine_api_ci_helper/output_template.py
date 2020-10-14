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
        <div id="main">
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
        </div>
    </body>
</html>
'''

template = Template(html_template_string)
