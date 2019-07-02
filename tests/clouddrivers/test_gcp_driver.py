import pytest
from mock import patch, MagicMock
from powerfulseal.clouddrivers import gcp_driver
from powerfulseal.node import (Node, NodeState)

@pytest.fixture
def gcp_instances():
    return [
        {
            'id': '1234567',
            'name': 'dummyinstance',
            'zone': 'https://www.googleapis.com/compute/v1/projects/project/zones/us-west1-a',
            'status': 'RUNNING',
            'networkInterfaces': [
                {
                    'networkIP': '10.10.0.1',
                    'accessConfigs': [
                        {
                            'natIP': '33.10.0.1',
                        },
                    ],
                },
            ],
        },
    ]

@patch('powerfulseal.clouddrivers.gcp_driver.create_compute')
def test_get_by_ip_private_ip_nodes(create_compute, gcp_instances):
    driver = gcp_driver.GCPDriver()
    driver.remote_servers = gcp_instances
    node = driver.get_by_ip('10.10.0.1')

    assert node.id == gcp_instances[0]['id']
    assert node.name == gcp_instances[0]['name']
    assert node.ip == '10.10.0.1'
    assert node.extIp == '33.10.0.1'
    assert node.az == 'us-west1-a'
    assert node.state == NodeState.UP

    assert driver.get_by_ip('10.10.0.2') is None

@patch('powerfulseal.clouddrivers.gcp_driver.create_compute')
def test_get_by_ip_public_ip_nodes(create_compute, gcp_instances):
    driver = gcp_driver.GCPDriver()
    driver.remote_servers = gcp_instances
    node = driver.get_by_ip('33.10.0.1')

    assert node.id == gcp_instances[0]['id']
    assert node.name == gcp_instances[0]['name']
    assert node.ip == '10.10.0.1'
    assert node.extIp == '33.10.0.1'
    assert node.az == 'us-west1-a'
    assert node.state == NodeState.UP

    assert driver.get_by_ip('33.10.0.2') is None
