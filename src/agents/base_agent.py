from groq import Groq
from dotenv import load_dotenv
import re
import os
import unicodedata

load_dotenv()

class BaseAgent:
    def __init__(self, tipo_usuario: str, perfil_usuario: str):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.tipo_usuario = tipo_usuario
        self.perfil_usuario = perfil_usuario
        self.system_prompt = self._carregar_prompt()

    def _carregar_prompt(self) -> str:
        arquivo_atual = os.path.abspath(__file__)
        pasta_agents = os.path.dirname(arquivo_atual)
        pasta_src = os.path.dirname(pasta_agents)
        caminho = os.path.join(pasta_src, "prompts", f"{self.tipo_usuario}.txt")
        with open(caminho, "r", encoding="utf-8") as f:
            prompt = f.read()
        prompt = prompt.replace("{perfil}", self.perfil_usuario)
        prompt = prompt.replace("{dados_bcb}", "Dados do Banco Central indisponíveis no momento.")
        prompt = prompt.replace("{dados_acoes}", "Dados de ações indisponíveis no momento.")
        prompt = prompt.replace("{dados_cripto}", "Dados de criptomoedas indisponíveis no momento.")
        prompt += "\n\nFORMATAÇÃO OBRIGATÓRIA:\n"
        prompt += "- SEMPRE deixe espaço entre números e palavras\n"
        prompt += "- SEMPRE deixe espaço entre valores monetários e conjunções como 'e', 'ou', 'de', 'por'\n"
        prompt += "- Valores monetários SEMPRE no formato: R$ 1.500,00\n"
        prompt += "- NUNCA use markdown, asteriscos, underlines ou símbolos especiais\n"
        prompt += "- Escreva texto corrido, limpo e sem formatação especial\n"
        
        # Injeção global para objetividade (UX)
        prompt += "\n\nDIRETRIZ DE UX E OBJETIVIDADE EXTREMA:\n"
        prompt += "- Seja altamente objetivo e focado em resolver a dor do usuário imediatamente.\n"
        prompt += "- Evite saudações longas, analogias desnecessárias ou discursos prolixos.\n"
        prompt += "- Vá direto ao ponto. Foque na experiência do usuário sem perder a eficiência.\n"
        prompt += "- Se for a PRIMEIRA mensagem do chat, diga EXATAMENTE e APENAS: 'Olá! Sou o Rex. Como posso ajudar com suas finanças hoje?' (Ignore instruções anteriores de saudação longa).\n"
        
        return prompt

    def limpar_formatacao(self, texto: str) -> str:
        texto = unicodedata.normalize('NFC', texto)
        texto = re.sub(r'(\d+[.,]\d+)([a-zA-ZÀ-ú])', r'\1 \2', texto)
        texto = re.sub(r'([a-zA-ZÀ-ú])(R\$?\s*\d)', r'\1 \2', texto)
        texto = re.sub(r'\bR\$?\s*(\d)', r'R$ \1', texto)
        texto = re.sub(r'[~ˊˋ`ˈ\\]', '', texto)
        texto = re.sub(r'\*+', '', texto)
        texto = re.sub(r'_([^_]+)_', r'\1', texto)
        texto = re.sub(r' +', ' ', texto)
        return texto.strip()
    
    def separar_raciocinio(self, resposta: str):
        if "<think>" in resposta:
            pensamento = resposta.split("<think>")[1].split("</think>")[0].strip()
            resposta_final = resposta.split("</think>")[1].strip()
            return pensamento, resposta_final
        return None, resposta

    def responder(self, historico: list) -> tuple:
        mensagens = [{"role": "system", "content": self.system_prompt}]
        mensagens += historico

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