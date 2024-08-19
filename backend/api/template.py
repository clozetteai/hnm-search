
from fastapi import APIRouter, Depends, status, HTTPException
from models.user import PromptTemplate
from api.helper.helper import get_db
from sqlalchemy.orm import Session

router = APIRouter()

# Prompt template endpoints (TODO)
@router.post("/prompt-templates/", status_code=status.HTTP_201_CREATED)
async def create_prompt_template(name: str, content: str, db: Session = Depends(get_db)):
    new_template = PromptTemplate(name=name, content=content)
    db.add(new_template)
    db.commit()
    db.refresh(new_template)
    return new_template

@router.get("/prompt-templates/")
async def list_prompt_templates(db: Session = Depends(get_db)):
    templates = db.query(PromptTemplate).all()
    return templates
