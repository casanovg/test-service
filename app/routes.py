"""
API Routes / Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from . import schemas, models
from .database import get_db
from .config import settings

router = APIRouter()


@router.get("/", tags=["Root"])
async def root():
    """Root endpoint - welcome message"""
    return {
        "message": f"Welcome to {settings.SERVICE_NAME}",
        "version": settings.SERVICE_VERSION,
        "docs": "/docs"
    }


@router.get("/health", response_model=schemas.HealthResponse, tags=["Health"])
async def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint - verifies database connectivity
    """
    try:
        # Test database connection
        db.execute("SELECT 1")
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return schemas.HealthResponse(
        status="healthy" if db_status == "connected" else "unhealthy",
        service=settings.SERVICE_NAME,
        version=settings.SERVICE_VERSION,
        database=db_status
    )


# Example CRUD endpoints - customize for your use case

@router.get("/examples", response_model=List[schemas.ExampleResponse], tags=["Examples"])
async def get_examples(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get list of examples"""
    examples = db.query(models.ExampleModel)\
        .offset(skip)\
        .limit(limit)\
        .all()
    return examples


@router.get("/examples/{example_id}", response_model=schemas.ExampleResponse, tags=["Examples"])
async def get_example(example_id: int, db: Session = Depends(get_db)):
    """Get example by ID"""
    example = db.query(models.ExampleModel)\
        .filter(models.ExampleModel.id == example_id)\
        .first()
    
    if not example:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Example with id {example_id} not found"
        )
    
    return example


@router.post("/examples", response_model=schemas.ExampleResponse, status_code=status.HTTP_201_CREATED, tags=["Examples"])
async def create_example(
    example: schemas.ExampleCreate,
    db: Session = Depends(get_db)
):
    """Create new example"""
    db_example = models.ExampleModel(**example.model_dump())
    db.add(db_example)
    db.commit()
    db.refresh(db_example)
    return db_example


@router.put("/examples/{example_id}", response_model=schemas.ExampleResponse, tags=["Examples"])
async def update_example(
    example_id: int,
    example: schemas.ExampleUpdate,
    db: Session = Depends(get_db)
):
    """Update example"""
    db_example = db.query(models.ExampleModel)\
        .filter(models.ExampleModel.id == example_id)\
        .first()
    
    if not db_example:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Example with id {example_id} not found"
        )
    
    # Update only provided fields
    update_data = example.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_example, field, value)
    
    db.commit()
    db.refresh(db_example)
    return db_example


@router.delete("/examples/{example_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Examples"])
async def delete_example(example_id: int, db: Session = Depends(get_db)):
    """Delete example"""
    db_example = db.query(models.ExampleModel)\
        .filter(models.ExampleModel.id == example_id)\
        .first()
    
    if not db_example:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Example with id {example_id} not found"
        )
    
    db.delete(db_example)
    db.commit()
    return None
