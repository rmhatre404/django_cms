import os
from django.core.exceptions import ValidationError

def validate_pdf(value):
    ext = os.path.splitext(value.name)[1]  # Get the file extension
    if ext.lower() != '.pdf':
        raise ValidationError("Only PDF files are allowed.")
