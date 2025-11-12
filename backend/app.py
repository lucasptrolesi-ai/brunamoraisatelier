import os
import io
import time
import base64
import requests
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

# ====== CONFIGURAÇÕES INICIAIS ======
st.set_page_config(page_title="Painel Administrativo - Bruna Morais Peixoto Atelier", page_icon="💍", layout="wide")

# ====== ESTILO PERSONALIZADO ======
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Cormorant Garamond', serif !important;
    background: #fdf9f3;
    color: #4b3832;
}
h1, h2, h3 {
    color: #d4af37;
    font-weight: 600;
    text-align: center;
}
div.stButton > button {
    background: #d4af37;
    color: white;
    border-radius: 24px;
    padding: 10px 18px;
    font-weight: 600;
}
div.stButton > button:hover {
    background: #b8962b;
    transform: scale(1.02);
}
.stTextInput input, .stTextArea textarea {
    background: #fffaf0;
    border: 1px solid #ccbfa1;
    border-radius: 10px;
}
@media (max-width: 768px) {
    h1 { font-size: 1.6rem; }
    h2 { font-size: 1.2rem; }
    div.stButton > button { width: 100%; }
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>💎 Painel Administrativo<br>Bruna Morais Peixoto Atelier</h1>", unsafe_allow_html=True)
st.divider()

# ====== VARIÁVEIS DO PROJETO ======
REPO_OWNER = "lucasptrolesi-ai"
REPO_NAME = "brunamoraisatelier"
BRANCH = "main"

CSV_PATH = "catalogo.csv"
IMG_DIR = "imagens"
RAW_BASE = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/{BRANCH}"

# ====== TOKEN DO GITHUB ======
load_dotenv()
default_token = os.getenv("GITHUB_TOKEN", "")
token = st.text_input("🔑 Token do GitHub (repo access)", type="password", value=default_token)

if not token:
    st.warning("Informe seu token do GitHub acima para publicar no repositório.")
headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github+json"}

# ====== FUNÇÕES AUXILIARES ======
def gh_url(path): 
    return f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{path}"

def get_sha(path):
    r = requests.get(gh_url(path), headers=headers)
    return r.json().get("sha") if r.status_code == 200 else None

def upload_to_repo(path, content_bytes, message):
    sha = get_sha(path)
    payload = {
        "message": message,
        "content": base64.b64encode(content_bytes).decode(),
        "branch": BRANCH
    }
    if sha:
        payload["sha"] = sha
    r = requests.put(gh_url(path), headers=headers, json=payload)
    return r.status_code in [200, 201], r.text

def get_csv():
    r = requests.get(f"{RAW_BASE}/{CSV_PATH}")
    if r.status_code == 200:
        return pd.read_csv(io.StringIO(r.text))
    return pd.DataFrame(columns=["Nome", "Descrição", "Preço", "Imagem"])

def normalize_drive_link(url):
    if "drive.google.com/file/d/" in url:
        file_id = url.split("/d/")[1].split("/")[0]
        return f"https://drive.google.com/uc?export=view&id={file_id}"
    return url

# ====== CARREGAR CATÁLOGO ======
df = get_csv()
st.subheader("📋 Catálogo Atual")
if df.empty:
    st.info("Nenhum produto cadastrado.")
else:
    st.dataframe(df, use_container_width=True)

st.divider()
st.subheader("➕ Adicionar Novo Produto")

# ====== FORMULÁRIO ======
col1, col2 = st.columns(2)
with col1:
    nome = st.text_input("Nome da Peça")
    preco = st.text_input("Preço (ex: 199,90)")
with col2:
    descricao = st.text_area("Descrição", height=100)

st.markdown("**Imagem do Produto** — arraste o arquivo ou cole o link")
col_up1, col_up2 = st.columns(2)
with col_up1:
    img_file = st.file_uploader("Upload de Imagem", type=["jpg", "jpeg", "png"])
with col_up2:
    img_url = st.text_input("Ou URL/Link (Google Drive, etc.)")

# ====== SALVAR ======
if st.button("💾 Salvar Produto"):
    if not token:
        st.error("Token do GitHub é obrigatório.")
    elif not (nome and descricao and preco and (img_file or img_url)):
        st.warning("Preencha todos os campos e adicione uma imagem.")
    else:
        # --- Upload da Imagem ---
        if img_file:
            ext = os.path.splitext(img_file.name)[1]
            filename = f"{int(time.time())}_{nome.replace(' ', '_')}{ext}"
            path_img = f"{IMG_DIR}/{filename}"
            ok_img, msg = upload_to_repo(path_img, img_file.getvalue(), f"🖼️ Upload imagem {filename}")
            if not ok_img:
                st.error("Erro ao enviar imagem.")
                st.stop()
            img_final = f"{RAW_BASE}/{path_img}"
        else:
            img_final = normalize_drive_link(img_url)

        # --- Atualizar CSV ---
        new_row = pd.DataFrame([[nome, descricao, preco, img_final]], columns=df.columns)
        df_new = pd.concat([df, new_row], ignore_index=True)
        ok_csv, msg_csv = upload_to_repo(CSV_PATH, df_new.to_csv(index=False).encode(), f"📦 Novo produto: {nome}")

        if ok_csv:
            st.success("✅ Produto publicado com sucesso!")
            st.info("Atualize a página (Ctrl + R) para ver o novo produto no catálogo.")
        else:
            st.error("Erro ao atualizar catálogo.")

st.divider()
st.subheader("❌ Remover Produto")

if df.empty:
    st.info("Nenhum produto para remover.")
else:
    alvo = st.selectbox("Selecione o produto para remover", df["Nome"])
    if st.button("Remover 🗑️"):
        df2 = df[df["Nome"] != alvo]
        ok, msg = upload_to_repo(CSV_PATH, df2.to_csv(index=False).encode(), f"🗑️ Remove produto: {alvo}")
        if ok:
            st.success(f"Produto '{alvo}' removido com sucesso!")
        else:
            st.error("Erro ao remover produto.")
