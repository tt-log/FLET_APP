import flet as ft
import json
import os
#____________TARSIS TAA SANTOS BENTES___________________
ARQUIVO = "alunos.json"


def carregar_alunos():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    return []


def salvar_alunos(alunos):
    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(alunos, arquivo, ensure_ascii=False, indent=4)


def main(page: ft.Page):
    page.title = "Student Hub"
    page.bgcolor = "#F4F6FA"
    page.padding = 0

    alunos = carregar_alunos()
    aluno_editando = None

    # --------------------------------------------------
    # CAMPOS TARSIS
    # --------------------------------------------------

    nome = ft.TextField(
        label="Nome completo",
        hint_text="Digite o nome do aluno",
        border_radius=10,
        bgcolor="#FFFFFF",
        border_color="#D9DEE8",
        focused_border_color="#5B5BD6",
    )

    idade = ft.TextField(
        label="Idade",
        hint_text="Ex: 20",
        width=180,
        border_radius=10,
        bgcolor="#FFFFFF",
        border_color="#D9DEE8",
        focused_border_color="#5B5BD6",
    )

    curso = ft.TextField(
        label="Curso",
        hint_text="Digite o curso",
        expand=True,
        border_radius=10,
        bgcolor="#FFFFFF",
        border_color="#D9DEE8",
        focused_border_color="#5B5BD6",
    )

    pesquisa = ft.TextField(
        hint_text="Pesquisar aluno...",
        prefix_icon=ft.Icons.SEARCH,
        border_radius=10,
        bgcolor="#FFFFFF",
        border_color="#D9DEE8",
        expand=True,
    )

    lista = ft.Column(
        spacing=8,
        scroll=ft.ScrollMode.AUTO,
    )

    mensagem = ft.Text(
        "",
        size=13,
        weight=ft.FontWeight.W_500,
    )

    contador = ft.Text(
        f"{len(alunos)} alunos",
        size=13,
        color="#6B7280",
    )

    # --------------------------------------------------
    # FUNÇÕES TARSIS
    # --------------------------------------------------

    def mostrar_mensagem(texto, sucesso=True):
        mensagem.value = texto
        mensagem.color = "#238636" if sucesso else "#D92D20"
        page.update()

    def atualizar_contador():
        quantidade = len(alunos)

        if quantidade == 1:
            contador.value = "1 aluno"
        else:
            contador.value = f"{quantidade} alunos"

    def atualizar_lista(e=None):
        lista.controls.clear()

        texto_pesquisa = pesquisa.value.lower().strip()

        alunos_filtrados = [
            aluno
            for aluno in alunos
            if texto_pesquisa in aluno["nome"].lower()
            or texto_pesquisa in aluno["curso"].lower()
        ]

        if not alunos_filtrados:
            lista.controls.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(
                                ft.Icons.PEOPLE_OUTLINE,
                                size=45,
                                color="#9CA3AF",
                            ),
                            ft.Text(
                                "Nenhum aluno encontrado",
                                size=15,
                                color="#6B7280",
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=30,
                    alignment=ft.Alignment.CENTER,
                )
            )

        for aluno in alunos_filtrados:
            lista.controls.append(criar_linha(aluno))

        atualizar_contador()
        page.update()

    def criar_linha(aluno):
        return ft.Container(
            bgcolor="#FFFFFF",
            border_radius=10,
            padding=12,
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.Text(
                            f"{aluno['id']:02d}",
                            size=12,
                            weight=ft.FontWeight.BOLD,
                            color="#5B5BD6",
                        ),
                        width=42,
                        height=32,
                        bgcolor="#EEEEFF",
                        border_radius=8,
                        alignment=ft.Alignment.CENTER,
                    ),

                    ft.Column(
                        [
                            ft.Text(
                                aluno["nome"],
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                color="#20232A",
                            ),
                            ft.Text(
                                aluno["curso"],
                                size=12,
                                color="#737B8C",
                            ),
                        ],
                        spacing=2,
                        expand=True,
                    ),

                    ft.Container(
                        content=ft.Text(
                            f"{aluno['idade']} anos",
                            size=12,
                            color="#596273",
                        ),
                        width=70,
                    ),

                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.Icons.EDIT_OUTLINED,
                                tooltip="Editar aluno",
                                icon_color="#5B5BD6",
                                on_click=lambda e, a=aluno: editar(a),
                            ),

                            ft.IconButton(
                                icon=ft.Icons.DELETE_OUTLINE,
                                tooltip="Excluir aluno",
                                icon_color="#D92D20",
                                on_click=lambda e, a=aluno: confirmar_exclusao(a),
                            ),
                        ],
                        spacing=0,
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

    def limpar_campos():
        nome.value = ""
        idade.value = ""
        curso.value = ""

    def cadastrar(e):
        nonlocal aluno_editando

        if not nome.value.strip():
            mostrar_mensagem("Digite o nome do aluno.", False)
            return

        if not idade.value.strip():
            mostrar_mensagem("Digite a idade do aluno.", False)
            return

        if not curso.value.strip():
            mostrar_mensagem("Digite o curso do aluno.", False)
            return

        if aluno_editando is None:

            novo_id = 1

            if alunos:
                novo_id = max(aluno["id"] for aluno in alunos) + 1

            novo_aluno = {
                "id": novo_id,
                "nome": nome.value.strip(),
                "idade": idade.value.strip(),
                "curso": curso.value.strip(),
            }

            alunos.append(novo_aluno)

            mensagem.value = "Aluno cadastrado com sucesso!"
            mensagem.color = "#238636"

        else:

            aluno_editando["nome"] = nome.value.strip()
            aluno_editando["idade"] = idade.value.strip()
            aluno_editando["curso"] = curso.value.strip()

            aluno_editando = None

            botao_principal.text = "Adicionar aluno"
            botao_principal.icon = ft.Icons.ADD

            mensagem.value = "Aluno atualizado com sucesso!"
            mensagem.color = "#238636"

        salvar_alunos(alunos)
        limpar_campos()
        atualizar_lista()

    def editar(aluno):
        nonlocal aluno_editando

        aluno_editando = aluno

        nome.value = aluno["nome"]
        idade.value = aluno["idade"]
        curso.value = aluno["curso"]

        botao_principal.text = "Salvar alterações"
        botao_principal.icon = ft.Icons.SAVE_OUTLINED

        mostrar_mensagem(
            f"Editando o aluno {aluno['nome']}.",
            True,
        )

    def excluir(aluno):
        alunos.remove(aluno)

        salvar_alunos(alunos)

        dialog.open = False

        mostrar_mensagem(
            f"Aluno {aluno['nome']} excluído.",
            True,
        )

        atualizar_lista()

    def cancelar_edicao(e):
        nonlocal aluno_editando

        aluno_editando = None

        limpar_campos()

        botao_principal.text = "Adicionar aluno"
        botao_principal.icon = ft.Icons.ADD

        mensagem.value = ""

        page.update()

    def confirmar_exclusao(aluno):

        dialog.title = ft.Text("Excluir aluno?")

        dialog.content = ft.Text(
            f"Tem certeza que deseja excluir {aluno['nome']}?"
        )

        dialog.actions = [
            ft.TextButton(
                "Cancelar",
                on_click=lambda e: fechar_dialog(),
            ),
            ft.Button(
                "Excluir",
                icon=ft.Icons.DELETE_OUTLINE,
                on_click=lambda e: excluir(aluno),
            ),
        ]

        dialog.open = True

        page.update()

    def fechar_dialog():
        dialog.open = False
        page.update()

    # --------------------------------------------------
    # DIÁLOGO
    # --------------------------------------------------

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Excluir aluno?"),
        content=ft.Text("Essa ação não poderá ser desfeita."),
    )

    page.overlay.append(dialog)

    # --------------------------------------------------
    # BOTÕES
    # --------------------------------------------------

    botao_principal = ft.Button(
        "Adicionar aluno",
        icon=ft.Icons.ADD,
        on_click=cadastrar,
        height=45,
        bgcolor="#5B5BD6",
        color="#FFFFFF",
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
    )

    botao_cancelar = ft.TextButton(
        "Cancelar edição",
        icon=ft.Icons.CLOSE,
        on_click=cancelar_edicao,
    )

    pesquisa.on_change = atualizar_lista

    # --------------------------------------------------
    # CABEÇALHO
    # --------------------------------------------------

    cabecalho = ft.Container(
        bgcolor="#24243A",
        padding=ft.Padding.symmetric(horizontal=35, vertical=25),
        content=ft.Row(
            [
                ft.Container(
                    width=48,
                    height=48,
                    bgcolor="#5B5BD6",
                    border_radius=12,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Icon(
                        ft.Icons.SCHOOL_OUTLINED,
                        color="#FFFFFF",
                        size=27,
                    ),
                ),

                ft.Column(
                    [
                        ft.Text(
                            "Student Hub",
                            size=23,
                            weight=ft.FontWeight.BOLD,
                            color="#FFFFFF",
                        ),
                        ft.Text(
                            "Gerenciamento de alunos",
                            size=12,
                            color="#B8BAC8",
                        ),
                    ],
                    spacing=2,
                    expand=True,
                ),

                ft.Container(
                    bgcolor="#33334D",
                    border_radius=20,
                    padding=ft.Padding.symmetric(
                        horizontal=15,
                        vertical=8,
                    ),
                    content=contador,
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )

    # --------------------------------------------------
    # FORMULÁRIO
    # --------------------------------------------------

    formulario = ft.Container(
        bgcolor="#FFFFFF",
        border_radius=14,
        padding=25,
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text(
                                    "Novo aluno",
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                    color="#20232A",
                                ),
                                ft.Text(
                                    "Preencha os dados abaixo",
                                    size=12,
                                    color="#7A8291",
                                ),
                            ],
                            expand=True,
                        ),

                        mensagem,
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),

                ft.Divider(
                    height=20,
                    color="#ECEEF2",
                ),

                nome,

                ft.Row(
                    [
                        idade,
                        curso,
                    ],
                    spacing=15,
                ),

                ft.Row(
                    [
                        botao_principal,
                        botao_cancelar,
                    ],
                    spacing=10,
                ),
            ],
            spacing=15,
        ),
    )

    # --------------------------------------------------
    # LISTA
    # --------------------------------------------------

    painel_lista = ft.Container(
        bgcolor="#FFFFFF",
        border_radius=14,
        padding=25,
        expand=True,
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text(
                                    "Alunos cadastrados",
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                    color="#20232A",
                                ),
                                ft.Text(
                                    "Consulte e gerencie os alunos",
                                    size=12,
                                    color="#7A8291",
                                ),
                            ],
                            expand=True,
                        ),

                        pesquisa,
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),

                ft.Divider(
                    height=20,
                    color="#ECEEF2",
                ),

                lista,
            ],
            expand=True,
        ),
    )

    # --------------------------------------------------
    # PÁGINA
    # --------------------------------------------------

    page.add(
        cabecalho,

        ft.Container(
            padding=ft.Padding.only(
                left=35,
                right=35,
                top=25,
                bottom=25,
            ),
            expand=True,
            content=ft.Column(
                [
                    formulario,
                    painel_lista,
                ],
                spacing=20,
                expand=True,
            ),
        ),
    )

    atualizar_lista()


ft.run(main)