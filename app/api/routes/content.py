"""
Endpoint: criar conteúdo (imagem + legenda) com base em parâmetros.
"""
from fastapi import APIRouter, HTTPException

from app.schemas import CreateContentRequest, CreateContentResponse
from app.services.content_service import ContentService

router = APIRouter()


@router.post("/create", response_model=CreateContentResponse)
def criar_conteudo(body: CreateContentRequest) -> CreateContentResponse:
    """
    Gera uma imagem (DALL-E) e uma legenda (ChatGPT via LangChain) para post no Instagram.

    - **tema**: assunto do post (obrigatório).
    - **estilo_visual**: estilo da imagem (ex.: minimalista, colorido).
    - **tom_legenda**: tom do texto (ex.: informal, motivacional).
    - **hashtags_sugeridas**: incluir hashtags na legenda.
    - **max_caracteres_legenda**: limite de caracteres (até 2200).
    """
    try:
        service = ContentService()
        return service.criar_conteudo(body)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar conteúdo: {e!s}")
