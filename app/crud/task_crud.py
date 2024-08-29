# app/crud/task_crud.py
from sqlalchemy.orm import Session
from app.models import Task
from app.schemas.tasks import TaskCreate, TaskUpdate
from app.crud.base import CRUDBase

class TaskCRUD(CRUDBase[Task, TaskCreate, TaskUpdate]):

    def update_task(self, db: Session, task_id: int, task_update: TaskUpdate):
        db_task = self.get(db, id=task_id)
        if db_task:
            return self.update(db, db_obj=db_task, obj_in=task_update)
        return None



    def delete_task(self, db: Session, task_id: int):
        return self.remove(db, id=task_id)


task = TaskCRUD(Task)
