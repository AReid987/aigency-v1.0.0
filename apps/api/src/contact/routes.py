
from fastapi import APIRouter
from apps.api.src.contact.controllers import process_contact_form, ContactForm

router = APIRouter()

@router.post("/contact")
async def contact(form_data: ContactForm):
    return await process_contact_form(form_data)
