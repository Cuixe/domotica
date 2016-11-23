from models import Task
task_list = []

def get_task(id):
    task_list_size = len(task_list)
    index = 0;
    while (index < task_list_size):
        task = task_list[index];
        if task.id == id:
            return task
