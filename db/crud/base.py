from typing import Any, TypeVar, Generic, Type, Optional, List, Union, Dict

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status

from db.session import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

# CRUD 的基类，其他CRUD应继承此类
class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        result = db.query(self.model).filter(self.model.id == id).first()
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=self.model.__class__.__name__ + "not found",
            )
        return result

    def get_multi(self, db: Session, skip: int=0, limit: int=100) -> List[ModelType]:
        results = db.query(self.model).offset(skip).limit(limit).all()
        return results

    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, id:int, obj_in: UpdateSchemaType) -> ModelType:
        db_obj = self.get(db, id)
        if not db_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=self.model.__class__.__name__ + "not found"
            )
        update_data = obj_in.dict(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_obj, key, value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: int):
        db_obj = self.get(db, id)
        if not db_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail= self.model.__class__.__name__ + "not found"
            )
        db.delete(db_obj)
        db.commit()
        return db_obj


