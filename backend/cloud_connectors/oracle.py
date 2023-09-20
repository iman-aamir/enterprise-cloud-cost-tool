
# backend/cloud_connectors/oracle.py

import oci
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.orm import sessionmaker

class OracleConnector:
    def __init__(self):
        self.engine = create_engine('sqlite:///cloud_data.db')
        self.metadata = MetaData()
        self.oracle_table = Table('oracle', self.metadata, autoload_with=self.engine)
        self.session = sessionmaker(bind=self.engine)()

    def connect(self, credentials):
        """
        Connect to Oracle Cloud using provided credentials
        """
        self.config = {
            "user": credentials['user'],
            "key_file": credentials['key_file'],
            "fingerprint": credentials['fingerprint'],
            "tenancy": credentials['tenancy'],
            "region": credentials['region'],
        }
        self.identity = oci.identity.IdentityClient(self.config)

    def get_data(self):
        """
        Fetch data from Oracle Cloud
        """
        data = []
        for compartment in self.identity.list_compartments(self.config['tenancy']).data:
            for instance in oci.core.ComputeClient(self.config).list_instances(compartment.id).data:
                row = {
                    'compartment_id': compartment.id,
                    'compartment_name': compartment.name,
                    'instance_id': instance.id,
                    'instance_name': instance.display_name,
                    'state': instance.lifecycle_state,
                    'shape': instance.shape,
                    'created_at': instance.time_created.isoformat(),
                }
                data.append(row)

        # Insert data into database
        with self.engine.connect() as connection:
            for row in data:
                stmt = self.oracle_table.insert().values(**row)
                connection.execute(stmt)

        return data

