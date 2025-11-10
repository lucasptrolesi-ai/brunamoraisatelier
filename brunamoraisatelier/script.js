document.addEventListener("DOMContentLoaded", function() {
  const whatsappBtn = document.querySelector(".whatsapp-btn");
  if (whatsappBtn) {
    whatsappBtn.addEventListener("click", () => {
      console.log("Redirecionando para WhatsApp...");
    });
  }
});