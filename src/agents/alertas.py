import os
import sys
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.base_agent import BaseAgent

class AlertasAgent(BaseAgent):
    """
    Agente de Alertas e Riscos Financeiros:
    Especialista em saúde financeira preventiva, identificação de riscos de endividamento,
    uso de cheque especial/cartão rotativo e cálculo da necessidade de reserva de emergência.
    """

    def __init__(self, tipo_usuario: str, perfil_usuario: str):
        super().__init__(tipo_usuario, perfil_usuario)
        self.nome_agente = "Gestor de Riscos e Alertas"
        self.icone = "⚠️"

    def diagnosticar_riscos(self) -> str:
        try:
            dados = json.loads(self.perfil_usuario)
        except Exception:
            return ""

        alertas = []

        # 1. Checagem de dívidas nocivas
        dividas = dados.get("dividas", {})
        if dividas.get("cheque_especial", 0) > 0:
            alertas.append(
                f"🚨 ALERTA CRÍTICO: Cheque especial ativo no valor de R$ {dividas['cheque_especial']:.2f}. "
                "Esta é uma das linhas de crédito com taxas mais altas do país (acima de 300% a.a.)."
            )
        if dividas.get("cartao_credito", 0) > 0:
            alertas.append(
                f"⚠️ ATENÇÃO: Saldo devedor em cartão de crédito de R$ {dividas['cartao_credito']:.2f}. "
                "Evite o pagamento mínimo para não cair no crédito rotativo."
            )

        # 2. Reserva de emergência
        reserva_atual = dados.get("reserva_emergencia", 0)
        meta_reserva = dados.get("meta_reserva_emergencia", 0)
        if meta_reserva > 0 and reserva_atual < (meta_reserva * 0.3):
            alertas.append(
                f"🛡️ RESERVA INSUFICIENTE: Reserva atual de R$ {reserva_atual:.2f} cobre menos de 30% da meta recomendada (R$ {meta_reserva:.2f})."
            )

        if not alertas:
            return "Nenhum risco financeiro crítico detectado no perfil atual."

        return "\n".join(alertas)

    def responder(self, historico: list) -> tuple:
        diagnostico = self.diagnosticar_riscos()

        instrucoes_alertas = (
            f"\n\nDIAGNÓSTICO AUTOMÁTICO DE RISCO FINANCEIRO:\n"
            f"{diagnostico}\n\n"
            "INSTRUÇÃO DO GESTOR DE RISCO:\n"
            "- Seja direto, empático e focado em estancar vazamentos de dinheiro.\n"
            "- Oriente prioridade total para quitação de juros caros antes de qualquer investimento arrojado.\n"
            "- Sugira estratégias de renegociação ou amortização prioritária.\n"
        )

        prompt_atualizado = self.system_prompt + instrucoes_alertas
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

