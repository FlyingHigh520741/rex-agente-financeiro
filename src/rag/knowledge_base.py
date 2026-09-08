import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class KnowledgeBase:
    """
    Base de conhecimento vetorial para RAG (Retrieval-Augmented Generation).
    Utiliza vetorização TF-IDF e Similaridade de Cosseno para busca semântica em tempo real,
    garantindo velocidade, ausência de dependências pesadas externas e portabilidade.
    """

    def __init__(self):
        self.documentos = []
        self.titulos = []
        self._carregar_base()
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words=None)
        if self.documentos:
            self.tfidf_matrix = self.vectorizer.fit_transform(self.documentos)
        else:
            self.tfidf_matrix = None

    def _carregar_base(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        produtos_path = os.path.join(base_dir, "data", "produtos_financeiros.json")

        # 1. Carrega produtos financeiros
        if os.path.exists(produtos_path):
            with open(produtos_path, "r", encoding="utf-8") as f:
                produtos = json.load(f)
                for p in produtos:
                    doc = (
                        f"Produto: {p.get('nome')}. Categoria: {p.get('categoria')}. "
                        f"Risco: {p.get('risco')}. Rentabilidade: {p.get('rentabilidade')}. "
                        f"Aporte Mínimo: R$ {p.get('aporte_minimo', 0):.2f}. "
                        f"Indicado para: {p.get('indicado_para')}."
                    )
                    self.titulos.append(p.get("nome", "Produto Financeiro"))
                    self.documentos.append(doc)

        # 2. Conhecimentos Didáticos e Regulatórios Essenciais
        conteudos_educativos = [
            (
                "Diferença entre Selic e CDI",
                "A Selic é a taxa básica de juros da economia brasileira, fixada pelo Copom do Banco Central. "
                "O CDI (Certificado de Depósito Interbancário) é a taxa que os bancos cobram para emprestar dinheiro entre si no curto prazo. "
                "Na prática, o CDI anda praticamente colado na Selic, geralmente 0,10 ponto percentual abaixo da meta Selic. "
                "Quando um investimento rende 100% do CDI, ele acompanha de perto a taxa básica de juros."
            ),
            (
                "Reserva de Emergência",
                "A reserva de emergência deve cobrir de 3 a 6 meses de despesas fixas para assalariados (CLT) "
                "e de 6 a 12 meses para autônomos, MEI ou profissionais liberais. "
                "Deve ser aplicada exclusivamente em ativos de baixíssimo risco e alta liquidez imediata, "
                "tais como Tesouro Selic ou CDB com liquidez diária de grandes bancos a 100% do CDI."
            ),
            (
                "Regra 50-30-20 de Orçamento Pessoal",
                "Método clássico de organização financeira que divide a renda líquida em três partes: "
                "50% para necessidades essenciais (moradia, saúde, alimentação e transporte); "
                "30% para desejos pessoais e estilo de vida (lazer, restaurantes, assinaturas); "
                "20% para prioridades financeiras (quitação de dívidas e investimentos/reserva)."
            ),
            (
                "Dívidas e Cheque Especial vs Cartão de Crédito",
                "Os juros do cheque especial e do rotativo do cartão de crédito costumam ser os mais altos do mercado (superando 300% ao ano). "
                "A estratégia prioritária deve ser liquidar essas dívidas de juros abusivos antes de alocar recursos em investimentos, "
                "ou buscar portabilidade de crédito para taxas menores via empréstimo consignado ou pessoal."
            ),
            (
                "Capital de Giro e Gestão de Caixa PJ",
                "Para Pessoa Jurídica (PJ/MEI/PME), o capital de giro é o montante necessário para cobrir a operação "
                "entre o pagamento de fornecedores e o recebimento das vendas dos clientes. "
                "Nunca misture a conta de pessoa física (PF) com a da empresa (PJ), faça retiradas estruturadas de pró-labore."
            ),
            (
                "Isenção de Imposto de Renda em LCI e LCA",
                "As Letras de Crédito Imobiliário (LCI) e do Agronegócio (LCA) são títulos de renda fixa isentos de Imposto de Renda para pessoa física. "
                "Por serem isentas, uma LCI de 90% a 95% do CDI frequentemente rende mais líquido do que um CDB de 100% ou 105% do CDI sujeito à tabela regressiva de IR."
            ),
            (
                "Fundos Imobiliários (FIIs) e Dividendos",
                "FIIs reúnem investidores para aplicar em imóveis comerciais (shoppings, galpões logísticos, lajes corporativas) ou títulos do setor. "
                "Os rendimentos distribuídos mensalmente (dividendos) são isentos de Imposto de Renda para pessoas físicas na legislação atual, "
                "sendo indicados para perfis moderados e arrojados em busca de renda passiva recorrente."
            )
        ]

        for titulo, conteudo in conteudos_educativos:
            self.titulos.append(titulo)
            self.documentos.append(f"Tópico: {titulo}. Conteúdo: {conteudo}")

    def buscar_contexto(self, query: str, top_k: int = 2) -> str:
        """
        Realiza busca semântica por similaridade para extrair os trechos mais relevantes à dúvida do usuário.
        """
        if not self.documentos or self.tfidf_matrix is None:
            return ""

        query_vec = self.vectorizer.transform([query])
        similaridades = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        top_indices = similaridades.argsort()[::-1][:top_k]

        contextos = []
        for idx in top_indices:
            if similaridades[idx] > 0.05:  # Filtro mínimo de relevância
                contextos.append(f"[{self.titulos[idx]}]\n{self.documentos[idx]}")

        if not contextos:
            return "Nenhum documento específico encontrado na base para esta consulta."

        return "\n\n".join(contextos)

if __name__ == "__main__":
    kb = KnowledgeBase()
    print("Testando busca RAG para 'o que é cdi e selic':")
    print(kb.buscar_contexto("o que é cdi e selic"))

