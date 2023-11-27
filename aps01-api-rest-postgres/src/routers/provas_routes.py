from fastapi import APIRouter
from fastapi.responses import JSONResponse
from http import HTTPStatus
from sqlmodel import select

from src.models.provas_model import Provas
from src.models.resultados_model import Resultados
from src.config.database import get_session

provas_router = APIRouter(prefix="/provas")

@provas_router.post("")
def cria_prova(prova: Provas):
    with get_session() as session:
        statement = select(Provas).where(Provas.desc_avaliacao == prova.desc_avaliacao, 
                    Provas.data_realizacao == prova.data_realizacao)
        p_existe = session.exec(statement=statement).first()
        if p_existe:
           return JSONResponse(content={"message": "Prova já existe!"}, status_code=HTTPStatus.BAD_REQUEST)
        else:
            session.add(prova)
            session.commit()
            session.refresh(prova)
            return prova
        
        
@provas_router.delete("/{prova_id}")
def deletar_prova(id: int):
    with get_session() as session:
        statement = select(Resultados).where(Resultados.prova_id == id)
        resultado = session.exec(statement=statement).first()
        
        if resultado:
            return JSONResponse(content={"message": "Prova já possui resltados!"}, status_code=HTTPStatus.BAD_REQUEST)
        
    session.delete(resultado)
    session.commit
    
    return JSONResponse(content=None, status_code=HTTPStatus.NO_CONTENT)