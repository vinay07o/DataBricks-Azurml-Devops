"""Helper function for pyspark"""
import IPython
import pandas as pd
import pymssql
import warnings
from pyspark.sql import SparkSession
warnings.filterwarnings("ignore")

# Create a SparkSession object
spark = SparkSession.builder.appName("Datainjesion").getOrCreate()
dbutils = IPython.get_ipython().user_ns["dbutils"]


def mount_storage(container_name, storage_account_name, mount_point_name, account_key):
    """Mount azure blob storage."""
    try:
        dbutils.fs.mount(
            source=f"wasbs://{container_name}@{storage_account_name}.blob.core.windows.net/",
            mount_point=f"/mnt/{mount_point_name}",
            extra_configs={
                f"fs.azure.account.key.{storage_account_name}.blob.core.windows.net": account_key
            },
        )
    except Exception:
        print(f"already mounted. Try to unmount first /mnt/{mount_point_name}")
    return [i[0] for i in dbutils.fs.ls(f"/mnt/{mount_point_name}")]


def unmount_storage(mount_path):
    if any(mount.mountPoint == mount_path for mount in dbutils.fs.mounts()):
        dbutils.fs.unmount(mount_path)
    else:
        print(f"Not Found {mount_path}. Mount first.")

def read_sql(jdbcHostName, jdbcPort, jdbcDataBase, jdbcUserName, jdbcPassword, jdbcDriver,
             table_name, read_programming="Pyspark"):
    jdbcUrl = f"jdbc:sqlserver://{jdbcHostName}:{jdbcPort};databaseName={jdbcDataBase};user={jdbcUserName};password={jdbcPassword}"

    if read_programming.lower() == "pyspark":
        df = spark.read.format("jdbc").option("url", jdbcUrl).option("dbtable", table_name).load()
    elif read_programming.lower() == "python":
        con = pymssql.connect(server=jdbcHostName,user=jdbcUserName,password=jdbcPassword,database=jdbcDataBase)
        cursor = con.cursor()

        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        df = pd.read_sql(query, con)
        con.close()
    
    else:
        raise KeyError("connection failed")

    return df
