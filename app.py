import streamlit as st

# 1. ESTILO E CONFIGURAÇÃO
st.set_page_config(page_title="Simulação de Mobilidade", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #F0F2F5; }
    h1 { color: #014687; font-family: 'Inter', sans-serif; font-weight: 800; text-align: center; }
    h3 { color: #014687; margin-bottom: 5px; }
    .stNumberInput, .stSlider { background-color: #FFFFFF; border-radius: 8px; padding: 2px; }
    
    .res-box {
        background-color: #FFFFFF;
        padding: 0px 10px;
        border-radius: 10px;
        border: 1px solid #ddd;
        margin-bottom: 8px;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
    }
    .info-icon {
        position: absolute;
        top: 3px;
        right: 5px;
        font-size: 0.65rem;
        color: #ccc;
        cursor: help;
        border: 1px solid #eee;
        border-radius: 50%;
        width: 14px;
        height: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .res-label { font-size: 0.8rem; color: #666; font-weight: bold; margin: 0; text-align: center; }
    .res-value { font-size: 1rem; font-weight: 800; color: #333; margin: 0; text-align: center; }
    
    /* --- SELO DO VENCEDOR IMPARCIAL --- */
    .selo-vencedor {
        background-color: #E6FDF2; /* Verde Sucesso sempre */
        border: 2px solid #34D399;
        color: #064E3B;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(52, 211, 153, 0.2);
        margin-top: 25px;
    }
    
    .selo-label {
        font-size: 0.9rem;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #064E3B;
    }
    
    .selo-nome-vencedor {
        font-size: 2.2rem;
        font-weight: 900;
        margin: 5px 0;
        color: #10B981;
        text-shadow: 1px 1px 0px rgba(255,255,255,0.5);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Simulação de Mobilidade")

# --- 📍 CENÁRIO ---
c1, c2 = st.columns(2)
v_carro = c1.number_input("Valor Total do Veículo (R$)", value=200000.0)
meses_uso = c2.number_input("Tempo de Uso (Meses)", value=36)

st.divider()

# --- INPUTS ---
col1, col2 = st.columns(2)
with col1:
    st.markdown("### 🛒 Compra")
    ent = st.number_input("Entrada (R$)", value=45000.0)
    parc = st.number_input("Parcela (R$)", value=1850.0)
    with st.expander("Despesas e Depreciação"):
        ipva = st.number_input("IPVA/Seguro (Anual)", value=16000.0)
        manut = st.number_input("Manutenção (Anual)", value=2000.0)
        deprec = st.slider("Depreciação Anual (%)", 0, 20, 10)

with col2:
    st.markdown("### 🔑 Assinatura")
    aluguel = st.number_input("Valor Mensal (R$)", value=3490.0)
    v_investido = st.number_input("Valor de Investimento", value=45000.0)
    taxa_retorno = st.number_input("Retorno Mensal (%)", value=0.85)

# --- LÓGICA DE CÁLCULO ---
i, n = taxa_retorno / 100, meses_uso
valor_revenda = v_carro * ((1 - (deprec/100))**(n/12))
total_despesas = ((ipva + manut) / 12) * n
pat_liq_compra = valor_revenda - total_despesas 
lucro_oport_perdido = (ent * ((1 + i) ** n)) - ent
custo_mensal_compra = (parc + ((ipva + manut) / 12) + ((v_carro - valor_revenda) / n) + (lucro_oport_perdido / n))
pat_bruto_inv = v_investido * ((1 + i) ** n)
total_aluguel = aluguel * n
pat_liq_assinatura = pat_bruto_inv - total_aluguel
lucro_investimento = pat_bruto_inv - v_investido
custo_mensal_assinatura = aluguel - (lucro_investimento / n)

# --- CENTRAL DE RESULTADOS ---
st.markdown("### 📊 Central de Resultados Líquidos")
f_pat = "Compra: Valor de Revenda - Custos Fixos (IPVA/Seg/Manut) | Assinatura: Montante Investido - Total Aluguel"
f_gas = "Compra: Entrada + Σ Parcelas + Σ Custos Fixos | Assinatura: Σ Mensalidades"
f_mes = "Compra: Parcela + Custos Fixos + Depreciação + Custo Oportunidade | Assinatura: Aluguel - Rendimento Mensal"

h1, h2, h3 = st.columns(3)
h2.markdown("<p style='text-align:center; font-weight:bold; color:#d32f2f; margin-bottom:5px;'>🛒 COMPRA</p>", unsafe_allow_html=True)
h3.markdown("<p style='text-align:center; font-weight:bold; color:#2e7d32; margin-bottom:5px;'>🔑 ASSINATURA</p>", unsafe_allow_html=True)

def render_row(label, val_compra, val_assinatura, formula):
    c1, c2, c3 = st.columns(3)
    c1.markdown(f"""<div class='res-box'><span class='info-icon' title='{formula}'>?</span><p class='res-label'>{label}</p></div>""", unsafe_allow_html=True)
    c2.markdown(f"""<div class='res-box'><p class='res-value'>R$ {val_compra:,.2f}</p></div>""", unsafe_allow_html=True)
    c3.markdown(f"""<div class='res-box'><p class='res-value'>R$ {val_assinatura:,.2f}</p></div>""", unsafe_allow_html=True)

render_row("Patrimônio Líquido", pat_liq_compra, pat_liq_assinatura, f_pat)
render_row("Gasto Total", (ent + (parc * n) + total_despesas), total_aluguel, f_gas)
render_row("Custo Mensal Real", custo_mensal_compra, custo_mensal_assinatura, f_mes)

# --- VEREDITO FINAL ---
vencedor = "ASSINATURA" if custo_mensal_assinatura < custo_mensal_compra else "COMPRA"

st.markdown(f"""
    <div class="selo-vencedor">
        <div class="selo-label">Vantagem Financeira Identificada</div>
        <div class="selo-nome-vencedor">★ {vencedor} ★</div>
        <div class="selo-label" style="font-size:0.7rem; margin-top:10px;">Opção com menor custo mensal real</div>
    </div>
    """, unsafe_allow_html=True)