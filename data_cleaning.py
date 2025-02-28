import pandas as pd
import os

# Set paths
raw_data_path = "data/"
cleaned_data_path = "cleaned_data/"

# Create folder if it doesn't exist
os.makedirs(cleaned_data_path, exist_ok=True)

# Load all CSV files from the "data" folder
all_files = [f for f in os.listdir(raw_data_path) if f.endswith(".csv")]

# Read and combine data
df_list = [pd.read_csv(os.path.join(raw_data_path, file)) for file in all_files]
df = pd.concat(df_list, ignore_index=True)

print(f"✅ Loaded {len(df)} rows from {len(all_files)} files.")

# Drop irrelevant columns (Modify based on dataset)
df = df.drop(columns=["start_station_name", "end_station_name"], errors="ignore")

# Fill missing values
df.fillna(method="ffill", inplace=True)

# Convert date columns
df["started_at"] = pd.to_datetime(df["started_at"], errors="coerce")
df["ended_at"] = pd.to_datetime(df["ended_at"], errors="coerce")

# Calculate ride duration in minutes
df["ride_duration"] = (df["ended_at"] - df["started_at"]).dt.total_seconds() / 60  # In minutes

print("🛠️ Missing values handled & data types fixed.")

# Remove negative ride durations
df = df[df["ride_duration"] > 0]

# Remove extreme outliers (rides longer than 24 hours)
df = df[df["ride_duration"] <= 1440]

# Save cleaned data
cleaned_file_path = os.path.join(cleaned_data_path, "cleaned_cyclistic_data.csv")
df.to_csv(cleaned_file_path, index=False)

printf("🎯 Cleaned data saved to {cleaned_file_path}.")
