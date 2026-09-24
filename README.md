# FLET_APP - Student Hub

Aplicativo desenvolvido em **Python utilizando Flet**, com o objetivo de demonstrar as operações básicas de um sistema CRUD.

## Sobre o projeto

O **Student Hub** é um aplicativo simples para cadastro e gerenciamento de alunos.

O sistema permite:

* Cadastrar alunos
* Visualizar alunos cadastrados
* Editar informações
* Excluir alunos
* Pesquisar alunos
* Salvar os dados em um arquivo JSON

## Tecnologias utilizadas

* Python
* Flet
* JSON
* Visual Studio Code
* GitHub

## Operações CRUD

O projeto utiliza as quatro operações básicas de um CRUD:

| Operação | Função                           |
| -------- | -------------------------------- |
| Create   | Cadastrar um novo aluno          |
| Read     | Visualizar os alunos cadastrados |
| Update   | Alterar os dados de um aluno     |
| Delete   | Excluir um aluno                 |

## Informações cadastradas

Para cada aluno, o sistema armazena:

* Nome completo
* Idade
* Curso

Os dados são armazenados no arquivo `alunos.json`, permitindo que sejam recuperados quando o aplicativo for executado novamente.

## Como executar

### 1. Instalar o Python

É necessário ter o Python instalado no computador.

### 2. Instalar o Flet

No terminal, execute:

```bash
pip install flet
```

### 3. Executar o aplicativo

Dentro da pasta do projeto, execute:

```bash
flet run main.py
```

Também é possível executar no navegador:

```bash
flet run --web main.py
```

## Estrutura do projeto

```text
FLET_APP/
│
├── main.py
├── alunos.json
└── README.md
```

## Fontes de pesquisa

* Documentação oficial do Flet
* Documentação oficial do Python
* Documentação do JSON no Python

## Autor

Projeto desenvolvido individualmente para atividade acadêmica.

**Tarsis Taã**
