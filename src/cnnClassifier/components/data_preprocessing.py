import pandas as pd
import boto3
import sys, os

# raw_s3_path="data/raw/raw_data.csv"
# processed_data_path="data/processed/dev_preprocessed_data.csv"

def main(raw_s3_path, processed_data_path):
    # Read raw data from S3
    # s3 = boto3.client('s3')
    # bucket_name, key = raw_s3_path.replace("s3://", "").split("/", 1)
    # obj = s3.get_object(Bucket=bucket_name, Key=key)
    raw_data = pd.read_csv(raw_s3_path)

    # Process the data (example processing step)
    processed_data = raw_data.dropna()  # Example: Remove rows with NaN values

    # Ensure the output directory exists
    output_dir = os.path.dirname(processed_data_path)
    os.makedirs(output_dir, exist_ok=True)

    # Save processed data locally
    processed_data.to_csv(processed_data_path, index=False)

if __name__ == "__main__":
    raw_s3_path = sys.argv[1]
    processed_data_path = sys.argv[2]
    main(raw_s3_path, processed_data_path)
