# test_file.py

import json
from asyncio import all_tasks

from server import add_task, list_active_todos, update_subtask_status, get_task_by_id, complete_task, soft_delete_task

if __name__ == "__main__":
    # # == Professional Tasks ==
    # # 1. Complex task with subtasks and a due date
    # add_task(title="Prepare for Q4 Financial Review", description="Compile all sales and expense data.", due_date="2025-10-07", subtasks=["Gather sales reports", "Consolidate expense sheets", "Create presentation slides"])
    #
    # # 2. Simple task
    # add_task(title="Follow up with the design team on mockups")
    #
    # # 3. Detailed task with subtasks
    # add_task(title="Onboard the new marketing hire", description="Prepare accounts and schedule meetings.", subtasks=["Set up email and software accounts", "Schedule 1-on-1 with team lead", "Assign a starter project"])
    #
    # # 4. Simple task
    # add_task(title="Review and merge pull request #117")
    #
    # # 5. A task with a description and due date, but no subtasks
    # add_task(title="Submit project timesheet", description="Fill out hours for the 'Orion Project'.", due_date="2025-10-03")
    #
    # # == Personal Tasks ==
    # # 6. Complex personal task with a due date
    # add_task(title="Plan weekend trip to Lonavala", due_date="2025-10-11", subtasks=["Book hotel or Airbnb", "Check bus/train tickets", "Pack a small bag"])
    #
    # # 7. Simple recurring task
    # add_task(title="Pay monthly electricity bill")
    #
    # # 8. Task with subtasks
    # add_task(title="Weekly grocery shopping", subtasks=["Milk and bread", "Vegetables (Onion, Tomato)", "Fruits", "Cheese"])
    #
    # # 9. Simple task
    # add_task(title="Schedule a dentist appointment")
    #
    # # 10. A task with a description and due date
    # add_task(title="Renew car insurance", description="Policy is expiring next month, compare quotes online.",
    #              due_date="2025-10-25")
    # all_tasks = list_active_todos()
    # print(all_tasks)
    # print(update_subtask_status(3,"completed"))
    print(get_task_by_id(2))
    # print(complete_task(1))
    # print(soft_delete_task(5))