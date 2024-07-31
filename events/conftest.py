import subprocess
import time

import boto3
import pytest
from moto import mock_aws

@pytest.fixture(scope='session', autouse=True)
def kafka_setup_teardown():
    # Start Kafka and Zookeeper using Docker Compose
    # subprocess.run(["docker-compose", "up", "-d"], check=True)
    # time.sleep(10)  # Wait for Kafka to fully start
    mock = mock_aws()
    mock.start()
    yield  # This is where the testing happens
    mock.stop()
    # Tear down Kafka and Zookeeper
    # subprocess.run(["docker-compose", "down"], check=True)
