function switchTab(type) {
    // Esconde todos
    document.getElementById("client-area").classList.remove("active");
    document.getElementById("barbershop-area").classList.remove("active");

    // Tira cor das abas
    const tabs = document.querySelectorAll(".tab");
    tabs.forEach((t) => t.classList.remove("active"));

    // Ativa o correto
    if (type === "client") {
        document.getElementById("client-area").classList.add("active");
        tabs[0].classList.add("active");
    } else {
        document.getElementById("barbershop-area").classList.add("active");
        tabs[1].classList.add("active");
    }
}
