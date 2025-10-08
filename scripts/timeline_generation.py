import pandas as pd
import os

# Paths
entity_file = "../outputs/entity_resolution_table.csv"
data_folder = "../data"
output_file = "../outputs/entity_timeline.csv"

# Load entity table
entities = pd.read_csv(entity_file)
print(f"Loaded entity table: {entities.shape}")

# List of activity CSVs
activity_files = [
    "campus_card_swipe.csv",
    "wifi_association.csv",
    "library_checkouts.csv",
    "lab_booking.csv",
    "cctv_frames.csv",
    "free_text_notes.csv"
]

activity_dfs = []

# Load each activity CSV and add entity_id by merging
for file in activity_files:
    path = os.path.join(data_folder, file)
    df = pd.read_csv(path)
    
    # Merge with entity table on matching identifiers
    merge_cols = [col for col in ['student_id','card_id','device_hash','face_id','email'] if col in df.columns]
    if merge_cols:
        df = df.merge(entities, how="left", on=merge_cols)
    
    # Add activity type column
    df['activity_type'] = file.replace(".csv","")
    
    activity_dfs.append(df)

# Combine all activities
all_activities = pd.concat(activity_dfs, ignore_index=True)

# Ensure timestamp column exists and convert to datetime
if 'timestamp' in all_activities.columns:
    all_activities['timestamp'] = pd.to_datetime(all_activities['timestamp'], errors='coerce')

# Sort by entity_id and timestamp
all_activities.sort_values(by=['entity_id','timestamp'], inplace=True)

# Save timeline
all_activities.to_csv(output_file, index=False)
print(f"✅ Timeline saved to {output_file}")
