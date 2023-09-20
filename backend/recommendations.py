
# backend/recommendations.py

import pandas as pd
from sklearn.cluster import KMeans

def generate_recommendations(data):
    """
    Generate recommendations for resource allocation and cost-saving opportunities.
    """
    # Convert the data into a pandas DataFrame for easier analysis
    df = pd.DataFrame(data)

    # Create a new column for the cost of each instance, based on its shape/size
    df['cost'] = df['shape'].map(get_cost) if 'shape' in df.columns else df['vm_size'].map(get_cost)

    # Group the data by compartment/resource group and calculate the total cost
    groupby_field = 'compartment_id' if 'compartment_id' in df.columns else 'resource_group'
    total_cost = df.groupby(groupby_field)['cost'].sum()

    # Use KMeans clustering to identify compartments/resource groups with similar costs
    kmeans = KMeans(n_clusters=3)
    kmeans.fit(total_cost.values.reshape(-1, 1))
    df['cluster'] = kmeans.labels_

    # Identify the compartments/resource groups in the highest cost cluster
    high_cost_cluster = df['cluster'].value_counts().idxmax()
    high_cost_compartments = df[df['cluster'] == high_cost_cluster][groupby_field].unique()

    # Return the recommendations
    return {
        'high_cost_compartments': high_cost_compartments.tolist(),
        'recommendation': 'Consider reallocating resources or finding cost-saving opportunities in the above compartments.'
    }

def get_cost(shape_or_size):
    """
    Return the cost of an instance based on its shape/size.
    This is a simplified example and in a real-world scenario, the cost would likely be fetched from a pricing API.
    """
    if shape_or_size in ['VM.Standard.E2.1.Micro', 'Standard_B1s']:
        return 0.01
    elif shape_or_size in ['VM.Standard.E2.2', 'Standard_B2s']:
        return 0.02
    elif shape_or_size in ['VM.Standard.E3', 'Standard_D2s_v3']:
        return 0.03
    else:
        return 0.04

