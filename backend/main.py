from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from schemas import Inquiry, InquiryResponse
from database import create_document, get_documents, db

app = FastAPI(title="HVAC Company API", version="1.0.0")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["health"]) 
def root():
    return {"status": "ok", "service": "hvac"}


@app.get("/test", tags=["health"]) 
def test_db():
    try:
        if db is None:
            raise Exception("DB not initialized")
        # ping by listing collections (non-intrusive)
        _ = db.list_collection_names()
        return {"database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/inquiries", response_model=InquiryResponse, tags=["inquiries"]) 
def create_inquiry(inquiry: Inquiry):
    try:
        inserted_id = create_document("inquiry", inquiry)
        return InquiryResponse(id=inserted_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class Testimonial(BaseModel):
    name: str
    quote: str
    role: str


@app.get("/testimonials", response_model=List[Testimonial], tags=["content"]) 
def get_testimonials():
    # Static for demo; could be from DB later
    return [
        Testimonial(name="Marius P.", role="Dezvoltator imobiliar", quote="Intervenție rapidă și execuție impecabilă. Recomand!"),
        Testimonial(name="Irina D.", role="Proprietar casă", quote="Au instalat încălzirea în pardoseală la superlativ. Comunicare excelentă."),
        Testimonial(name="Andrei S.", role="Administrator firmă", quote="Corecți, punctuali și transparenti. Am primit garanție reală.")
    ]
