# Progresso do Projeto — Rex

## Sobre o Projeto
Agente financeiro inteligente com multi-agentes, RAG e dados reais.
Atende Pessoa Física (PF) e Pessoa Jurídica (PJ).
Desenvolvido como projeto de portfólio / competição DIO.

## Stack
- Python 3.11
- Streamlit (interface)
- Groq API (LLM — LLaMA 3, gratuito)
- ChromaDB (banco vetorial — Sprint 2)
- sentence-transformers (embeddings — Sprint 2)
- pandas (análise de dados)
- requests (APIs externas)

## APIs Externas Planejadas
- Banco Central (BCB SGS): Selic, IPCA, câmbio — gratuita
- BrasilAPI: consulta CNPJ — gratuita
- Brapi: cotações B3 — gratuita
- CoinGecko: criptomoedas — gratuita
- CVM: fundos de investimento — gratuita

## Agente
- Nome: Rex (de "regere" = guiar em latim)
- Perfis PF: iniciante, intermediário, avançado
- Perfis PJ: MEI, pequena empresa, média empresa, atacado
- Anti-alucinação: 6 regras em todos os prompts
- Placeholders prontos: {perfil}, {dados_bcb}, {dados_acoes}, {dados_cripto}

---

## Sprints

### Sprint 1 — Fundação (18/03 — 22/03) 🔄 em andamento
**Meta:** app.py rodando com Groq API e perfis PF/PJ

#### Sessão 18/03 (Qua) ✅
- [x] Projeto clonado no VS Code
- [x] .env e .gitignore criados
- [x] Dependências instaladas
- [x] Estrutura de pastas criada (agents, prompts, api, rag)
- [x] 7 prompts criados e revisados
- [x] Agente renomeado para Rex
- [x] Produtos de crédito PJ incluídos por perfil
- [x] Primeiro PR mergeado na main

#### Sessão 20/03 (Sex) ⏳
- [ ] Criar src/agents/base_agent.py
- [ ] Criar src/app.py com Groq + seletor PF/PJ
- [ ] Criar data/perfil_pf.json
- [ ] Criar data/perfil_pj.json
- [ ] Testar Rex respondendo de verdade

#### Sessão 21/03 (Sáb) ⏳
- [ ] Criar data/transacoes_pf.csv
- [ ] Criar data/transacoes_pj.csv
- [ ] Refinar prompts com base nos testes
- [ ] Testes ponta a ponta PF e PJ
- [ ] Commit + PR Sprint 1 completa
- [ ] Tag v0.1.0

#### Sessão 22/03 (Dom) ⏳
- [ ] Buffer / revisão geral Sprint 1
- [ ] Adiantar Sprint 2 se estiver bem

---

### Sprint 2 — RAG + APIs Reais (24/03 — 30/03) ⏳
**Meta:** respostas ancoradas em dados reais

- [ ] ChromaDB + embeddings (sentence-transformers)
- [ ] Criar rag/knowledge_base.py
- [ ] Indexar documentos financeiros
- [ ] Função buscar_contexto(query)
- [ ] Criar api/banco_central.py (Selic, IPCA, câmbio)
- [ ] Criar api/brasil_api.py (CNPJ)
- [ ] Criar api/brapi.py (cotações B3)
- [ ] Criar api/coingecko.py (criptomoedas)
- [ ] Cache local 6h para APIs
- [ ] Painel de dados reais na UI
- [ ] Tag v0.2.0

---

### Sprint 3 — Multi-agentes (31/03 — 02/04) ⏳
**Meta:** orquestrador + 3 agentes funcionando

- [ ] Criar agents/orquestrador.py
- [ ] Criar agents/educador.py
- [ ] Criar agents/analista.py (pandas + CSV)
- [ ] Criar agents/alertas.py (regras de risco)
- [ ] Lógica de roteamento por intenção
- [ ] Log de qual agente respondeu na UI
- [ ] Integrar orquestrador no app.py
- [ ] Testes com 10 perguntas variadas
- [ ] Tag v0.3.0

---

### Sprint 4 — Portfólio (04/04 — 05/04) ⏳
**Meta:** projeto impressiona no GitHub

- [ ] README profissional com arquitetura
- [ ] Demo GIF (Streamlit com PF e PJ)
- [ ] requirements.txt + .env.example
- [ ] Seção anti-alucinação documentada
- [ ] Fechar todas as issues no GitHub Projects
- [ ] Tag v1.0.0

---

## Estrutura de Pastas
```
dio-lab-bia-do-futuro/
├── .env                        # chaves de API (não vai pro GitHub)
├── .gitignore
├── README.md
├── data/
│   ├── perfil_pf.json          # Sprint 1
│   ├── perfil_pj.json          # Sprint 1
│   ├── transacoes_pf.csv       # Sprint 1
│   └── transacoes_pj.csv       # Sprint 1
├── docs/
│   └── progresso.md            # este arquivo
└── src/
    ├── app.py                  # Sprint 1
    ├── agents/
    │   ├── base_agent.py       # Sprint 1
    │   ├── educador.py         # Sprint 3
    │   ├── analista.py         # Sprint 3
    │   ├── alertas.py          # Sprint 3
    │   └── orquestrador.py     # Sprint 3
    ├── api/
    │   ├── banco_central.py    # Sprint 2
    │   ├── brasil_api.py       # Sprint 2
    │   ├── brapi.py            # Sprint 2
    │   └── coingecko.py        # Sprint 2
    ├── prompts/
    │   ├── pf_iniciante.txt    ✅
    │   ├── pf_intermediario.txt✅
    │   ├── pf_avancado.txt     ✅
    │   ├── pj_mei.txt          ✅
    │   ├── pj_pequena.txt      ✅
    │   ├── pj_media.txt        ✅
    │   └── pj_atacado.txt      ✅
    └── rag/
        └── knowledge_base.py   # Sprint 2
```

## Convenção de Commits
- feat: nova funcionalidade
- fix: correção de bug
- docs: documentação
- refactor: refatoração sem nova funcionalidade
- test: testes

## Convenção de Branches
- feat/nome-da-funcionalidade
- fix/nome-do-bug