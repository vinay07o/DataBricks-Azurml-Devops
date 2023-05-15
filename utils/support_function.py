"""Helper function for pyspark"""
import IPython

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
