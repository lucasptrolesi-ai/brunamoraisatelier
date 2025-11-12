import streamlit as st
import pandas as pd
import io
from github import Github

# === CONFIGURAÇÃO ===
st.set_page_config(page_title="Painel Administrativo - Bruna Morais Peixoto Atelier", layout="wide")

st.markdown("<h1 style='text-align: center;'>💎 Painel Administrativo<br>Bruna Morais Peixoto Atelier</h1>", unsafe_allow_html=True)
st.divider()

# === 1️⃣ AUTENTICAÇÃO GITHUB ===
st.subheader("🔑 Autenticação do GitHub")

# Campo para inserir o token
token = st.text_input("Cole aqui seu token do GitHub (necessário apenas uma vez):", type="password")
salvar_token = st.button("Salvar Token 🔒")

if "gh_token" not in st.session_state:
    st.session_state.gh_token = None

if salvar_token and token:
    st.session_state.gh_token = token
    st.success("✅ Token salvo com sucesso! Agora você pode gerenciar o catálogo.")

# Mostrar aviso se não houver token
if not st.session_state.gh_token:
    st.warning("⚠️ É necessário inserir seu token do GitHub acima para acessar o painel.")
    st.stop()

# === 2️⃣ CONEXÃO COM O REPOSITÓRIO ===
try:
    g = Github(st.session_state.gh_token)
    repo = g.get_user().get_repo("brunamoraisatelier")  # nome exato do repositório
    st.success("🔗 Conectado com sucesso ao repositório brunamoraisatelier.")
except Exception as e:
    st.error(f"❌ Erro ao conectar ao GitHub: {e}")
    st.stop()

# === 3️⃣ LEITURA DO CATÁLOGO ===
csv_path = "catalogo.csv"
try:
    content = repo.get_contents(csv_path)
    df = pd.read_csv(io.StringIO(content.decoded_content.decode()))
except Exception:
    df = pd.DataFrame(columns=["Nome", "Descrição", "Preço", "Imagem"])

st.subheader("📋 Catálogo Atual")
st.dataframe(df if not df.empty else pd.DataFrame([{"Status": "Nenhum produto cadastrado"}]))

# === 4️⃣ ADICIONAR PRODUTO ===
st.subheader("➕ Adicionar Novo Produto")

nome = st.text_input("Nome da Peça")
descricao = st.text_area("Descrição")
preco = st.text_input("Preço (ex: 199,90)")
imagem = st.text_input("Link da Imagem (Google Drive ou URL direta)")

if st.button("💾 Salvar Produto"):
    if nome and descricao and preco and imagem:
        novo = pd.DataFrame([[nome, descricao, preco, imagem]],
                            columns=["Nome", "Descrição", "Preço", "Imagem"])
        df = pd.concat([df, novo], ignore_index=True)
        buffer = io.StringIO()
        df.to_csv(buffer, index=False)

        try:
            if 'content' in locals():
                repo.update_file(content.path, "Atualiza catálogo via painel", buffer.getvalue(), content.sha)
            else:
                repo.create_file(csv_path, "Cria catálogo inicial", buffer.getvalue())
            st.success("✅ Produto salvo com sucesso no GitHub!")
        except Exception as e:
            st.error(f"❌ Erro ao salvar: {e}")
    else:
        st.warning("⚠️ Preencha todos os campos antes de salvar.")

# === 5️⃣ REMOVER PRODUTO ===
st.subheader("❌ Remover Produto")
if not df.empty:
    remover = st.selectbox("Selecione o produto para remover", df["Nome"])
    if st.button("Remover Produto"):
        df = df[df["Nome"] != remover]
        buffer = io.StringIO()
        df.to_csv(buffer, index=False)

        try:
            repo.update_file(content.path, f"Remove produto: {remover}", buffer.getvalue(), content.sha)
            st.success(f"✅ Produto '{remover}' removido com sucesso!")
        except Exception as e:
            st.error(f"❌ Erro ao remover produto: {e}")
else:
    st.info("Nenhum produto cadastrado para remover.")
