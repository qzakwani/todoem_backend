


def insert_tasklist(model_list, model_task, data):
    tasks = data.pop("tasks")
    tasks_num = len(tasks)
    bulk_tasks = []
    if tasks_num > 100:
        tasks = tasks[:100]
        tasks_num = 100
        
    
    task_list = model_list.objects.create(tasks_num=tasks_num, **data)
    
    for task in tasks:
        bulk_tasks.append(model_task(tasklist=task_list, **task))

    model_task.objects.bulk_create(bulk_tasks)
    
    return task_list