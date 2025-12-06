# BarberTop

Sistema web de agendamento e gestão para barbearias, desenvolvido com Django.

## 🎯 Objetivos do Projeto

O objetivo principal é conectar clientes a barbearias locais, oferecendo uma plataforma unificada para:

-   **Clientes:** Encontrar barbearias, visualizar serviços/preços, agendar horários, avaliar atendimentos e gerenciar seu histórico.
-   **Barbearias:** Gerenciar agenda, cadastrar equipe, serviços, horários de funcionamento e visualizar métricas de desempenho (dashboard).

## 👥 Integrantes

-   Emerson Neves Santos
-   Harisson Caio Da Silva Xavier

## 📹 Vídeo de Demonstração

Assista à apresentação das funcionalidades do projeto no link abaixo:
**https://youtu.be/8nEWo7pjCCE?si=48Qr8PcdMyS-hsCc**

## 🚀 Como rodar localmente

### Opção 1: Via Docker (Recomendado)

A maneira mais simples de rodar o projeto, já com banco de dados configurado.

**Pré-requisitos:**

-   Docker e Docker Compose instalados.

**Passo a passo:**

1. **Clone o repositório**

    ```bash
    git clone https://github.com/seu-usuario/barbertop-django.git
    cd barbertop-django
    ```

2. **Suba os containers**

    ```bash
    docker-compose up --build
    ```

3. **Aplique as migrações (Em outro terminal)**

    ```bash
    # Identifique o container web ou use o comando via compose
    docker-compose exec web python manage.py migrate
    ```

4. **Crie um superusuário (Opcional)**
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

O projeto estará acessível em: `http://localhost:8000/`

---

### Opção 2: Instalação Manual (Python/Virtualenv)

Caso prefira rodar sem Docker.

**Pré-requisitos:**

-   Python 3.10+
-   Git
-   PostgreSQL (ou configurar para usar SQLite no settings.py)

**Passo a passo:**

1. **Crie e ative o ambiente virtual**

    ```bash
    # Linux/Mac
    python3 -m venv .venv
    source .venv/bin/activate

    # Windows
    python -m venv .venv
    .venv\Scripts\activate
    ```

2. **Instale as dependências**

    ```bash
    pip install -r requirements.txt
    ```

3. **Configure o Banco de Dados**
   Certifique-se de que as variáveis de ambiente do DB estejam configuradas ou ajuste o `settings.py`.

4. **Execute as migrações e inicie**
    ```bash
    python manage.py migrate
    python manage.py runserver
    ```
