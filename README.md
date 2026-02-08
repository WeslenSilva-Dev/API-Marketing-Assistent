# API de Geração de Conteúdo para Instagram

API em Python (FastAPI) para criar conteúdo para Instagram com **DALL-E**, **ChatGPT** (via LangChain) e publicar no feed via **Facebook Graph API**.

## Funcionalidades

- **Criar conteúdo**: gera imagem (DALL-E) + legenda (ChatGPT) a partir de parâmetros (tema, estilo visual, tom).
- **Postar no Instagram**: publica imagem e legenda no feed usando a Graph API.

## Estrutura do projeto

```
.
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── content.py    # POST /api/content/create
│   │       └── instagram.py # POST /api/instagram/post
│   ├── core/
│   │   └── config.py        # Configurações (.env)
│   ├── schemas/
│   │   └── content.py       # Request/Response (Pydantic)
│   └── services/
│       ├── image_service.py      # DALL-E
│       ├── caption_service.py    # LangChain + ChatGPT (legenda)
│       ├── content_service.py    # Orquestração (prompt imagem + DALL-E + legenda)
│       └── instagram_service.py # Facebook Graph API
├── main.py
├── requirements.txt
└── .env.example
```

## Como rodar

### 1. Ambiente virtual

```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Dependências

```bash
pip install -r requirements.txt
```

### 3. Variáveis de ambiente

Copie `.env.example` para `.env` e configure:

- **OPENAI_API_KEY**: obrigatório (DALL-E e ChatGPT).
- **IG_USER_ID**, **USER_ACCESS_TOKEN**: obrigatórios para publicar no Instagram (conta Business/Creator).

### 4. Subir a API

```bash
uvicorn main:app --reload
```

Documentação: **http://127.0.0.1:8000/docs**

## Caso tenha dificuldade para conseguir o longer-lived access token (USER_ACCESS_TOKEN)

Assista a esse video **https://youtu.be/OXCAAIUdFnE?si=jRa2XNpGbdBDZ8_Q** me ajudou muito.

## Endpoints

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/content/create` | Gera imagem + legenda (tema, estilo, tom, etc.). |
| POST | `/api/instagram/post` | Publica no feed (imagem_url + legenda). |

## Tecnologias

- **FastAPI** – API web
- **LangChain** – Orquestração (prompt da imagem + geração de legenda com ChatGPT)
- **OpenAI** – DALL-E 3 e GPT (ChatGPT)
- **Facebook Graph API** – Publicação no Instagram
