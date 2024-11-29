import eel
import json


eel.init('web')  # Define o diretório com os arquivos HTML, CSS e JS


# Funções de manipulação de tarefas
def load_tasks_from_file():
    try:
        with open('tasks.json', 'r') as file:
            data = json.load(file)
            return data.get("tasks", []), data.get("theme", "light")  # "light" é o tema padrão
    except FileNotFoundError:
        return [], "light"


def save_tasks_to_file(tasks, theme="light"):
    with open('tasks.json', 'w') as file:
        json.dump({"tasks": tasks, "theme": theme}, file)


tasks, theme = load_tasks_from_file()


@eel.expose
def add_task(task):
    tasks.append({"task": task, "completed": False})
    save_tasks_to_file(tasks, theme)
    return tasks


@eel.expose
def load_tasks():
    return tasks


@eel.expose
def toggle_task_completion(task_text):
    for task in tasks:
        if task["task"] == task_text:
            task["completed"] = not task["completed"]
    save_tasks_to_file(tasks, theme)
    return tasks


@eel.expose
def edit_task(old_task_text, new_task_text):
    for task in tasks:
        if task["task"] == old_task_text:
            task["task"] = new_task_text
    save_tasks_to_file(tasks, theme)
    return tasks


@eel.expose
def delete_task(task_text):
    global tasks
    tasks = [task for task in tasks if task["task"] != task_text]
    save_tasks_to_file(tasks, theme)
    return tasks


@eel.expose
def set_theme(new_theme):
    global theme
    theme = new_theme
    save_tasks_to_file(tasks, theme)


@eel.expose
def get_theme():
    return theme


eel.start('index.html')


