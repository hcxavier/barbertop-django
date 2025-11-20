function toggleFuncionarioBtn() {
    const chk = document.getElementById("trabalhoSozinho");
    const btn = document.getElementById("btnAddFuncionario");
    const lista = document.getElementById("listaFuncionarios");

    if (chk.checked) {
        btn.disabled = true;
        btn.classList.add("opacity-50");
        if (lista) lista.style.display = "none";
    } else {
        btn.disabled = false;
        btn.classList.remove("opacity-50");
        if (lista) lista.style.display = "flex";
    }
}

function previewImagem(event) {
    const input = event.target;
    const placeholder = document.getElementById("uploadPlaceholder");
    const preview = document.getElementById("imagePreview");

    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function (e) {
            preview.src = e.target.result;
            placeholder.style.display = "none";
            preview.style.display = "block";
        };
        reader.readAsDataURL(input.files[0]);
    } else {
        preview.src = "";
        preview.style.display = "none";
        placeholder.style.display = "block";
    }
}

// --- Lógica de Modais (Mantida) ---

function salvarServico() {
    const nome = document.getElementById("nomeServico").value;
    const preco = document.getElementById("precoServico").value;
    const desc = document.getElementById("descServico").value;

    if (nome === "" || preco === "") {
        alert("Preencha nome e preço!");
        return;
    }

    document.getElementById("avisoListaVazia").style.display = "none";

    const novoItemHTML = `
                <div class="item-servico d-flex justify-content-between align-items-center p-3 rounded-3" 
                     style="background-color: #27272a;"
                     data-nome="${nome}" data-preco="${preco}" data-desc="${desc}">
                    <div class="d-flex gap-3 align-items-center">
                        <div class="d-flex align-items-center justify-content-center rounded bg-dark" style="width: 40px; height: 40px;">
                            <i class="bi bi-scissors text-white"></i>
                        </div>
                        <div>
                            <h6 class="mb-0 fw-bold text-white">${nome}</h6>
                            <small class="text-muted">R$ ${parseFloat(preco).toFixed(2)}</small>
                        </div>
                    </div>
                    <button class="btn btn-sm text-danger" onclick="removerItem(this)"><i class="bi bi-trash"></i></button>
                </div>`;

    document.getElementById("listaServicos").insertAdjacentHTML("beforeend", novoItemHTML);
    bootstrap.Modal.getInstance(document.getElementById("modalServico")).hide();
    document.getElementById("formServico").reset();
}

function removerItem(botao) {
    botao.closest(".d-flex.justify-content-between").remove();
    if (document.getElementById("listaServicos").children.length === 0) {
        document.getElementById("avisoListaVazia").style.display = "block";
    }
}

function salvarFuncionario() {
    const nome = document.getElementById("nomeFuncionario").value;
    if (nome === "") {
        alert("Digite o nome!");
        return;
    }

    document.getElementById("avisoFuncionarioVazio").style.display = "none";

    const novoFuncionarioHTML = `
                <div class="item-funcionario d-flex justify-content-between align-items-center p-3 rounded-3" 
                     style="background-color: #27272a;" data-nome="${nome}">
                    <div class="d-flex gap-3 align-items-center">
                        <div class="d-flex align-items-center justify-content-center rounded-circle bg-dark text-secondary" style="width: 40px; height: 40px; font-size: 1.5rem;">
                            <i class="bi bi-person-circle"></i>
                        </div>
                        <div>
                            <h6 class="mb-0 fw-bold text-white">${nome}</h6>
                            <small class="text-muted">Profissional</small>
                        </div>
                    </div>
                    <button class="btn btn-sm text-danger" onclick="removerFuncionario(this)"><i class="bi bi-trash"></i></button>
                </div>`;

    document.getElementById("listaFuncionarios").insertAdjacentHTML("beforeend", novoFuncionarioHTML);
    bootstrap.Modal.getInstance(document.getElementById("modalFuncionario")).hide();
    document.getElementById("formFuncionario").reset();
}

function removerFuncionario(botao) {
    botao.closest(".d-flex").remove();
}
