import json
import streamlit as st
import sys
import os
import pandas as pd

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from agents.orquestrador import OrquestradorAgent
from api.banco_central import BancoCentralAPI
from api.market_api import MarketAPI

# ============ CONFIGURAÇÃO DA PÁGINA ============
st.set_page_config(
    page_title="Rex — Conselheiro Financeiro Inteligente",
    page_icon="💼",
    layout="wide"
)

# ============ FUNÇÕES AUXILIARES ============
def carregar_mock(tipo_usuario: str) -> str:
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    caminho = os.path.join(base, "data", "mock", f"{tipo_usuario}.json")
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)
        return json.dumps(dados, ensure_ascii=False, indent=2)
    return "{}"

def carregar_transacoes() -> pd.DataFrame:
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base, "data", "transacoes.csv")
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    return pd.DataFrame()

def inicializar_sessao():
    if "mensagens" not in st.session_state:
        st.session_state.mensagens = []
    if "orquestrador" not in st.session_state:
        st.session_state.orquestrador = None
    if "perfil_escolhido" not in st.session_state:
        st.session_state.perfil_escolhido = None
    if "onboarding_completo" not in st.session_state:
        st.session_state.onboarding_completo = False

# ============ SIDEBAR COM MÉTRICAS AO VIVO ============
def renderizar_sidebar():
    with st.sidebar:
        st.title("💼 Rex AI")
        st.caption("Conselheiro Financeiro Multi-Agente & RAG")
        st.markdown("---")

        st.subheader("📌 Perfil Ativo")
        if st.session_state.perfil_escolhido:
            st.info(f"**Modo:** `{st.session_state.perfil_escolhido}`")
            if st.button("🔄 Trocar Perfil", use_container_width=True):
                st.session_state.mensagens = []
                st.session_state.orquestrador = None
                st.session_state.perfil_escolhido = None
                st.session_state.onboarding_completo = False
                st.rerun()

        st.markdown("---")
        st.subheader("🌐 Indicadores Econômicos (Tempo Real)")
        try:
            indicadores_bcb = BancoCentralAPI.obter_resumo_indicadores()
            mercado = MarketAPI.obter_resumo_mercado()

            col_a, col_b = st.columns(2)
            with col_a:
                st.metric(label="Taxa Selic", value=indicadores_bcb["selic"])
                st.metric(label="Dólar PTAX", value=indicadores_bcb["dolar"])
            with col_b:
                st.metric(label="IPCA Mensal", value=indicadores_bcb["ipca"])
                st.metric(label="Bitcoin", value=mercado["bitcoin"])

            st.caption("Fontes: Banco Central do Brasil (SGS) & CoinGecko")
        except Exception as e:
            st.warning("Indicadores em modo de contingência.")

        st.markdown("---")
        st.markdown(
            "**Agentes Especialistas:**\n"
            "- 📚 *Educador:* Conceitos, RAG & Produtos\n"
            "- 📊 *Analista:* Planilha & Gastos com Pandas\n"
            "- ⚠️ *Alertas:* Riscos & Saúde Financeira"
        )

# ============ TELA DE ONBOARDING ============
def tela_onboarding():
    renderizar_sidebar()

    st.title("💼 Bem-vindo ao Rex!")
    st.markdown(
        "Seu **Conselheiro Financeiro Inteligente** com arquitetura multi-agente, "
        "ancoragem de dados em tempo real (RAG) e análise preditiva de despesas."
    )
    st.markdown("Para começarmos de forma personalizada, selecione o seu perfil:")

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

    if st.button("🚀 Iniciar Consultoria com o Rex", type="primary", use_container_width=True):
        tipo_usuario = mapa[nivel]
        perfil = carregar_mock(tipo_usuario)
        st.session_state.orquestrador = OrquestradorAgent(tipo_usuario, perfil)
        st.session_state.perfil_escolhido = tipo_usuario
        st.session_state.onboarding_completo = True
        st.rerun()

# ============ TELA DO CHAT ============
def tela_chat():
    renderizar_sidebar()

    st.title("💼 Rex — Conversa com Especialistas")

    # Mensagem inicial do Rex
    if len(st.session_state.mensagens) == 0:
        with st.chat_message("assistant"):
            with st.spinner("Rex está preparando a sessão..."):
                nome_agente, icone, pensamento, resposta = st.session_state.orquestrador.responder([])
                st.markdown(f"**{icone} {nome_agente}**")
                st.write(resposta)
        st.session_state.mensagens.append({
            "role": "assistant",
            "agente": nome_agente,
            "icone": icone,
            "content": resposta,
            "pensamento": pensamento
        })
        st.rerun()

    # Exibir histórico de mensagens
    for msg in st.session_state.mensagens:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.write(msg["content"])
        else:
            with st.chat_message("assistant"):
                icone = msg.get("icone", "💼")
                nome = msg.get("agente", "Rex")
                st.caption(f"{icone} Resposta via: **{nome}**")
                st.write(msg["content"])
                if msg.get("pensamento"):
                    with st.expander("💭 Ver raciocínio interno do modelo"):
                        st.text(msg["pensamento"])

    # Gráfico interativo se o Analista foi acionado recentemente
    df_transacoes = carregar_transacoes()
    if not df_transacoes.empty:
        ultimas_mensagens = [m["content"].lower() for m in st.session_state.mensagens if m["role"] == "user"]
        if ultimas_mensagens and any(w in ultimas_mensagens[-1] for w in ["gasto", "gastei", "despesa", "extrato", "categoria", "saldo"]):
            with st.expander("📊 Gráfico de Despesas por Categoria (Motor Pandas)", expanded=True):
                saidas = df_transacoes[df_transacoes["tipo"] == "saida"]
                cat_sum = saidas.groupby("categoria")["valor"].sum()
                st.bar_chart(cat_sum)

    # Input do usuário
    if pergunta := st.chat_input("Pergunte sobre seus gastos, taxas de juros, Selic, dívidas ou investimentos..."):
        st.session_state.mensagens.append({
            "role": "user",
            "content": pergunta
        })

        with st.chat_message("user"):
            st.write(pergunta)

        with st.chat_message("assistant"):
            with st.spinner("Orquestrador analisando intenção e consultando especialista..."):
                historico = [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.mensagens
                ]
                nome_agente, icone, pensamento, resposta = st.session_state.orquestrador.responder(historico)
                st.caption(f"{icone} Resposta via: **{nome_agente}**")
                st.write(resposta)
                if pensamento:
                    with st.expander("💭 Ver raciocínio interno do modelo"):
                        st.text(pensamento)

        st.session_state.mensagens.append({
            "role": "assistant",
            "agente": nome_agente,
            "icone": icone,
            "content": resposta,
            "pensamento": pensamento
        })
        st.rerun()

# ============ MAIN ============
inicializar_sessao()

if not st.session_state.onboarding_completo:
    tela_onboarding()
else:
    tela_chat()