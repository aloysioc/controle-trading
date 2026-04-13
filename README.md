# 📊 Controle de Lotes — Trading

Aplicação web em [Streamlit](https://streamlit.io/) para controle de lotes disponíveis em ativos e ações de trading.

## Funcionalidades

- Resumo visual dos lotes disponíveis por ativo (🟢 folgado / 🟡 baixo / 🔴 esgotado)
- Registro de uso de lotes por data, com observação opcional
- Histórico completo com opção de exclusão de registros
- Persistência local em arquivo JSON (`trading_lotes.json`)

## Ativos monitorados

| Tipo  | Nome                            | Lotes Iniciais |
|-------|---------------------------------|----------------|
| Ativo | SP-JUN26                        | 42             |
| Ativo | NSDQ-JUN26                      | 46             |
| Ativo | DOW-JUN26                       | 78             |
| Ativo | DAX-JUN26                       | 79             |
| Ativo | BRENT CRUDE OIL                 | 89             |
| Ativo | CL SWEET CRUDE OIL              | 94             |
| Ação  | DHR - DANAHER CORPORATION       | 18             |
| Ação  | NETFLIX - NETFLIX INC           | 17             |
| Ação  | ISRG - INTUITIVE SURGICAL INC   | 20             |
| Ação  | AMD - ADVANCED MICRO DEVICES INC| 1              |

## Como executar

```bash
pip install -r requirements.txt
streamlit run controle_trading.py