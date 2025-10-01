
from mcp.server.fastmcp import FastMCP
from datetime import datetime
from typing import List, Dict, Any, Union
from database import get_db_connection

# MCP server instance
server = FastMCP(name="todo_manager", host="127.0.0.1", port=8000)

#tools
@server.tool()
def list_active_todos() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    try:
        tasks_rows = conn.execute("SELECT * FROM tasks WHERE status == 'pending'").fetchall()

        tasks_with_subtasks = []
        for task_row in tasks_rows:
            task_dict = dict(task_row)
            subtasks_rows = conn.execute(
                "SELECT * FROM subtasks WHERE parent_task_id = ? AND status == 'pending'",
                (task_dict['id'],)
            ).fetchall()
            task_dict['subtasks'] = [dict(row) for row in subtasks_rows]
            tasks_with_subtasks.append(task_dict)

        return tasks_with_subtasks
    finally:
        conn.close()


@server.tool()
def get_task_by_id(task_id: int) -> Union[Dict[str, Any], str]:
    conn = get_db_connection()
    try:
        task_row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if not task_row:
            return f"Error: Task with ID {task_id} not found."

        task_dict = dict(task_row)
        subtasks_rows = conn.execute(
            "SELECT * FROM subtasks WHERE parent_task_id = ?",
            (task_dict['id'],)
        ).fetchall()
        task_dict['subtasks'] = [dict(row) for row in subtasks_rows]
        return task_dict
    finally:
        conn.close()


@server.tool()
def add_task(title: str, description: str = "", due_date: str = None, subtasks: List[str] = None) -> str:
    """add task and subtask"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #task
        cursor.execute(
            "INSERT INTO tasks (title, description, status, due_date, created_at) VALUES (?, ?, ?, ?, ?)",
            (title, description, "pending", due_date, created_at)
        )
        parent_task_id = cursor.lastrowid

        # If subtasks
        if subtasks:
            for subtask_title in subtasks:
                cursor.execute(
                    "INSERT INTO subtasks (title, status, created_at, parent_task_id) VALUES (?, ?, ?, ?)",
                    (subtask_title, "pending", created_at, parent_task_id)
                )

        conn.commit()

        subtask_count = len(subtasks) if subtasks else 0
        return f"Task '{title}' (ID: {parent_task_id}) and {subtask_count} subtasks added successfully."

    except Exception as e:
        conn.rollback()  # Undo changes if anything went wrong
        return f"An error occurred: {e}"
    finally:
        conn.close()


@server.tool()
def update_subtask_status(subtask_id: int, status: str) -> str:
    if status not in ['pending', 'completed', 'inactive']:
        return "Error: Invalid status. Must be 'pending', 'completed', or 'inactive'."
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE subtasks SET status = ? WHERE id = ?", (status, subtask_id))
        rows_affected = cursor.rowcount
        conn.commit()
        if rows_affected > 0:
            return f"Subtask ID {subtask_id} status updated to '{status}'."
        else:
            return f"Error: Subtask with ID {subtask_id} not found."
    finally:
        conn.close()


@server.tool()
def complete_task(task_id: int) -> str:
    """
    Marks as 'completed'.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET status = 'completed' WHERE id = ?", (task_id,))
        rows_affected = cursor.rowcount
        conn.commit()
        if rows_affected > 0:
            return f"Task ID {task_id} marked as completed."
        else:
            return f"Error: Task with ID {task_id} not found."
    finally:
        conn.close()


@server.tool()
def soft_delete_task(task_id: int) -> str:
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET status = 'inactive' WHERE id = ?", (task_id,))
        rows_affected = cursor.rowcount
        if rows_affected > 0:
            cursor.execute("UPDATE subtasks SET status = 'inactive' WHERE parent_task_id = ?", (task_id,))
            conn.commit()
            return f"Task ID {task_id} and all its subtasks were set to inactive."
        else:
            conn.rollback()
            return f"Error: Task with ID {task_id} not found."
    finally:
        conn.close()


if __name__ == "__main__":
    print("Starting MCP Server...")
    server.run(transport="streamable-http")