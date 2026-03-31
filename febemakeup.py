import streamlit as st
from google import genai
from google.genai import types

# --- 1. CONFIGURAÇÃO VISUAL DA PÁGINA (BRANDING DO AGENTE DE BELEZA) ---
# Troque [NOME DA SUA AMIGA] pelo nome dela real (ex: Juliana, Camila)
NOME_AMIGA = "[NOME DA SUA AMIGA]"
st.set_page_config(page_title=f"CMO de Beleza: {NOME_AMIGA}", page_icon="🪞", layout="centered")

st.title(f"🪞 CMO de Beleza: {NOME_AMIGA}")
st.caption(f"Olá {NOME_AMIGA}! Sou seu Diretor de Marketing Digital, pronto para viralizar seu talento.")

# --- 2. INICIALIZAÇÃO BLINDADA DO AGENTE (MODO ECONÔMICO) ---
# Usamos cache para a conexão nunca "fechar" durante os recarregamentos
@st.cache_resource
def iniciar_chat_beleza():
    # Coloque sua chave da API Gemini aqui!
    cliente = genai.Client(api_key="COLOQUE_SUA_API_KEY_AQUI")
    
    # PROMPT DE ELITE DO CMO DE BELEZA (O "cérebro" do agente)
    instrucoes_marketing = """
    Persona: Você é o Diretor de Marketing Digital e Storymaker de Elite, especializado exclusivamente no nicho de Maquiagem e Beleza. Você conversa diretamente com uma Maquiadora Profissional.
    
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
    
    config_agente = types.GenerateContentConfig(
        system_instruction=instrucoes_marketing,
        temperature=0.7 
    )
    
    # Criamos o chat usando o modelo certo para a biblioteca
    return cliente.chats.create(
        model="gemini-3-flash-preview", 
        config=config_agente
    )

# Resgata o chat blindado e travado na memória
agente_chat = iniciar_chat_beleza()

# --- 3. GERENCIAMENTO DO HISTÓRICO DE MENSAGENS NA TELA ---
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

# Exibe as mensagens antigas para não perder o contexto
for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 4. CAIXA DE ENTRADA DO CHAT ---
if prompt := st.chat_input(f"Oi {NOME_AMIGA}, o que vamos criar hoje?"):
    
    # Exibe a mensagem da sua amiga
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.mensagens.append({"role": "user", "content": prompt})
    
    # Alpha (o CMO de Beleza) digita a resposta
    with st.chat_message("assistant"):
        with st.spinner("Estudando tendências e criando..."):
            resposta = agente_chat.send_message(prompt)
            st.markdown(resposta.text)
            
    # Salva a resposta no histórico
    st.session_state.mensagens.append({"role": "assistant", "content": resposta.text})