# Esquema do Banco de Dados - BarberTop

Este documento detalha as tabelas e atributos do banco de dados do projeto, organizado por **Django Apps**.

## 1. App: Users (`users`)

Responsável pelo gerenciamento de usuários e autenticação.

### Tabela: `CustomUser` (Estende `AbstractUser`)
*Representa os usuários do sistema, incluindo clientes e donos de barbearia.*

| Atributo | Tipo | Detalhes | Descrição |
| :--- | :--- | :--- | :--- |
| `id` | AutoField | PK | Identificador único. |
| `username` | CharField | Unique | Nome de usuário (herdado). |
| `password` | CharField | | Hash da senha (herdado). |
| `email` | EmailField | | Endereço de email (herdado). |
| `first_name` | CharField | | Primeiro nome (herdado). |
| `last_name` | CharField | | Sobrenome (herdado). |
| `role` | CharField | Choices: `CLIENT`, `OWNER` | Define se o usuário é cliente ou dono. Default: `CLIENT`. |
| `phone` | CharField | Max: 20 | Telefone de contato. |
| `cpf` | CharField | Max: 11, Unique | CPF do usuário. |
| `date_joined` | DateTime | | Data de cadastro (herdado). |
| `updatedAt` | DateTime | Auto Now | Data da última atualização do perfil. |

---

## 2. App: Barbershops (`barbershops`)

Responsável pelos dados das barbearias, serviços e funcionários.

### Tabela: `Address`
*Armazena endereços físicos das barbearias.*

| Atributo | Tipo | Detalhes | Descrição |
| :--- | :--- | :--- | :--- |
| `id` | AutoField | PK | Identificador único. |
| `city` | CharField | Max: 255 | Cidade. |
| `number` | IntegerField | | Número do endereço. |
| `neighbourhood` | CharField | Max: 255 | Bairro. |
| `state` | CharField | Max: 255 | Estado (UF). |
| `street` | CharField | Max: 255 | Rua/Logradouro. |

### Tabela: `Barbershop`
*Representa uma barbearia no sistema.*

| Atributo | Tipo | Detalhes | Descrição |
| :--- | :--- | :--- | :--- |
| `id` | AutoField | PK | Identificador único. |
| `owner` | OneToOne | FK -> `CustomUser` | Dono da barbearia. |
| `slug` | SlugField | Unique | Identificador amigável para URL. |
| `name` | CharField | Max: 255 | Nome da barbearia. |
| `description` | TextField | | Descrição detalhada. |
| `address` | OneToOne | FK -> `Address` | Endereço da barbearia. |
| `imageUrl` | TextField | | URL da imagem de capa/perfil. |
| `createdAt` | DateTime | Auto Now Add | Data de criação. |
| `updatedAt` | DateTime | Auto Now | Data de atualização. |

### Tabela: `Operation`
*Define os horários de funcionamento da barbearia.*

| Atributo | Tipo | Detalhes | Descrição |
| :--- | :--- | :--- | :--- |
| `id` | AutoField | PK | Identificador único. |
| `barbershop` | ForeignKey | FK -> `Barbershop` | Barbearia associada. |
| `weekDay` | SmallInt | 0-6 | Dia da semana (0=Seg, 6=Dom). |
| `timeInitial` | TimeField | | Horário de abertura. |
| `timeFinal` | TimeField | | Horário de fechamento. |

### Tabela: `Employee`
*Funcionários/Barbeiros que trabalham na barbearia.*

| Atributo | Tipo | Detalhes | Descrição |
| :--- | :--- | :--- | :--- |
| `id` | AutoField | PK | Identificador único. |
| `barbershop` | ForeignKey | FK -> `Barbershop` | Local de trabalho. |
| `name` | CharField | Max: 255 | Nome do funcionário. |
| `urlProfilePhoto` | URLField | | Foto do funcionário. |

### Tabela: `BarbershopService`
*Serviços oferecidos (corte, barba, etc).*

| Atributo | Tipo | Detalhes | Descrição |
| :--- | :--- | :--- | :--- |
| `id` | AutoField | PK | Identificador único. |
| `barbershop` | ForeignKey | FK -> `Barbershop` | Barbearia que oferece o serviço. |
| `name` | CharField | Max: 255 | Nome do serviço. |
| `description` | TextField | | Descrição do serviço. |
| `imageUrl` | URLField | | Imagem ilustrativa. |
| `price` | Decimal | 10,2 | Preço do serviço. |

### Tabela: `Rating`
*Avaliações dos clientes sobre as barbearias.*

| Atributo | Tipo | Detalhes | Descrição |
| :--- | :--- | :--- | :--- |
| `id` | AutoField | PK | Identificador único. |
| `barbershop` | ForeignKey | FK -> `Barbershop` | Barbearia avaliada. |
| `customer` | ForeignKey | FK -> `CustomUser` | Cliente que avaliou. |
| `ratingNumber` | IntegerField | | Nota (numérica). |
| `ratingDescription` | TextField | | Comentário da avaliação. |
| `createdAt` | DateTime | Auto Now Add | Data da avaliação. |

---

## 3. App: Bookings (`bookings`)

Responsável pelo agendamento de serviços.

### Tabela: `Booking`
*Registro de um agendamento.*

| Atributo | Tipo | Detalhes | Descrição |
| :--- | :--- | :--- | :--- |
| `id` | AutoField | PK | Identificador único. |
| `customer` | ForeignKey | FK -> `CustomUser` | Cliente que agendou. |
| `service` | ForeignKey | FK -> `BarbershopService` | Serviço escolhido. |
| `employee` | ForeignKey | FK -> `Employee` | Profissional escolhido. |
| `schedule` | DateTime | | Data e hora do agendamento. |
| `status` | CharField | Choices | `PENDENTE`, `CONFIRMADO`, `CANCELADO`, `CONCLUIDO`. |
| `createdAt` | DateTime | Auto Now Add | Data de criação do registro. |
| `updatedAt` | DateTime | Auto Now | Última atualização do status. |

---

# Por que o projeto é fragmentado em diferentes "Apps"?

A estrutura fragmentada em "Apps" (`users`, `barbershops`, `bookings`) é um padrão arquitetural fundamental e encorajado no **Django**. 

Aqui estão os principais motivos:

1.  **Separação de Responsabilidades (Separation of Concerns):**
    *   Cada app tem um propósito único e bem definido. 
    *   `users` cuida apenas de quem são as pessoas.
    *   `barbershops` cuida do catálogo (locais, serviços, empregados).
    *   `bookings` cuida da transação/processo de agendar.
    *   Isso evita "arquivos gigantes" (`god objects`) e mistura de lógicas não relacionadas.

2.  **Organização e Manutenibilidade:**
    *   É muito mais fácil encontrar e corrigir um bug relacionado a agendamentos indo direto na pasta `bookings` do que procurando em um arquivo `models.py` único com 5000 linhas.

3.  **Desacoplamento e Reusabilidade:**
    *   Teoricamente, se você quiser usar o sistema de usuários (`users`) em outro projeto, pode copiar a pasta do app com poucas modificações.
    *   As dependências são explícitas (via `ForeignKey`), o que ajuda a entender como as partes do sistema interagem.

4.  **Escalabilidade de Time:**
    *   Um desenvolvedor pode trabalhar nas regras de negócio de agendamento (`bookings`) enquanto outro refina o cadastro de barbearias (`barbershops`) com menor risco de conflitos de código (merge conflicts).

5.  **Convenção do Framework:**
    *   O Django é construído em torno desse conceito. Funcionalidades como *migrations*, *admin*, e *tests* são executadas ou organizadas por app, facilitando o ciclo de vida do desenvolvimento.
