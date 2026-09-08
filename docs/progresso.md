# Progresso do Projeto — Rex (Conselheiro Financeiro Inteligente)

## 📌 Sobre o Projeto
Agente financeiro inteligente com arquitetura **Multi-Agentes**, **RAG (Retrieval-Augmented Generation)** e **ancoragem em dados econômicos reais**.
Atende perfis diversificados de **Pessoa Física (PF)** e **Pessoa Jurídica (PJ)** com proteção anti-alucinação e análise quantitativa de despesas via Pandas.
Desenvolvido como projeto de destaque para **Portfólio de IA Generativa & Engenharia de Dados**.

---

## 🛠️ Stack Tecnológica
- **Python 3.11+**
- **Streamlit** (Interface Web Interativa com Dashboard Econômico)
- **Groq API** (LLM de altíssima velocidade — `openai/gpt-oss-120b`)
- **Scikit-Learn / TF-IDF Vectorizer** (Mecanismo RAG semântico rápido e autocontido)
- **Pandas** (Análise de séries temporais, extratos e transações)
- **APIs de Mercado e Governo:**
  - **Banco Central do Brasil (SGS):** Selic, IPCA e Dólar PTAX
  - **CoinGecko:** Cotação Bitcoin em BRL
  - **Brapi:** Cotação IBOVESPA

---

## 🤖 Arquitetura Multi-Agentes
1. **Orquestrador (`OrquestradorAgent`):**
   - Classificação de intenção em linguagem natural e despacho dinâmico.
2. **Educador Financeiro (`EducadorAgent`):**
   - Didática personalizada, RAG sobre produtos financeiros e cotações reais injetadas.
3. **Analista de Dados (`AnalistaAgent`):**
   - Análise quantitativa de transações com agregação por categoria e cálculo de fluxo de caixa via Pandas.
4. **Gestor de Risco e Alertas (`AlertasAgent`):**
   - Varredura de cheque especial, juros rotativos de cartão e dimensionamento de reserva de emergência.

---

## 📅 Roadmap de Sprints & Entregas

### ✅ Sprint 1 — Fundação & MVP Conversacional
- [x] Estrutura modular (`agents`, `prompts`, `mock data`).
- [x] Criação de 7 personas especializadas em prompts (PF: Iniciante, Intermediário, Avançado / PJ: MEI, Pequena, Média, Atacado).
- [x] Implementação do `BaseAgent` com Groq API.
- [x] Mocks estruturados em JSON para cada perfil.
- [x] Filtros anti-alucinação e sanitização de caracteres/espaçamento.

### ✅ Sprint 2 — RAG & APIs Financeiras Reais
- [x] Módulo `src/api/banco_central.py` integrado à API SGS oficial do Banco Central (Selic, IPCA, Dólar).
- [x] Módulo `src/api/market_api.py` integrado à CoinGecko e Brapi (Bitcoin e IBOVESPA).
- [x] Sistema de Cache resiliente para tolerância a falhas e economia de requisições.
- [x] Módulo `src/rag/knowledge_base.py` com busca semântica por similaridade de cosseno sobre produtos e diretrizes normativas.

### ✅ Sprint 3 — Arquitetura Multi-Agentes Especializada
- [x] Implementação do `OrquestradorAgent` com roteamento automático por intenção.
- [x] Agente especialista `EducadorAgent` com injeção em tempo real de RAG + BCB.
- [x] Agente especialista `AnalistaAgent` com leitura de extrato CSV e agregação via Pandas.
- [x] Agente especialista `AlertasAgent` com detecção de dívidas abusivas e suficiência de reserva.
- [x] Interface Streamlit enriquecida com identificação visual do agente ativo e gráficos de despesa.

### ✅ Sprint 4 — Finalização de Portfólio & Apresentação
- [x] `README.md` de nível sênior com diagrama visual Mermaid e guia de execução.
- [x] `.env.example` e `requirements.txt` atualizados e testados.
- [x] Código desacoplado e pronto para publicação no GitHub.