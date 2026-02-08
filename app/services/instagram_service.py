"""
Serviço de publicação no Instagram via Facebook Graph API.
"""
from typing import Optional

import httpx

from app.core.config import settings


class InstagramService:
    """
    Publica conteúdo no feed do Instagram usando a Facebook Graph API.

    Fluxo: criar container de mídia -> publicar o container.
    A imagem deve estar em uma URL pública acessível pelo Meta.
    """

    BASE_URL = "https://graph.facebook.com/v21.0"

    def __init__(self) -> None:
        self._token: Optional[str] = settings.user_access_token
        self._ig_user_id: Optional[str] = settings.ig_user_id

    def _ensure_config(self) -> None:
        if not self._token:
            raise ValueError(
                "USER_ACCESS_TOKEN não configurado. Configure no .env para publicar no Instagram."
            )
        if not self._ig_user_id:
            raise ValueError(
                "IG_USER_ID não configurado. Configure no .env (ID da conta Business/Creator)."
            )

    def publicar_no_feed(self, imagem_url: str, legenda: str) -> dict:
        """
        Publica uma imagem no feed do Instagram.

        Args:
            imagem_url: URL pública da imagem (deve ser acessível pelo servidor do Meta).
            legenda: Legenda do post.

        Returns:
            Dict com sucesso, post_id e/ou mensagem de erro.
        """
        self._ensure_config()
        url = f"{self.BASE_URL}/{self._ig_user_id}/media"

        # 1) Criar container de mídia (image_url + caption)
        payload = {
            "image_url": imagem_url,
            "caption": legenda[:2200],
            "access_token": self._token,
        }

        with httpx.Client(timeout=30.0) as client:
            resp = client.post(url, params=payload)
            data = resp.json()

        if "error" in data:
            return {
                "sucesso": False,
                "post_id": None,
                "mensagem": data["error"].get("message", str(data)),
            }

        container_id = data.get("id")
        if not container_id:
            return {
                "sucesso": False,
                "post_id": None,
                "mensagem": "Resposta da API sem ID do container",
            }

        # 2) Publicar o container (criar o post)
        publish_url = f"{self.BASE_URL}/{self._ig_user_id}/media_publish"
        publish_payload = {
            "creation_id": container_id,
            "access_token": self._token,
        }

        with httpx.Client(timeout=30.0) as client:
            pub_resp = client.post(publish_url, params=publish_payload)
            pub_data = pub_resp.json()

        if "error" in pub_data:
            return {
                "sucesso": False,
                "post_id": None,
                "mensagem": pub_data["error"].get("message", str(pub_data)),
            }

        post_id = pub_data.get("id")
        return {
            "sucesso": True,
            "post_id": post_id,
            "mensagem": "Post publicado no feed do Instagram com sucesso.",
        }
