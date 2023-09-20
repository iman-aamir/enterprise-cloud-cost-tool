
# backend/forecasting.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics

def forecast_expenses(data):
    """
    Forecast future expenses based on historical cloud usage data.
    """
    # Convert the data into a pandas DataFrame for easier analysis
    df = pd.DataFrame(data)

    # Convert the 'created_at' column to datetime
    df['created_at'] = pd.to_datetime(df['created_at'])

    # Create a new column 'days_since_creation' which will be used for forecasting
    df['days_since_creation'] = (df['created_at'] - df['created_at'].min()).dt.days

    # Assume that the cost is directly proportional to the number of instances
    # Therefore, we can use the number of instances per day as a proxy for cost
    daily_costs = df.groupby('days_since_creation').size()

    # Prepare the data for the linear regression model
    X = daily_costs.index.values.reshape(-1, 1)  # features (number of days since the first instance was created)
    y = daily_costs.values  # target (number of instances per day)

    # Split the data into training set and test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    # Train the linear regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Use the model to make predictions
    y_pred = model.predict(X_test)

    # Calculate the mean absolute error of the predictions
    mae = metrics.mean_absolute_error(y_test, y_pred)

    # Use the model to forecast the expenses for the next 30 days
    future_days = pd.Series(range(X.max()[0] + 1, X.max()[0] + 31)).values.reshape(-1, 1)
    future_expenses = model.predict(future_days)

    # Return the forecast and the error of the model
    return {
        'forecast': list(future_expenses),
        'error': mae,
    }

