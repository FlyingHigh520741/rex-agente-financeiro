import os
import sys
import json
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.base_agent import BaseAgent

class AnalistaAgent(BaseAgent):
    """
    Agente Analista Financeiro:
    Especialista em análise quantitativa de fluxo de caixa, transações e orçamentos com Pandas.
    Processa dados tabulares e gera insights claros sobre despesas e receitas.
    """

    def __init__(self, tipo_usuario: str, perfil_usuario: str):
        super().__init__(tipo_usuario, perfil_usuario)
        self.nome_agente = "Analista de Dados"
        self.icone = "📊"
        self.df_transacoes = self._carregar_transacoes()

    def _carregar_transacoes(self) -> pd.DataFrame:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        csv_path = os.path.join(base_dir, "data", "transacoes.csv")
        if os.path.exists(csv_path):
            return pd.read_csv(csv_path)
        return pd.DataFrame()

    def gerar_relatorio_gastos(self) -> str:
        if self.df_transacoes.empty:
            return "Nenhuma planilha de transações recente carregada."

        df = self.df_transacoes
        entradas = df[df["tipo"] == "entrada"]["valor"].sum()
        saidas = df[df["tipo"] == "saida"]["valor"].sum()
        saldo = entradas - saidas

        por_categoria = (
            df[df["tipo"] == "saida"]
            .groupby("categoria")["valor"]
            .sum()
            .sort_values(ascending=False)
        )

        linhas_cat = []
        for cat, val in por_categoria.items():
            pct = (val / saidas * 100) if saidas > 0 else 0
            linhas_cat.append(f"- {cat.capitalize()}: R$ {val:.2f} ({pct:.1f}% do total)")

        relatorio = (
            f"Total de Entradas: R$ {entradas:.2f}\n"
            f"Total de Saídas: R$ {saidas:.2f}\n"
            f"Saldo Livre: R$ {saldo:.2f}\n"
            f"Distribuição por Categoria:\n" + "\n".join(linhas_cat)
        )
        return relatorio

    def responder(self, historico: list) -> tuple:
        relatorio_analise = self.gerar_relatorio_gastos()

        instrucoes_analista = (
            f"\n\nDADOS CALCULADOS PELO MOTOR PANDAS DO ANALISTA:\n"
            f"{relatorio_analise}\n\n"
            "INSTRUÇÃO DE ANALISTA:\n"
            "- Apresente os números de forma clara e objetiva.\n"
            "- Aponte as categorias de maior impacto no orçamento.\n"
            "- Faça perguntas consultivas sobre como otimizar os maiores grupos de despesa.\n"
        )

        prompt_atualizado = self.system_prompt + instrucoes_analista
        mensagens = [{"role": "system", "content": prompt_atualizado}] + historico

        resposta = self.client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=mensagens,
            temperature=0.3,
            max_tokens=1024,
        )

        texto_completo = resposta.choices[0].message.content
        texto_completo = self.limpar_formatacao(texto_completo)
        pensamento, resposta_final = self.separar_raciocinio(texto_completo)
        return pensamento, resposta_final
