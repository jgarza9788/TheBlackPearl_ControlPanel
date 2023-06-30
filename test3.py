import shutil

total, used, free = shutil.disk_usage(r"D:\")
print(total, used, free)