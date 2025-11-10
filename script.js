document.addEventListener("DOMContentLoaded", async () => {
  // 🔗 Novo backend (Google Sheets publicado)
  const url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQO0ciGyUyPSAuWnR5L39zInL8lqS2BLZPVquCNqWnYZYUF2wSzm6X6CQ7hf4zPKQ/pub?output=csv";

  try {
    const resposta = await fetch(url);
    const texto = await resposta.text();
    const linhas = texto.split("\n").slice(1); // pula cabeçalho
    const container = document.getElementById("lista-produtos");
    container.innerHTML = "";

    linhas.forEach(linha => {
      const [nome, descricao, preco, imagem] = linha.split(",");

      if (nome && descricao && preco && imagem) {
        const produto = document.createElement("div");
        produto.className = "produto";
        produto.innerHTML = `
          <img src="${imagem.trim()}" alt="${nome.trim()}">
          <h3>${nome.trim()}</h3>
          <p>${descricao.trim()}</p>
          <div class="preco">R$ ${preco.trim()}</div>
        `;
        container.appendChild(produto);
      }
    });

    if (container.innerHTML.trim() === "") {
      container.innerHTML = "<p>Nenhum produto cadastrado no momento.</p>";
    }
  } catch (erro) {
    console.error("Erro ao carregar produtos:", erro);
    document.getElementById("lista-produtos").innerHTML =
      "<p>Erro ao carregar catálogo.</p>";
  }
});
