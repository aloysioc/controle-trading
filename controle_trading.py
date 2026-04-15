import streamlit as st
import datetime as dt
import json
import uuid
from pathlib import Path

# ---------- CONFIGURAÇÃO ----------

ARQUIVO = Path("trading_lotes.json")

ATIVOS = [
    {"tipo": "Ativo", "nome": "SP-JUN26", "lotes_iniciais": 42, "cat": "indice"},
    {"tipo": "Ativo", "nome": "NSDQ-JUN26", "lotes_iniciais": 46, "cat": "indice"},
    {"tipo": "Ativo", "nome": "DOW-JUN26", "lotes_iniciais": 78, "cat": "indice"},
    {"tipo": "Ativo", "nome": "DAX-JUN26", "lotes_iniciais": 79, "cat": "indice"},
    {"tipo": "Ativo", "nome": "BRENT CRUDE OIL", "lotes_iniciais": 89, "cat": "petroleo"},
    {"tipo": "Ativo", "nome": "CL SWEET CRUDE OIL", "lotes_iniciais": 94, "cat": "petroleo"},
    {"tipo": "Ação", "nome": "DHR - DANAHER CORPORATION", "lotes_iniciais": 18, "cat": "acao"},
    {"tipo": "Ação", "nome": "NETFLIX - NETFLIX INC", "lotes_iniciais": 17, "cat": "acao"},
    {"tipo": "Ação", "nome": "ISRG - INTUITIVE SURGICAL INC", "lotes_iniciais": 20, "cat": "acao"},
    {"tipo": "Ação", "nome": "AMD - ADVANCED MICRO DEVICES INC", "lotes_iniciais": 1, "cat": "acao"},
]

COR_CATEGORIA = {
    "indice": "#D32F2F",    # vermelho
    "petroleo": "#7B1FA2",  # roxo
    "acao": "#2E7D32",       # verde
}

COR_CATEGORIA_POR_NOME = {a["nome"]: a["cat"] for a in ATIVOS}

NOMES_ATIVOS = [a["nome"] for a in ATIVOS]
LOTES_INICIAIS = {a["nome"]: a["lotes_iniciais"] for a in ATIVOS}

# ---------- PERSISTÊNCIA ----------


def carregar_dados():
    if ARQUIVO.exists():
        dados = json.loads(ARQUIVO.read_text(encoding="utf-8"))
        modificado = False
        for r in dados["registros"]:
            if "id" not in r:
                r["id"] = str(uuid.uuid4())
                modificado = True
        if modificado:
            salvar_dados(dados)
        return dados
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
    usados_pct = 1 - (disponivel / total)
    if usados_pct >= 1:
        return "🟢"
    elif usados_pct >= 0.7:
        return "🟡"
    else:
        return "🔴"


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
    color: #222;
}
.tbl-trading th, .tbl-trading td {
    border: 1px solid #999;
    padding: 6px 10px;
    text-align: center;
}
.tbl-trading th {
    background-color: #e0e2e6;
    font-weight: 600;
    color: #111;
}
.tbl-trading td {
    background-color: #fff;
    color: #222;
    font-weight: 600;
}
.tbl-trading td.nome {
    text-align: left;
}
.tbl-trading tr:nth-child(even) td {
    background-color: #f2f2f2;
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
    cor = COR_CATEGORIA[ativo["cat"]]
    html_resumo += (
        f"<tr style='color:{cor}'>"
        f"<td style='color:{cor}'>{ativo['tipo']}</td>"
        f"<td class='nome' style='color:{cor}'>{nome}</td>"
        f"<td>{total}</td>"
        f"<td>{usados:.2f}</td>"
        f"<td>{disponivel:.2f}</td>"
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
        qtd = st.number_input("Lotes usados", min_value=0.01, value=1.0, step=0.1, format="%.2f")

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
                    "id": str(uuid.uuid4()),
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
        cor = COR_CATEGORIA.get(COR_CATEGORIA_POR_NOME.get(reg["ativo"], ""), "#222")
        html_hist += (
            f"<tr>"
            f"<td>{reg['data']}</td>"
            f"<td class='nome' style='color:{cor}'>{reg['ativo']}</td>"
            f"<td>{reg['lotes']}</td>"
            f"<td class='nome'>{reg.get('obs', '')}</td>"
            f"</tr>"
        )
    html_hist += "</table>"
    st.markdown(html_hist, unsafe_allow_html=True)

    st.markdown("#### Gerenciar registros")
    opcoes = [
        f"{r['data']} | {r['ativo']} | {r['lotes']} lote(s)"
        for r in registros_ordenados
    ]
    # Mapa de opção → id para identificação segura
    opcao_para_id = {
        f"{r['data']} | {r['ativo']} | {r['lotes']} lote(s)": r["id"]
        for r in registros_ordenados
    }
    id_para_reg = {r["id"]: r for r in registros_ordenados}

    sel = st.selectbox("Selecione o registro", opcoes, key="sel_registro")
    rid = opcao_para_id[sel]
    reg_alvo = id_para_reg[rid]

    # Sufixo dinâmico para recriar widgets ao trocar de registro
    _sfx = f"_{rid}"

    # Pré-carrega o valor de Observação no session_state (text_input ignora value)
    obs_key = f"edit_obs{_sfx}"
    if obs_key not in st.session_state:
        st.session_state[obs_key] = reg_alvo.get("obs", "")

    col_edit, col_del = st.columns(2)

    with col_edit:
        with st.expander("✏️ Editar registro"):
            with st.form(f"form_editar{_sfx}", clear_on_submit=False):
                novo_ativo = st.selectbox(
                    "Ativo / Ação",
                    NOMES_ATIVOS,
                    index=NOMES_ATIVOS.index(reg_alvo["ativo"]),
                    key=f"edit_ativo{_sfx}",
                )
                nova_data = st.date_input(
                    "Data",
                    value=dt.date.fromisoformat(reg_alvo["data"]),
                    key=f"edit_data{_sfx}",
                )
                novo_lotes = st.number_input(
                    "Lotes",
                    min_value=0.01,
                    value=float(reg_alvo["lotes"]),
                    step=0.1,
                    format="%.2f",
                    key=f"edit_lotes{_sfx}",
                )
                nova_obs = st.text_input(
                    "Observação",
                    key=obs_key,
                )
                salvar_edicao = st.form_submit_button("Salvar alterações")

                if salvar_edicao:
                    for i, r in enumerate(dados["registros"]):
                        if r["id"] == rid:
                            dados["registros"][i] = {
                                "id": rid,
                                "ativo": novo_ativo,
                                "data": nova_data.isoformat(),
                                "lotes": novo_lotes,
                                "obs": nova_obs,
                            }
                            break
                    salvar_dados(dados)
                    st.success("Registro atualizado.")
                    st.rerun()

    with col_del:
        if st.button("🗑️ Excluir selecionado"):
            dados["registros"] = [r for r in dados["registros"] if r["id"] != rid]
            salvar_dados(dados)
            st.rerun()
