# Events

Entry point for all Dripp.ai iOS app stuff, all calls are 
routed through events API, which are then routed to appropriate
topics and actioned by various microservice listeners. 
All deployment is kubernetes based.

## Build instructions:
Always make sure you are working off a venv. conda envs are fine too (and preferred)

### Pre-requisite:
Ensure that aws cli is installed.

### Actions
0.

- Clear our dist dir 
- Delete existing packages and distribution:

```
aws codeartifact delete-package-versions --domain goldilocksfashion --domain-owner 730335644490 --repository dripp-ai-infrastructure --format pypi  --package dripp_events --versions 0.1.0

```
- Run packaging command:

```
python setup.py sdist bdist_wheel
```

1. login

```
    aws codeartifact login --tool pip --repository dripp-ai-infrastructure --domain goldilocksfashion --domain-owner 730335644490 --region us-west-2
```
2. Ensure that you have pypirc updated (~/.pypirc) is 
like repositories file for sbt that lists indexes pip has to
grab data from.

3. Ensure you have twine installed otherwise run:

```
pip install twine
```

3.
```
run  following command (see distribute.sh)
aws codeartifact put-package-versions \
    --domain goldilocksfashion \
    --domain-owner 730335644490 \
    --repository dripp-ai-infrastructure \
    --format pypi \
    --namespace dripp-ai \
    --package dripp_events \
    --package-version 0.1 \
    --asset dist \
    --asset-name dripp_events-0.1.tar.gz \
    --asset-hash $(sha256sum dist/dripp_events-0.1.tar.gz | awk '{print $1}') \
    --asset-hash-algorithm sha256
```

