"""
Schemas Pydantic para criação de conteúdo e publicação no Instagram.
"""
from typing import Optional

from pydantic import BaseModel, Field


class CreateContentRequest(BaseModel):
    """Parâmetros para gerar imagem + legenda do post."""

    tema: str = Field(..., description="Tema ou assunto do post")
    estilo_visual: Optional[str] = Field(
        "moderno e clean",
        description="Estilo da imagem (ex: minimalista, colorido, profissional)",
    )
    tom_legenda: Optional[str] = Field(
        "amigável",
        description="Tom da legenda (ex: informal, motivacional, profissional)",
    )
    hashtags_sugeridas: Optional[bool] = Field(
        True,
        description="Incluir sugestão de hashtags na legenda",
    )
    max_caracteres_legenda: Optional[int] = Field(
        2200,
        ge=100,
        le=2200,
        description="Máximo de caracteres da legenda (limite Instagram ~2200)",
    )


class CreateContentResponse(BaseModel):
    """Resposta com imagem gerada e legenda."""

    imagem_url: str = Field(..., description="URL da imagem gerada (DALL-E)")
    legenda: str = Field(..., description="Legenda gerada (ChatGPT)")
    prompt_imagem: Optional[str] = Field(None, description="Prompt usado na geração da imagem")
    sucesso: bool = True


class PostToInstagramRequest(BaseModel):
    """Dados para publicar no feed do Instagram."""

    imagem_url: str = Field(..., description="URL pública da imagem a ser publicada")
    legenda: str = Field(..., description="Legenda do post")


class PostToInstagramResponse(BaseModel):
    """Resposta da publicação no Instagram."""

    sucesso: bool = Field(..., description="Se a publicação foi criada com sucesso")
    post_id: Optional[str] = Field(None, description="ID do post no Instagram")
    mensagem: Optional[str] = Field(None, description="Mensagem de erro ou confirmação")
