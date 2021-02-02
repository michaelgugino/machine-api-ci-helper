# machine-api-ci-helper

Helps you diagnose what's going on with the machine-api
so you can leave the cloud team alone.

python main.py 'https://gcsweb-ci.apps.ci.l2s4.p1.openshiftapps.com/gcs/origin-ci-test/pr-logs/pull/openshift_machine-api-operator/640/pull-ci-openshift-machine-api-operator-master-e2e-aws/1285194383225786368/artifacts/e2e-aws/gather-extra/'


podman run -it localhost/mapi-helper mapi-ci-helper 'https://gcsweb-ci.apps.ci.l2s4.p1.openshiftapps.com/gcs/origin-ci-test/pr-logs/pull/openshift_machine-api-operator/793/pull-ci-openshift-machine-api-operator-master-e2e-azure/1354912605105295360/artifacts/e2e-azure/gather-extra/'

The above command will store the output in the container's /tmp directory, which
might not be useful unless you can read it :)

You can mount a shared dir into the container to get the output.  Be sure to
chmod 777 this directory.  Here, we use /tmp/t1 (SELinux complains about /tmp itself).

podman run -v /tmp/t1:/tmp/:Z -it localhost/mapi-helper mapi-ci-helper 'https://gcsweb-ci.apps.ci.l2s4.p1.openshiftapps.com/gcs/origin-ci-test/pr-logs/pull/openshift_machine-api-operator/793/pull-ci-openshift-machine-api-operator-master-e2e-azure/1354912605105295360/artifacts/e2e-azure/gather-extra/'
