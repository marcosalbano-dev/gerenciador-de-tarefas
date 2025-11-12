# Importa o módulo tkinter com o alias 'tk'.
# Tkinter é uma biblioteca de interface gráfica padrão do Python,
# usada para criar janelas e outros elementos gráficos.
import tkinter as tk

# Importa módulos específicos do tkinter:
# - ttk é um conjunto de widgets que fornece uma aparência mais
# moderna e temática para os elementos da interface gráfica.
# - messagebox é um módulo utilizado para abrir janelas de
# mensagem, como alertas e confirmações.
from tkinter import ttk, messagebox


from tkinter import font 

# Importa a classe ObjectId do módulo bson.
# ObjectId é um identificador único utilizado pelo MongoDB para documentos.
# É frequentemente usado para buscar ou referenciar documentos específicos.
from bson.objectid import ObjectId

# Importa a classe MongoClient do módulo pymongo.
# MongoClient é usado para estabelecer uma conexão com o banco de
# dados MongoDB, permitindo operações como ler e escrever dados.
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

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
        self.janela.configure(bg="#f0f0f0")

        # Conexão com o MongoDB
        # Cria uma instância do MongoClient para conectar ao
        # servidor MongoDB local na porta padrão 27017.
        try:
            self.cliente = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=2000)
            # Testa a conexão tentando acessar o servidor
            self.cliente.admin.command('ping')
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            messagebox.showerror("Erro de Conexão", 
                                "Não foi possível conectar ao MongoDB.\n\n"
                                "Certifique-se de que o MongoDB está instalado e rodando.\n"
                                "Para iniciar o MongoDB, execute: mongod\n\n"
                                f"Erro: {str(e)}")
            self.cliente = None
            self.db = None
            self.colecao = None
        else:
            # Acessa o banco de dados chamado 'gerenciador_tarefas_db'. Se o banco de
            # dados não existir, ele será criado automaticamente ao
            # inserir os primeiros dados.
            self.db = self.cliente["gerenciador_tarefas_db"]

            # Acessa a coleção 'tarefas' dentro do banco de dados. Coleções no
            # MongoDB são equivalentes a tabelas em bancos de dados relacionais.
            self.colecao = self.db["tarefas"]

        # Criação de estilo para o Treeview
        # Cria uma instância de Style do módulo ttk para customizar a
        # aparência dos widgets ttk.
        estilo = ttk.Style()

        # Define o tema de estilo como 'default'. Esse é o tema padrão do
        # ttk que será base para as customizações.
        estilo.theme_use("default")

        # Configura o estilo para o widget Treeview. Define o fundo das
        # linhas como branco, o texto como preto,
        # a altura das linhas como 25 pixels, o fundo dos
        # campos como branco e a fonte como Arial tamanho 11.
        estilo.configure("Treeview", 
                           background="#ffffff",
                           foreground="black", 
                           rowheight=25, 
                           fieldbackground="#ffffff",
                           font=("Arial", 12))

        # Configura o estilo para o cabeçalho das colunas do Treeview.
        # Define a fonte como Arial tamanho 12 em negrito.
        # Essa configuração é aplicada aos cabeçalhos das colunas do Treeview,
        # fornecendo um estilo visual distinto e de fácil leitura.
        estilo.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        # Configurações adicionais para o estilo do Treeview ao
        # selecionar uma linha.
        # Define o fundo da linha selecionada como preto e o texto
        # como branco para melhorar a visibilidade da seleção.
        estilo.map("Treeview", background=[("selected", "black")])
        estilo.map("Treeview", foreground=[("selected", "white")])

        # Criação de um quadro para os campos de entrada de dados no aplicativo.
        # Um quadro é um container que organiza e agrupa widgets
        # dentro da janela principal.
        quadro_entrada = tk.Frame(self.janela, bg="#f0f0f0")

        # Empacota o quadro dentro da janela principal.
        # pady e padx adicionam um espaçamento vertical e horizontal
        # ao redor do quadro.
        # fill='x' faz com que o quadro se expanda horizontalmente para
        # preencher o espaço disponível.
        quadro_entrada.pack(fill="x", padx=10, pady=10)

        # Criação de um rótulo (label) para o campo "Título da Tarefa".
        # Um rótulo é um widget que exibe texto na interface gráfica.
        rotulo_titulo = tk.Label(quadro_entrada, text="Título da Tarefa:", bg="#f0f0f0", font=("Arial", 12))

        # Posiciona o rótulo no quadro de entrada usando o gerenciador de layout grid.
        # - row=0 e column=0 posicionam o rótulo na primeira linha e primeira coluna do grid.
        # - sticky='e' alinha o rótulo à direita (east) dentro da célula grid.
        # - padx e pady adicionam um espaçamento externo de 5 pixels em
        # todas as direções para separar visualmente os elementos.
        rotulo_titulo.grid(row=0, column=0, sticky="e", padx=5, pady=5)

        # Criação de um campo de entrada (Entry) para digitar o título da tarefa.
        # Entry é um widget que permite ao usuário inserir uma linha de texto.
        self.entrada_titulo = tk.Entry(quadro_entrada, width=55, font=("Arial", 11))

        # Posiciona o campo de entrada no quadro usando o gerenciador de layout grid.
        # - row=0 e column=1 posicionam o campo na primeira linha e segunda coluna do grid.
        # - columnspan=3 faz com que o campo de entrada se estenda por três
                # colunas do grid, para utilizar melhor o espaço disponível.
        # - sticky='w' alinha o campo de entrada à esquerda (west) dentro da célula grid.
        # - padx e pady adicionam um espaçamento externo para estética e
                # para evitar a aglomeração de widgets.
        self.entrada_titulo.grid(row=0, column=1, sticky="w", padx=5, pady=5)

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
                                           columns=("Título", "Descrição", "Status"),
                                           show="headings",
                                           height=15,
                                           yscrollcommand=barra_rolagem.set)

        # Configura o cabeçalho da coluna "Título" no Treeview para exibir "Título".
        self.arvore_tarefas.heading("Título", text="Título")

        # Configura o cabeçalho da coluna "Descrição" no Treeview para exibir "Descrição".
        self.arvore_tarefas.heading("Descrição", text="Descrição")

        # Configura o cabeçalho da coluna "Status" no Treeview para exibir "Status".
        self.arvore_tarefas.heading("Status", text="Status")

        # Configura a largura da coluna "Título" no Treeview.
        # A largura é definida como 220 pixels para garantir que o
        # conteúdo da coluna "Título" seja exibido adequadamente,
        # mesmo que o texto seja um pouco longo, mantendo uma
        # aparência equilibrada na interface.
        self.arvore_tarefas.column("Título", width=220)

        # Configura a largura da coluna "Descrição" no Treeview.
        # A largura é ajustada para 480 pixels, sendo a maior entre as
        # colunas, pois a descrição das tarefas geralmente contém mais texto.
        # Isso assegura que a maior parte do conteúdo fique visível sem
        # necessidade de rolagem horizontal.
        self.arvore_tarefas.column("Descrição", width=480)

        # Configura a largura da coluna "Status" no Treeview.
        # A largura é definida como 120 pixels, pois o conteúdo esperado nesta
        # coluna é curto, geralmente "Pendente" ou "Concluída".
        # Isso ajuda a otimizar o espaço ocupado pelo Treeview na interface.
        self.arvore_tarefas.column("Status", width=120)

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

        # Verifica se há conexão com o MongoDB
        if not self.colecao:
            return

        # Limpa todos os itens atualmente exibidos no Treeview para evitar duplicação de dados.
        # 'get_children()' retorna todos os identificadores de itens no Treeview.
        # Para cada item, 'delete(item)' remove-o do Treeview.
        for item in self.arvore_tarefas.get_children():
            self.arvore_tarefas.delete(item)

        try:
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

                # Insere cada tarefa no Treeview.
                # - "" especifica que o item será inserido na raiz do Treeview, ou seja, sem um pai.
                # - tk.END insere o item no final da lista.
                # - 'values' define os valores a serem exibidos nas colunas do Treeview.
                # - 'iid' atribui um identificador exclusivo ao item no Treeview,
                # aqui convertido do '_id' do MongoDB para string.
                self.arvore_tarefas.insert("", tk.END,
                                           values=(tarefa["titulo"], tarefa["descricao"], tarefa["status"]),
                                           iid=str(tarefa["_id"]))
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            messagebox.showerror("Erro de Conexão", 
                                "Não foi possível conectar ao MongoDB.\n\n"
                                "Certifique-se de que o MongoDB está rodando.\n\n"
                                f"Erro: {str(e)}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar tarefas: {str(e)}")


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

        # Verifica se o campo título está vazio.
        # Se o título não for fornecido, exibe uma mensagem de aviso
        # ao usuário usando o messagebox.
        if not titulo:

            messagebox.showwarning("Aviso", "O título da tarefa não pode estar vazio.")  # Exibe um alerta.
            return  # Interrompe a execução do método.

        # Verifica se há conexão com o MongoDB
        if not self.colecao:
            messagebox.showerror("Erro", "Não há conexão com o MongoDB.")
            return

        try:
            # Cria um dicionário representando a nova tarefa, com os
            # valores coletados dos campos de entrada.
            nova_tarefa = {
                "titulo": titulo,  # Atribui o valor do título inserido.
                "descricao": descricao,  # Atribui o valor da descrição inserida.
                "status": status  # Atribui o status selecionado no ComboBox.
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
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            messagebox.showerror("Erro de Conexão", 
                                "Não foi possível conectar ao MongoDB.\n\n"
                                "Certifique-se de que o MongoDB está rodando.\n\n"
                                f"Erro: {str(e)}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar tarefa: {str(e)}")


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

        # Verifica se o título da tarefa foi preenchido.
        # Caso o título esteja vazio, exibe uma mensagem de aviso ao
        # usuário e interrompe a execução do método.
        if not titulo:

            messagebox.showwarning("Aviso", "O título da tarefa não pode estar vazio.")  # Exibe um alerta.
            return  # Interrompe o método para evitar uma atualização inválida.

        # Verifica se há conexão com o MongoDB
        if not self.colecao:
            messagebox.showerror("Erro", "Não há conexão com o MongoDB.")
            return

        try:
            # Cria um dicionário contendo os dados atualizados da tarefa.
            # O operador "$set" é utilizado no MongoDB para atualizar apenas os
            # campos especificados no documento.
            dados_atualizacao = {
                "$set": {
                    "titulo": titulo,  # Atualiza o campo "titulo" com o valor coletado da interface.
                    "descricao": descricao,  # Atualiza o campo "descricao" com o valor coletado da interface.
                    "status": status  # Atualiza o campo "status" com o valor selecionado no ComboBox.
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
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            messagebox.showerror("Erro de Conexão", 
                                "Não foi possível conectar ao MongoDB.\n\n"
                                "Certifique-se de que o MongoDB está rodando.\n\n"
                                f"Erro: {str(e)}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar tarefa: {str(e)}")

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

            # Verifica se há conexão com o MongoDB
            if not self.colecao:
                messagebox.showerror("Erro", "Não há conexão com o MongoDB.")
                return

            try:
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
            except (ConnectionFailure, ServerSelectionTimeoutError) as e:
                messagebox.showerror("Erro de Conexão", 
                                    "Não foi possível conectar ao MongoDB.\n\n"
                                    "Certifique-se de que o MongoDB está rodando.\n\n"
                                    f"Erro: {str(e)}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir tarefa: {str(e)}")

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

            # Verifica se há conexão com o MongoDB
            if not self.colecao:
                return

            try:
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
            except (ConnectionFailure, ServerSelectionTimeoutError) as e:
                messagebox.showerror("Erro de Conexão", 
                                    "Não foi possível conectar ao MongoDB.\n\n"
                                    "Certifique-se de que o MongoDB está rodando.\n\n"
                                    f"Erro: {str(e)}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar tarefa: {str(e)}")


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
       