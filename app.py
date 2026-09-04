import json
import os
import streamlit as st

# 1. Configuração da página
st.set_page_config(
    page_title="Aura Nutrition",
    page_icon="⚡",
    layout="wide"
)

# 2. Persistência de Dados (Arquivo JSON local)
DATA_FILE = "user_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {"preferences": {}, "cart": []}

def save_data():
    data = {
        "preferences": st.session_state.get("preferences", {}),
        "cart": st.session_state.get("cart", [])
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Inicializa o session_state com dados salvos
if "data_loaded" not in st.session_state:
    saved_data = load_data()
    st.session_state.preferences = saved_data.get("preferences", {})
    st.session_state.cart = saved_data.get("cart", [])
    st.session_state.data_loaded = True

# 3. Estilização CSS (Fundo degradê e cantos arredondados)
st.markdown("""
    <style>
    /* Fundo degradê levemente branco e azul */
    .stApp {
        background: linear-gradient(135deg, #ffffff 0%, #f0f7ff 50%, #e0f0ff 100%);
        color: #1e293b;
    }
    
    /* Arredondamento e bordas para cards/conteúdos */
    div[data-testid="stVerticalBlock"] > div {
        border-radius: 20px;
    }

    .stButton>button {
        border-radius: 12px;
        background-color: #0284c7;
        color: white;
        border: none;
        padding: 8px 16px;
        font-weight: bold;
    }

    .stButton>button:hover {
        background-color: #0369a1;
        color: white;
    }

    /* Estilo dos cards de produtos */
    .product-card {
        background-color: rgba(255, 255, 255, 0.85);
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Lista de Produtos com links do Mercado Livre
PRODUCTS = [
    {
        "id": 1,
        "name": "Whey Protein Concentrado 1kg",
        "category": "Massa Muscular",
        "form": "Pó",
        "price": "R$ 99,90",
        "link": "https://lista.mercadolivre.com.br/whey-protein",
        "desc": "Proteína de alta qualidade para recuperação muscular rápida."
    },
    {
        "id": 2,
        "name": "Creatina Monohidratada 300g",
        "category": "Força / Performance",
        "form": "Pó",
        "price": "R$ 80,00",
        "link": "https://lista.mercadolivre.com.br/creatina",
        "desc": "Aumento de força explosiva e volume muscular."
    },
    {
        "id": 3,
        "name": "Multivitamínico Complete 90 Caps",
        "category": "Saúde Geral",
        "form": "Cápsula",
        "price": "R$ 45,00",
        "link": "https://lista.mercadolivre.com.br/multivitaminico",
        "desc": "Vitamins e minerais essenciais para o seu dia a dia."
    },
    {
        "id": 4,
        "name": "Pré-Treino Pro Focus 300g",
        "category": "Energia",
        "form": "Pó",
        "price": "R$ 110,00",
        "link": "https://lista.mercadolivre.com.br/pre-treino",
        "desc": "Energia máxima e foco total para os seus treinos."
    }
]

# Cabecalho
st.title("⚡ Aura Nutrition")
st.caption("Sua loja oficial de suplementos e performance")

# Menu de Navegação por Abas
tab_loja, tab_pref, tab_recom, tab_links = st.tabs([
    "🛒 Loja de Suplementos", 
    "⚙️ Preferência de Produtos", 
    "⭐ Recomendações", 
    "🔗 Links Úteis"
])

# --- ABA 1: LOJA ---
with tab_loja:
    st.subheader("Catálogo de Produtos")
    
    # Filtro dinâmico baseado na preferência salva
    pref_cat = st.session_state.preferences.get("objetivo", "Todos")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        for p in PRODUCTS:
            if pref_cat == "Todos" or p["category"] == pref_cat:
                st.markdown(f"""
                <div class="product-card">
                    <h3>{p['name']}</h3>
                    <p><b>Categoria:</b> {p['category']} | <b>Formato:</b> {p['form']}</p>
                    <p>{p['desc']}</p>
                    <h4>{p['price']}</h4>
                </div>
                """, unsafe_allow_html=True)
                
                col_btn1, col_btn2 = st.columns([1, 4])
                with col_btn1:
                    st.link_button("Comprar no ML 🔗", p["link"])
                with col_btn2:
                    if st.button(f"Adicionar ao Carrinho", key=f"add_{p['id']}"):
                        st.session_state.cart.append(p["name"])
                        save_data()
                        st.success(f"{p['name']} salvo no seu carrinho!")

    with col2:
        st.subheader("Seu Carrinho Salvo")
        if st.session_state.cart:
            for item in st.session_state.cart:
                st.write(f"- {item}")
            if st.button("Limpar Carrinho"):
                st.session_state.cart = []
                save_data()
                st.rerun()
        else:
            st.info("O carrinho está vazio.")

# --- ABA 2: PREFERÊNCIA DE PRODUTOS ---
with tab_pref:
    st.subheader("Personalize seu Perfil")
    st.write("Escolha seu objetivo para filtrarmos os produtos ideais para você.")
    
    objetivo = st.selectbox(
        "Qual é o seu objetivo principal?",
        ["Todos", "Massa Muscular", "Força / Performance", "Energia", "Saúde Geral"],
        index=["Todos", "Massa Muscular", "Força / Performance", "Energia", "Saúde Geral"].index(
            st.session_state.preferences.get("objetivo", "Todos")
        )
    )
    
    formato = st.radio(
        "Preferência de formato:",
        ["Pó", "Cápsulas", "Tanto faz"],
        index=["Pó", "Cápsulas", "Tanto faz"].index(
            st.session_state.preferences.get("formato", "Tanto faz")
        )
    )
    
    if st.button("Salvar Preferências"):
        st.session_state.preferences = {
            "objetivo": objetivo,
            "formato": formato
        }
        save_data()
        st.success("Preferências salvas com sucesso! Elas serão mantidas quando você fechar a página.")

# --- ABA 3: RECOMENDAÇÕES ---
with tab_recom:
    st.subheader("Recomendações Especiais")
    st.write("Combinações recomendadas para acelerar seus resultados:")
    
    rec_col1, rec_col2 = st.columns(2)
    
    with rec_col1:
        st.markdown("""
        <div class="product-card">
            <h3>Kit Hipertrofia Acelerada 🔥</h3>
            <p>Combine <b>Whey Protein + Creatina</b> no pós-treino para garantir a máxima síntese proteica e ganho de força.</p>
        </div>
        """, unsafe_allow_html=True)
        st.link_button("Ver Kits no Mercado Livre", "https://lista.mercadolivre.com.br/kit-whey-creatina")

    with rec_col2:
        st.markdown("""
        <div class="product-card">
            <h3>Kit Foco & Energia ⚡</h3>
            <p>Combine <b>Pré-treino + Multivitamínico</b> para treinar em alto nível e manter a imunidade blindada.</p>
        </div>
        """, unsafe_allow_html=True)
        st.link_button("Ver Pré-Treinos no Mercado Livre", "https://lista.mercadolivre.com.br/pre-treino")

# --- ABA 4: LINKS ÚTEIS ---
with tab_links:
    st.subheader("Central de Links e Parceiros")
    
    st.write("Acesse os nossos canais de venda direta e conteúdos adicionais:")
    
    st.markdown("- [Loja Oficial no Mercado Livre](https://www.mercadolivre.com.br)")
    st.markdown("- [Calculadora de Proteína Diária](https://www
