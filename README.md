# 🧥 Brechó Online - Backend com FastAPI e SQLite

Este projeto é um backend para gerenciamento de um brechó, utilizando FastAPI com banco de dados SQLite.

---

## ✅ Requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)
- Git Bash (opcional no Windows)

---

## 🚀 Como rodar o projeto

### ▶️ 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/brecho-backend.git
cd brecho-backend
```

### ▶️ 2. Como iniciar o backend

#### Windows 

**Git bash**

```bash
python -m venv venv
source venv/Scripts/activate
```
**CMD**

```bash
python -m venv venv
venv\Scripts\activate
```

**Power Shell**

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

**Se você já tem o arquivo requirements.txt (recomendado):**
```bash
pip install -r requirements.txt
```
**Se não tiver, instale os pacotes manualmente e depois gere o arquivo:**
```bash
pip install fastapi uvicorn python-dotenv
pip freeze > requirements.txt
```

#### Iniciar aplicação

**Rode o comando no seu terminal**
```bash
uvicorn main:app --reload
```

**Interface padrão:** http://127.0.0.1:8000


## Autores

- [Lucas Mendes](https://github.com/Luke074)
- [Adson Ferreira](https://github.com/adsonferr)
- [Helena Oliveira](https://github.com/HelenaOliveira366)
- [Marcos](https://github.com/Masterpharao1911)

