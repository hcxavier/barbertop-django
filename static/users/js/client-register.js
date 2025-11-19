document.addEventListener("DOMContentLoaded", function () {
    // Seleciona os dois inputs
    const passwordInput = document.getElementById("id_password1");
    const confirmInput = document.getElementById("id_password2");

    // Seleciona o elemento da lista "As senhas conferem"
    const matchReq = document.getElementById("req-match");
    const matchIcon = matchReq.querySelector("i");

    // Mapeamento dos requisitos de REGEX (Senha 1)
    const requirements = {
        length: { regex: /.{8,}/, element: document.getElementById("req-length") },
        number: { regex: /\d/, element: document.getElementById("req-number") },
        upper: { regex: /[A-Z]/, element: document.getElementById("req-upper") },
    };

    // Função que valida a força da Senha 1
    function validateStrength() {
        const val = passwordInput.value;
        for (const key in requirements) {
            const req = requirements[key];
            const icon = req.element.querySelector("i");

            if (req.regex.test(val)) {
                req.element.classList.remove("text-muted", "text-danger");
                req.element.classList.add("text-success");
                icon.classList.remove("bi-circle", "bi-x-circle");
                icon.classList.add("bi-check-circle-fill");
            } else {
                req.element.classList.remove("text-success");
                req.element.classList.add(val.length > 0 ? "text-danger" : "text-muted");
                icon.classList.remove("bi-check-circle-fill", "bi-circle");
                icon.classList.add(val.length > 0 ? "bi-x-circle" : "bi-circle");
            }
        }
    }

    // Função que valida se as duas são iguais
    function validateMatch() {
        const val1 = passwordInput.value;
        const val2 = confirmInput.value;

        // Se o campo de confirmação estiver vazio, fica cinza (neutro)
        if (val2.length === 0) {
            matchReq.className = "text-muted mt-2 pt-2 border-top border-secondary";
            matchIcon.className = "bi bi-circle me-1";
            return;
        }

        // Compara as duas
        if (val1 === val2) {
            // IGUAIS (Verde)
            matchReq.className = "text-success mt-2 pt-2 border-top border-secondary";
            matchIcon.className = "bi bi-check-circle-fill me-1";
        } else {
            // DIFERENTES (Vermelho)
            matchReq.className = "text-danger mt-2 pt-2 border-top border-secondary";
            matchIcon.className = "bi bi-x-circle me-1";
        }
    }

    // Adiciona os "ouvintes" (Listeners)

    // Quando digita na Senha 1: Valida força E verifica se bate com a Senha 2
    passwordInput.addEventListener("input", function () {
        validateStrength();
        validateMatch();
    });

    // Quando digita na Senha 2: Só precisa verificar se bate
    confirmInput.addEventListener("input", validateMatch);
});
