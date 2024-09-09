from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
from datetime import datetime

app = FastAPI()

# Banco de dados em memória
banco = {}

# Modelo de dados
class Noticia(BaseModel):
    titulo: str
    conteudo: str
    autor: str
    publicado: bool = False

# Endpoints

@app.get("/noticias")
def listar_todas_noticias():
    return banco

@app.get("/noticias/buscar/{noticia_id}")
def listar_noticia(noticia_id: str):
    if noticia_id not in banco:
        raise HTTPException(status_code=404, detail="Notícia não encontrada")
    return banco[noticia_id]

@app.post("/noticias/adicionar")
def adicionar_noticia(noticia: Noticia):
    identificador = uuid.uuid4().hex
    data_criacao = str(datetime.now())
    banco[identificador] = {
        'id': identificador,
        'titulo': noticia.titulo,
        'conteudo': noticia.conteudo,
        'autor': noticia.autor,
        'publicado': noticia.publicado,
        'data_criacao': data_criacao
    }
    return banco[identificador]

@app.put("/noticias/editar/{noticia_id}")
def editar_noticia(noticia_id: str, noticia: Noticia):
    if noticia_id not in banco:
        raise HTTPException(status_code=404, detail="Notícia não encontrada")
    data_criacao = banco[noticia_id]['data_criacao']
    data_ultima_edicao = str(datetime.now())
    banco[noticia_id] = {
        'id': noticia_id,
        'titulo': noticia.titulo,
        'conteudo': noticia.conteudo,
        'autor': noticia.autor,
        'publicado': noticia.publicado,
        'data_criacao': data_criacao,
        'data_ultima_edicao': data_ultima_edicao
    }
    return banco[noticia_id]

@app.delete("/noticias/remover/{noticia_id}")
def remover_noticia(noticia_id: str):
    if noticia_id not in banco:
        raise HTTPException(status_code=404, detail="Notícia não encontrada")
    del banco[noticia_id]
    return {"detail": "Notícia removida com sucesso"}

# Para rodar o servidor, use o comando:
# uvicorn main:app --reload