# machine-api-ci-helper

Helps you diagnose what's going on with the machine-api
so you can leave the cloud team alone.

python main.py 'https://gcsweb-ci.apps.ci.l2s4.p1.openshiftapps.com/gcs/origin-ci-test/pr-logs/pull/openshift_machine-api-operator/640/pull-ci-openshift-machine-api-operator-master-e2e-aws/1285194383225786368/artifacts/e2e-aws/gather-extra/'

## quickstart with [pipenv](https://pipenv.pypa.io/en/latest/)

install virtual environment and dependencies
```
pipenv install
```

run the helper
```
pipenv run helper https://gcsweb-ci.apps.ci.l2s4.p1.openshiftapps.com/gcs/origin-ci-test/pr-logs/pull/openshift_machine-api-operator/640/pull-ci-openshift-machine-api-operator-master-e2e-aws/1285194383225786368/artifacts/e2e-aws/gather-extra/
```
