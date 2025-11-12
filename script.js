// URL do CSV publicado da aba "Catalogo"
const CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQO0ciGyUyPSAuWnR5L39zInL8lqS2BLZPVquCNqWnYZYUF2wSzm6X6CQ7hf4zPKQ/pub?gid=1833522644&single=true&output=csv";

// Corrige link do Google Drive para visualização direta
function driveView(url) {
  if (!url) return "";
  if (url.includes("drive.google.com/file/d/")) {
    const id = url.split("/d/")[1]?.split("/")[0];
    return `https://drive.google.com/uc?export=view&id=${id}`;
  }
  return url;
}

// Normaliza e formata preço (aceita com vírgula ou ponto)
function formataPreco(valor) {
  if (!valor) return "";
  const v = String(valor).replace(/[^\d,\.]/g, "").replace(",", ".");
  const n = Number(v);
  if (isNaN(n)) return valor;
  return n.toFixed(2).replace(".", ",");
}

// Renderização dos cards
function renderProdutos(rows, container) {
  container.innerHTML = "";
  rows.forEach((row) => {
    const nome = (row["Nome"] || "").trim();
    const desc = (row["Descrição"] || "").trim();
    const preco = formataPreco(row["Preço"]);
    const imgRaw = (row["Imagem"] || "").trim();
    const img = driveView(imgRaw);

    if (!nome) return;

    const card = document.createElement("div");
    card.className = "produto";
    card.innerHTML = `
      <img src="${img}" alt="${nome}" onerror="this.src='https://placehold.co/600x400?text=Imagem+indisponível'">
      <h3>${nome}</h3>
      <p>${desc}</p>
      <div class="preco">R$ ${preco}</div>
    `;
    container.appendChild(card);
  });

  if (!container.children.length) {
    container.innerHTML = "<p>Nenhum produto cadastrado no momento.</p>";
  }
}

// Carrega + aplica filtros e ordenação
async function carregarCatalogo() {
  const container = document.getElementById("lista-produtos");
  if (!container) return;

  container.innerHTML = "<p>Carregando produtos…</p>";
  try {
    const resp = await fetch(`${CSV_URL}&_t=${Date.now()}`, { cache: "no-cache" });
    if (!resp.ok) throw new Error("Falha ao baixar CSV");
    const csvText = await resp.text();

    const parsed = Papa.parse(csvText, { header: true, skipEmptyLines: true });
    let rows = parsed.data; // [{Nome, Descrição, Preço, Imagem}, ...]

    // busca
    const busca = document.getElementById("busca")?.value?.toLowerCase() || "";
    if (busca) {
      rows = rows.filter((r) => {
        const n = (r["Nome"] || "").toLowerCase();
        const d = (r["Descrição"] || "").toLowerCase();
        return n.includes(busca) || d.includes(busca);
      });
    }

    // ordenação
    const ordem = document.getElementById("ordem")?.value || "";
    const num = (v) => Number(String(v || "").replace(/[^\d,\.]/g, "").replace(",", "."));
    if (ordem === "nome-asc") rows.sort((a,b)=> (a["Nome"]||"").localeCompare(b["Nome"]||""));
    if (ordem === "nome-desc") rows.sort((a,b)=> (b["Nome"]||"").localeCompare(a["Nome"]||""));
    if (ordem === "preco-asc") rows.sort((a,b)=> num(a["Preço"])-num(b["Preço"]));
    if (ordem === "preco-desc") rows.sort((a,b)=> num(b["Preço"])-num(a["Preço"]));

    renderProdutos(rows, container);
  } catch (err) {
    console.error(err);
    container.innerHTML = "<p>Erro ao carregar catálogo.</p>";
  }
}

// eventos
document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("busca")?.addEventListener("input", carregarCatalogo);
  document.getElementById("ordem")?.addEventListener("change", carregarCatalogo);
  document.getElementById("btn-recarregar")?.addEventListener("click", carregarCatalogo);
  carregarCatalogo();
});
