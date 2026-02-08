"""
Orquestração: geração de prompt da imagem com LangChain + DALL-E + legenda com ChatGPT.
"""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.core.config import settings
from app.schemas.content import CreateContentRequest, CreateContentResponse
from .image_service import ImageService
from .caption_service import CaptionService


PROMPT_IMAGEM_TEMPLATE = """Você é um diretor de arte para posts no Instagram.
Com base no tema e no estilo visual pedidos, crie UM único prompt em inglês para gerar uma imagem com DALL-E 3.

- Tema do post: {tema}
- Estilo visual desejado: {estilo_visual}

Regras do prompt:
- Seja específico e visual (cores, composição, ambiente).
- O prompt deve resultar em uma imagem adequada para feed do Instagram, quadrada ou vertical.
- Retorne APENAS o texto do prompt, sem aspas nem explicações.
- Máximo 2 a 4 frases."""


class ContentService:
    """Orquestra geração de imagem (DALL-E) e legenda (ChatGPT via LangChain)."""

    def __init__(self) -> None:
        self._image_service = ImageService()
        self._caption_service = CaptionService()
        self._prompt_chain = None

    def _get_prompt_chain(self):
        if self._prompt_chain is None:
            llm = ChatOpenAI(
                model="gpt-4o-mini",
                api_key=settings.openai_api_key,
                temperature=0.6,
            )
            prompt = ChatPromptTemplate.from_messages([
                ("system", "Você gera prompts em inglês para geração de imagens."),
                ("human", PROMPT_IMAGEM_TEMPLATE),
            ])
            self._prompt_chain = prompt | llm | StrOutputParser()
        return self._prompt_chain

    def criar_conteudo(self, body: CreateContentRequest) -> CreateContentResponse:
        """
        Gera imagem (DALL-E) e legenda (ChatGPT) com base nos parâmetros.

        1. LangChain gera o prompt da imagem a partir de tema + estilo.
        2. DALL-E gera a imagem.
        3. LangChain/ChatGPT gera a legenda.
        """
        # 1) Prompt da imagem com LangChain
        chain = self._get_prompt_chain()
        prompt_imagem = chain.invoke({
            "tema": body.tema,
            "estilo_visual": body.estilo_visual or "moderno e clean",
        })
        prompt_imagem = (prompt_imagem or "").strip()

        # 2) Gerar imagem com DALL-E
        imagem_url = self._image_service.gerar_imagem(prompt_imagem)

        # 3) Gerar legenda com LangChain/ChatGPT
        legenda = self._caption_service.gerar_legenda(
            tema=body.tema,
            estilo_visual=body.estilo_visual or "moderno e clean",
            tom_legenda=body.tom_legenda or "amigável",
            hashtags_sugeridas=body.hashtags_sugeridas if body.hashtags_sugeridas is not None else True,
            max_caracteres=body.max_caracteres_legenda or 2200,
        )

        return CreateContentResponse(
            imagem_url=imagem_url,
            legenda=legenda,
            prompt_imagem=prompt_imagem,
            sucesso=True,
        )
