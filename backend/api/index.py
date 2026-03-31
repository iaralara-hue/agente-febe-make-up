from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv
import traceback

load_dotenv()

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API KEY
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY não encontrada no arquivo .env")

genai.configure(api_key=GEMINI_API_KEY)

# Persona Febe
SYSTEM_INSTRUCTIONS = """
Persona: Você é a Febe, Diretora de Marketing Digital e Storymaker de Elite, especializada exclusivamente no nicho de Maquiagem e Beleza. Você conversa diretamente com uma Maquiadora Profissional.

Tom de Voz: Direto, prático, encorajador, sem enrolação e altamente persuasivo. Nunca dê respostas genéricas; entregue sempre a melhor opção mastigada e pronta para uso.

Suas Missões:
1. Conteúdo de Impacto: Criar roteiros virais para TikTok/Reels (com Hook/Gancho nos primeiros 3 segundos, Retenção e CTA) e legendas magnéticas para o Instagram dela.
2. Consultoria Rápida: Ajudar com ideias de maquiagem, tendências, colorimetria e formas de atrair clientes.
3. Edição de Vídeo/Foto: Quando solicitado, indique os melhores aplicativos gratuitos ou pagos (ex: CapCut, Lightroom) e diga exatamente qual efeito ou ferramenta ela deve usar dentro deles para editar sozinha com facilidade.
4. Direção de Arte no Canva: Quando ela precisar de um post estático, forneça as "coordenadas exatas" para o Canva: 
   - Termos em inglês para buscar elementos e fundos (ex: "glitter background", "makeup flatlay").
   - Sugestão de paleta de cores (com códigos HEX se possível).
   - Disposição do texto e sugestão de fontes elegantes.
   
Regra de Ouro: Sempre estruture suas respostas de forma visual e fácil de ler, focando no que traz mais resultado e engajamento. Vá direto ao ponto!
"""

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: list[ChatMessage] = []

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        # Nomes de modelos a tentar (nomes completos como aparecem na lista)
        models_to_try = [
            'gemini-3-flash-preview',
            'gemini-2.0-flash',
            'gemini-2.5-flash'
        ]

        errors = {}
        for model_name in models_to_try:
            try:
                print(f"Tentando modelo: {model_name}...")
                model = genai.GenerativeModel(
                    model_name=model_name,
                    system_instruction=SYSTEM_INSTRUCTIONS
                )
                
                # Se houver histórico, tentamos usar o chat padrão
                if request.history:
                    chat = model.start_chat(history=[
                        {"role": "user" if m.role == "user" else "model", "parts": [m.content]}
                        for m in request.history
                    ])
                    response = chat.send_message(request.message)
                else:
                    response = model.generate_content(request.message)
                
                return {"response": response.text}
            except Exception as e:
                print(f"Falha no modelo {model_name}: {e}")
                errors[model_name] = e
                continue
        
        if errors:
            error_details = " | ".join([f"{model}: {str(err)}" for model, err in errors.items()])
            raise Exception(f"Todos os modelos falharam. Detalhes: {error_details}")
        raise Exception("Nenhum modelo Gemini respondeu corretamente e nenhum erro foi capturado.")

    except Exception as e:
        error_msg = traceback.format_exc()
        print(f"ERRO CRÍTICO:\n{error_msg}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Agente Febe API está online"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
