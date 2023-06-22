from flask import Flask, render_template, request
import copy
import uuid

app = Flask(__name__)

class Task:
    def __init__(self, description, completed=False):
        self.id = str(uuid.uuid4())
        self.description = description
        self.completed = completed

class ArrayStack:
    def __init__(self):
        self.items = []
        
    def is_empty(self):
        return len(self.items) == 0
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.items.pop()
    
    def peek(self):
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.items[-1]

tasks_stack = ArrayStack()  # Stack to store the tasks
undo_stack = ArrayStack()  # Stack to store the actions for undo

@app.route('/', methods=['GET', 'POST'])
def task_tracker():
    if request.method == 'POST':
        action = request.form['action']
        
        if action == 'add':
            description = request.form['description']
            if description.strip():
                task = Task(description)
                tasks_stack.push(task)
                undo_stack.push(('add', task))
        elif action == 'complete':
            task_id = request.form['task_id']
            for task in tasks_stack.items[::-1]:
                if task.id == task_id:
                    task.completed = not task.completed
                    undo_stack.push(('complete', task))
                    break
        elif action == 'undo':
            if not undo_stack.is_empty():
                last_action, last_task = undo_stack.pop()
                if last_action == 'add':
                    tasks_stack.items.remove(last_task)
                elif last_action == 'complete':
                    last_task.completed = not last_task.completed
        
    tasks = copy.deepcopy(tasks_stack.items[::-1])
    
    return render_template('index.html', tasks=tasks)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
