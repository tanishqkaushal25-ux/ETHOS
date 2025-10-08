import pandas as pd

# Path to your large CSV file
input_file = "../outputs/entity_timeline.csv"
output_file = "../outputs/entity_timeline_sample.csv"

# Read only first 5000 rows (you can increase or decrease as needed)
sample_size = 5000

print("Loading sample data... Please wait.")

try:
    # Read limited rows
    df_sample = pd.read_csv(input_file, nrows=sample_size)

    # Save the smaller sample file
    df_sample.to_csv(output_file, index=False)

    print(f"✅ Sample file created successfully: {output_file}")
    print(f"Total rows in sample: {len(df_sample)}")

except Exception as e:
    print("❌ Error while creating sample:", e)
