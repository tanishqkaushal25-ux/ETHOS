import pandas as pd

# Path to the big timeline CSV
input_file = "../outputs/entity_timeline.csv"

# Path for smaller CSV
output_file = "../outputs/entity_timeline_summary.csv"

# Only load the columns you need for dashboard
cols_to_use = ['entity_id', 'timestamp', 'event_type']  # adjust columns as needed
df = pd.read_csv(input_file, usecols=cols_to_use)

# Convert timestamp to datetime and sort
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.sort_values(by='timestamp')

# Save smaller CSV
df.to_csv(output_file, index=False)

print("Dashboard-ready CSV created:", output_file)
