let employeesList = [];

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

function renderEmployees() {
    const lista = document.getElementById("listaFuncionarios");
    lista.innerHTML = "";
    
    if (employeesList.length === 0) {
        document.getElementById("avisoFuncionarioVazio").style.display = "block";
        return;
    }
    
    document.getElementById("avisoFuncionarioVazio").style.display = "none";

    employeesList.forEach((emp, index) => {
        const novoFuncionarioHTML = `
            <div class="item-funcionario d-flex justify-content-between align-items-center p-3 rounded-3" 
                 style="background-color: #27272a;">
                <div class="d-flex gap-3 align-items-center">
                    <div class="d-flex align-items-center justify-content-center rounded-circle bg-dark text-secondary overflow-hidden" style="width: 40px; height: 40px;">
                        ${ emp.file ? `<img src="${URL.createObjectURL(emp.file)}" style="width: 100%; height: 100%; object-fit: cover;">` : `<i class="bi bi-person-circle" style="font-size: 1.5rem;"></i>` }
                    </div>
                    <div>
                        <h6 class="mb-0 fw-bold text-white">${emp.name}</h6>
                        <small class="text-muted">${emp.file ? 'Com foto' : 'Sem foto'}</small>
                    </div>
                </div>
                <button class="btn btn-sm text-danger" onclick="removerFuncionario(${index})"><i class="bi bi-trash"></i></button>
            </div>`;
        lista.insertAdjacentHTML("beforeend", novoFuncionarioHTML);
    });
}

function salvarFuncionario() {
    const nome = document.getElementById("nomeFuncionario").value;
    const fileInput = document.getElementById("fotoFuncionario");
    
    if (nome === "") {
        alert("Digite o nome!");
        return;
    }

    const file = fileInput.files.length > 0 ? fileInput.files[0] : null;
    
    employeesList.push({
        name: nome,
        file: file
    });

    renderEmployees();
    bootstrap.Modal.getInstance(document.getElementById("modalFuncionario")).hide();
    document.getElementById("formFuncionario").reset();
}

function removerFuncionario(index) {
    employeesList.splice(index, 1);
    renderEmployees();
}
