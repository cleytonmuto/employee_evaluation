# app/api/v1/evaluations.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.api.deps import get_current_user
from app.schemas.evaluation import EvaluationCreate, EvaluationOut
from app.crud.evaluation import create_evaluation, get_evaluation, list_evaluations, delete_evaluation
from app.crud.user import get_user_by_id

router = APIRouter()

@router.post("/", response_model=EvaluationOut)
def create_evaluation_endpoint(payload: EvaluationCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # current_user is the evaluator
    return create_evaluation(db, current_user, payload.evaluated_id, payload.score, payload.comments)

@router.get("/", response_model=list[EvaluationOut])
def list_evaluations_endpoint(db: Session = Depends(get_db), current_user = Depends(get_current_user), skip: int = 0, limit: int = 100):
    return list_evaluations(db, current_user=current_user, skip=skip, limit=limit)

@router.get("/{evaluation_id}", response_model=EvaluationOut)
def get_evaluation_endpoint(evaluation_id: UUID, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    ev = get_evaluation(db, evaluation_id)
    if ev is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    # allow admin, evaluator, or evaluated
    if current_user.role.name != "admin" and str(ev.evaluator_id) != str(current_user.id) and str(ev.evaluated_id) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return ev

@router.delete("/{evaluation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_evaluation_endpoint(evaluation_id: UUID, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    ev = get_evaluation(db, evaluation_id)
    if ev is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    # only admin can delete (customize if you prefer evaluator can delete their own)
    if current_user.role.name != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    delete_evaluation(db, ev)
