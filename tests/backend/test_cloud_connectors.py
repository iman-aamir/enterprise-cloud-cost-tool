
# tests/backend/test_cloud_connectors.py

import pytest
from unittest.mock import patch, MagicMock
from backend.cloud_connectors.oracle import OracleConnector
from backend.cloud_connectors.azure import AzureConnector

def test_oracle_connector():
    # Mocking the Oracle Cloud SDK
    with patch('oci.identity.IdentityClient') as MockIdentityClient, patch('oci.core.ComputeClient') as MockComputeClient:
        # Mocking the response from Oracle Cloud SDK
        mock_identity_client = MagicMock()
        mock_compute_client = MagicMock()
        MockIdentityClient.return_value = mock_identity_client
        MockComputeClient.return_value = mock_compute_client

        mock_identity_client.list_compartments.return_value.data = []
        mock_compute_client.list_instances.return_value.data = []

        # Testing the OracleConnector
        oracle_connector = OracleConnector()
        oracle_connector.connect({
            "user": 'test_user',
            "key_file": 'test_key_file',
            "fingerprint": 'test_fingerprint',
            "tenancy": 'test_tenancy',
            "region": 'test_region',
        })
        data = oracle_connector.get_data()

        assert data == []

def test_azure_connector():
    # Mocking the Azure Cloud SDK
    with patch('azure.identity.DefaultAzureCredential') as MockDefaultAzureCredential, patch('azure.mgmt.resource.ResourceManagementClient') as MockResourceManagementClient, patch('azure.mgmt.compute.ComputeManagementClient') as MockComputeManagementClient:
        # Mocking the response from Azure Cloud SDK
        mock_credential = MagicMock()
        mock_resource_client = MagicMock()
        mock_compute_client = MagicMock()
        MockDefaultAzureCredential.return_value = mock_credential
        MockResourceManagementClient.return_value = mock_resource_client
        MockComputeManagementClient.return_value = mock_compute_client

        mock_resource_client.resource_groups.list.return_value = []
        mock_compute_client.virtual_machines.list.return_value = []

        # Testing the AzureConnector
        azure_connector = AzureConnector()
        azure_connector.connect({
            "subscription_id": 'test_subscription_id',
        })
        data = azure_connector.get_data()

        assert data == []

if __name__ == "__main__":
    pytest.main()

