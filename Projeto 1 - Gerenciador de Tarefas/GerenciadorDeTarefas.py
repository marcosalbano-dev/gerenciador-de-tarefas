# Importa o módulo tkinter com o alias 'tk'.
# Tkinter é uma biblioteca de interface gráfica padrão do Python,
# usada para criar janelas e outros elementos gráficos.
import tkinter as tk
from os import times

# Importa módulos específicos do tkinter:
# - ttk é um conjunto de widgets que fornece uma aparência mais
# moderna e temática para os elementos da interface gráfica.
# - messagebox é um módulo utilizado para abrir janelas de
# mensagem, como alertas e confirmações.
from tkinter import ttk, messagebox

# Importa a classe MongoClient do módulo pymongo.
# MongoClient é usado para estabelecer uma conexão com o banco de
# dados MongoDB, permitindo operações como ler e escrever dados.
from pymongo import MongoClient

# Importa a classe ObjectId do módulo bson.
# ObjectId é um identificador único utilizado pelo MongoDB para documentos.
# É frequentemente usado para buscar ou referenciar documentos específicos.
from bson.objectid import ObjectId

# Importa o módulo datetime para trabalhar com datas.
from datetime import datetime, time

# Importa o DateEntry do tkcalendar para seleção de datas.
# Se o tkcalendar não estiver instalado, será necessário instalá-lo com: pip install tkcalendar
try:
    from tkcalendar import DateEntry
except ImportError:
    # Se tkcalendar não estiver disponível, usaremos Entry com validação
    DateEntry = None

# Importa módulos para geração de PDF.
# Se o reportlab não estiver instalado, será necessário instalá-lo com: pip install reportlab
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.units import inch
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

# Importa filedialog para selecionar onde salvar o PDF
from tkinter import filedialog


# Define a classe GerenciadorTarefasApp que será responsável pela
# lógica e interface gráfica do aplicativo.
class GerenciadorTarefasApp:

    # Método construtor com o parâmetro 'janela', que é a janela
    # principal do aplicativo.
    def __init__(self, janela):

        # Atribui a janela passada como argumento à variável de instância 'self.janela',
        # armazenando uma referência à janela principal.
        self.janela = janela

        # Define o título da janela principal do aplicativo.
        self.janela.title("Gerenciador de Tarefas")

        # Configura as dimensões da janela principal, definindo sua
        # largura como 950 pixels e altura como 700 pixels.
        self.janela.geometry("950x700")

        # Define a cor de fundo da janela principal usando o valor
        # hexadecimal #f0f0f0, que é um tom claro de cinza.
        self.janela.configure(bg="#f0f0f0")  # Cor de fundo

        # Conexão com o MongoDB
        # Cria uma instância do MongoClient para conectar ao
        # servidor MongoDB local na porta padrão 27017.
        self.cliente = MongoClient("mongodb://localhost:27017/")

        # Acessa o banco de dados chamado 'gerenciador_tarefas_db'. Se o banco de
        # dados não existir, ele será criado automaticamente ao
        # inserir os primeiros dados.
        self.bd = self.cliente["gerenciador_tarefas_db"]

        # Acessa a coleção 'tarefas' dentro do banco de dados. Coleções no
        # MongoDB são equivalentes a tabelas em bancos de dados relacionais.
        self.colecao = self.bd["tarefas"]

        # Acessa a coleção 'tecnicos' dentro do banco de dados.
        # Esta coleção armazena os técnicos disponíveis para atribuição às tarefas.
        self.colecao_tecnicos = self.bd["tecnicos"]

        # Criação de estilo para o Treeview
        # Cria uma instância de Style do módulo ttk para customizar a
        # aparência dos widgets ttk.
        estilo = ttk.Style()

        # Define o tema de estilo como 'default'. Esse é o tema padrão do
        # ttk que será base para as customizações.
        estilo.theme_use('default')

        # Configura o estilo para o widget Treeview. Define o fundo das
        # linhas como branco, o texto como preto,
        # a altura das linhas como 25 pixels, o fundo dos
        # campos como branco e a fonte como Arial tamanho 11.
        estilo.configure("Treeview",
                         background="#ffffff",  # Cor de fundo das linhas.
                         foreground="black",  # Cor do texto das linhas.
                         rowheight=25,  # Altura de cada linha do Treeview.
                         fieldbackground="#ffffff",  # Cor de fundo dos campos do Treeview.
                         font=("Arial", 11))  # Tipo e tamanho da fonte.

        # Configura o estilo para o cabeçalho das colunas do Treeview.
        # Define a fonte como Arial tamanho 12 em negrito.
        # Essa configuração é aplicada aos cabeçalhos das colunas do Treeview,
        # fornecendo um estilo visual distinto e de fácil leitura.
        estilo.configure("Treeview.Heading",
                         font=("Arial", 12, "bold"))  # Fonte para o cabeçalho das colunas.

        # Configurações adicionais para o estilo do Treeview ao
        # selecionar uma linha.
        # Define o fundo da linha selecionada como preto e o texto
        # como branco para melhorar a visibilidade da seleção.
        estilo.map("Treeview",

                   # Cor de fundo para linhas selecionadas.
                   background=[("selected", "black")],

                   # Cor do texto para linhas selecionadas.
                   foreground=[("selected", "white")])

        # Criação de um quadro para os campos de entrada de dados no aplicativo.
        # Um quadro é um container que organiza e agrupa widgets
        # dentro da janela principal.
        quadro_entrada = tk.Frame(self.janela,
                                  bg="#f0f0f0")

        # Empacota o quadro dentro da janela principal.
        # pady e padx adicionam um espaçamento vertical e horizontal
        # ao redor do quadro.
        # fill='x' faz com que o quadro se expanda horizontalmente para
        # preencher o espaço disponível.
        quadro_entrada.pack(pady=10,
                            padx=10,
                            fill='x')

        # Criação de um rótulo (label) para o campo "Título da Tarefa".
        # Um rótulo é um widget que exibe texto na interface gráfica.
        rotulo_titulo = tk.Label(quadro_entrada,
                                 text="Título da Tarefa:",
                                 font=("Arial", 12),
                                 bg="#f0f0f0")

        # Posiciona o rótulo no quadro de entrada usando o gerenciador de layout grid.
        # - row=0 e column=0 posicionam o rótulo na primeira linha e primeira coluna do grid.
        # - sticky='e' alinha o rótulo à direita (east) dentro da célula grid.
        # - padx e pady adicionam um espaçamento externo de 5 pixels em
        # todas as direções para separar visualmente os elementos.
        rotulo_titulo.grid(row=0,
                           column=0,
                           sticky='e',
                           padx=5,
                           pady=5)

        # Criação de um campo de entrada (Entry) para digitar o título da tarefa.
        # Entry é um widget que permite ao usuário inserir uma linha de texto.
        self.entrada_titulo = tk.Entry(quadro_entrada,
                                       width=55,
                                       font=("Arial", 11))

        # Posiciona o campo de entrada no quadro usando o gerenciador de layout grid.
        # - row=0 e column=1 posicionam o campo na primeira linha e segunda coluna do grid.
        # - columnspan=3 faz com que o campo de entrada se estenda por três
                # colunas do grid, para utilizar melhor o espaço disponível.
        # - sticky='w' alinha o campo de entrada à esquerda (west) dentro da célula grid.
        # - padx e pady adicionam um espaçamento externo para estética e
                # para evitar a aglomeração de widgets.
        self.entrada_titulo.grid(row=0,
                                 column=1,
                                 columnspan=3,
                                 sticky='w',
                                 pady=5,
                                 padx=5)

        # Criação de um rótulo (label) para o campo "Descrição da Tarefa".
        # Este rótulo serve como um indicativo visual para o usuário sobre o
                # que deve ser inserido no campo associado.
        rotulo_descricao = tk.Label(quadro_entrada,
                                    text="Descrição da Tarefa:",
                                    font=("Arial", 12),
                                    bg="#f0f0f0")

        # Posiciona o rótulo no quadro de entrada usando o gerenciador de layout grid.
        # - row=1 coloca o rótulo na segunda linha do grid.
        # - column=0 coloca o rótulo na primeira coluna.
        # - sticky='ne' alinha o rótulo ao canto superior direito da célula grid (norte-leste),
                #   o que é útil para manter o alinhamento visual com o rótulo do título acima.
        # - padx e pady definem o espaçamento externo de 5 pixels, ajudando a
                # evitar um layout apertado e melhorando a legibilidade.
        rotulo_descricao.grid(row=1,
                              column=0,
                              sticky='ne',
                              padx=5,
                              pady=5)

        # Criação de um widget de texto (Text) para a entrada da descrição da tarefa.
        # O widget Text permite a inserção de múltiplas linhas de texto,
                # diferente do Entry que é limitado a uma única linha.
        self.texto_descricao = tk.Text(quadro_entrada,
                                       width=53,
                                       height=5,
                                       font=("Arial", 11))

        # Posiciona o widget de texto no grid do quadro de entrada.
        # - row=1 indica que está na segunda linha, alinhado com o
                # rótulo da descrição.
        # - column=1 inicia o widget na segunda coluna.
        # - columnspan=3 faz com que o widget de texto ocupe três colunas,
                # proporcionando espaço suficiente para a entrada de texto extenso.
        # - sticky='w' alinha o widget à esquerda da célula grid, mantendo a
                # consistência com o campo de entrada do título.
        # - pady e padx adicionam espaçamento externo para assegurar que o
                # widget não fique muito próximo dos outros elementos.
        self.texto_descricao.grid(row=1,
                                  column=1,
                                  columnspan=3,
                                  sticky='w',
                                  pady=5,
                                  padx=5)


        # Criação de um rótulo para o campo "Status da Tarefa".
        # Este rótulo serve para indicar ao usuário onde
        # selecionar o status da tarefa no formulário.
        rotulo_status = tk.Label(quadro_entrada,
                                 text="Status:",
                                 font=("Arial", 12),
                                 bg="#f0f0f0")

        # Posiciona o rótulo para o status no quadro de entrada
                # usando o gerenciador de layout grid.
        # - row=2 posiciona o rótulo na terceira linha, garantindo que esteja
                # abaixo dos campos de título e descrição.
        # - column=0 posiciona o rótulo na primeira coluna.
        # - sticky='e' alinha o rótulo à direita dentro de sua célula grid,
                # ajudando na organização e alinhamento visual com outros rótulos.
        # - padx e pady adicionam um espaçamento externo de 5 pixels
                # para evitar que os elementos fiquem muito juntos e
                # melhorar a estética.
        rotulo_status.grid(row=2,
                           column=0,
                           sticky='e',
                           padx=5,
                           pady=5)

        # Criação de uma variável de string tkinter que irá armazenar o
        # valor do status escolhido pelo usuário.
        self.var_status = tk.StringVar()

        # Criação de um ComboBox para permitir ao usuário selecionar um
        # status para a tarefa.
        # Um ComboBox é um widget que combina uma caixa de listagem com uma
        # caixa de entrada, permitindo seleções dentro de um conjunto definido.
        self.combo_status = ttk.Combobox(quadro_entrada,

                                         textvariable=self.var_status,

                                         # Opções disponíveis para seleção.
                                         values=["Pendente", "Concluída"],

                                         # Configura o ComboBox para ser somente leitura, impedindo a entrada de texto não listado.
                                         state='readonly',

                                         # Define a fonte para Arial tamanho 11.
                                         font=("Arial", 11))

        # Posiciona o ComboBox no quadro de entrada usando o grid.
        # - row=2 indica que está na mesma linha do rótulo correspondente.
        # - column=1 indica que está na segunda coluna,
        # diretamente ao lado do rótulo.
        # - sticky não é especificado aqui, o que permite que o
        # ComboBox alinhe-se ao padrão, que é centralizar na célula.
        # - pady e padx mantêm a consistência no espaçamento com
        # outros elementos de entrada.
        self.combo_status.grid(row=2,
                               column=1,
                               pady=5,
                               padx=5)

        # Define o índice inicial do ComboBox 'combo_status' como 0.
        # Isso seleciona automaticamente o primeiro item da lista de
        # opções, que é "Pendente", quando a interface é inicializada.
        # Este passo é crucial para garantir que um status padrão esteja
        # sempre selecionado, evitando erros de usuário ao esquecer
        # de selecionar um status.
        self.combo_status.current(0)

        # Criação de um rótulo para o campo "Data da Criação".
        # Este rótulo serve para indicar ao usuário onde
        # deve ser inserida ou selecionada a data de criação da tarefa.
        rotulo_data = tk.Label(quadro_entrada,
                               text="Data da Criação:",
                               font=("Arial", 12),
                               bg="#f0f0f0")

        # Posiciona o rótulo da data no quadro de entrada usando o grid.
        # - row=3 indica que está na terceira linha, abaixo do campo de status.
        # - column=0 posiciona o rótulo na primeira coluna.
        # - sticky='e' alinha o rótulo à direita dentro de sua célula grid.
        # - padx e pady adicionam um espaçamento externo de 5 pixels.
        rotulo_data.grid(row=3,
                        column=0,
                        sticky='e',
                        padx=5,
                        pady=5)

        # Criação de um campo de seleção de data.
        # Se o tkcalendar estiver disponível, usa DateEntry.
        # Caso contrário, usa um Entry comum com validação.
        if DateEntry:
            # Usa DateEntry do tkcalendar para uma seleção de data mais amigável.
            # DateEntry fornece um calendário popup para seleção de datas.
            self.entrada_data = DateEntry(quadro_entrada,
                                          width=12,
                                          background='darkblue',
                                          foreground='white',
                                          borderwidth=2,
                                          date_pattern='dd/mm/yyyy',
                                          font=("Arial", 11))
        else:
            # Se tkcalendar não estiver disponível, usa Entry comum.
            # O usuário precisará digitar a data no formato DD/MM/YYYY.
            self.entrada_data = tk.Entry(quadro_entrada,
                                        width=15,
                                        font=("Arial", 11))
            # Define a data atual como padrão
            data_atual = datetime.now().strftime("%d/%m/%Y")
            self.entrada_data.insert(0, data_atual)

        # Posiciona o campo de data no quadro usando o grid.
        # - row=3 indica que está na mesma linha do rótulo correspondente.
        # - column=1 indica que está na segunda coluna.
        # - sticky='w' alinha o campo à esquerda.
        # - pady e padx mantêm a consistência no espaçamento.
        self.entrada_data.grid(row=3,
                              column=1,
                              sticky='w',
                              pady=5,
                              padx=5)

        # Criação de um rótulo para o campo "Técnico Responsável".
        # Este rótulo serve para indicar ao usuário onde
        # deve ser selecionado o técnico responsável pela tarefa.
        rotulo_tecnico = tk.Label(quadro_entrada,
                                  text="Técnico Responsável:",
                                  font=("Arial", 12),
                                  bg="#f0f0f0")

        # Posiciona o rótulo do técnico no quadro de entrada usando o grid.
        # - row=4 indica que está na quarta linha, abaixo do campo de data.
        # - column=0 posiciona o rótulo na primeira coluna.
        # - sticky='e' alinha o rótulo à direita dentro de sua célula grid.
        # - padx e pady adicionam um espaçamento externo de 5 pixels.
        rotulo_tecnico.grid(row=4,
                           column=0,
                           sticky='e',
                           padx=5,
                           pady=5)

        # Cria uma variável de string tkinter que irá armazenar o
        # nome do técnico selecionado.
        self.var_tecnico = tk.StringVar()

        # Criação de um ComboBox para permitir ao usuário selecionar um
        # técnico responsável pela tarefa.
        self.combo_tecnico = ttk.Combobox(quadro_entrada,
                                          textvariable=self.var_tecnico,
                                          state='readonly',
                                          font=("Arial", 11),
                                          width=52)

        # Carrega a lista de técnicos do banco de dados.
        self.carregar_tecnicos()

        # Posiciona o ComboBox no quadro de entrada usando o grid.
        # - row=4 indica que está na mesma linha do rótulo correspondente.
        # - column=1 indica que está na segunda coluna.
        # - sticky='w' alinha o campo à esquerda.
        # - pady e padx mantêm a consistência no espaçamento.
        self.combo_tecnico.grid(row=4,
                               column=1,
                               sticky='w',
                               pady=5,
                               padx=5)

        # Cria um botão para cadastrar novos técnicos.
        # Este botão abre uma janela para adicionar novos técnicos à lista.
        botao_cadastrar_tecnico = tk.Button(quadro_entrada,
                                           text="+",
                                           command=self.cadastrar_tecnico,
                                           bg="#81c784",
                                           font=("Arial", 10, "bold"),
                                           width=3)

        # Posiciona o botão ao lado do ComboBox de técnico.
        botao_cadastrar_tecnico.grid(row=4,
                                    column=2,
                                    sticky='w',
                                    pady=5,
                                    padx=5)


        # Criação de um quadro (Frame) que irá conter os botões de ações principais
        # do aplicativo: Adicionar, Atualizar e Excluir.
        # Este quadro atua como um container para manter os botões agrupados e
        # organizados, facilitando a gestão do layout e da estética.
        # - bg="#f0f0f0" define a cor de fundo do quadro com um tom de
        # cinza claro (#f0f0f0). Esta cor é um cinza muito suave, quase branco,
        #   que ajuda a criar uma interface visualmente leve e não intrusiva.
        # A escolha dessa cor visa a manter a interface amigável e fácil de usar,
        #   evitando cansaço visual em longos períodos de uso e mantendo a
        # harmonia visual com o design geral do aplicativo.
        quadro_botoes = tk.Frame(self.janela,
                                 bg="#f0f0f0")

        # Empacota o quadro 'quadro_botoes' na janela principal.
        # A função pack é usada aqui para a inserção automática do quadro
        # na janela, posicionando-o de acordo com as necessidades de layout.
        # - pady=10 adiciona um espaçamento vertical de 10 pixels acima e
        # abaixo do quadro, separando-o visualmente dos outros
        # componentes da interface, como o quadro de entrada.
        # Este espaçamento é essencial para não só manter uma boa separação
        # visual mas também para garantir que os elementos não
        # fiquem visualmente congestionados.
        quadro_botoes.pack(pady=10)

        # Cria o botão "Adicionar Tarefa" no quadro de botões. Este botão será
        # usado pelo usuário para adicionar novas tarefas ao sistema.
        botao_adicionar = tk.Button(quadro_botoes,

                                    # Texto exibido no botão.
                                    text="Adicionar Tarefa",

                                    # Função a ser executada quando o botão é clicado. Aqui, ele
                                    # chama o método 'adicionar_tarefa'.
                                    command=self.adicionar_tarefa,

                                    # Define a cor de fundo do botão como verde claro (#a5d6a7), que é
                                    # visualmente associado à adição ou criação.
                                    bg="#a5d6a7",

                                    # Configura a fonte do texto no botão como Arial, tamanho 11 e em
                                    # negrito, para destaque.
                                    font=("Arial", 11, "bold"),

                                    # Define a largura do botão para garantir que todos os botões tenham o
                                    # mesmo tamanho e alinhamento.
                                    width=18)

        # Posiciona o botão 'Adicionar Tarefa' dentro do quadro usando o gerenciador grid.
        # Configura a posição do botão na primeira coluna e primeira linha, com
        # espaçamentos de 10 pixels horizontalmente e 5 pixels verticalmente.
        botao_adicionar.grid(row=0, column=0, padx=10, pady=5)

        # Cria o botão "Atualizar Tarefa", semelhante ao botão de adicionar, mas
        # utilizado para atualizar as informações de tarefas existentes.
        botao_atualizar = tk.Button(quadro_botoes,

                                    # Texto no botão.
                                    text="Atualizar Tarefa",

                                    # Método chamado ao clicar no botão, que executa a atualização
                                    # da tarefa selecionada.
                                    command=self.atualizar_tarefa,

                                    # Cor de fundo amarelo claro (#fff59d), sugerindo
                                    # modificação ou continuidade.
                                    bg="#fff59d",

                                    # Mesmo estilo de fonte do botão anterior para consistência visual.
                                    font=("Arial", 11, "bold"),

                                    # Largura consistente com os outros botões.
                                    width=18)

        # Posiciona o botão 'Atualizar Tarefa' ao lado do botão 'Adicionar Tarefa'.
        # Na mesma linha do botão adicionar, na segunda coluna, com o mesmo espaçamento.
        botao_atualizar.grid(row=0, column=1, padx=10, pady=5)

        # Cria o botão "Excluir Tarefa", que permite ao usuário remover uma tarefa existente.
        botao_excluir = tk.Button(quadro_botoes,

                                  # Texto no botão.
                                  text="Excluir Tarefa",

                                  # Método chamado ao clicar no botão, que executa a
                                  # exclusão da tarefa selecionada.
                                  command=self.excluir_tarefa,

                                  # Cor de fundo vermelho claro (#ef9a9a), geralmente associada à
                                  # ação de deletar ou remover.
                                  bg="#ef9a9a",

                                  # Mantém o mesmo estilo de fonte para uniformidade.
                                  font=("Arial", 11, "bold"),

                                  # Mesma largura para alinhamento e aparência consistente.
                                  width=18)

        # Posiciona o botão 'Excluir Tarefa' ao lado do botão 'Atualizar Tarefa'.
        # Colocado na terceira coluna da mesma linha, com espaçamento
        # igual aos outros botões.
        botao_excluir.grid(row=0, column=2, padx=10, pady=5)

        # Cria o botão "Gerar Relatório PDF", que permite ao usuário gerar
        # um relatório em PDF com todas as tarefas ou filtrado por técnico.
        botao_gerar_pdf = tk.Button(quadro_botoes,

                                    # Texto no botão.
                                    text="Gerar Relatório PDF",

                                    # Método chamado ao clicar no botão, que abre uma janela
                                    # para escolher o tipo de relatório (geral ou por técnico).
                                    command=self.selecionar_tipo_relatorio,

                                    # Cor de fundo azul claro (#90caf9), geralmente associada à
                                    # ação de exportar ou gerar documentos.
                                    bg="#90caf9",

                                    # Mantém o mesmo estilo de fonte para uniformidade.
                                    font=("Arial", 11, "bold"),

                                    # Mesma largura para alinhamento e aparência consistente.
                                    width=18)

        # Posiciona o botão 'Gerar Relatório PDF' ao lado do botão 'Excluir Tarefa'.
        # Colocado na quarta coluna da mesma linha, com espaçamento
        # igual aos outros botões.
        botao_gerar_pdf.grid(row=0, column=3, padx=10, pady=5)

        # Criação de um quadro para agrupar os elementos de filtro de
        # status na janela principal.
        # Este quadro serve para organizar visualmente os controles
        # relacionados ao filtro, mantendo a interface limpa e ordenada.
        quadro_filtro = tk.Frame(self.janela,

                                 # Define a cor de fundo do quadro. O código de cor "#f0f0f0" é um
                                 # cinza muito claro.
                                 bg="#f0f0f0")

        # Posiciona o quadro 'quadro_filtro' na janela principal.
        # O método 'pack' é usado para inserir o quadro na janela. Ele organiza os
        # widgets em blocos antes de colocá-los na janela.
        # 'pady=10' adiciona um espaçamento vertical de 10 pixels
        # acima e abaixo do quadro.
        quadro_filtro.pack(pady=10)

        # Criação de um rótulo dentro do quadro 'quadro_filtro' que serve como indicação
        # para o usuário sobre a funcionalidade do campo associado.
        rotulo_filtro = tk.Label(quadro_filtro,

                                 # Texto exibido no rótulo, claramente informando o propósito do
                                 # filtro adjacentemente configurado.
                                 text="Filtrar por Status:",

                                 # Define o estilo da fonte como Arial tamanho 12, garantindo que o
                                 # texto seja legível e esteticamente agradável.
                                 font=("Arial", 12),

                                 # A cor de fundo do rótulo é a mesma do quadro para manter a
                                 # consistência visual.
                                 bg="#f0f0f0")

        # Posicionamento do rótulo 'rotulo_filtro' dentro do quadro usando o método 'grid'.
        # O 'grid' permite um posicionamento mais preciso dos widgets em
        # uma matriz de linhas e colunas.
        # Posicionado na primeira linha e primeira coluna do grid.
        # 'padx=5' adiciona um espaçamento horizontal de 5 pixels
        # ao lado do rótulo,
        # ajudando a separar visualmente o rótulo de outros widgets
        # ou bordas do quadro.
        rotulo_filtro.grid(row=0, column=0, padx=5)

        # Criação de uma variável StringVar para armazenar e gerenciar o
        # status selecionado no ComboBox.
        # StringVar é um tipo de variável do tkinter que facilita a
        # manipulação de valores de strings em widgets, como
        # atualizações e leituras.
        self.var_filtro = tk.StringVar()

        # Criação do ComboBox para filtrar as tarefas por status.
        # Combobox é um widget que combina uma caixa de entrada de texto com
        # uma lista suspensa de opções permitindo seleções.
        # Define que o ComboBox será posicionado dentro do 'quadro_filtro'.
        self.combo_filtro = ttk.Combobox(quadro_filtro,

                                         # Vincula a variável StringVar ao valor atualmente selecionado no ComboBox.
                                         textvariable=self.var_filtro,

                                         # Define as opções disponíveis para seleção.
                                         values=["Todos", "Pendente", "Concluída"],

                                         # Configura o ComboBox para ser apenas de leitura, impedindo a
                                         # entrada de texto pelo usuário.
                                         state='readonly',

                                         # Define a fonte do texto no ComboBox para Arial tamanho 11,
                                         # mantendo a consistência estética.
                                         font=("Arial", 11))

        # Define a opção padrão que será selecionada quando a interface for carregada.
        # 'current(0)' seleciona automaticamente o primeiro item da
        # lista de valores do ComboBox, que é "Todos".
        self.combo_filtro.current(0)

        # Posicionamento do ComboBox no quadro usando o gerenciador de layout grid.
        # Este método coloca o ComboBox em uma grade para organização com outros widgets.
        # Posiciona o ComboBox na primeira linha e segunda coluna do grid.
        self.combo_filtro.grid(row=0,
                               column=1,

                               # 'padx=5' adiciona um espaçamento horizontal de 5 pixels, garantindo um
                               # espaço adequado entre o ComboBox e outros elementos ou bordas.
                               padx=5)

        # Criação do botão "Aplicar Filtro" no quadro de filtros.
        # Este botão é usado para aplicar o filtro de status selecionado no
        # ComboBox, atualizando a lista de tarefas exibida.
        # Define que o botão será posicionado dentro do 'quadro_filtro'.
        botao_filtro = tk.Button(quadro_filtro,

                                 # Texto exibido no botão, informando claramente sua função.
                                 text="Aplicar Filtro",

                                 # Método vinculado ao botão, que é chamado quando o botão é clicado.
                                 command=self.aplicar_filtro,

                                 # Define a cor de fundo do botão como um azul claro (#81d4fa),
                                 # que é visualmente tranquilo e amigável.
                                 bg="#81d4fa",

                                 # Define a fonte do texto no botão para Arial tamanho 11 em
                                 # negrito, para destacar.
                                 font=("Arial", 11, "bold"),

                                 # Define a largura do botão para manter a uniformidade
                                 # com outros elementos.
                                 width=15)

        # Posicionamento do botão 'botao_filtro' dentro do quadro usando o
        # gerenciador de layout grid.
        # Posiciona o botão na primeira linha e terceira coluna do grid.
        botao_filtro.grid(row=0, column=2,

                          # 'padx=5' adiciona um espaçamento horizontal de 5 pixels,
                          # garantindo espaço adequado ao redor do botão.
                          padx=5)

        # Criação de um quadro para conter o Treeview, que é usado para listar as tarefas.
        # Este quadro serve como um container para organizar visualmente a lista de
        # tarefas dentro da interface gráfica.
        # Define que o quadro será posicionado dentro da janela principal.
        quadro_arvore = tk.Frame(self.janela,

                                 # Define a cor de fundo do quadro como cinza claro (#f0f0f0),
                                 # mantendo a consistência visual com o restante da interface.
                                 bg="#f0f0f0")

        # Posicionamento do 'quadro_arvore' na janela principal usando o método 'pack'.
        # O método 'pack' é frequentemente usado para inserção de quadros pois
        # permite um alinhamento e dimensionamento eficientes.
        # 'pady=20' adiciona um espaçamento vertical de 20 pixels
        # acima e abaixo do quadro,
        quadro_arvore.pack(pady=20,

                           # 'fill='both'' faz com que o quadro se expanda tanto na horizontal
                           # quanto na vertical, preenchendo o espaço disponível.
                           fill='both',

                           # 'expand=True' permite que o quadro expanda para preencher qualquer
                           # espaço extra na janela, garantindo que o Treeview utilize
                           # todo o espaço disponível.
                           expand=True)

        # Criação de uma barra de rolagem para ser usada com o Treeview.
        # A barra de rolagem permite ao usuário navegar verticalmente pela
        # lista de tarefas quando esta excede o limite de altura do quadro.
        # Posiciona a barra de rolagem dentro do 'quadro_arvore'.
        barra_rolagem = tk.Scrollbar(quadro_arvore,

                                     # Configura a orientação da barra de rolagem como vertical.
                                     orient='vertical')

        # Posicionamento da barra de rolagem usando o método 'pack'.
        # Posiciona a barra de rolagem no lado direito do quadro.
        barra_rolagem.pack(side=tk.RIGHT,

                           # A opção 'fill=tk.Y' faz com que a barra de rolagem expanda ao
                           # longo do eixo Y (vertical), cobrindo toda a altura do quadro.
                           fill=tk.Y)

        # Localiza o Treeview dentro do quadro designado para a árvore de tarefas.
        # Define as colunas que o Treeview deve ter.
        # Garante que apenas os cabeçalhos das colunas sejam mostrados,
        # omitindo a coluna de ícones à esquerda.
        # Define a altura do Treeview, permitindo mostrar 15 linhas
        # antes de necessitar rolagem.
        self.arvore_tarefas = ttk.Treeview(quadro_arvore,
                                           columns=("Título", "Descrição", "Status", "Data da Criação", "Técnico"),
                                           show="headings",
                                           height=15,
                                           yscrollcommand=barra_rolagem.set)

        # Configura o cabeçalho da coluna "Título" no Treeview para exibir "Título".
        self.arvore_tarefas.heading("Título", text="Título")

        # Configura o cabeçalho da coluna "Descrição" no Treeview para exibir "Descrição".
        self.arvore_tarefas.heading("Descrição", text="Descrição")

        # Configura o cabeçalho da coluna "Status" no Treeview para exibir "Status".
        self.arvore_tarefas.heading("Status", text="Status")

        # Configura o cabeçalho da coluna "Data da Criação" no Treeview para exibir "Data da Criação".
        self.arvore_tarefas.heading("Data da Criação", text="Data da Criação")

        # Configura o cabeçalho da coluna "Técnico" no Treeview para exibir "Técnico".
        self.arvore_tarefas.heading("Técnico", text="Técnico")

        # Configura a largura da coluna "Título" no Treeview.
        # A largura é definida como 180 pixels para garantir que o
        # conteúdo da coluna "Título" seja exibido adequadamente,
        # mesmo que o texto seja um pouco longo, mantendo uma
        # aparência equilibrada na interface.
        self.arvore_tarefas.column("Título", width=180)

        # Configura a largura da coluna "Descrição" no Treeview.
        # A largura é ajustada para 350 pixels, sendo a maior entre as
        # colunas, pois a descrição das tarefas geralmente contém mais texto.
        # Isso assegura que a maior parte do conteúdo fique visível sem
        # necessidade de rolagem horizontal.
        self.arvore_tarefas.column("Descrição", width=350)

        # Configura a largura da coluna "Status" no Treeview.
        # A largura é definida como 90 pixels, pois o conteúdo esperado nesta
        # coluna é curto, geralmente "Pendente" ou "Concluída".
        # Isso ajuda a otimizar o espaço ocupado pelo Treeview na interface.
        self.arvore_tarefas.column("Status", width=90)

        # Configura a largura da coluna "Data da Criação" no Treeview.
        # A largura é definida como 120 pixels para exibir a data no formato DD/MM/YYYY.
        # Isso garante que a data seja exibida completamente sem cortes.
        self.arvore_tarefas.column("Data da Criação", width=120)

        # Configura a largura da coluna "Técnico" no Treeview.
        # A largura é definida como 150 pixels para exibir o nome do técnico.
        # Isso garante que o nome do técnico seja exibido completamente.
        self.arvore_tarefas.column("Técnico", width=150)

        # Vincula o evento "TreeviewSelect" ao método 'ao_selecionar_tarefa'.
        # O evento "TreeviewSelect" é disparado quando o usuário
        # seleciona uma linha no Treeview.
        # O método 'ao_selecionar_tarefa' será chamado automaticamente
        # para tratar a seleção, carregando os dados da tarefa
        # selecionada nos campos de entrada.
        self.arvore_tarefas.bind("<<TreeviewSelect>>", self.ao_selecionar_tarefa)

        # Posiciona o Treeview na interface gráfica usando o método 'pack'.
        # - pady=10 adiciona um espaçamento vertical de 10 pixels acima e abaixo do Treeview.
        # - padx=10 adiciona um espaçamento horizontal de 10 pixels em ambos os lados.
        # - fill='both' faz com que o Treeview se expanda horizontal e
        # verticalmente para preencher todo o espaço disponível no quadro.
        # - expand=True permite que o Treeview aumente de tamanho
        # proporcionalmente ao redimensionamento da janela.
        self.arvore_tarefas.pack(pady=10,
                                 padx=10,
                                 fill='both',
                                 expand=True)

        # Configura a barra de rolagem para sincronizar com o Treeview.
        # O método 'config' associa o comando de rolagem vertical da
        # barra de rolagem à função 'yview' do Treeview.
        # Isso permite que a barra de rolagem controle a navegação pelas
        # linhas do Treeview quando o conteúdo excede a altura disponível.
        barra_rolagem.config(command=self.arvore_tarefas.yview)

        # Inicializa a variável 'id_tarefa_selecionada' com o valor None.
        # Esta variável é usada para armazenar o identificador único (ID)
        # da tarefa atualmente selecionada no Treeview.
        # Ao inicializar como None, garantimos que nenhuma tarefa esteja
        # selecionada ao iniciar o aplicativo.
        self.id_tarefa_selecionada = None

        # Chama o método 'carregar_tarefas' para carregar as tarefas do banco
        # de dados ou outra fonte de dados ao iniciar a aplicação.
        # Este método é responsável por preencher o Treeview com as tarefas
        # disponíveis, garantindo que a interface comece funcional e populada.
        self.carregar_tarefas()

    # Define o método 'carregar_tecnicos', que carrega a lista de técnicos
    # do banco de dados e atualiza o ComboBox de técnicos.
    def carregar_tecnicos(self):

        """
        Este método carrega os técnicos cadastrados no MongoDB e
        atualiza o ComboBox de técnicos com a lista disponível.
        """

        try:
            # Busca todos os técnicos do banco de dados MongoDB.
            tecnicos = self.colecao_tecnicos.find().sort("nome", 1)

            # Cria uma lista com os nomes dos técnicos.
            lista_tecnicos = [tecnico["nome"] for tecnico in tecnicos]

            # Adiciona uma opção vazia no início da lista.
            lista_tecnicos.insert(0, "")

            # Atualiza os valores do ComboBox com a lista de técnicos.
            self.combo_tecnico['values'] = lista_tecnicos

        except Exception as e:
            # Em caso de erro, define uma lista vazia.
            self.combo_tecnico['values'] = [""]

    # Define o método 'cadastrar_tecnico', que abre uma janela para
    # cadastrar um novo técnico no banco de dados.
    def cadastrar_tecnico(self):

        """
        Este método abre uma janela de diálogo para cadastrar um novo técnico.
        O técnico será salvo no banco de dados MongoDB e adicionado à lista
        de técnicos disponíveis no ComboBox.
        """

        # Cria uma janela top-level (popup) para cadastrar técnico.
        janela_tecnico = tk.Toplevel(self.janela)
        janela_tecnico.title("Cadastrar Técnico")
        janela_tecnico.geometry("400x150")
        janela_tecnico.configure(bg="#f0f0f0")
        janela_tecnico.transient(self.janela)  # Mantém a janela acima da principal
        janela_tecnico.grab_set()  # Torna a janela modal

        # Cria um rótulo para o campo de nome do técnico.
        rotulo_nome = tk.Label(janela_tecnico,
                              text="Nome do Técnico:",
                              font=("Arial", 12),
                              bg="#f0f0f0")
        rotulo_nome.grid(row=0, column=0, padx=10, pady=20, sticky='e')

        # Cria um campo de entrada para o nome do técnico.
        entrada_nome = tk.Entry(janela_tecnico,
                               width=30,
                               font=("Arial", 11))
        entrada_nome.grid(row=0, column=1, padx=10, pady=20)
        entrada_nome.focus()  # Define o foco no campo de entrada

        # Função interna para salvar o técnico.
        def salvar_tecnico():
            nome_tecnico = entrada_nome.get().strip()

            # Valida se o nome foi preenchido.
            if not nome_tecnico:
                messagebox.showwarning("Aviso", "O nome do técnico não pode estar vazio.")
                return

            # Verifica se o técnico já existe.
            tecnico_existente = self.colecao_tecnicos.find_one({"nome": nome_tecnico})
            if tecnico_existente:
                messagebox.showwarning("Aviso", "Este técnico já está cadastrado.")
                return

            try:
                # Insere o novo técnico no banco de dados.
                self.colecao_tecnicos.insert_one({"nome": nome_tecnico})

                # Recarrega a lista de técnicos no ComboBox.
                self.carregar_tecnicos()

                # Exibe mensagem de sucesso.
                messagebox.showinfo("Sucesso", f"Técnico '{nome_tecnico}' cadastrado com sucesso!")

                # Fecha a janela de cadastro.
                janela_tecnico.destroy()

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao cadastrar técnico:\n\n{str(e)}")

        # Cria um botão para salvar o técnico.
        botao_salvar = tk.Button(janela_tecnico,
                                text="Salvar",
                                command=salvar_tecnico,
                                bg="#81c784",
                                font=("Arial", 11, "bold"),
                                width=12)
        botao_salvar.grid(row=1, column=0, columnspan=2, pady=10)

        # Permite salvar pressionando Enter.
        entrada_nome.bind('<Return>', lambda e: salvar_tecnico())


    # Define o método 'carregar_tarefas', que é responsável por carregar as
    # tarefas do banco de dados e exibi-las no Treeview.
    # O parâmetro 'filtro_status' permite que o método carregue apenas tarefas
    # com um status específico (por exemplo, "Pendente" ou "Concluída").
    def carregar_tarefas(self, filtro_status=None):

        """
        Este método carrega as tarefas do MongoDB e as exibe no Treeview.
        Se 'filtro_status' for igual a 'Pendente' ou 'Concluída', ele filtra as tarefas por esse status.
        Caso contrário, ele carrega todas as tarefas disponíveis no banco de dados.
        """

        # Limpa todos os itens atualmente exibidos no Treeview para evitar duplicação de dados.
        # 'get_children()' retorna todos os identificadores de itens no Treeview.
        # Para cada item, 'delete(item)' remove-o do Treeview.
        for item in self.arvore_tarefas.get_children():
            self.arvore_tarefas.delete(item)

        # Cria um dicionário vazio para a consulta ao banco de dados.
        # Este dicionário será usado como filtro para buscar
        # tarefas específicas no MongoDB.
        consulta = {}

        # Verifica se o filtro 'filtro_status' é válido.
        # Se 'filtro_status' não for None e estiver na lista ["Pendente", "Concluída"],
        # atualiza o dicionário 'consulta'.
        # O filtro "status" será usado para buscar tarefas no banco de
        # dados com o status correspondente.
        if filtro_status and filtro_status in ["Pendente", "Concluída"]:
            consulta = {"status": filtro_status}

        # Realiza a consulta no banco de dados MongoDB usando o método 'find'.
        # O método 'find(consulta)' retorna todos os documentos da coleção que
        # correspondem aos critérios especificados em 'consulta'.
        tarefas = self.colecao.find(consulta)

        # Itera sobre as tarefas retornadas pela consulta ao banco de dados.
        for tarefa in tarefas:

            # Formata a data da criação para exibição.
            # Se a tarefa tiver uma data de criação, formata no formato DD/MM/YYYY.
            # Caso contrário, usa a data atual como padrão.
            if "data_criacao" in tarefa:
                # Se a data estiver armazenada como string, usa diretamente.
                # Se estiver como datetime, formata para string.
                if isinstance(tarefa["data_criacao"], datetime):
                    data_formatada = tarefa["data_criacao"].strftime("%d/%m/%Y")
                else:
                    data_formatada = tarefa["data_criacao"]
            else:
                # Se não houver data, usa a data atual.
                data_formatada = datetime.now().strftime("%d/%m/%Y")

            # Obtém o nome do técnico responsável pela tarefa.
            # Se não houver técnico atribuído, exibe "N/A".
            tecnico_tarefa = tarefa.get("tecnico", "N/A")
            if not tecnico_tarefa:
                tecnico_tarefa = "N/A"

            # Insere cada tarefa no Treeview.
            # - "" especifica que o item será inserido na raiz do Treeview, ou seja, sem um pai.
            # - tk.END insere o item no final da lista.
            # - 'values' define os valores a serem exibidos nas colunas do Treeview.
            # - 'iid' atribui um identificador exclusivo ao item no Treeview,
            # aqui convertido do '_id' do MongoDB para string.
            self.arvore_tarefas.insert("", tk.END,
                                       values=(tarefa["titulo"], tarefa["descricao"], tarefa["status"], data_formatada, tecnico_tarefa),
                                       iid=str(tarefa["_id"]))


    # Define o método 'adicionar_tarefa', responsável por adicionar uma
    # nova tarefa ao banco de dados MongoDB.
    def adicionar_tarefa(self):

        """
        Este método adiciona uma nova tarefa ao banco de dados MongoDB.
        Ele coleta os dados inseridos pelo usuário nos campos da interface, valida o título da tarefa,
        e insere a nova tarefa na coleção do MongoDB.
        """

        # Obtém o texto do campo de entrada do título e remove quaisquer
        # espaços em branco no início e no final da string.
        titulo = self.entrada_titulo.get().strip()

        # Obtém o texto do campo de descrição, desde a posição "1.0" (primeira
        # linha, primeira coluna) até o final.
        # 'strip()' é usado para remover espaços em branco desnecessários.
        descricao = self.texto_descricao.get("1.0", tk.END).strip()

        # Obtém o valor selecionado no ComboBox de status.
        # Este valor é gerenciado pela variável tkinter 'StringVar' associada ao ComboBox.
        status = self.var_status.get()

        # Obtém a data selecionada no campo de data.
        # Se DateEntry estiver disponível, obtém a data como objeto datetime.
        # Caso contrário, obtém como string e converte para datetime.
        if DateEntry and isinstance(self.entrada_data, DateEntry):
            # DateEntry retorna um objeto date, convertemos para datetime
            data_selecionada = datetime.combine(self.entrada_data.get_date(), time.min)
        else:
            # Se for Entry comum, obtém a string e converte para datetime
            data_str = self.entrada_data.get().strip()
            try:
                # Tenta converter a string no formato DD/MM/YYYY para datetime
                data_selecionada = datetime.strptime(data_str, "%d/%m/%Y")
            except ValueError:
                # Se a conversão falhar, usa a data atual
                data_selecionada = datetime.now()

        # Verifica se o campo título está vazio.
        # Se o título não for fornecido, exibe uma mensagem de aviso
        # ao usuário usando o messagebox.
        if not titulo:

            messagebox.showwarning("Aviso", "O título da tarefa não pode estar vazio.")  # Exibe um alerta.
            return  # Interrompe a execução do método.

        # Obtém o técnico selecionado no ComboBox de técnicos.
        # Se nenhum técnico for selecionado, o valor será uma string vazia.
        tecnico = self.var_tecnico.get().strip()

        # Cria um dicionário representando a nova tarefa, com os
        # valores coletados dos campos de entrada.
        nova_tarefa = {
            "titulo": titulo,  # Atribui o valor do título inserido.
            "descricao": descricao,  # Atribui o valor da descrição inserida.
            "status": status,  # Atribui o status selecionado no ComboBox.
            "data_criacao": data_selecionada.strftime("%d/%m/%Y"),  # Atribui a data de criação formatada.
            "tecnico": tecnico if tecnico else ""  # Atribui o técnico selecionado, ou string vazia se nenhum for selecionado.
        }

        # Insere o dicionário 'nova_tarefa' no banco de dados
        # MongoDB, na coleção especificada.
        # 'insert_one' adiciona um único documento à coleção.
        self.colecao.insert_one(nova_tarefa)

        # Atualiza o Treeview para refletir a nova tarefa adicionada.
        # Isso recarrega todas as tarefas do banco de dados e as exibe na interface.
        self.carregar_tarefas()

        # Limpa os campos de entrada na interface para que o usuário possa
        # adicionar uma nova tarefa sem interferência de dados anteriores.
        self.limpar_campos_entrada()

        # Exibe uma mensagem de sucesso ao usuário indicando que a
        # tarefa foi adicionada com sucesso.
        messagebox.showinfo("Sucesso", "Tarefa adicionada com sucesso!")


    # Define o método 'limpar_campos_entrada', que é usado para limpar os
    # campos de entrada da interface.
    # Este método é chamado após adicionar, atualizar ou excluir uma
    # tarefa para garantir que os campos fiquem vazios
    # e prontos para uma nova entrada de dados.
    def limpar_campos_entrada(self):

        """
        Este método limpa os campos de entrada da interface gráfica.
        Ele é utilizado após operações como adicionar, atualizar ou excluir uma tarefa,
        para evitar que dados anteriores permaneçam visíveis nos campos.
        """

        # Limpa o campo de entrada de texto associado ao título da tarefa.
        # 'delete(0, tk.END)' remove todo o texto do início (índice 0)
        # até o final (tk.END) do campo de entrada.
        self.entrada_titulo.delete(0, tk.END)

        # Limpa o campo de texto da descrição da tarefa.
        # 'delete("1.0", tk.END)' remove todo o texto do campo de
        # texto desde a primeira linha (1.0)
        # até o final (tk.END).
        self.texto_descricao.delete("1.0", tk.END)

        # Redefine o ComboBox de status para o valor padrão "Pendente".
        # O ComboBox está vinculado à variável tkinter 'self.var_status',
        # e 'set' altera o valor atual.
        self.var_status.set("Pendente")

        # Limpa ou redefine o campo de data.
        # Se DateEntry estiver disponível, define a data atual.
        # Caso contrário, limpa o Entry e define a data atual.
        if DateEntry and isinstance(self.entrada_data, DateEntry):
            # DateEntry: define a data atual
            self.entrada_data.set_date(datetime.now().date())
        else:
            # Entry comum: limpa e define a data atual
            self.entrada_data.delete(0, tk.END)
            data_atual = datetime.now().strftime("%d/%m/%Y")
            self.entrada_data.insert(0, data_atual)

        # Limpa o campo de técnico, redefinindo para vazio.
        self.var_tecnico.set("")


    # Define o método 'atualizar_tarefa', que é responsável por
    # atualizar as informações de uma tarefa existente no MongoDB.
    def atualizar_tarefa(self):

        """
        Este método atualiza a tarefa atualmente selecionada no MongoDB.
        Ele coleta os dados dos campos de entrada da interface gráfica e
                sobrescreve os valores da tarefa correspondente no banco de dados.
        """

        # Verifica se existe uma tarefa selecionada.
        # 'self.id_tarefa_selecionada' contém o identificador da tarefa
        # selecionada no Treeview.
        # Caso nenhuma tarefa esteja selecionada, exibe uma mensagem de
        # aviso e interrompe a execução do método.
        if not self.id_tarefa_selecionada:

            # Exibe um aviso ao usuário.
            messagebox.showwarning("Aviso", "Nenhuma tarefa selecionada para atualizar.")

            # Retorna imediatamente, encerrando o método, já que
            # não há tarefa para atualizar.
            return

        # Obtém o valor do campo de entrada de título.
        # 'get()' recupera o texto digitado pelo usuário, enquanto 'strip()'
        # remove espaços extras no início e no final.
        titulo = self.entrada_titulo.get().strip()

        # Obtém o valor do campo de texto da descrição.
        # O método 'get("1.0", tk.END)' recupera o texto do campo de texto a
        # partir da linha 1, coluna 0 até o final.
        # 'strip()' remove espaços extras.
        descricao = self.texto_descricao.get("1.0", tk.END).strip()

        # Obtém o status selecionado no ComboBox associado à
        # variável tkinter 'StringVar'.
        status = self.var_status.get()

        # Obtém a data selecionada no campo de data.
        # Se DateEntry estiver disponível, obtém a data como objeto datetime.
        # Caso contrário, obtém como string e converte para datetime.
        if DateEntry and isinstance(self.entrada_data, DateEntry):
            # DateEntry retorna um objeto date, convertemos para datetime
            data_selecionada = datetime.combine(self.entrada_data.get_date(), time.min)
        else:
            # Se for Entry comum, obtém a string e converte para datetime
            data_str = self.entrada_data.get().strip()
            try:
                # Tenta converter a string no formato DD/MM/YYYY para datetime
                data_selecionada = datetime.strptime(data_str, "%d/%m/%Y")
            except ValueError:
                # Se a conversão falhar, usa a data atual
                data_selecionada = datetime.now()

        # Verifica se o título da tarefa foi preenchido.
        # Caso o título esteja vazio, exibe uma mensagem de aviso ao
        # usuário e interrompe a execução do método.
        if not titulo:

            messagebox.showwarning("Aviso", "O título da tarefa não pode estar vazio.")  # Exibe um alerta.
            return  # Interrompe o método para evitar uma atualização inválida.

        # Obtém o técnico selecionado no ComboBox de técnicos.
        # Se nenhum técnico for selecionado, o valor será uma string vazia.
        tecnico = self.var_tecnico.get().strip()

        # Cria um dicionário contendo os dados atualizados da tarefa.
        # O operador "$set" é utilizado no MongoDB para atualizar apenas os
        # campos especificados no documento.
        dados_atualizacao = {
            "$set": {
                "titulo": titulo,  # Atualiza o campo "titulo" com o valor coletado da interface.
                "descricao": descricao,  # Atualiza o campo "descricao" com o valor coletado da interface.
                "status": status,  # Atualiza o campo "status" com o valor selecionado no ComboBox.
                "data_criacao": data_selecionada.strftime("%d/%m/%Y"),  # Atualiza o campo "data_criacao" com a data formatada.
                "tecnico": tecnico if tecnico else ""  # Atualiza o campo "tecnico" com o técnico selecionado.
            }
        }

        # Executa a atualização no banco de dados MongoDB.
        # 'update_one' atualiza um único documento na coleção que
        # corresponde ao filtro especificado.
        # O filtro utiliza o "_id" para identificar o documento a ser
        # atualizado, convertido para ObjectId.
        self.colecao.update_one({"_id": ObjectId(self.id_tarefa_selecionada)}, dados_atualizacao)

        # Recarrega as tarefas exibidas no Treeview.
        # Isso garante que os dados atualizados sejam refletidos
        # imediatamente na interface.
        self.carregar_tarefas()

        # Limpa os campos de entrada na interface.
        # Isso prepara os campos para que o usuário possa realizar outras
        # operações sem interferência dos dados anteriores.
        self.limpar_campos_entrada()

        # Redefine o identificador da tarefa selecionada para None.
        # Isso indica que nenhuma tarefa está atualmente selecionada
        # após a atualização.
        self.id_tarefa_selecionada = None

        # Exibe uma mensagem de sucesso ao usuário.
        # Informa que a tarefa foi atualizada com sucesso.
        messagebox.showinfo("Sucesso", "Tarefa atualizada com sucesso!")


    # Define o método 'excluir_tarefa', que remove uma
    # tarefa do banco de dados MongoDB.
    def excluir_tarefa(self):

        """
        Este método exclui a tarefa atualmente selecionada no banco de dados MongoDB.
        Ele confirma a exclusão com o usuário antes de executar a operação.
        """

        # Verifica se uma tarefa foi selecionada no Treeview.
        # Se 'self.id_tarefa_selecionada' for None, significa que
        # nenhuma tarefa está selecionada.
        if not self.id_tarefa_selecionada:

            # Exibe uma mensagem de aviso ao usuário informando que
            # não há tarefa selecionada.
            messagebox.showwarning("Aviso", "Nenhuma tarefa selecionada para excluir.")

            # Interrompe o método, já que não há tarefa para excluir.
            return

        # Exibe uma mensagem de confirmação antes de prosseguir com a exclusão.
        # O 'askyesno' exibe uma caixa de diálogo com as opções "Sim" e "Não".
        # Retorna True se o usuário clicar em "Sim" e False se clicar em "Não".
        confirmar = messagebox.askyesno("Confirmar Exclusão", "Deseja realmente excluir esta tarefa?")

        # Verifica se o usuário confirmou a exclusão.
        if confirmar:

            # Remove a tarefa do banco de dados MongoDB.
            # O método 'delete_one' exclui o documento que corresponde ao
            # filtro fornecido.
            # O identificador da tarefa é convertido para ObjectId antes de
            # ser usado na consulta.
            self.colecao.delete_one({"_id": ObjectId(self.id_tarefa_selecionada)})

            # Recarrega a lista de tarefas no Treeview para refletir a exclusão.
            self.carregar_tarefas()

            # Limpa os campos de entrada na interface.
            # Isso evita que informações de uma tarefa excluída permaneçam visíveis.
            self.limpar_campos_entrada()

            # Redefine o identificador da tarefa selecionada para None.
            # Isso indica que nenhuma tarefa está atualmente selecionada.
            self.id_tarefa_selecionada = None

            # Exibe uma mensagem de sucesso informando ao usuário que a tarefa foi excluída.
            messagebox.showinfo("Sucesso", "Tarefa excluída com sucesso!")


    # Define o método 'aplicar_filtro', que aplica o filtro de
    # status escolhido pelo usuário.
    def aplicar_filtro(self):

        """
        Este método obtém o status selecionado no ComboBox de filtros,
        aplica o filtro de status escolhido e recarrega a lista de tarefas no Treeview.
        """

        # Obtém o valor selecionado no ComboBox de filtro.
        # A variável tkinter 'self.var_filtro' é vinculada ao ComboBox e
        # contém o valor atualmente selecionado.
        filtro_escolhido = self.var_filtro.get()

        # Verifica se o filtro escolhido é "Todos".
        # Se for, carrega todas as tarefas no Treeview sem aplicar nenhum filtro.
        if filtro_escolhido == "Todos":

            # Chama o método 'carregar_tarefas' sem argumentos para
            # carregar todas as tarefas.
            self.carregar_tarefas()

        else:

            # Caso contrário, aplica o filtro de status escolhido.
            # O método 'carregar_tarefas' é chamado com o argumento 'filtro_status',
            # que corresponde ao status selecionado no ComboBox (por
            # exemplo, "Pendente" ou "Concluída").
            self.carregar_tarefas(filtro_status=filtro_escolhido)


    # Define o método 'selecionar_tipo_relatorio', que abre uma janela
    # para o usuário escolher entre relatório geral ou por técnico.
    def selecionar_tipo_relatorio(self):

        """
        Este método abre uma janela de diálogo para o usuário escolher
        o tipo de relatório: geral (todas as tarefas) ou por técnico.
        """

        # Cria uma janela top-level (popup) para seleção do tipo de relatório.
        janela_selecao = tk.Toplevel(self.janela)
        janela_selecao.title("Tipo de Relatório")
        janela_selecao.geometry("400x200")
        janela_selecao.configure(bg="#f0f0f0")
        janela_selecao.transient(self.janela)  # Mantém a janela acima da principal
        janela_selecao.grab_set()  # Torna a janela modal

        # Cria um rótulo de instrução.
        rotulo_instrucao = tk.Label(janela_selecao,
                                    text="Selecione o tipo de relatório:",
                                    font=("Arial", 12, "bold"),
                                    bg="#f0f0f0")
        rotulo_instrucao.grid(row=0, column=0, columnspan=2, padx=10, pady=20)

        # Cria uma variável para armazenar a escolha do tipo de relatório.
        tipo_relatorio = tk.StringVar(value="geral")

        # Cria um botão de rádio para relatório geral.
        radio_geral = tk.Radiobutton(janela_selecao,
                                     text="Relatório Geral (Todas as tarefas)",
                                     variable=tipo_relatorio,
                                     value="geral",
                                     font=("Arial", 11),
                                     bg="#f0f0f0")
        radio_geral.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='w')

        # Cria um botão de rádio para relatório por técnico.
        radio_tecnico = tk.Radiobutton(janela_selecao,
                                      text="Relatório por Técnico",
                                      variable=tipo_relatorio,
                                      value="tecnico",
                                      font=("Arial", 11),
                                      bg="#f0f0f0")
        radio_tecnico.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='w')

        # Cria um rótulo para o ComboBox de técnicos.
        rotulo_tecnico = tk.Label(janela_selecao,
                                  text="Selecione o técnico:",
                                  font=("Arial", 11),
                                  bg="#f0f0f0")
        rotulo_tecnico.grid(row=3, column=0, padx=10, pady=10, sticky='e')

        # Cria uma variável para o técnico selecionado.
        var_tecnico_selecao = tk.StringVar()

        # Cria um ComboBox para selecionar o técnico.
        combo_tecnico_selecao = ttk.Combobox(janela_selecao,
                                             textvariable=var_tecnico_selecao,
                                             state='readonly',
                                             font=("Arial", 11),
                                             width=25)

        # Carrega a lista de técnicos.
        try:
            tecnicos = self.colecao_tecnicos.find().sort("nome", 1)
            lista_tecnicos = [tecnico["nome"] for tecnico in tecnicos]
            combo_tecnico_selecao['values'] = lista_tecnicos
        except:
            combo_tecnico_selecao['values'] = []

        combo_tecnico_selecao.grid(row=3, column=1, padx=10, pady=10, sticky='w')

        # Função para habilitar/desabilitar o ComboBox de técnicos.
        def atualizar_combo():
            if tipo_relatorio.get() == "tecnico":
                combo_tecnico_selecao.config(state='readonly')
            else:
                combo_tecnico_selecao.config(state='disabled')
                var_tecnico_selecao.set("")

        # Vincula a função aos botões de rádio.
        radio_geral.config(command=atualizar_combo)
        radio_tecnico.config(command=atualizar_combo)

        # Inicializa o estado do ComboBox.
        atualizar_combo()

        # Função para gerar o relatório.
        def gerar_relatorio():
            tipo = tipo_relatorio.get()
            tecnico_selecionado = None

            if tipo == "tecnico":
                tecnico_selecionado = var_tecnico_selecao.get().strip()
                if not tecnico_selecionado:
                    messagebox.showwarning("Aviso", "Por favor, selecione um técnico.")
                    return

            # Fecha a janela de seleção.
            janela_selecao.destroy()

            # Chama o método de geração de PDF com o filtro apropriado.
            self.gerar_relatorio_pdf(tecnico_filtro=tecnico_selecionado)

        # Cria um botão para gerar o relatório.
        botao_gerar = tk.Button(janela_selecao,
                               text="Gerar Relatório",
                               command=gerar_relatorio,
                               bg="#90caf9",
                               font=("Arial", 11, "bold"),
                               width=15)
        botao_gerar.grid(row=4, column=0, columnspan=2, pady=20)


    # Define o método 'gerar_relatorio_pdf', que é responsável por
    # gerar um relatório em PDF com todas as tarefas do banco de dados
    # ou filtrado por técnico.
    def gerar_relatorio_pdf(self, tecnico_filtro=None):

        """
        Este método gera um relatório em PDF contendo as tarefas
        cadastradas no banco de dados MongoDB. O usuário pode escolher
        onde salvar o arquivo PDF.
        
        Parâmetros:
        - tecnico_filtro: Nome do técnico para filtrar as tarefas (opcional).
                         Se None, gera relatório com todas as tarefas.
        """

        # Verifica se o reportlab está disponível.
        if not REPORTLAB_AVAILABLE:
            messagebox.showerror("Erro", 
                                "A biblioteca reportlab não está instalada.\n\n"
                                "Para instalar, execute: pip install reportlab")
            return

        # Solicita ao usuário onde salvar o arquivo PDF.
        # Abre uma janela de diálogo para escolher o local e nome do arquivo.
        arquivo_pdf = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            title="Salvar Relatório PDF"
        )

        # Verifica se o usuário cancelou a seleção do arquivo.
        if not arquivo_pdf:
            return

        try:
            # Cria a consulta para buscar as tarefas.
            consulta = {}
            
            # Se houver filtro por técnico, adiciona à consulta.
            if tecnico_filtro:
                consulta["tecnico"] = tecnico_filtro

            # Busca as tarefas do banco de dados MongoDB.
            # Ordena por data de criação (1 = ascendente).
            # Se não houver campo data_criacao, a ordenação será ignorada.
            tarefas = list(self.colecao.find(consulta).sort("data_criacao", 1))

            # Verifica se há tarefas para incluir no relatório.
            if not tarefas:
                if tecnico_filtro:
                    messagebox.showwarning("Aviso", 
                                         f"Não há tarefas para o técnico '{tecnico_filtro}'.")
                else:
                    messagebox.showwarning("Aviso", "Não há tarefas para gerar o relatório.")
                return

            # Cria o documento PDF usando SimpleDocTemplate.
            # 'arquivo_pdf' é o caminho onde o PDF será salvo.
            # 'pagesize=A4' define o tamanho da página como A4.
            doc = SimpleDocTemplate(arquivo_pdf, pagesize=A4)

            # Lista que armazenará os elementos do PDF (tabelas, parágrafos, etc.).
            elementos = []

            # Obtém estilos de texto pré-definidos.
            estilos = getSampleStyleSheet()

            # Cria um estilo personalizado para o título do relatório.
            estilo_titulo = ParagraphStyle(
                'TituloCustomizado',
                parent=estilos['Heading1'],
                fontSize=20,
                textColor=colors.HexColor('#1976d2'),
                spaceAfter=30,
                alignment=1  # Centralizado
            )

            # Define o título do relatório conforme o tipo.
            if tecnico_filtro:
                titulo_texto = f"Relatório de Tarefas - {tecnico_filtro}"
            else:
                titulo_texto = "Relatório de Tarefas - Geral"

            # Adiciona o título do relatório ao PDF.
            titulo = Paragraph(titulo_texto, estilo_titulo)
            elementos.append(titulo)

            # Adiciona a data de geração do relatório.
            data_geracao = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            estilo_data = ParagraphStyle(
                'DataCustomizada',
                parent=estilos['Normal'],
                fontSize=10,
                textColor=colors.HexColor('#666666'),
                alignment=1  # Centralizado
            )
            data_paragrafo = Paragraph(f"Gerado em: {data_geracao}", estilo_data)
            elementos.append(data_paragrafo)
            elementos.append(Spacer(1, 0.3 * inch))

            # Prepara os dados para a tabela.
            # Cabeçalho da tabela.
            dados_tabela = [['Título', 'Descrição', 'Status', 'Data de Criação', 'Técnico']]

            # Adiciona cada tarefa como uma linha na tabela.
            for tarefa in tarefas:
                # Obtém os dados da tarefa, tratando valores ausentes.
                titulo_tarefa = tarefa.get("titulo", "N/A")
                descricao_tarefa = tarefa.get("descricao", "N/A")
                # Limita o tamanho da descrição para não quebrar o layout
                if len(descricao_tarefa) > 40:
                    descricao_tarefa = descricao_tarefa[:37] + "..."
                status_tarefa = tarefa.get("status", "N/A")

                # Formata a data de criação.
                if "data_criacao" in tarefa:
                    data_criacao = tarefa["data_criacao"]
                    if isinstance(data_criacao, datetime):
                        data_formatada = data_criacao.strftime("%d/%m/%Y")
                    else:
                        data_formatada = str(data_criacao)
                else:
                    data_formatada = "N/A"

                # Obtém o nome do técnico responsável.
                tecnico_tarefa = tarefa.get("tecnico", "N/A")
                if not tecnico_tarefa:
                    tecnico_tarefa = "N/A"

                # Adiciona a linha da tarefa aos dados da tabela.
                dados_tabela.append([titulo_tarefa, descricao_tarefa, status_tarefa, data_formatada, tecnico_tarefa])

            # Cria a tabela com os dados.
            # Ajusta as larguras das colunas para caber na página A4 (largura útil ~7.5 inch).
            # Título: 1.5 inch, Descrição: 2.2 inch, Status: 0.9 inch, Data: 1.2 inch, Técnico: 1.2 inch
            tabela = Table(dados_tabela, colWidths=[1.5*inch, 2.2*inch, 0.9*inch, 1.4*inch, 1.3*inch])

            # Define o estilo da tabela.
            estilo_tabela = TableStyle([
                # Estilo do cabeçalho
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1976d2')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('TOPPADDING', (0, 0), (-1, 0), 12),
                # Estilo das linhas de dados
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
            ])

            # Aplica o estilo à tabela.
            tabela.setStyle(estilo_tabela)

            # Adiciona a tabela aos elementos do PDF.
            elementos.append(tabela)

            # Adiciona informações de resumo no final do relatório.
            elementos.append(Spacer(1, 0.3 * inch))
            total_tarefas = len(tarefas)
            pendentes = sum(1 for t in tarefas if t.get("status") == "Pendente")
            concluidas = sum(1 for t in tarefas if t.get("status") == "Concluída")

            estilo_resumo = ParagraphStyle(
                'ResumoCustomizado',
                parent=estilos['Normal'],
                fontSize=11,
                textColor=colors.HexColor('#333333'),
                spaceAfter=10
            )

            resumo = Paragraph(
                f"<b>Resumo:</b><br/>"
                f"Total de tarefas: {total_tarefas}<br/>"
                f"Pendentes: {pendentes}<br/>"
                f"Concluídas: {concluidas}",
                estilo_resumo
            )
            elementos.append(resumo)

            # Constrói o PDF com todos os elementos adicionados.
            doc.build(elementos)

            # Exibe mensagem de sucesso ao usuário.
            messagebox.showinfo("Sucesso", 
                              f"Relatório PDF gerado com sucesso!\n\n"
                              f"Arquivo salvo em:\n{arquivo_pdf}")

        except Exception as e:
            # Em caso de erro, exibe uma mensagem de erro ao usuário.
            messagebox.showerror("Erro", 
                               f"Erro ao gerar o relatório PDF:\n\n{str(e)}")


    # Define o método 'ao_selecionar_tarefa', que é chamado automaticamente
    # quando uma tarefa é selecionada no Treeview.
    # O parâmetro 'event' contém informações sobre o evento
    # disparado pela seleção no Treeview.
    def ao_selecionar_tarefa(self, event):

        """
        Este método é executado ao selecionar uma tarefa no Treeview.
        Ele carrega os dados da tarefa selecionada nos campos de entrada da interface,
        permitindo que o usuário visualize ou edite as informações.
        """

        # Obtém a seleção atual no Treeview.
        # 'selection()' retorna uma lista com os identificadores dos
        # itens selecionados no Treeview.
        selecionado = self.arvore_tarefas.selection()

        # Verifica se há algum item selecionado no Treeview.
        if selecionado:

            # Define 'id_tarefa_selecionada' como o identificador do
            # primeiro item selecionado.
            # Neste caso, o identificador corresponde ao '_id' do
            # MongoDB convertido para string.
            self.id_tarefa_selecionada = selecionado[0]

            # Busca os dados completos da tarefa no banco de dados
            # MongoDB usando o identificador '_id'.
            # 'find_one' retorna o documento correspondente ao filtro fornecido.
            # 'ObjectId' é usado para converter o identificador string de
            # volta para o formato de objeto do MongoDB.
            dados_tarefa = self.colecao.find_one({"_id": ObjectId(self.id_tarefa_selecionada)})

            # Verifica se a tarefa foi encontrada no banco de dados.
            if dados_tarefa:

                # Limpa o campo de entrada do título, removendo qualquer
                # texto anteriormente inserido.
                self.entrada_titulo.delete(0, tk.END)

                # Insere o título da tarefa encontrada no campo de entrada.
                self.entrada_titulo.insert(tk.END, dados_tarefa["titulo"])

                # Limpa o campo de texto da descrição, removendo qualquer
                # texto previamente inserido.
                self.texto_descricao.delete("1.0", tk.END)

                # Insere a descrição da tarefa encontrada no campo de texto.
                self.texto_descricao.insert(tk.END, dados_tarefa["descricao"])

                # Define o status da tarefa no ComboBox, atualizando a
                # seleção para o status da tarefa carregada.
                self.var_status.set(dados_tarefa["status"])

                # Define o técnico da tarefa no ComboBox, atualizando a
                # seleção para o técnico da tarefa carregada.
                tecnico_tarefa = dados_tarefa.get("tecnico", "")
                self.var_tecnico.set(tecnico_tarefa if tecnico_tarefa else "")

                # Define a data da tarefa no campo de data.
                # Se a tarefa tiver uma data de criação, carrega essa data.
                # Caso contrário, usa a data atual.
                if "data_criacao" in dados_tarefa:
                    data_tarefa = dados_tarefa["data_criacao"]
                    # Se a data estiver como string, converte para datetime
                    if isinstance(data_tarefa, str):
                        try:
                            data_obj = datetime.strptime(data_tarefa, "%d/%m/%Y")
                        except ValueError:
                            data_obj = datetime.now()
                    else:
                        data_obj = data_tarefa
                else:
                    data_obj = datetime.now()

                # Atualiza o campo de data com a data da tarefa.
                if DateEntry and isinstance(self.entrada_data, DateEntry):
                    # DateEntry: define a data usando set_date
                    self.entrada_data.set_date(data_obj.date())
                else:
                    # Entry comum: limpa e insere a data formatada
                    self.entrada_data.delete(0, tk.END)
                    self.entrada_data.insert(0, data_obj.strftime("%d/%m/%Y"))


# Cria a janela principal da aplicação.
# 'tk.Tk()' inicializa a instância principal da janela Tkinter, que
        # será usada como o contêiner principal da interface gráfica.
janela_principal = tk.Tk()

# Cria uma instância da classe 'GerenciadorTarefasApp'.
# A janela principal criada anteriormente ('janela_principal') é
        # passada como argumento para o construtor da classe.
# Isso permite que a interface gráfica definida na classe 'GerenciadorTarefasApp'
        # seja exibida na janela principal.
app = GerenciadorTarefasApp(janela_principal)

# Inicia o loop principal da interface gráfica.
# 'mainloop()' é um método do Tkinter que mantém a janela
        # aberta e responsiva a interações do usuário,
# como cliques, entradas de dados e comandos. Ele monitora eventos e
        # atualiza a interface constantemente.
janela_principal.mainloop()