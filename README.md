# 📄 DODF Text Miner API
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Version](https://img.shields.io/badge/V1.0-100000?style=for-the-badge&logo=github&logoColor=white)

API RESTful desenvolvida em **FastAPI** para processar PDFs do **Diário Oficial do DF**, extraindo seções específicas e retornando os dados em JSON estruturado.  

O projeto inclui suporte a upload de PDFs e download direto via URL, além de cache interno para agilizar respostas repetidas.

---

## 🚀 Tecnologias

| Categoria | Tecnologia |
|------------|-------------|
| **Linguagem / Framework** | Python 3.11 + FastAPI |
| **Serviços PDF** | PyPDF2 / PDF Reader personalizado |
| **Cache** | Cache em memória (dicionário interno) |
| **Validação de PDF** | Multipart/FormData (UploadFile FastAPI) |
| **Containerização** | Docker & Docker Compose |
| **Documentação** | Swagger (OpenAPI 3.0 via FastAPI) |

---

## 📦 Pré-requisitos

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- Conexão com internet para downloads via URL

## 🐳 Rodando com Docker

Para iniciar a API:

``` bsh
  docker compose up --build
```

A API será iniciada em:

📍 http://localhost:8000
