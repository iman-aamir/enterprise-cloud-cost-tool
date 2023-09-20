
# backend/analysis.py

import pandas as pd

def analyze_data(data):
    """
    Analyze the cloud usage data and return a summary.
    """
    # Convert the data into a pandas DataFrame for easier analysis
    df = pd.DataFrame(data)

    # Calculate the total number of instances
    total_instances = df['instance_id'].nunique()

    # Calculate the total number of compartments/resource groups
    total_compartments = df['compartment_id'].nunique() if 'compartment_id' in df.columns else df['resource_group'].nunique()

    # Calculate the number of instances per state
    instances_per_state = df['state'].value_counts().to_dict() if 'state' in df.columns else df['vm_state'].value_counts().to_dict()

    # Calculate the number of instances per shape/size
    instances_per_shape = df['shape'].value_counts().to_dict() if 'shape' in df.columns else df['vm_size'].value_counts().to_dict()

    # Calculate the earliest and latest creation times
    df['created_at'] = pd.to_datetime(df['created_at'])
    earliest_created_at = df['created_at'].min().isoformat()
    latest_created_at = df['created_at'].max().isoformat()

    # Return the analysis summary
    return {
        'total_instances': total_instances,
        'total_compartments': total_compartments,
        'instances_per_state': instances_per_state,
        'instances_per_shape': instances_per_shape,
        'earliest_created_at': earliest_created_at,
        'latest_created_at': latest_created_at,
    }

