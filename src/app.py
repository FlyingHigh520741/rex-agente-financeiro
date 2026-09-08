import json
import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from agents.base_agent import BaseAgent

# ============ CONFIGURAÇÃO DA PÁGINA ============
st.set_page_config(
    page_title="Rex — Conselheiro Financeiro",
    page_icon="💼",
    layout="centered"
)

# ============ FUNÇÕES AUXILIARES ============
def carregar_mock(tipo_usuario: str) -> str:
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    caminho = os.path.join(base, "data", "mock", f"{tipo_usuario}.json")
    with open(caminho, "r", encoding="utf-8") as f:
        dados = json.load(f)
    return json.dumps(dados, ensure_ascii=False, indent=2)

def inicializar_sessao():
    if "mensagens" not in st.session_state:
        st.session_state.mensagens = []
    if "agente" not in st.session_state:
        st.session_state.agente = None
    if "perfil_escolhido" not in st.session_state:
        st.session_state.perfil_escolhido = None
    if "onboarding_completo" not in st.session_state:
        st.session_state.onboarding_completo = False

# ============ TELA DE ONBOARDING ============
def tela_onboarding():
    st.title("💼 Rex — Conselheiro Financeiro")
    st.markdown("Olá! Eu sou o **Rex**, seu conselheiro financeiro pessoal.")
    st.markdown("Antes de começar, me conta um pouco sobre você:")

    col1, col2 = st.columns(2)

    with col1:
        tipo = st.selectbox(
            "Você é:",
            ["Pessoa Física", "Pessoa Jurídica"]
        )

    with col2:
        if tipo == "Pessoa Física":
            st.markdown("**Seu nível financeiro:**")
            nivel = st.radio(
                "Escolha o que mais combina com você:",
                ["Iniciante", "Intermediário", "Avançado"],
                captions=[
                    "Estou começando a organizar minhas finanças agora",
                    "Já invisto em CDB, Tesouro Direto e quero otimizar",
                    "Invisto em ações, FIIs e busco análises aprofundadas"
                ]
            )
            mapa = {
                "Iniciante": "pf_iniciante",
                "Intermediário": "pf_intermediario",
                "Avançado": "pf_avancado"
            }
        else:
            st.markdown("**Tipo de empresa:**")
            nivel = st.radio(
                "Escolha o que melhor descreve seu negócio:",
                ["MEI / Autônomo", "Pequena Empresa", "Média Empresa", "Atacado / Distribuidor"],
                captions=[
                    "Faturamento até R$ 81 mil/ano, sem funcionários ou com poucos",
                    "Simples Nacional, 1 a 10 funcionários, faturamento até R$ 4,8 mi/ano",
                    "Lucro Real ou Presumido, faturamento acima de R$ 4,8 mi/ano",
                    "Distribuidor ou atacadista, alto volume e margem reduzida"
                ]
            )
            mapa = {
                "MEI / Autônomo": "pj_mei",
                "Pequena Empresa": "pj_pequena",
                "Média Empresa": "pj_media",
                "Atacado / Distribuidor": "pj_atacado"
            }

    if st.button("Começar conversa com o Rex"):
        tipo_usuario = mapa[nivel]
        perfil = carregar_mock(tipo_usuario)
        st.session_state.agente = BaseAgent(tipo_usuario, perfil)
        st.session_state.perfil_escolhido = tipo_usuario
        st.session_state.onboarding_completo = True
        st.rerun()

# ============ TELA DO CHAT ============
def tela_chat():
    st.title("💼 Rex — Conselheiro Financeiro")

    # Sidebar com info do perfil
    with st.sidebar:
        st.markdown("### Seu perfil")
        st.markdown(f"`{st.session_state.perfil_escolhido}`")
        if st.button("Trocar perfil"):
            st.session_state.mensagens = []
            st.session_state.agente = None
            st.session_state.perfil_escolhido = None
            st.session_state.onboarding_completo = False
            st.rerun()

    # Mensagem inicial do Rex — só chama API se histórico vazio
    if len(st.session_state.mensagens) == 0:
        with st.chat_message("assistant"):
            with st.spinner("Rex está pensando..."):
                pensamento, resposta = st.session_state.agente.responder([])
                st.write(resposta)
        st.session_state.mensagens.append({
            "role": "assistant",
            "content": resposta,
            "pensamento": pensamento
        })
        st.rerun()

    # Exibir histórico de mensagens
    for msg in st.session_state.mensagens:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Input do usuário
    if pergunta := st.chat_input("Sua dúvida financeira..."):
        st.session_state.mensagens.append({
            "role": "user",
            "content": pergunta
        })

        with st.chat_message("user"):
            st.write(pergunta)

        with st.chat_message("assistant"):
            with st.spinner("Rex está pensando..."):
                historico = [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.mensagens
                ]
                pensamento, resposta = st.session_state.agente.responder(historico)
                st.write(resposta)

        st.session_state.mensagens.append({
            "role": "assistant",
            "content": resposta,
            "pensamento": pensamento
        })

# ============ MAIN ============
inicializar_sessao()

if not st.session_state.onboarding_completo:
    tela_onboarding()
else:
    tela_chat()