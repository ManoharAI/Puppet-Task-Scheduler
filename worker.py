from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time

# Database connection with retry
engine = None
while True:
    try:
        engine = create_engine('postgresql://user:password@db:5432/mydb')
        engine.connect()
        break
    except Exception as e:
        print("Waiting for database...")
        time.sleep(5)

Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    task_data = Column(String)
    status = Column(String)

Session = sessionmaker(bind=engine)

while True:
    session = Session()
    pending_tasks = session.query(Task).filter_by(status='pending').all()
    for task in pending_tasks:
        print(f"Processing task {task.id}")
        task.status = 'completed'
        session.commit()
    session.close()
    print("Processed tasks. Sleeping...")
    time.sleep(10)