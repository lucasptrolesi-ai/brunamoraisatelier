document.addEventListener("DOMContentLoaded", async () => {
  // 🔗 Novo backend publicado (Sheets)
  const url =
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vQO0ciGyUyPSAuWnR5L39zInL8lqS2BLZPVquCNqWnYZYUF2wSzm6X6CQ7hf4zPKQ/pub?output=csv";

  try {
    const resposta = await fetch(url);
    const texto = await resposta.text();
    const linhas = texto.split("\n").map(l => l.trim()).filter(Boolean);
    const container = document.getElementById("lista-produtos");
    container.innerHTML = "";

    // Ignora o cabeçalho (começa da linha 2)
    for (let i = 1; i < linhas.length; i++) {
      const linha = linhas[i];
      const partes = linha.split(",");

      // Garante que há 4 colunas
      if (partes.length >= 4) {
        const [nome, descricao, preco, imagem] = partes.map(x => x.trim());

        // Só cria produto se houver dados reais
        if (nome && descricao && preco && imagem) {
          const produto = document.createElement("div");
          produto.className = "produto";
          produto.innerHTML = `
            <img src="${imagem}" alt="${nome}">
            <h3>${nome}</h3>
            <p>${descricao}</p>
            <div class="preco">R$ ${preco}</div>
          `;
          container.appendChild(produto);
        }
      }
    }

    if (container.innerHTML.trim() === "") {
      container.innerHTML = "<p>Nenhum produto cadastrado no momento.</p>";
    }
  } catch (erro) {
    console.error("Erro ao carregar produtos:", erro);
    document.getElementById("lista-produtos").innerHTML =
      "<p>Erro ao carregar catálogo.</p>";
  }
});
