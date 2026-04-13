import streamlit as st
import datetime as dt
import json
from pathlib import Path

# ---------- CONFIGURAÇÃO ----------

ARQUIVO = Path("trading_lotes.json")

ATIVOS = [
    {"tipo": "Ativo", "nome": "SP-JUN26", "lotes_iniciais": 42},
    {"tipo": "Ativo", "nome": "NSDQ-JUN26", "lotes_iniciais": 46},
    {"tipo": "Ativo", "nome": "DOW-JUN26", "lotes_iniciais": 78},
    {"tipo": "Ativo", "nome": "DAX-JUN26", "lotes_iniciais": 79},
    {"tipo": "Ativo", "nome": "BRENT CRUDE OIL", "lotes_iniciais": 89},
    {"tipo": "Ativo", "nome": "CL SWEET CRUDE OIL", "lotes_iniciais": 94},
    {"tipo": "Ação", "nome": "DHR - DANAHER CORPORATION", "lotes_iniciais": 18},
    {"tipo": "Ação", "nome": "NETFLIX - NETFLIX INC", "lotes_iniciais": 17},
    {"tipo": "Ação", "nome": "ISRG - INTUITIVE SURGICAL INC", "lotes_iniciais": 20},
    {"tipo": "Ação", "nome": "AMD - ADVANCED MICRO DEVICES INC", "lotes_iniciais": 1},
]

NOMES_ATIVOS = [a["nome"] for a in ATIVOS]
LOTES_INICIAIS = {a["nome"]: a["lotes_iniciais"] for a in ATIVOS}

# ---------- PERSISTÊNCIA ----------


def carregar_dados():
    if ARQUIVO.exists():
        return json.loads(ARQUIVO.read_text(encoding="utf-8"))
    return {"registros": []}


def salvar_dados(dados):
    ARQUIVO.write_text(
        json.dumps(dados, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def calcular_lotes_usados(dados, nome_ativo):
    return sum(
        r["lotes"] for r in dados["registros"] if r["ativo"] == nome_ativo
    )


# ---------- INDICADOR VISUAL ----------


def indicador(disponivel, total):
    if total == 0:
        return "⚪"
    pct = disponivel / total
    if pct <= 0:
        return "🔴"
    elif pct <= 0.3:
        return "🟡"
    else:
        return "🟢"


# ---------- APP ----------

st.set_page_config(
    "Controle de Lotes – Trading", layout="centered", initial_sidebar_state="collapsed"
)

st.markdown(
    "<h2 style='margin-bottom:0.5rem'>📊 Controle de Lotes — Trading</h2>",
    unsafe_allow_html=True,
)

dados = carregar_dados()

# ===== RESUMO =====

st.markdown("### Resumo de lotes")

html_resumo = """
<style>
.tbl-trading {
    width: 100%;
    border-collapse: collapse;
    font-size: 14px;
    margin-bottom: 1rem;
}
.tbl-trading th, .tbl-trading td {
    border: 1px solid #CCC;
    padding: 6px 10px;
    text-align: center;
}
.tbl-trading th {
    background-color: #f0f2f6;
    font-weight: 600;
}
.tbl-trading td.nome {
    text-align: left;
}
.tbl-trading tr:nth-child(even) {
    background-color: #fafafa;
}
</style>
<table class="tbl-trading">
<tr>
    <th>Tipo</th>
    <th>Ativo / Ação</th>
    <th>Iniciais</th>
    <th>Usados</th>
    <th>Disponíveis</th>
    <th></th>
</tr>
"""

for ativo in ATIVOS:
    nome = ativo["nome"]
    total = ativo["lotes_iniciais"]
    usados = calcular_lotes_usados(dados, nome)
    disponivel = total - usados
    status = indicador(disponivel, total)
    html_resumo += (
        f"<tr>"
        f"<td>{ativo['tipo']}</td>"
        f"<td class='nome'>{nome}</td>"
        f"<td>{total}</td>"
        f"<td>{usados}</td>"
        f"<td>{disponivel}</td>"
        f"<td>{status}</td>"
        f"</tr>"
    )

html_resumo += "</table>"
st.markdown(html_resumo, unsafe_allow_html=True)

st.markdown("---")

# ===== REGISTRO DE USO =====

st.markdown("### Registrar uso de lotes")

with st.form("form_registro", clear_on_submit=True):
    col1, col2, col3 = st.columns([3, 1.5, 1.5])
    with col1:
        ativo_sel = st.selectbox("Ativo / Ação", NOMES_ATIVOS)
    with col2:
        data_uso = st.date_input("Data", value=dt.date.today())
    with col3:
        qtd = st.number_input("Lotes usados", min_value=1, value=1, step=1)

    obs = st.text_input("Observação (opcional)")
    enviar = st.form_submit_button("Registrar")

    if enviar:
        disponivel = LOTES_INICIAIS[ativo_sel] - calcular_lotes_usados(dados, ativo_sel)
        if qtd > disponivel:
            st.error(
                f"Quantidade ({qtd}) excede os lotes disponíveis ({disponivel}) para {ativo_sel}."
            )
        else:
            dados["registros"].append(
                {
                    "ativo": ativo_sel,
                    "data": data_uso.isoformat(),
                    "lotes": qtd,
                    "obs": obs,
                }
            )
            salvar_dados(dados)
            st.success(f"{qtd} lote(s) registrado(s) para {ativo_sel}.")
            st.rerun()

st.markdown("---")

# ===== HISTÓRICO =====

st.markdown("### Histórico de uso")

if not dados["registros"]:
    st.info("Nenhum registro de uso ainda.")
else:
    filtro = st.selectbox(
        "Filtrar por ativo",
        ["Todos"] + NOMES_ATIVOS,
        key="filtro_hist",
    )

    registros = dados["registros"]
    if filtro != "Todos":
        registros = [r for r in registros if r["ativo"] == filtro]

    registros_ordenados = sorted(registros, key=lambda r: r["data"], reverse=True)

    html_hist = """
    <table class="tbl-trading">
    <tr>
        <th>Data</th>
        <th>Ativo / Ação</th>
        <th>Lotes</th>
        <th>Observação</th>
    </tr>
    """
    for reg in registros_ordenados:
        html_hist += (
            f"<tr>"
            f"<td>{reg['data']}</td>"
            f"<td class='nome'>{reg['ativo']}</td>"
            f"<td>{reg['lotes']}</td>"
            f"<td class='nome'>{reg.get('obs', '')}</td>"
            f"</tr>"
        )
    html_hist += "</table>"
    st.markdown(html_hist, unsafe_allow_html=True)

    st.markdown("#### Excluir registro")
    opcoes = [
        f"{r['data']} | {r['ativo']} | {r['lotes']} lote(s)"
        for r in registros_ordenados
    ]
    sel = st.selectbox("Selecione o registro", opcoes, key="del_sel")
    if st.button("🗑️ Excluir selecionado"):
        idx_sel = opcoes.index(sel)
        reg_alvo = registros_ordenados[idx_sel]
        idx_original = dados["registros"].index(reg_alvo)
        dados["registros"].pop(idx_original)
        salvar_dados(dados)
        st.rerun()
