// mapa de campos
const fieldMap = {
    username: "inputUsername",
    email: "inputEmail",
    telephone: "inputTelefone",
    password1: "inputSenha",
    password2: "inputConfirmSenha",
    shop_name: "inputNomeBarbearia",
    description: "inputDescricao",
    street: "inputRua",
    number: "inputNumero",
    neighbourhood: "inputBairro",
    city: "inputCidade",
    state: "inputEstado",
};

function clearErrors() {
    const globalAlert = document.getElementById("globalErrorAlert");
    if (globalAlert) globalAlert.style.setProperty("display", "none", "important");

    // Remove classes invalidas e textos de erro
    document.querySelectorAll(".form-control").forEach((input) => {
        input.classList.remove("is-invalid");
    });

    document.querySelectorAll(".invalid-feedback").forEach((el) => el.remove());
}

function showFieldErrors(errors) {
    for (const [fieldName, messages] of Object.entries(errors)) {
        // Descobre qual ID do HTML corresponde ao campo do Django
        const inputId = fieldMap[fieldName];

        if (inputId) {
            const input = document.getElementById(inputId);
            if (input) {
                input.classList.add("is-invalid");

                const errorDiv = document.createElement("div");
                errorDiv.className = "invalid-feedback";
                errorDiv.innerText = messages[0]; // Pega a primeira mensagem de erro

                // Insere no DOM logo após o input
                input.parentNode.insertBefore(errorDiv, input.nextSibling);
            }
        } else {
            // caso o erro seja de um campo não mapeado
            showGlobalError(`${fieldName}: ${messages[0]}`);
        }
    }
}

function showGlobalError(message) {
    const alertBox = document.getElementById("globalErrorAlert");
    const alertText = document.getElementById("globalErrorText");
    if (alertBox && alertText) {
        alertText.innerText = message;
        alertBox.style.display = "flex";
        // Rola a página para o topo para ver o erro
        window.scrollTo({ top: 0, behavior: "smooth" });
    } else {
        alert(message);
    }
}

async function finalizarCadastro() {
    const btnSubmit = document.getElementById("btnFinalizarCadastro");
    clearErrors();

    // validações básicas
    const senha = document.getElementById("inputSenha").value;
    const confirmSenha = document.getElementById("inputConfirmSenha").value;
    const nomeBarb = document.getElementById("inputNomeBarbearia").value;
    const username = document.getElementById("inputUsername").value;
    const telefone = document.getElementById("inputTelefone").value;

    if (!telefone) {
        showGlobalError("Preencha o telefone comercial.");
        return;
    }

    if (senha !== confirmSenha) {
        document.getElementById("inputSenha").classList.add("is-invalid");
        document.getElementById("inputConfirmSenha").classList.add("is-invalid");
        showGlobalError("As senhas não conferem!");
        return;
    }

    const totalServicos = document.querySelectorAll(".item-servico").length;
    if (totalServicos === 0) {
        showGlobalError("Você precisa cadastrar pelo menos um serviço (ex: Corte de Cabelo).");
        return;
    }

    const trabalhaSozinho = document.getElementById("trabalhoSozinho").checked;
    const totalFuncionarios = document.querySelectorAll(".item-funcionario").length;

    if (!trabalhaSozinho && totalFuncionarios === 0) {
        showGlobalError("Se você não trabalha sozinho, adicione os membros da sua equipe.");
        return;
    }

    // monta o formData
    const formData = new FormData();
    formData.append("username", username);
    formData.append("email", document.getElementById("inputEmail").value);
    formData.append("telephone", document.getElementById("inputTelefone").value);

    formData.append("password1", senha);
    formData.append("password2", confirmSenha);

    formData.append("shop_name", nomeBarb);
    formData.append("description", document.getElementById("inputDescricao").value);
    formData.append("street", document.getElementById("inputRua").value);
    formData.append("number", document.getElementById("inputNumero").value);
    formData.append("neighbourhood", document.getElementById("inputBairro").value);
    formData.append("city", document.getElementById("inputCidade").value);
    formData.append("state", document.getElementById("inputEstado").value);

    formData.append("work_alone", trabalhaSozinho ? "true" : "false");

    const fileInput = document.getElementById("inputImagemPerfil");
    if (fileInput.files[0]) {
        formData.append("profile_image", fileInput.files[0]);
    }

    // Listas
    let listaServicos = [];
    document.querySelectorAll(".item-servico").forEach((el) => {
        listaServicos.push({
            nome: el.dataset.nome,
            preco: el.dataset.preco,
            desc: el.dataset.desc,
        });
    });
    formData.append("services", JSON.stringify(listaServicos));

    let listaEquipe = [];
    if (!document.getElementById("trabalhoSozinho").checked) {
        document.querySelectorAll(".item-funcionario").forEach((el) => {
            listaEquipe.push({ nome: el.dataset.nome });
        });
    }
    formData.append("employees", JSON.stringify(listaEquipe));

    // 4. Fetch
    const URL = "/users/api/register-barbershop/";

    try {
        const originalText = btnSubmit.innerText;
        btnSubmit.innerText = "CADASTRANDO...";
        btnSubmit.disabled = true;

        // pega o Token CSRF
        let csrfToken = "";
        const tokenInput = document.querySelector("[name=csrfmiddlewaretoken]");
        if (tokenInput) csrfToken = tokenInput.value;

        const response = await fetch(URL, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken,
            },
            body: formData,
        });

        const data = await response.json();

        btnSubmit.innerText = originalText;
        btnSubmit.disabled = false;

        if (response.ok) {
            window.location.href = "/";
        } else {
            // ERRO DO DJANGO
            if (data.errors) {
                showFieldErrors(data.errors);
                showGlobalError("Verifique os campos destacados em vermelho.");
            } else {
                showGlobalError(data.message || "Ocorreu um erro desconhecido.");
            }
        }
    } catch (error) {
        console.error("Erro de rede:", error);
        showGlobalError("Erro de conexão com o servidor. Tente novamente.");
        btnSubmit.innerText = "FINALIZAR CADASTRO";
        btnSubmit.disabled = false;
    }
}
