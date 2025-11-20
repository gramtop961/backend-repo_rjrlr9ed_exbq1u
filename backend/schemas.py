from pydantic import BaseModel, Field, constr
from typing import Optional

class Inquiry(BaseModel):
    name: constr(strip_whitespace=True, min_length=2) = Field(..., description="Numele solicitantului")
    phone: constr(strip_whitespace=True, min_length=6) = Field(..., description="Telefon contact")
    message: constr(strip_whitespace=True, min_length=5) = Field(..., description="Mesaj / detalii lucrare")

class InquiryResponse(BaseModel):
    id: str
    status: str = "received"
