import boto3
import pandas as pd
from io import BytesIO
from config import *

s3 = boto3.client("s3")

obj = s3.get_object(
    Bucket=BRONZE_BUCKET,
    Key=INPUT_FILE
)

df = pd.read_parquet(BytesIO(obj["Body"].read()))

df["city"] = df["city"].fillna("Unknown")

df["amount"] = df["amount"].astype(float)

buffer = BytesIO()

df.to_parquet(buffer, index=False)

buffer.seek(0)

s3.put_object(
    Bucket=SILVER_BUCKET,
    Key=OUTPUT_FOLDER + "customer.parquet",
    Body=buffer.getvalue()
)

print("Silver layer completed")