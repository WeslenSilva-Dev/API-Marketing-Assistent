"""
Endpoint: publicar no feed do Instagram via Facebook Graph API.
"""
from fastapi import APIRouter, HTTPException

from app.schemas import PostToInstagramRequest, PostToInstagramResponse
from app.services.instagram_service import InstagramService

router = APIRouter()


@router.post("/post", response_model=PostToInstagramResponse)
def postar_no_instagram(body: PostToInstagramRequest) -> PostToInstagramResponse:
    """
    Publica uma imagem no feed do Instagram.

    A **imagem_url** deve ser uma URL pública acessível pelos servidores do Meta.
    Use o resultado de `POST /content/create` (imagem_url) ou qualquer URL pública.
    """
    try:
        service = InstagramService()
        result = service.publicar_no_feed(
            imagem_url=body.imagem_url,
            legenda=body.legenda,
        )
        return PostToInstagramResponse(
            sucesso=result["sucesso"],
            post_id=result.get("post_id"),
            mensagem=result.get("mensagem"),
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao publicar: {e!s}")
