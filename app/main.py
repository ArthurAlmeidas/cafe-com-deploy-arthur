import os

from fastapi import Depends, FastAPI, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Cafe

app = FastAPI(title="Café com Deploy")


def preco_com_desconto(preco: float, pct: float) -> float:
    maximo = float(os.getenv("DESCONTO_MAXIMO", "50"))
    if not 0 <= pct <= maximo:
        raise ValueError("desconto inválido")
    return round(preco * (1 - pct / 100), 2)


class CafeIn(BaseModel):
    nome: str = Field(min_length=1, max_length=80)
    preco: float = Field(gt=0, lt=10000)
    origem: str | None = Field(default=None, max_length=80)


class CafeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nome: str
    preco: float
    origem: str | None = None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/version")
def version():
    return {"version": os.getenv("APP_VERSION", "dev")}


@app.get("/cafes", response_model=list[CafeOut])
def listar_cafes(db: Session = Depends(get_db)):
    return db.scalars(select(Cafe).order_by(Cafe.id)).all()


@app.post("/cafes", response_model=CafeOut, status_code=201)
def criar_cafe(dados: CafeIn, db: Session = Depends(get_db)):
    cafe = Cafe(nome=dados.nome, preco=dados.preco, origem=dados.origem)
    db.add(cafe)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="café já cadastrado")
    db.refresh(cafe)
    return cafe


@app.get("/cafes/{cafe_id}", response_model=CafeOut)
def obter_cafe(cafe_id: int, db: Session = Depends(get_db)):
    cafe = db.get(Cafe, cafe_id)
    if cafe is None:
        raise HTTPException(status_code=404, detail="café não encontrado")
    return cafe


@app.get("/cafes/{cafe_id}/preco")
def preco_do_cafe(
    cafe_id: int,
    desconto: float = Query(default=0),
    db: Session = Depends(get_db),
):
    cafe = db.get(Cafe, cafe_id)
    if cafe is None:
        raise HTTPException(status_code=404, detail="café não encontrado")
    try:
        final = preco_com_desconto(cafe.preco, desconto)
    except ValueError as erro:
        raise HTTPException(status_code=422, detail=str(erro))
    return {"id": cafe.id, "preco_original": cafe.preco, "preco_final": final}