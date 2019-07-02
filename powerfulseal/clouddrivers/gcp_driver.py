from googleapiclient import discovery

from . import AbstractDriver
from .no_cloud_driver import NoCloudDriver
from ..node import Node, NodeState

MAPPING_STATES_STATUS = {
    "PROVISIONING": NodeState.DOWN,
    "STAGING": NodeState.DOWN,
    "RUNNING": NodeState.UP,
    "STOPPING": NodeState.DOWN,
    "TERMINATED": NodeState.DOWN,
}


def server_status_to_state(status):
    """ Translate GCE Instance status into NodeState
    """
    return MAPPING_STATES_STATUS.get(status, NodeState.UNKNOWN)


def create_node_from_server(server, networkConfig):
    """ Translate GCE Instance representation into a Node object.
    """
    return Node(
        id=server['id'],
        ip=networkConfig['networkIP'],
        # TODO: should only match external-nat
        extIp=networkConfig['accessConfigs'][0]['natIP'],
        az=server['zone'].split('/')[-1],
        name=server['name'],
        state=server_status_to_state(server['status']),
    )


def create_compute():
    """ Build GCE api connection, mocked in tests
    """
    return discovery.build('compute', 'v1')


class GCPDriver(NoCloudDriver):
    def __init__(self, project=None):
        NoCloudDriver.__init__(self)
        self.project = project
        self.compute = create_compute()
        self.remote_servers = []

    def get_zones(self):
        cr = self.compute.zones().list(project=self.project).execute()
        if 'items' in cr.keys():
            return [zone['name'] for zone in cr['items']]
        return []

    def get_instances_in_zone(self, zone):
        cr = self.compute.instances().list(project=self.project, zone=zone).execute()
        if 'items' in cr.keys():
            return cr['items']
        return []

    def get_all_instances(self):
        zones = self.get_zones()
        instances = []
        for zone in zones:
            instances_in_zone = self.get_instances_in_zone(zone)
            if instances_in_zone:
                instances.extend(instances_in_zone)
        return instances

    def sync(self):
        """ Downloads a fresh set of nodes form the API.
        """
        self.logger.info("Synchronizing remote nodes")
        self.remote_servers = self.get_all_instances()
        self.logger.info("Fetched %s remote servers" % len(self.remote_servers))

    def get_by_ip(self, ip):
        """ Retrieve an instance of Node by its IP.
        """
        for server in self.remote_servers:
            for network in server['networkInterfaces']:
                if ip == network['networkIP']:
                    return create_node_from_server(server, network)
                if 'accessConfigs' in network.keys():
                    if ip in [ac['natIP'] for ac in network['accessConfigs'] if 'natIP' in ac.keys()]:
                        return create_node_from_server(server, network)
        return None
