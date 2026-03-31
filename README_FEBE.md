# Agente Febe - Instruções de Execução

Este projeto foi totalmente remodelado para oferecer uma experiência "Premium" e profissional, funcionando perfeitamente em PCs e Celulares.

## Estrutura
- `/backend`: Servidor API em FastAPI (Python).
- `/frontend`: Aplicação Web em React + Vite.

## Como Executar Localmente

### 1. Backend
Navegue até a pasta `backend` e execute:
```bash
pip install -r requirements.txt
python main.py
```
O servidor rodará em `http://localhost:8000`.

### 2. Frontend
Navegue até a pasta `frontend` e execute:
```bash
npm install
npm run dev
```
A aplicação abrirá em `http://localhost:3000`.

## Como disponibilizar via Link (Deploy)

Para que funcione em qualquer lugar apenas com o link, recomendo:
1. **Frontend**: Suba a pasta `frontend` no **Vercel** ou **Netlify** (Gratuito).
2. **Backend**: Suba a pasta `backend` no **Render**, **Railway** ou **Koyeb** (Gratuito/Baixo custo).
3. **Variáveis de Ambiente**: No painel do seu host de backend, adicione a chave `GEMINI_API_KEY`.

---
Desenvolvido com foco em estética e performance.
