# Databricks notebook source
from utils import mount_storage, unmount_storage

# COMMAND ----------

container_name = "datatable"
storage_account_name = "datafordataengineering"
account_key = "tg6m/4VA7vDUeIV5nOitARYGV1/g+sPgM0bCuUEsZ2BVkDfYHcu9i2rTWf4lzW4AyhFTz+dM5AQ/+ASt2l6ptQ=="
mount_point_name = "blobstorage"

# COMMAND ----------

unmount_storage("/mnt/blobstorage")

# COMMAND ----------

mount_storage(container_name, storage_account_name, mount_point_name, account_key)

# COMMAND ----------

# Read data using Spark
spark_df = spark.read.format("csv")\
    .option("header", "true") \
    .load("dbfs:/mnt/blobstorage/insurance_claims.csv")

spark_df.display()

# COMMAND ----------

# Read data using Python pandas
import pandas as pd
df = pd.read_csv("/dbfs/mnt/blobstorage/insurance_claims.csv")

df.head()
