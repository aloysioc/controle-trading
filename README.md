# 📊 Controle de Lotes — Trading

Aplicação web em [Streamlit](https://streamlit.io/) para controle de lotes disponíveis em ativos e ações de trading.

## Funcionalidades

- Tabela resumo estilo planilha com bordas, cabeçalho e linhas alternadas
- Cores por categoria: vermelho (índices), roxo (petróleo), verde (ações)
- Indicadores visuais de progresso por ativo (🔴 pendente / 🟡 em andamento / 🟢 concluído)
- Registro de uso de lotes por data, com observação opcional
- Suporte a lotes fracionados (até 2 casas decimais)
- Validação: não permite registrar mais lotes do que os disponíveis
- Histórico completo com filtro por ativo, edição e exclusão de registros
- Persistência local em arquivo JSON (`trading_lotes.json`)
- Compatível com tema claro e escuro do Streamlit

## Ativos monitorados

| Tipo  | Nome                             | Lotes Iniciais |
|-------|----------------------------------|----------------|
| Ativo | SP-JUN26                         | 42             |
| Ativo | NSDQ-JUN26                       | 46             |
| Ativo | DOW-JUN26                        | 78             |
| Ativo | DAX-JUN26                        | 79             |
| Ativo | BRENT CRUDE OIL                  | 89             |
| Ativo | CL SWEET CRUDE OIL               | 94             |
| Ação  | DHR - DANAHER CORPORATION        | 18             |
| Ação  | NETFLIX - NETFLIX INC            | 17             |
| Ação  | ISRG - INTUITIVE SURGICAL INC    | 20             |
| Ação  | AMD - ADVANCED MICRO DEVICES INC | 1              |

## Como executar

```bash
pip install -r requirements.txt
streamlit run controle_trading.py
```

A aplicação abre em `http://localhost:8502` (porta configurada em `.streamlit/config.toml`).

## Estrutura do projeto

```
controle-trading/
├── controle_trading.py       # Aplicação principal Streamlit
├── .streamlit/config.toml    # Configuração (porta 8502)
├── .gitignore
├── requirements.txt
├── README.md
└── trading_lotes.json        # Dados persistidos (criado automaticamente)
```

## Tecnologias

- [Streamlit](https://streamlit.io/) >= 1.40.0
- Python 3.8+