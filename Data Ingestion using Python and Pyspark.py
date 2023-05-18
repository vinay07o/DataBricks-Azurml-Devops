# Databricks notebook source
import pandas as pd

from pyspark.sql import SparkSession

from utils import mount_storage, unmount_storage, read_sql

# Create a SparkSession object
spark = SparkSession.builder.appName("Datainjesion").getOrCreate()

# COMMAND ----------

# data lake connection
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
spark_df = (
    spark.read.format("csv")
    .option("header", "true")
    .load("dbfs:/mnt/blobstorage/insurance_claims.csv")
)

spark_df.display()

# COMMAND ----------

# Read data using Python pandas
df = pd.read_csv("/dbfs/mnt/blobstorage/insurance_claims.csv")

df.head()

# COMMAND ----------

# sql server connection
jdbcHostName = "dataengservervinu.database.windows.net"
jdbcPort = "1433"
jdbcDataBase = "dataeng"
jdbcUserName = "vinay"
jdbcPassword = "Keeru@0526"
jdbcDriver = "com.microsoft.sqlserver.jdbc.SqlServerDriver"
table_name = "SalesLT.Product"

# COMMAND ----------

df_read = read_sql(jdbcHostName, jdbcPort, jdbcDataBase, jdbcUserName, jdbcPassword, jdbcDriver,
             table_name, read_programming="Pyspark")

# COMMAND ----------

df_read.display()

# COMMAND ----------

df_pandas = df_read.toPandas()

# COMMAND ----------

type(df_pandas)
