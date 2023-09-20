
# tests/backend/test_analysis.py

import pytest
import pandas as pd
from backend.analysis import analyze_data

def test_analyze_data():
    # Prepare test data
    data = [
        {
            'compartment_id': 'compartment1',
            'instance_id': 'instance1',
            'state': 'running',
            'shape': 'shape1',
            'created_at': '2021-01-01T00:00:00',
        },
        {
            'compartment_id': 'compartment1',
            'instance_id': 'instance2',
            'state': 'stopped',
            'shape': 'shape2',
            'created_at': '2021-02-01T00:00:00',
        },
        {
            'compartment_id': 'compartment2',
            'instance_id': 'instance3',
            'state': 'running',
            'shape': 'shape1',
            'created_at': '2021-03-01T00:00:00',
        },
    ]

    # Call the function with the test data
    result = analyze_data(data)

    # Check the result
    assert result['total_instances'] == 3
    assert result['total_compartments'] == 2
    assert result['instances_per_state'] == {'running': 2, 'stopped': 1}
    assert result['instances_per_shape'] == {'shape1': 2, 'shape2': 1}
    assert result['earliest_created_at'] == '2021-01-01T00:00:00'
    assert result['latest_created_at'] == '2021-03-01T00:00:00'

def test_analyze_data_empty():
    # Prepare test data
    data = []

    # Call the function with the test data
    result = analyze_data(data)

    # Check the result
    assert result['total_instances'] == 0
    assert result['total_compartments'] == 0
    assert result['instances_per_state'] == {}
    assert result['instances_per_shape'] == {}
    assert result['earliest_created_at'] is None
    assert result['latest_created_at'] is None

