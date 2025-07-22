
from pydantic import BaseModel

class ContactForm(BaseModel):
    name: str
    email: str
    message: str

async def process_contact_form(form_data: ContactForm) -> dict:
    """
    Processes the contact form data.
    """
    print(f"Received contact form submission from {form_data.name} ({form_data.email}):")
    print(f"Message: {form_data.message}")
    return {"message": "Contact form submitted successfully!"}
