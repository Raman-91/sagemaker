import boto3
import pandas as pd
from io import BytesIO
from datetime import datetime
from config import *

s3 = boto3.client("s3")

# Read file
obj = s3.get_object(
    Bucket=RAW_BUCKET,
    Key=INPUT_FILE
)

df = pd.read_csv(obj["Body"])

# Remove duplicates
df = df.drop_duplicates()

# Add ingestion time
df["ingestion_time"] = datetime.utcnow()

# Convert to parquet
buffer = BytesIO()
df.to_parquet(buffer, index=False)

buffer.seek(0)

# Upload to Bronze
s3.put_object(
    Bucket=BRONZE_BUCKET,
    Key=OUTPUT_FOLDER + "customer.parquet",
    Body=buffer.getvalue()
)

print("Bronze layer completed")