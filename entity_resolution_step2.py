import pandas as pd
import os

# Paths
input_file = "../outputs/combined_dataset.csv"
output_file = "../outputs/entity_resolution_table.csv"

# Read merged dataset
df = pd.read_csv(input_file)
print("Dataset loaded. Shape:", df.shape)

# Columns to consider for entity resolution
id_columns = ['student_id', 'email', 'card_id', 'device_hash', 'face_id']

# Create a unique key for each row by combining all IDs (ignoring NaN)
df['unique_key'] = df[id_columns].astype(str).agg('-'.join, axis=1)

# Remove duplicates based on unique_key
df_unique = df.drop_duplicates(subset='unique_key')

# Assign entity_id
df_unique = df_unique.reset_index(drop=True)
df_unique['entity_id'] = ['E{:03d}'.format(i+1) for i in range(len(df_unique))]

# Keep only relevant columns + entity_id
columns_to_keep = ['entity_id'] + id_columns
entity_df = df_unique[columns_to_keep]

# Save to CSV
os.makedirs("../outputs", exist_ok=True)
entity_df.to_csv(output_file, index=False)
print(f"✅ Entity resolution table saved to {output_file}")
