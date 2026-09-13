#!/usr/bin/env python
# coding: utf-8

# In[2]:


get_ipython().run_cell_magic('writefile', 'CRUD.py', '\nfrom fastapi import FastAPI\nfrom pydantic import BaseModel\nfrom sqlalchemy import create_engine, Integer, Column, String, Boolean\nfrom sqlalchemy.orm import declarative_base, sessionmaker\n\napp = FastAPI()\n\nDATABASE_URL = "sqlite:///./todo.db"\n\nengine = create_engine(\n    DATABASE_URL,\n    connect_args={"check_same_thread": False}\n)\n\nBase = declarative_base()\n\nSessionLocal = sessionmaker(\n    autocommit=False,\n    autoflush=False,\n    bind=engine\n)\n\n\nclass TaskDB(Base):\n    __tablename__ = "tasks"\n\n    id = Column(Integer, primary_key=True)\n    title = Column(String)\n    is_done = Column(Boolean, default=False)\n\n\nBase.metadata.create_all(bind=engine)\n\n\nclass Task(BaseModel):\n    id: int\n    title: str\n    is_done: bool = False\n\n\n@app.post("/tasks")\ndef create_task(task: Task):\n    db = SessionLocal()\n\n    new_task = TaskDB(\n        id=task.id,\n        title=task.title,\n        is_done=task.is_done\n    )\n\n    db.add(new_task)\n    db.commit()\n    db.refresh(new_task)\n    db.close()\n\n    return new_task\n\n\n@app.get("/tasks")\ndef get_task():\n    db = SessionLocal()\n\n    tasks = db.query(TaskDB).all()\n\n    db.close()\n\n    return tasks\n')


# In[ ]:




