from fastapi import FastAPI
from config.database import engine
from config.base import Base
from routes import user_routes, sprint_routes, task_routes

import models.user
import models.sprint
import models.task
import models.associations
import models.test

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sprint Board API", version="1.0.0")

app.include_router(user_routes.router)
app.include_router(sprint_routes.router)
app.include_router(task_routes.router)
