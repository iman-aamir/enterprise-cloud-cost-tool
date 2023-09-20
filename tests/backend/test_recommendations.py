
# tests/backend/test_recommendations.py

import pytest
from backend.recommendations import generate_recommendations, get_cost

def test_get_cost():
    assert get_cost('VM.Standard.E2.1.Micro') == 0.01
    assert get_cost('Standard_B1s') == 0.01
    assert get_cost('VM.Standard.E2.2') == 0.02
    assert get_cost('Standard_B2s') == 0.02
    assert get_cost('VM.Standard.E3') == 0.03
    assert get_cost('Standard_D2s_v3') == 0.03
    assert get_cost('VM.Standard.E4') == 0.04
    assert get_cost('Standard_D4s_v3') == 0.04

def test_generate_recommendations():
    data = [
        {'compartment_id': 'comp1', 'shape': 'VM.Standard.E2.1.Micro'},
        {'compartment_id': 'comp1', 'shape': 'VM.Standard.E2.2'},
        {'compartment_id': 'comp2', 'shape': 'VM.Standard.E3'},
        {'compartment_id': 'comp2', 'shape': 'VM.Standard.E4'},
        {'compartment_id': 'comp3', 'shape': 'VM.Standard.E2.1.Micro'},
        {'compartment_id': 'comp3', 'shape': 'VM.Standard.E2.1.Micro'},
        {'compartment_id': 'comp4', 'shape': 'VM.Standard.E4'},
        {'compartment_id': 'comp4', 'shape': 'VM.Standard.E4'},
    ]

    recommendations = generate_recommendations(data)

    assert 'high_cost_compartments' in recommendations
    assert 'recommendation' in recommendations
    assert isinstance(recommendations['high_cost_compartments'], list)
    assert isinstance(recommendations['recommendation'], str)
    assert len(recommendations['high_cost_compartments']) > 0
    assert recommendations['recommendation'] == 'Consider reallocating resources or finding cost-saving opportunities in the above compartments.'

