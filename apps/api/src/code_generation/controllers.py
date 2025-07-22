
from pathlib import Path

def generate_code(file_path: str, content: str) -> dict:
    """
    Writes the given content to the specified file.
    """
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    return {"message": f"Successfully generated code for {file_path}"}
