from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

Base = declarative_base()


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today().date())

    def __repr__(self):
        return f'{self.task}'


class ToDoList:

    def __init__(self, db_name):
        self.engine = create_engine(f'sqlite:///{db_name}.db?check_same_thread=False')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.today = datetime.today().date()
        self.ui()

    def ui(self):
        print("""
1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit""")
        action = input()
        if action == '1':
            self.print_tasks(self.today)
            self.ui()
        elif action == '2':
            self.week_tasks()
            self.ui()
        elif action == '3':
            self.all_tasks()
            self.ui()
        elif action == '4':
            self.missed_tasks()
            self.ui()
        elif action == '5':
            self.add_task()
            self.ui()
        elif action == '6':
            self.delete_task()
            self.ui()
        else:
            print('Bye!')
            pass

    def print_tasks(self, day, weekday='Today'):
        tasks = self.session.query(Task).filter(Task.deadline == day).all()
        print(f'\n{weekday} {day.day} {day.strftime("%b")}:')
        if tasks:
            for i, t in enumerate(tasks, 1):
                print(f'{i}. {t}')
        else:
            print('Nothing to do!')

    def week_tasks(self):
        days = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday',
                4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
        for i in range(7):
            date = self.today + timedelta(days=i)
            weekday = days[date.weekday()]
            self.print_tasks(date, weekday)

    def all_tasks(self, *ret):
        all_tasks = [task for task in self.session.query(Task).order_by(Task.deadline).all()]
        for i, task in enumerate(all_tasks, 1):
            print(f"{i}. {task}. {task.deadline.strftime('%#d %b')}")
        if ret:
            return all_tasks

    def delete_task(self):
        print('Choose the number of the task you want to delete:')
        task_list = self.all_tasks('Return')
        del_number = int(input())
        self.session.delete(task_list[del_number-1])
        self.session.commit()
        print('The task has been deleted!')

    def missed_tasks(self):
        missed_task = self.session.query(Task).filter(Task.deadline < self.today).order_by(Task.deadline).all()
        for i, task in enumerate(missed_task, 1):
            print(f"{i}. {task}. {task.deadline.strftime('%#d %b')}")

    def add_task(self):
        print('\nEnter task')
        task_to_add = input()
        print('Enter deadline')
        deadline = datetime.strptime(input(), '%Y-%m-%d').date()
        new_row = Task(task=task_to_add, deadline=deadline)
        self.session.add(new_row)
        self.session.commit()
        print('The task has been added!')


ToDoList('todo')
