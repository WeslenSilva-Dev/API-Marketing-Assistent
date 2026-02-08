"""
Serviço de geração de legendas com LangChain e ChatGPT (OpenAI).
"""
from typing import Optional

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.core.config import settings


# Template para geração de legenda com parâmetros do usuário
LEGENDA_PROMPT = """Você é um redator especializado em conteúdo para Instagram.
Crie UMA legenda para um post do Instagram com as seguintes especificações:

- Tema do post: {tema}
- Estilo visual da imagem: {estilo_visual}
- Tom da legenda: {tom_legenda}
- Incluir hashtags relevantes ao final: {hashtags}
- Limite de caracteres: até {max_caracteres} caracteres (respeite o limite do Instagram).

Regras:
- A legenda deve ser engajadora e adequada ao tema e tom pedidos.
- Use quebras de linha se fizer sentido para leitura.
- Se hashtags forem pedidas, adicione 3 a 8 hashtags no final, separadas por espaço.
- Retorne APENAS o texto da legenda, sem aspas extras ou explicações."""


class CaptionService:
    """Gera legendas para posts usando LangChain e ChatGPT."""

    def __init__(self) -> None:
        self._llm: Optional[ChatOpenAI] = None
        self._chain = None

    @property
    def llm(self) -> ChatOpenAI:
        if self._llm is None:
            if not settings.openai_api_key:
                raise ValueError("OPENAI_API_KEY não configurada no .env")
            self._llm = ChatOpenAI(
                model="gpt-4o-mini",
                api_key=settings.openai_api_key,
                temperature=0.7,
            )
        return self._llm

    def _get_chain(self):
        if self._chain is None:
            prompt = ChatPromptTemplate.from_messages([
                ("system", "Você é um redator de conteúdo para redes sociais."),
                ("human", LEGENDA_PROMPT),
            ])
            self._chain = prompt | self.llm | StrOutputParser()
        return self._chain

    def gerar_legenda(
        self,
        tema: str,
        estilo_visual: str = "moderno e clean",
        tom_legenda: str = "amigável",
        hashtags_sugeridas: bool = True,
        max_caracteres: int = 2200,
    ) -> str:
        """
        Gera uma legenda para o post com base nos parâmetros.

        Returns:
            Texto da legenda.
        """
        chain = self._get_chain()
        hashtags = "sim" if hashtags_sugeridas else "não"
        result = chain.invoke({
            "tema": tema,
            "estilo_visual": estilo_visual,
            "tom_legenda": tom_legenda,
            "hashtags": hashtags,
            "max_caracteres": max_caracteres,
        })
        return (result or "").strip()
