import streamlit as st
from google import genai
from google.genai import types

# 1. Configuração da página Web
st.set_page_config(page_title="Alpha", page_icon="🤖", layout="centered")
st.title("🤖 Alpha")
st.caption("Seu assistente especialista em conteúdo imobiliário.")

# 2. Inicialização do Cliente (Conexão Leve)
# Substitua pela sua CHAVE REAL
cliente = genai.Client(api_key="AIzaSyBCsgLltYMpPUDGqPwZDR9NiRgeSLswbEU")

instrucoes_marketing = """
Persona: Você é um Diretor de Marketing (CMO) especializado no setor imobiliário e administração de condomínios. Sua missão é transformar termos técnicos e burocráticos em conteúdo de alto desejo, autoridade e confiança para o Instagram.

Sempre entregue a seguinte estrutura:
1. Objetivo do Post.
2. Legenda magnética com Chamada para Ação (CTA).
3. Sugestão visual detalhada (Apenas descreva em texto).
4. 5 Hashtags estratégicas.
"""

# 3. Gerenciamento do Histórico na Memória do Navegador
if "mensagens_tela" not in st.session_state:
    st.session_state.mensagens_tela = []
    
if "historico_ia" not in st.session_state:
    # A IA precisa saber quem ela é logo no início da conversa
    st.session_state.historico_ia = [
        types.Content(role="user", parts=[types.Part.from_text(text="Instrução de Sistema: " + instrucoes_marketing)]),
        types.Content(role="model", parts=[types.Part.from_text(text="Entendido. Estou pronto para atuar como o Alpha, seu CMO imobiliário.")])
    ]

# Renderiza as mensagens antigas na tela
for msg in st.session_state.mensagens_tela:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. Caixa de texto e Processamento
if prompt := st.chat_input("Peça um post (ex: 'Post sobre prestação de contas')"):
    
    # Exibe a pergunta do usuário na tela
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Salva a pergunta do usuário no histórico visual
    st.session_state.mensagens_tela.append({"role": "user", "content": prompt})
    
    # Adiciona a pergunta do usuário no formato que a IA entende
    st.session_state.historico_ia.append(
        types.Content(role="user", parts=[types.Part.from_text(text=prompt)])
    )
    
    # Processa e mostra a resposta da IA
    with st.chat_message("assistant"):
        with st.spinner("Alpha está elaborando a estratégia..."):
            try:
                # Manda o histórico COMPLETO para a IA ler e responder
                resposta = cliente.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=st.session_state.historico_ia,
                    config=types.GenerateContentConfig(temperature=0.7)
                )
                
                # Exibe a resposta na tela
                st.markdown(resposta.text)
                
                # Salva a resposta no histórico visual
                st.session_state.mensagens_tela.append({"role": "assistant", "content": resposta.text})
                
                # Adiciona a resposta da IA no formato que a IA entende
                st.session_state.historico_ia.append(
                    types.Content(role="model", parts=[types.Part.from_text(text=resposta.text)])
                )
                
            except Exception as e:
                st.error(f"Erro na comunicação com o cérebro da IA: {e}")