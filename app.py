from flask import Flask, render_template_string, request, redirect
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time

app = Flask(__name__)

DB_URL = "sqlite:///task_scheduler.db"
engine = create_engine(DB_URL, echo=True)

Base = declarative_base()

# Define Task model
class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    task_data = Column(String)
    status = Column(String, default="pending")

# Create the database schema if not exists
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Task Manager</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="container mt-5">
    <h1 class="text-center">Manohar Reddy</h1>
    <h3 class="text-center">Roll Number: 2022BCD0027</h3>
    <h4 class="text-center text-muted">DevOps Enthusiast</h4>
    
    <hr>

    <h2 class="text-center">Task Manager</h2>
    
    <form action="/add-task" method="post" class="d-flex mb-3">
        <input type="text" name="task" class="form-control me-2" placeholder="Enter a new task..." required>
        <button type="submit" class="btn btn-success">Add Task</button>
    </form>

    <h3>Task List</h3>
    <ul class="list-group">
        {% for task in tasks %}
            <li class="list-group-item d-flex justify-content-between align-items-center">
                {{ task.task_data }} 
                <span class="badge bg-{{ 'success' if task.status == 'completed' else 'warning' }}">{{ task.status }}</span>
                {% if task.status == 'pending' %}
                    <a href="/complete-task/{{ task.id }}" class="btn btn-primary btn-sm">Complete</a>
                {% endif %}
            </li>
        {% endfor %}
    </ul>

</body>
</html>
"""

@app.route('/')
def index():
    session = Session()
    tasks = session.query(Task).all()
    session.close()
    return render_template_string(HTML_TEMPLATE, tasks=tasks)

@app.route('/add-task', methods=['POST'])
def add_task():
    task_data = request.form.get('task')
    session = Session()
    task = Task(task_data=task_data, status="pending")
    session.add(task)
    session.commit()
    session.close()
    return redirect('/')

@app.route('/complete-task/<int:task_id>')
def complete_task(task_id):
    session = Session()
    task = session.query(Task).filter_by(id=task_id).first()
    if task:
        task.status = "completed"
        session.commit()
    session.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8081, debug=True)