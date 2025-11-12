import streamlit as st
import pandas as pd
import os
import base64
import requests

# ================== CONFIGURAÇÃO ==================
st.set_page_config(
    page_title="Painel Administrativo - Bruna Morais Peixoto Atelier",
    page_icon="💎",
    layout="wide"
)

# ================== FUNÇÃO AUXILIAR ==================
def get_base64_of_image(img_path):
    with open(img_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# ================== ESTILO VISUAL ==================
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Cormorant Garamond', serif !important;
    background-color: #fdf9f3 !important;
    color: #2b2b2b !important;
}

h1, h2, h3 {
    color: #4b4b4b !important;
    text-align: center !important;
}

input[type="text"], input[type="number"], textarea, .stTextInput>div>div>input {
    background-color: #ffffff !important;
    color: #2b2b2b !important;
    border-radius: 8px !important;
    border: 1px solid #c5b8a5 !important;
    font-size: 1rem !important;
    padding: 8px 12px !important;
}

section[data-testid="stFileUploader"] div div div div {
    background-color: #ffffff !important;
    color: #2b2b2b !important;
    border: 1px solid #c5b8a5 !important;
    border-radius: 8px !important;
}

.stButton>button {
    background-color: #d4af37 !important;
    color: white !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 22px !important;
    transition: 0.25s ease-in-out !important;
    font-size: 1.05rem !important;
}
.stButton>button:hover {
    background-color: #b8962b !important;
    transform: scale(1.05);
}

div[data-testid="stAlert"] {
    border-radius: 10px !important;
}

a {
    color: #b8962b !important;
    text-decoration: none !important;
}
a:hover {
    text-decoration: underline !important;
}

/* Cards de produto */
.product-card {
    background-color: #ffffff;
    border: 1px solid #d4af37;
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 15px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    text-align: center;
}
.product-card img {
    width: 100%;
    border-radius: 8px;
    margin-bottom: 10px;
}

/* Rodapé */
.footer {
    text-align: center;
    margin-top: 60px;
    padding: 20px;
    font-size: 0.9rem;
    color: #4b4b4b;
    border-top: 1px solid #d4af37;
}
.footer img {
    width: 80px;
    margin-top: 10px;
    opacity: 0.85;
}
</style>
""", unsafe_allow_html=True)

# ================== LOGO ==================
logo_path = os.path.join("backend", "data", "banner.jpg")

if os.path.exists(logo_path):
    logo_base64 = get_base64_of_image(logo_path)
    st.markdown(
        f"""
        <div style="text-align: center; margin-top: -30px;">
            <img src="data:image/png;base64,{logo_base64}" 
                 alt="Logo Bruna Morais Peixoto Atelier" 
                 style="width: 180px; border-radius: 10px;">
            <h1 style="margin-top: 10px;">Painel Administrativo</h1>
            <h2>Bruna Morais Peixoto Atelier</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# ================== TOKEN DO GITHUB ==================
if "github_token" not in st.session_state:
    token_input = st.text_input("🔑 Token do GitHub (repo access)", type="password")
    if token_input:
        st.session_state["github_token"] = token_input
        st.success("✅ Token salvo com segurança.")
else:
    st.info("🔒 Token armazenado com segurança (oculto).")

# ================== CONFIGURAÇÃO DO GITHUB ==================
GITHUB_REPO = "lucasptrolesi-ai/brunamoraisatelier"
CATALOGO_PATH = "backend/data/catalogo.csv"

# ================== FUNÇÃO PARA ATUALIZAR O GITHUB ==================
def salvar_no_github(df):
    """Salva o catálogo no repositório do GitHub."""
    token = st.session_state.get("github_token")
    if not token:
        st.warning("⚠️ Informe o token do GitHub antes de salvar.")
        return

    csv_content = df.to_csv(index=False).encode()
    b64 = base64.b64encode(csv_content).decode()

    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{CATALOGO_PATH}"
    headers = {"Authorization": f"token {token}"}
    response = requests.get(url, headers=headers)
    sha = response.json().get("sha") if response.status_code == 200 else None

    data = {
        "message": "Atualização automática do catálogo",
        "content": b64,
        "branch": "main"
    }
    if sha:
        data["sha"] = sha

    r = requests.put(url, headers=headers, json=data)
    if r.status_code in (200, 201):
        st.success("📤 Catálogo atualizado no GitHub com sucesso!")
    else:
        st.error(f"Erro ao salvar no GitHub: {r.text}")

# ================== CATÁLOGO ==================
st.header("📦 Catálogo Atual")

catalog_path = os.path.join("backend", "data", "catalogo.csv")
if os.path.exists(catalog_path):
    df = pd.read_csv(catalog_path)
else:
    df = pd.DataFrame(columns=["Nome", "Descrição", "Preço", "Imagem"])

if len(df) == 0:
    st.warning("Nenhum produto cadastrado.")
else:
    for _, row in df.iterrows():
        st.markdown(
            f"""
            <div class="product-card">
                <img src="{row['Imagem']}" alt="{row['Nome']}">
                <h4>{row['Nome']}</h4>
                <p>{row['Descrição']}</p>
                <strong>R$ {row['Preço']}</strong>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("---")

# ================== ADICIONAR PRODUTO ==================
st.header("➕ Adicionar Novo Produto")

col1, col2 = st.columns(2)
with col1:
    nome = st.text_input("Nome da Peça")
    preco = st.text_input("Preço (ex: 199,90)")
with col2:
    descricao = st.text_area("Descrição")
    imagem_file = st.file_uploader("Imagem do Produto", type=["jpg", "jpeg", "png"])
    imagem_link = st.text_input("Ou URL da Imagem (Google Drive, etc.)")

if st.button("💾 Salvar Produto"):
    if not nome or not preco:
        st.error("Preencha pelo menos o nome e o preço do produto.")
    else:
        if imagem_file:
            img_bytes = imagem_file.read()
            img_base64 = base64.b64encode(img_bytes).decode()
            img_src = f"data:image/png;base64,{img_base64}"
        elif imagem_link:
            img_src = imagem_link
        else:
            img_src = ""

        new_row = {"Nome": nome, "Descrição": descricao, "Preço": preco, "Imagem": img_src}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(catalog_path, index=False)
        salvar_no_github(df)
        st.success(f"✅ Produto '{nome}' adicionado com sucesso!")

st.markdown("---")

# ================== REMOVER PRODUTO ==================
st.header("❌ Remover Produto")
if len(df) > 0:
    produto_remover = st.selectbox("Selecione o produto:", df["Nome"])
    if st.button("Remover Produto"):
        df = df[df["Nome"] != produto_remover]
        df.to_csv(catalog_path, index=False)
        salvar_no_github(df)
        st.success(f"🗑️ Produto '{produto_remover}' removido.")
else:
    st.info("Nenhum produto para remover.")

# ================== RODAPÉ ==================
if os.path.exists(logo_path):
    logo_footer = get_base64_of_image(logo_path)
    st.markdown(
        f"""
        <div class="footer">
            <p>Desenvolvido com 💻 por <strong>Lucas Morais Peixoto</strong></p>
            <img src="data:image/png;base64,{logo_footer}" alt="Logo Bruna Morais Peixoto Atelier">
        </div>
        """,
        unsafe_allow_html=True
    )
