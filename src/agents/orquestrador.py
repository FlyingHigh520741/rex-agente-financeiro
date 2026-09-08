import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.educador import EducadorAgent
from agents.analista import AnalistaAgent
from agents.alertas import AlertasAgent

class OrquestradorAgent:
    """
    Orquestrador Inteligente Multi-Agentes:
    Analisa a intenção da mensagem do usuário e delega o processamento
    ao agente especialista mais adequado:
    - EducadorAgent (Conceitos, Produtos, RAG, Taxas ao vivo)
    - AnalistaAgent (Extrato, Gastos, Cálculos de fluxo de caixa com Pandas)
    - AlertasAgent (Saúde financeira, Dívidas, Cheque Especial, Riscos)
    """

    def __init__(self, tipo_usuario: str, perfil_usuario: str):
        self.tipo_usuario = tipo_usuario
        self.perfil_usuario = perfil_usuario

        # Instanciação dos sub-agentes especializados
        self.educador = EducadorAgent(tipo_usuario, perfil_usuario)
        self.analista = AnalistaAgent(tipo_usuario, perfil_usuario)
        self.alertas = AlertasAgent(tipo_usuario, perfil_usuario)

    def classificar_intencao(self, texto_usuario: str) -> str:
        """
        Classifica a intenção usando correspondência semântica e palavras-chave estruturadas.
        """
        texto_lower = texto_usuario.lower().strip()

        # Gatilhos do Analista (Gastos, Extrato, Transações, Números)
        gatilhos_analista = [
            "gastei", "gasto", "despesa", "extrato", "transação", "transacoes",
            "categoria", "alimentacao", "aluguel", "transporte", "quanto sobrou",
            "saldo", "planilha", "contas do mês", "onde estou gastando"
        ]
        if any(w in texto_lower for w in gatilhos_analista):
            return "ANALISTA"

        # Gatilhos de Alertas e Riscos (Dívidas, Rotativo, Emergência, Crítico)
        gatilhos_alertas = [
            "dívida", "divida", "cheque especial", "cartão de crédito", "rotativo",
            "juros abusivos", "endividado", "negativado", "perigo", "risco",
            "reserva de emergência", "aperto", "renegociar"
        ]
        if any(w in texto_lower for w in gatilhos_alertas):
            return "ALERTAS"

        # Padrão: Educador Financeiro (Conceitos, Cotações, RAG)
        return "EDUCADOR"

    def responder(self, historico: list) -> tuple:
        """
        Executa o roteamento dinâmico e retorna:
        (nome_agente, icone, pensamento, resposta_final)
        """
        if not historico:
            # Saudação inicial é responsabilidade do educador
            pensamento, resposta = self.educador.responder([])
            return self.educador.nome_agente, self.educador.icone, pensamento, resposta

        ultima_msg = historico[-1].get("content", "")
        intencao = self.classificar_intencao(ultima_msg)

        if intencao == "ANALISTA":
            agente = self.analista
        elif intencao == "ALERTAS":
            agente = self.alertas
        else:
            agente = self.educador

        pensamento, resposta = agente.responder(historico)
        return agente.nome_agente, agente.icone, pensamento, resposta

