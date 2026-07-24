import boto3
import pandas as pd
from io import BytesIO
from config import *

s3 = boto3.client("s3")

obj = s3.get_object(
    Bucket=SILVER_BUCKET,
    Key=INPUT_FILE
)

df = pd.read_parquet(BytesIO(obj["Body"].read()))

summary = (
    df.groupby("city", as_index=False)["amount"]
      .sum()
      .rename(columns={"amount": "total_sales"})
)

buffer = BytesIO()

summary.to_parquet(buffer, index=False)

buffer.seek(0)

s3.put_object(
    Bucket=GOLD_BUCKET,
    Key=OUTPUT_FOLDER + "sales_summary.parquet",
    Body=buffer.getvalue()
)

print("Gold layer completed")