
# backend/cloud_connectors/azure.py

from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.orm import sessionmaker

class AzureConnector:
    def __init__(self):
        self.engine = create_engine('sqlite:///cloud_data.db')
        self.metadata = MetaData()
        self.azure_table = Table('azure', self.metadata, autoload_with=self.engine)
        self.session = sessionmaker(bind=self.engine)()

    def connect(self, credentials):
        """
        Connect to Azure Cloud using provided credentials
        """
        self.subscription_id = credentials['subscription_id']
        self.credential = DefaultAzureCredential()
        self.resource_client = ResourceManagementClient(self.credential, self.subscription_id)
        self.compute_client = ComputeManagementClient(self.credential, self.subscription_id)

    def get_data(self):
        """
        Fetch data from Azure Cloud
        """
        data = []
        for group in self.resource_client.resource_groups.list():
            for vm in self.compute_client.virtual_machines.list(group.name):
                row = {
                    'resource_group': group.name,
                    'vm_id': vm.id,
                    'vm_name': vm.name,
                    'vm_state': vm.instance_view.statuses[-1].display_status,
                    'vm_size': vm.hardware_profile.vm_size,
                    'created_at': vm.instance_view.statuses[0].time.strftime('%Y-%m-%dT%H:%M:%S.%f'),
                }
                data.append(row)

        # Insert data into database
        with self.engine.connect() as connection:
            for row in data:
                stmt = self.azure_table.insert().values(**row)
                connection.execute(stmt)

        return data

