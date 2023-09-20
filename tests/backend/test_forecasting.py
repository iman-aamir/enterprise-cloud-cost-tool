
# tests/backend/test_forecasting.py

import pytest
import pandas as pd
from backend.forecasting import forecast_expenses

def test_forecast_expenses():
    # Create a sample data
    data = [
        {'created_at': '2021-01-01', 'instances': 10},
        {'created_at': '2021-01-02', 'instances': 15},
        {'created_at': '2021-01-03', 'instances': 20},
        # ...
        {'created_at': '2021-12-31', 'instances': 50},
    ]

    # Call the function with the sample data
    result = forecast_expenses(data)

    # Check the type of the result
    assert isinstance(result, dict), "The result should be a dictionary."

    # Check the keys of the result
    assert 'forecast' in result, "The result should have a 'forecast' key."
    assert 'error' in result, "The result should have an 'error' key."

    # Check the type of the forecast
    assert isinstance(result['forecast'], list), "The forecast should be a list."
    assert all(isinstance(x, (int, float)) for x in result['forecast']), "The forecast should be a list of numbers."

    # Check the type of the error
    assert isinstance(result['error'], (int, float)), "The error should be a number."

    # Check the length of the forecast
    assert len(result['forecast']) == 30, "The forecast should have 30 elements."

    # Check the value of the error
    assert result['error'] >= 0, "The error should be a non-negative number."

# Run the test
pytest.main(["-v", "-s", "tests/backend/test_forecasting.py"])

