import shutil

def perform_task(task):
    if task == 'disk_usage':
        total, used, free = shutil.disk_usage("/")
        return f"Total: {total // (2**30)} GB, Used: {used // (2**30)} GB, Free: {free // (2**30)} GB"
    else:
        return "Unknown task"
