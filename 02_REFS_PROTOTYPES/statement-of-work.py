# This Python script is a Statement of Work (SOW) generator that helps create professional project documentation through a simple command-line interface.

# Here's what it does in simple terms:

# 1. **Data Structure**: The code defines two main data models:
#    - `Milestone`: Tracks project checkpoints with descriptions, due dates, and who's responsible
#    - `StatementOfWork`: The complete document structure with all project details

# 2. **User Interaction**: The program asks you questions about your project:
#    - Basic info (project title, client name, manager, dates)
#    - Project objectives
#    - Scope items (what's included)
#    - Deliverables (what you'll produce)
#    - Milestones (key checkpoints with dates)
#    - Optional assumptions and approval information

# 3. **Data Validation**: It uses Pydantic to ensure data quality, like checking that the project title is at least 5 characters long.

# 4. **Document Creation**: After collecting all information, it:
#    - Formats everything into a professional template
#    - Shows you the completed document
#    - Saves it as a text file named after your project

# 5. **Error Handling**: If any information doesn't meet requirements, it shows a helpful error message.

# The code is well-structured with separate sections for data models, document templates, user interaction, formatting helpers, and the main process flow. It's designed to make creating standardized project documentation quick and error-free.
# Import necessary tools
from typing import List, Optional
from datetime import date
from pydantic import BaseModel, ValidationError  # For data validation
import textwrap  # For neat text formatting

# ========== DATA STRUCTURES ========== #
# Define what a project milestone looks like
class Milestone(BaseModel):
    description: str      # What needs to be done
    due_date: str         # When it's due (as string for flexibility)
    owner: Optional[str] = None  # Who's responsible (optional)

# Blueprint for the entire Statement of Work document
class StatementOfWork(BaseModel):
    project_title: str     # Name of the project
    client_name: str       # Who we're doing it for
    project_manager: str   # Who's in charge
    start_date: str        # Project start date
    end_date: str          # Project end date
    objectives: str        # What we aim to achieve
    scope: List[str]       # What's included in the project
    deliverables: List[str]  # What we'll actually produce
    milestones: List[Milestone]  # Key project checkpoints
    assumptions: Optional[List[str]] = None  # Things we're assuming
    approval: Optional[str] = None  # Who signs off

# ========== DOCUMENT TEMPLATE ========== #
# This is our SOW form that will auto-fill with user answers
SOW_TEMPLATE = textwrap.dedent("""
                        STATEMENT OF WORK - {project_title}

Client: {client_name}
Project Manager: {project_manager}
Dates: {start_date} to {end_date}

1. OBJECTIVES
{objectives}

2. SCOPE OF WORK
{scope}

3. DELIVERABLES
{deliverables}

4. MILESTONES
{milestones}

5. ASSUMPTIONS
{assumptions}

6. APPROVAL
{approval}
""")

# ========== USER CONVERSATION ========== #
# This function chats with the user to collect all needed information
def collect_sow_data() -> StatementOfWork:
    # Dictionary of questions we need to ask
    questions = {
        'project_title': "Enter project title: ",
        'client_name': "Enter client name: ",
        'project_manager': "Enter project manager name: ",
        'start_date': "Enter start date (MM/DD/YYYY): ",
        'end_date': "Enter end date (MM/DD/YYYY): ",
        'objectives': "Enter project objectives (1-2 paragraphs):\n",
        'scope': "Enter scope items (one per line, empty to finish):\n",
        'deliverables': "Enter deliverables (one per line, empty to finish):\n",
    }

    responses = {}  # Where we'll store user answers

    # Ask each question one by one
    for field, prompt in questions.items():
        # Handle list-type answers (scope/deliverables)
        if field in ['scope', 'deliverables']:
            print(prompt)
            responses[field] = []
            # Keep asking for items until user enters nothing
            while True:
                item = input("> ")
                if not item:  # Stop when user just presses Enter
                    break
                responses[field].append(item)
        else:
            # For normal single-answer questions
            responses[field] = input(prompt)

    # Special handling for milestones (more complex structure)
    responses['milestones'] = []
    print("\nLet's add project milestones:")
    while True:
        print("\nAdd a milestone (or type 'done' to finish):")
        desc = input("Description: ")
        if desc.lower() == 'done':
            break
        due = input("Due date (MM/DD/YYYY): ")
        owner = input("Owner (optional): ")
        # Store each milestone as a dictionary
        responses['milestones'].append({
            'description': desc,
            'due_date': due,
            'owner': owner or None  # Store None if empty
        })

    # Optional information collection
    print("\nAny assumptions we should note? (optional)")
    responses['assumptions'] = []
    while True:
        assumption = input("> ")
        if not assumption:
            break
        responses['assumptions'].append(assumption)

    # Final optional approval information
    responses['approval'] = input("\nApproval name/role (optional): ") or None

    # Package everything up with validation
    return StatementOfWork(**responses)

# ========== FORMATTING HELPERS ========== #
# Makes lists look pretty with bullet points
def format_list(items: List[str], prefix="- ") -> str:
    return '\n'.join([f"{prefix}{item}" for item in items])

# Special formatting for milestones with dates and owners
def format_milestones(milestones: List[Milestone]) -> str:
    return '\n\n'.join([
        f"• {ms.description}\n  Due: {ms.due_date}" +
        (f"\n  Owner: {ms.owner}" if ms.owner else "")
        for ms in milestones
    ])

# ========== MAIN PROCESS ========== #
def generate_sow():
    try:
        # Step 1: Collect all information from user
        sow_data = collect_sow_data()

        # Step 2: Format the collected data for the template
        formatted_scope = format_list(sow_data.scope)
        formatted_deliverables = format_list(sow_data.deliverables)
        formatted_milestones = format_milestones(sow_data.milestones)
        formatted_assumptions = format_list(sow_data.assumptions) if sow_data.assumptions else "N/A"

        # Step 3: Fill in the template
        document = SOW_TEMPLATE.format(
            **sow_data.dict(),  # Basic fields
            scope=formatted_scope,
            deliverables=formatted_deliverables,
            milestones=formatted_milestones,
            assumptions=formatted_assumptions
        )

        # Step 4: Show and save the result
        print("\nGENERATED STATEMENT OF WORK:\n")
        print(document)

        # Create a filename based on project title
        filename = f"{sow_data.project_title.replace(' ', '_')}_SOW.txt"
        with open(filename, "w") as f:
            f.write(document)
        print(f"\nDocument saved to {filename}")

    # Handle any data validation errors
    except ValidationError as e:
        print(f"Oops! There was a problem with your input: {e}")

# Start the program when run directly
if __name__ == "__main__":
    generate_sow()
