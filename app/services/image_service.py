"""
Serviço de geração de imagens com DALL-E (OpenAI).
"""
from typing import Optional

from openai import OpenAI

from app.core.config import settings


class ImageService:
    """Gera imagens a partir de prompt usando DALL-E 3."""

    def __init__(self) -> None:
        self._client: Optional[OpenAI] = None

    @property
    def client(self) -> OpenAI:
        if self._client is None:
            if not settings.openai_api_key:
                raise ValueError("OPENAI_API_KEY não configurada no .env")
            self._client = OpenAI(api_key=settings.openai_api_key)
        return self._client

    def gerar_imagem(
        self,
        prompt: str,
        tamanho: str = "1024x1024",
        qualidade: str = "standard",
        estilo: str = "vivid",
    ) -> str:
        """
        Gera uma imagem com DALL-E 3 e retorna a URL da imagem.

        Args:
            prompt: Descrição da imagem desejada.
            tamanho: 1024x1024, 1792x1024 ou 1024x1792.
            qualidade: "standard" ou "hd".
            estilo: "vivid" ou "natural".

        Returns:
            URL da imagem gerada.
        """
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=tamanho,
            quality=qualidade,
            style=estilo,
            n=1,
        )
        image = response.data[0]
        url = image.url
        if not url:
            raise RuntimeError("DALL-E não retornou URL da imagem")
        return url
