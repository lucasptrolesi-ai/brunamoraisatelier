import os, zipfile, textwrap

# === Criação das pastas ===
os.makedirs("brunamoraisatelier/imagens", exist_ok=True)
os.makedirs("brunamoraisatelier/produtos", exist_ok=True)

# === index.html ===
index_html = """<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Bruna Morais Peixoto Atelier</title>
  <link rel="stylesheet" href="style.css">
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;700&display=swap" rel="stylesheet">
</head>
<body>

  <header class="banner">
    <img src="imagens/banner.jpg" alt="Bruna Morais Peixoto Atelier">
    <div class="banner-text">
      <h1>Bruna Morais Peixoto</h1>
      <p>Ateliê de Joias Finas e Exclusivas</p>
    </div>
  </header>

  <section class="catalogo">
    <h2>Catálogo</h2>
    <div class="produtos">
      <div class="produto">
        <img src="produtos/anel1.jpg" alt="Anel Luxo">
        <h3>Anel Luxo Rosé</h3>
        <p>Design elegante em banho de ouro rosé.</p>
        <span class="preco">R$ 289,00</span>
      </div>
      <div class="produto">
        <img src="produtos/brinco1.jpg" alt="Brinco Elegância">
        <h3>Brinco Elegância</h3>
        <p>Brinco folheado com zircônias brancas.</p>
        <span class="preco">R$ 199,00</span>
      </div>
      <div class="produto">
        <img src="produtos/colar1.jpg" alt="Colar Brilho">
        <h3>Colar Brilho Dourado</h3>
        <p>Peça sofisticada, perfeita para eventos especiais.</p>
        <span class="preco">R$ 259,00</span>
      </div>
    </div>
  </section>

  <section class="contato">
    <h2>Entre em Contato</h2>
    <p>Atendimento personalizado com Bruna Morais.</p>
    <a href="https://wa.me/5535984595425" target="_blank" class="whatsapp-btn">💬 Falar no WhatsApp</a>
  </section>

  <footer>
    <p>© 2025 Bruna Morais Peixoto Atelier | Desenvolvido por Lucas Peixoto</p>
  </footer>

  <script src="script.js"></script>
</body>
</html>"""

# === style.css ===
style_css = """body {
  margin: 0;
  font-family: 'Cormorant Garamond', serif;
  background-color: #fdfbf9;
  color: #4b3832;
}
.banner {position: relative;text-align: center;}
.banner img {width: 100%;height: auto;filter: brightness(0.85);}
.banner-text {position: absolute;top: 50%;left: 50%;transform: translate(-50%, -50%);color: #b88a60;text-shadow: 1px 1px 4px rgba(0,0,0,0.2);}
.banner-text h1 {font-size: 3rem;margin: 0;}
.banner-text p {font-size: 1.3rem;}
.catalogo {text-align: center;padding: 50px 10%;}
.catalogo h2 {color: #b88a60;font-size: 2rem;margin-bottom: 30px;}
.produtos {display: flex;justify-content: center;flex-wrap: wrap;gap: 30px;}
.produto {background: #fff;border: 1px solid #f1e3d3;border-radius: 10px;padding: 15px;width: 280px;transition: all 0.3s ease;}
.produto:hover {transform: scale(1.03);box-shadow: 0 6px 20px rgba(0,0,0,0.1);}
.produto img {width: 100%;border-radius: 10px;}
.produto h3 {margin-top: 10px;color: #4b3832;}
.produto p {font-size: 1rem;color: #5c5048;}
.preco {color: #b88a60;font-weight: bold;font-size: 1.2rem;}
.contato {background-color: #f6f1ee;padding: 60px 10%;text-align: center;}
.contato h2 {color: #b88a60;font-size: 2rem;}
.whatsapp-btn {display: inline-block;margin-top: 20px;padding: 15px 25px;background-color: #b88a60;color: #fff;border-radius: 30px;text-decoration: none;font-size: 1.2rem;transition: 0.3s;}
.whatsapp-btn:hover {background-color: #8c6b4f;}
footer {background-color: #b88a60;color: #fff;text-align: center;padding: 15px;font-size: 1rem;}
"""

# === script.js ===
script_js = """document.addEventListener("DOMContentLoaded", function() {
  const whatsappBtn = document.querySelector(".whatsapp-btn");
  if (whatsappBtn) {
    whatsappBtn.addEventListener("click", () => {
      console.log("Redirecionando para WhatsApp...");
    });
  }
});"""

# === Criação dos arquivos ===
arquivos = {"index.html": index_html, "style.css": style_css, "script.js": script_js}

for nome, conteudo in arquivos.items():
    with open(f"brunamoraisatelier/{nome}", "w", encoding="utf-8") as f:
        f.write(conteudo)

# === Geração do ZIP ===
with zipfile.ZipFile("brunamoraisatelier.zip", "w") as zipf:
    for pasta, _, arquivos in os.walk("brunamoraisatelier"):
        for arquivo in arquivos:
            zipf.write(os.path.join(pasta, arquivo))

print("✅ brunamoraisatelier.zip gerado com sucesso!")
