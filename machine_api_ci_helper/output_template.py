from jinja2 import Template

html_template_string = '''<html>
    <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
        <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
    </head>
    <body>
        <div id="main">
            <button class="btn btn-primary" type="button" data-toggle="collapse" data-target="#maoco" aria-expanded="false" aria-controls="maoco">{{ data['maoco'].name }}</button>
            <div class="collapse k8sobj {{ data['maoco'].status }}" id="maoco">
                <h1>{{ data['maoco'].description }}</h1>
                <div class="k8sraw">
                    <pre>
                        <code>
                            {{ data['maoco'].data }}
                        </code>
                    </pre>
                </div>
        </div>
        </body>
</html>
'''

template = Template(html_template_string)
