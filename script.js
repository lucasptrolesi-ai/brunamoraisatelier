document.addEventListener("DOMContentLoaded", async () => {
  // 🔗 Link público da planilha publicada como CSV
  const url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR0V8f4lpv2pefKoPOdk3TEe4-X1QZE0OoMF45mgTaFTHo94uCkq2wPd3mje66pfmWm8Zsod8UQxkH-/pub?output=csv";

  try {
    const resposta = await fetch(url);
    const texto = await resposta.text();
    const linhas = texto.split("\n").slice(1); // Pula cabeçalho
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
