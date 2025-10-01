
from dataclasses import dataclass, field
from typing import Optional, Dict, List

@dataclass
class Subtask:
    id: int
    title: str
    status: str
    created_at: str
    parent_task_id: int

@dataclass
class Task:
    id: int
    title: str
    description: Optional[str] = ""
    status: str = "pending"
    due_date: Optional[str] = None
    created_at: str = ""
    subtasks: List[Subtask] = field(default_factory=list)

    def from_row(cls, row: tuple):
        """python object from tuple because sql.row_factory return tuple"""
        return cls(
            id=row[0], title=row[1], description=row[2],
            status=row[3], due_date=row[4], created_at=row[5]
        )
    def to_dict(self) -> Dict[str, any]:
        return {
            'id': self.id, 'title': self.title, 'description': self.description,
            'status': self.status, 'due_date': self.due_date, 'created_at': self.created_at,
            'subtasks': [sub.__dict__ for sub in self.subtasks]
        }