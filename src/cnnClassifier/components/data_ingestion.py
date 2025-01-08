import os
import boto3
import pandas as pd

def ingest_data(s3_path, output_path):
    s3 = boto3.client("s3")
    bucket, key = s3_path.replace("s3://", "").split("/", 1)

    # Ensure the output directory exists
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)
    
    # Download data from S3
    s3.download_file(bucket, key, output_path)

    # Confirm data download
    print(f"Data downloaded from {s3_path} to {output_path}")

if __name__ == "__main__":
    import sys
    ingest_data(sys.argv[1], sys.argv[2])
