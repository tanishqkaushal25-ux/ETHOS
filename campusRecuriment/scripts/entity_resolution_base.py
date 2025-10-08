import os
import pandas as pd

# Folder paths
data_folder = "../data"
output_folder = "../outputs"

# Find all CSV files
csv_files = [f for f in os.listdir(data_folder) if f.endswith('.csv')]
print("🔍 Found CSV files:", csv_files)

# Read and merge all CSVs
merged_data = []

for file in csv_files:
    path = os.path.join(data_folder, file)
    try:
        df = pd.read_csv(path)
        df['source_file'] = file
        merged_data.append(df)
        print(f"✅ Loaded {file} with {len(df)} rows.")
    except Exception as e:
        print(f"⚠️ Error loading {file}: {e}")

# Combine all data
if merged_data:
    combined_df = pd.concat(merged_data, ignore_index=True, sort=False)
    print(f"\n📊 Combined dataset shape: {combined_df.shape}")

    # Save combined dataset
    os.makedirs(output_folder, exist_ok=True)
    combined_df.to_csv(os.path.join(output_folder, "combined_dataset.csv"), index=False)
    print(f"💾 Saved merged dataset to {output_folder}/combined_dataset.csv")
else:
    print("❌ No CSV files loaded. Check your /data folder path.")
