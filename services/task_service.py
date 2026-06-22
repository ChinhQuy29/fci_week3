from repositories.task_repository import TaskRepository
from repositories.user_repository import UserRepository
from repositories.sprint_repository import SprintRepository
from models.task import Task, TaskStatus, TaskPriority

class TaskService():
    def __init__(self, task_repo: TaskRepository, user_repo: UserRepository, sprint_repo: SprintRepository):
        self.task_repo = task_repo
        self.user_repo = user_repo
        self.sprint_repo = sprint_repo

    def create_task(self, actor_id: int, sprint_id: int, title: str, description: str = None, priority: TaskPriority = TaskPriority.low) -> Task:
        actor = self.get_user(actor_id)
        if not actor.is_manager:
            raise PermissionError("Only managers can create tasks")
        task = Task(sprint_id=sprint_id, title=title, description=description, priority=priority)
        return self.task_repo.save(task)
        

    def assign_task(self, actor_id: int, task_id: int, assignee_id: int) -> Task:
        actor = self.get_user(actor_id)
        if not actor.is_manager and actor_id != assignee_id:
            raise PermissionError("Members can only assign tasks to themselves")
        task = self.get_task(task_id)
        if not self.sprint_repo.is_member(task.sprint_id, assignee_id):
            raise ValueError("Assignee is not a member of this sprint")
        task.assignee_id = assignee_id
        return self.task_repo.save(task)

    def unassign_task(self, actor_id: int, task_id: int) -> Task:
        actor = self.get_user(actor_id)
        task = self.get_task(task_id)
        if not actor.is_manager and task.assignee_id != actor_id:
            raise PermissionError("Only managers or the assignee can unassign tasks")
        task.assignee_id = None
        return self.task_repo.save(task)

    def start_task(self, actor_id: int, task_id: int) -> Task:
        return self.transition_task(actor_id, task_id, TaskStatus.in_progress)       

    def finish_task(self, actor_id: int, task_id: int) -> Task:
        return self.transition_task(actor_id, task_id, TaskStatus.done)

    def transition_task(self, actor_id: int, task_id: int, new_status: TaskStatus) -> Task:
        actor = self.get_user(actor_id)
        task = self.get_task(task_id)
        if not actor.is_manager and task.assignee_id != actor_id:
            raise PermissionError("Only managers and the assignee can update tasks' status")
        if not task.can_transition_to(new_status):
            raise ValueError(f"Task can not be moved from {task.status} to {new_status}")
        task.status = new_status
        return self.task_repo.save(task)

    def get_board(self, sprint_id: int) -> dict:
        tasks = self.task_repo.find_by_sprint(sprint_id)
        return {
            "todo": [task for task in tasks if task.status == TaskStatus.todo],
            "in_progress": [task for task in tasks if task.status == TaskStatus.in_progress],
            "done": [task for task in tasks if task.status == TaskStatus.done]
        }

    def get_user(self, user_id: int):
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise ValueError(f"User with ID: {user_id} does not exist")
        return user
    
    def get_task(self, task_id: int):
        task = self.task_repo.find_by_id(task_id)
        if not task:
            raise ValueError(f"Task with ID: {task_id} does not exist")
        return task

    # sua loi nhay bac
    def find_by_sprint(self, sprint_id: int) -> list[Task]:
        return self.task_repo.find_by_sprint(sprint_id)
    
    def find_by_id(self, task_id: int) -> Task:
        return self.task_repo.find_by_id(task_id)
    
    def get_all_tasks(self) -> list[Task]:
        return self.task_repo.find_all()