
from typing import List, Dict, Any
from uuid import UUID

async def get_kanban_board_data(project_id: UUID) -> Dict[str, Any]:
    """
    Retrieves mock Kanban board data for a given project.
    """
    # Mock data based on the provided stories
    epics = [
        {
            "id": "epic-1",
            "title": "The Aigency Collaboratory & Development Core",
            "stories": [
                {
                    "id": "story-1-1",
                    "title": "Story 1.1: Initiate a New Project via Conversation",
                    "status": "Done"
                },
                {
                    "id": "story-1-2",
                    "title": "Story 1.2: Scaffold the Project's File Structure",
                    "status": "Done"
                },
                {
                    "id": "story-1-3",
                    "title": "Story 1.3: Generate Initial Boilerplate Code",
                    "status": "Done"
                },
                {
                    "id": "story-1-4",
                    "title": "Story 1.4: Add a Functional Contact Form",
                    "status": "Done"
                }
            ]
        },
        {
            "id": "epic-2",
            "title": "Agile Project Management",
            "stories": [
                {
                    "id": "story-2-1",
                    "title": "Story 2.1: View Project Plan on Kanban Board",
                    "status": "To Do"
                },
                {
                    "id": "story-2-2",
                    "title": "Story 2.2: Update Story Status via Drag and Drop",
                    "status": "To Do"
                }
            ]
        },
        {
            "id": "epic-3",
            "title": "Prototyping & Visualization Showcase",
            "stories": [
                {
                    "id": "story-3-1",
                    "title": "Story 3.1: Preview Generated Web Application",
                    "status": "To Do"
                },
                {
                    "id": "story-3-2",
                    "title": "Story 3.2: Create and Display Data Visualization",
                    "status": "Done"
                }
            ]
        }
    ]

    # Organize stories by status for Kanban columns
    columns = {
        "To Do": [],
        "In Progress": [],
        "Done": []
    }

    for epic in epics:
        for story in epic["stories"]:
            status = story["status"]
            if status in columns:
                columns[status].append({"epic_id": epic["id"], "epic_title": epic["title"], **story})

    return {"project_id": str(project_id), "epics": epics, "columns": columns}

async def update_story_status(story_id: str, new_status: str) -> Dict[str, str]:
    """
    Simulates updating the status of a story.
    """
    # In a real application, you would update the database here.
    # For this POC, we just acknowledge the update.
    return {"message": f"Story {story_id} status updated to {new_status}."}
