"""Base repository class."""
from typing import Generic, TypeVar, Type, Optional, List
from sqlalchemy.orm import Session
from src.entities.base import BaseEntity

ModelType = TypeVar("ModelType", bound=BaseEntity)


class BaseRepository(Generic[ModelType]):
    """Base repository with common CRUD operations."""

    def __init__(self, model: Type[ModelType], db: Session):
        """
        Initialize repository.

        Args:
            model: SQLAlchemy model class
            db: Database session
        """
        self.model = model
        self.db = db

    def get_by_id(self, id: int) -> Optional[ModelType]:
        """Get entity by ID."""
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Get all entities with pagination."""
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def create(self, **kwargs) -> ModelType:
        """Create new entity."""
        entity = self.model(**kwargs)
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def update(self, id: int, **kwargs) -> Optional[ModelType]:
        """Update entity by ID."""
        entity = self.get_by_id(id)
        if entity:
            for key, value in kwargs.items():
                setattr(entity, key, value)
            self.db.commit()
            self.db.refresh(entity)
        return entity

    def delete(self, id: int) -> bool:
        """Delete entity by ID."""
        entity = self.get_by_id(id)
        if entity:
            self.db.delete(entity)
            self.db.commit()
            return True
        return False

    def count(self) -> int:
        """Count total entities."""
        return self.db.query(self.model).count()

