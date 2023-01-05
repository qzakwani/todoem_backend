


def insert_tasklist(model_list, model_task, data):
    """
    Insert a task list and its tasks into the database.

    Parameters:
        model_list (Type[Model]): The model class for the task list.
        model_task (Type[Model]): The model class for the tasks.
        data (Dict[str, Any]): The data for the task list and tasks. 
            It should contain a 'tasks' key with a list of dictionaries representing the tasks.

    Returns:
        task_list (Model): The task list model instance that was created.
    """
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