import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.base_agent import BaseAgent
from api.banco_central import BancoCentralAPI
from api.market_api import MarketAPI
from rag.knowledge_base import KnowledgeBase

class EducadorAgent(BaseAgent):
    """
    Agente Educador Financeiro:
    Especialista em conceitos, investimentos, taxas e produtos financeiros.
    Utiliza RAG (KnowledgeBase) e APIs em tempo real (BCB + Cripto/Mercado) para contextualizar suas respostas.
    """

    def __init__(self, tipo_usuario: str, perfil_usuario: str):
        super().__init__(tipo_usuario, perfil_usuario)
        self.nome_agente = "Educador Financeiro"
        self.icone = "📚"
        self.kb = KnowledgeBase()

    def _obter_dados_mercado_formatados(self) -> str:
        bcb = BancoCentralAPI.obter_resumo_indicadores()
        mercado = MarketAPI.obter_resumo_mercado()
        return (
            f"Taxa Selic Meta: {bcb['selic']} (fonte: Banco Central do Brasil)\n"
            f"IPCA: {bcb['ipca']} (fonte: Banco Central do Brasil)\n"
            f"Dólar Comercial: {bcb['dolar']}\n"
            f"Bitcoin: {mercado['bitcoin']}\n"
            f"Ibovespa: {mercado['ibovespa']}"
        )

    def responder(self, historico: list) -> tuple:
        ultima_duvida = ""
        for msg in reversed(historico):
            if msg.get("role") == "user":
                ultima_duvida = msg.get("content", "")
                break

        # 1. Busca semântica via RAG
        contexto_rag = self.kb.buscar_contexto(ultima_duvida) if ultima_duvida else ""

        # 2. Obtém dados em tempo real
        dados_mercado = self._obter_dados_mercado_formatados()

        # 3. Monta prompt customizado
        prompt_atualizado = self.system_prompt
        prompt_atualizado = prompt_atualizado.replace(
            "Dados do Banco Central indisponíveis no momento.",
            dados_mercado
        )

        if contexto_rag and "Nenhum documento" not in contexto_rag:
            prompt_atualizado += f"\n\nBASE DE CONHECIMENTO (RAG):\n{contexto_rag}\n"

        mensagens = [{"role": "system", "content": prompt_atualizado}] + historico

        resposta = self.client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=mensagens,
            temperature=0.4,
            max_tokens=1024,
        )

        texto_completo = resposta.choices[0].message.content
        texto_completo = self.limpar_formatacao(texto_completo)
        pensamento, resposta_final = self.separar_raciocinio(texto_completo)
        return pensamento, resposta_final

