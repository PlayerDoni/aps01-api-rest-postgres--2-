from fastapi import APIRouter
from sqlmodel import select
from fastapi.responses import JSONResponse
from http import HTTPStatus

from src.models.resultados_model import Resultados
from src.config.database import get_session
from src.models.provas_model import Provas

resultados_router = APIRouter(prefix="/resultados")

@resultados_router.post("")
def cria_resultados(resultado: Resultados):
    with get_session() as session:
        
        statement = select(Provas).where(Provas.id == resultado.prova_id)
        prova = session.exec(statement).first()
        
        if not prova:
            return JSONResponse(content={"message": "prova não encontrada!!"}, status_code=HTTPStatus.BAD_REQUEST)
        
        r_corretas_prova = [prova.q1, prova.q2, prova.q3, prova.q4,prova.q5, prova.q6, prova.q7, prova.q8, prova.q9, prova.q10]
        r_alunos = [resultado.q1, resultado.q2, resultado.q3, resultado.q4, resultado.q5, resultado.q6, resultado.q7, 
                           resultado.q8, resultado.q9, resultado.q10]
        
        nota_aluno = 0
        
        for i in range(len(r_alunos)):
            r_aluno = r_alunos[i]
            r_correta = r_corretas_prova[i]
            
            if r_aluno == r_correta:
                nota_aluno = nota_aluno + 1
                
        resultado.nota = nota_aluno

        session.add(resultado)
        session.commit()
        session.refresh(resultado)
        return resultado
    

@resultados_router.get("/{prova_id}")
async def obtem_resultados(prova_id: int):
    with get_session() as session:
        statement = select(Provas).where(Provas.id == prova_id)
        prova = session.exec(statement).first()
        
        if not prova:
            return JSONResponse(content={"message": "prova não encontrada!!"}, status_code=HTTPStatus.BAD_REQUEST)
        
        statement2 = select(Resultados).where(Resultados.prova_id == prova_id)
        result_alunos = session.exec(statement2).first()
        
        if not result_alunos:
            return JSONResponse(content={"message": "Não a resultados para a prova!"}, status_code=HTTPStatus.BAD_REQUEST)
        
        json_resultados = []
        for resultado in result_alunos:
            nivel_aprovacao = ''
            if resultado.nota >= 7:
                nivel_aprovacao = "aprovado"
            elif resultado.nota < 7 and resultado.nota >= 5:
                nivel_aprovacao = "recuperação"
            else:
                nivel_aprovacao = "reprovado" 
            json = {
                "nome": resultado.aluno_nome,
                "nota": resultado.nota_final,
                "resultado_final": nivel_aprovacao 
            }
            json_resultados.append(json)
        
        json_completo = {
            "descricao_prova": prova.descricao,
            "data_aplicacao": prova.data_realizacao,
            "resultados_alunos": json_resultados
        }
        
    return json_completo

@resultados_router.patch("/provas_aplicadas/{resultado_id}")
def atualiza_respostas(resultado_id: int, respostas: Resultados):
    with get_session() as session:
        statement = select(Resultados).where(Resultados.id == resultado_id)
        resultado = session.exec(statement).first()
        
        if not resultado:
            return JSONResponse(content={"message": "Não a resultados"}, status_code=HTTPStatus.BAD_REQUEST)
        
        statement2 = select(Provas).where(Provas.id == resultado.prova_id)
        prova = session.exec(statement2).first()
        
        if not prova:
            return JSONResponse(content={"message": "Prova não encontrada"}, status_code=HTTPStatus.BAD_REQUEST)
        
        resultado.q1 = respostas.q1
        resultado.q2 = respostas.q2
        resultado.q3 = respostas.q3
        resultado.q4 = respostas.q4
        resultado.q5 = respostas.q5
        resultado.q6 = respostas.q6
        resultado.q7 = respostas.q7
        resultado.q8 = respostas.q8
        resultado.q9 = respostas.q9
        resultado.q10 = respostas.q10
        
        session.commit()
        session.refresh(resultado)
        
        statement3 = select(Resultados).where(Resultados.id == resultado_id)
        resultado_novo = session.exec(statement3).first()
        
        if not resultado_novo:
            return JSONResponse(content={"message": "Não a resultados novos"}, status_code=HTTPStatus.BAD_REQUEST)
        
        r_corretas_prova = [prova.q1, prova.q2, prova.q3, prova.q4,prova.q5, prova.q6, prova.q7, prova.q8, prova.q9, prova.q10]
        r_alunos_novo = [resultado.q1, resultado.q2, resultado.q3, resultado.q4, resultado.q5, resultado.q6, resultado.q7, 
                        resultado.q8, resultado.q9, resultado.q10]
        nota_aluno = 0
        
        for i in range(len(r_alunos_novo)):
            r_aluno = r_alunos_novo[i]
            r_correta = r_corretas_prova[i]
            
            if r_aluno == r_correta:
                nota_aluno = nota_aluno + 1
                
        resultado.nota = nota_aluno
        
        session.commit()
        session.refresh(resultado)
        return resultado
        