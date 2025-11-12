document.addEventListener("DOMContentLoaded", async () => {
  // 🔗 Planilha publicada (backend oficial)
  const url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQO0ciGyUyPSAuWnR5L39zInL8lqS2BLZPVquCNqWnYZYUF2wSzm6X6CQ7hf4zPKQ/pub?output=csv";

  try {
    const resposta = await fetch(url);
    const texto = await resposta.text();
    const linhas = texto.split("\n").map(l => l.trim()).filter(Boolean);
    const container = document.getElementById("lista-produtos");
    container.innerHTML = "";

    // Ignora cabeçalho
    for (let i = 1; i < linhas.length; i++) {
      const partes = linhas[i].split(",").map(x => x.trim());
      if (partes.length >= 4) {
        let [nome, descricao, preco, imagem] = partes;

        // 🪄 Corrige automaticamente link do Google Drive
        if (imagem.includes("drive.google.com/file/d/")) {
          const id = imagem.split("/d/")[1]?.split("/")[0];
          imagem = `https://drive.google.com/uc?export=view&id=${id}`;
        }

        // Garante que todos os campos estejam preenchidos
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

    // Caso a planilha esteja vazia
    if (container.innerHTML.trim() === "") {
      container.innerHTML = "<p>Nenhum produto cadastrado no momento.</p>";
    }
  } catch (erro) {
    console.error("Erro ao carregar produtos:", erro);
    document.getElementById("lista-produtos").innerHTML =
      "<p>Erro ao carregar catálogo.</p>";
  }
});
