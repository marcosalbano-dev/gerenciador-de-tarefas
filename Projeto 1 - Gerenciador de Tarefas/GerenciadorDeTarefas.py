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
        self.cliente = MongoClient("mongodb://localhost:27017")

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

        # Inicializa a variável que armazenará o ID da tarefa selecionada.
        # Esta variável será usada para identificar qual tarefa deve ser
        # atualizada ou excluída quando o usuário selecionar uma tarefa no Treeview.
        self.id_tarefa_selecionada = None

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

        # Cria o botão "Excluir Tarefa", utilizado para remover tarefas do sistema.
        botao_excluir = tk.Button(quadro_botoes,
                                  text="Excluir Tarefa",
                                  command=self.excluir_tarefa,
                                  bg="#ef5350",
                                  font=("Arial", 11, "bold"),
                                  width=18)

        # Posiciona o botão 'Excluir Tarefa' ao lado dos outros botões.
        botao_excluir.grid(row=0, column=2, padx=10, pady=5)

        # Criação de um quadro para o Treeview que exibirá as tarefas.
        quadro_treeview = tk.Frame(self.janela, bg="#f0f0f0")
        quadro_treeview.pack(fill="both", expand=True, padx=10, pady=10)

        # Criação de um rótulo para o Treeview.
        rotulo_lista = tk.Label(quadro_treeview,
                               text="Lista de Tarefas:",
                               font=("Arial", 12, "bold"),
                               bg="#f0f0f0")
        rotulo_lista.pack(anchor="w", pady=(0, 5))

        # Criação de um quadro com scrollbar para o Treeview.
        quadro_scroll = tk.Frame(quadro_treeview, bg="#f0f0f0")
        quadro_scroll.pack(fill="both", expand=True)

        # Criação de uma scrollbar vertical para o Treeview.
        scrollbar = ttk.Scrollbar(quadro_scroll, orient="vertical")

        # Criação do Treeview para exibir as tarefas em formato de tabela.
        # O Treeview permite exibir dados em formato de árvore ou tabela.
        self.arvore_tarefas = ttk.Treeview(quadro_scroll,
                                           columns=("Título", "Descrição", "Status"),
                                           show="headings",
                                           yscrollcommand=scrollbar.set,
                                           height=15)

        # Configura a scrollbar para controlar o scroll do Treeview.
        scrollbar.config(command=self.arvore_tarefas.yview)

        # Configura os cabeçalhos das colunas do Treeview.
        self.arvore_tarefas.heading("Título", text="Título")
        self.arvore_tarefas.heading("Descrição", text="Descrição")
        self.arvore_tarefas.heading("Status", text="Status")

        # Configura a largura das colunas do Treeview.
        self.arvore_tarefas.column("Título", width=200)
        self.arvore_tarefas.column("Descrição", width=400)
        self.arvore_tarefas.column("Status", width=150)

        # Empacota a scrollbar e o Treeview no quadro.
        scrollbar.pack(side="right", fill="y")
        self.arvore_tarefas.pack(side="left", fill="both", expand=True)

        # Vincula o evento de seleção do Treeview ao método que preenche os campos.
        # Quando o usuário clicar em uma tarefa, os campos serão preenchidos automaticamente.
        self.arvore_tarefas.bind("<<TreeviewSelect>>", self.selecionar_tarefa)

        # Criação de um quadro para os filtros de status.
        quadro_filtros = tk.Frame(self.janela, bg="#f0f0f0")
        quadro_filtros.pack(fill="x", padx=10, pady=5)

        # Rótulo para os filtros.
        rotulo_filtro = tk.Label(quadro_filtros,
                                text="Filtrar por Status:",
                                font=("Arial", 11),
                                bg="#f0f0f0")
        rotulo_filtro.pack(side="left", padx=5)

        # Botão para mostrar todas as tarefas.
        botao_todas = tk.Button(quadro_filtros,
                               text="Todas",
                               command=lambda: self.carregar_tarefas(),
                               bg="#e0e0e0",
                               font=("Arial", 10),
                               width=12)
        botao_todas.pack(side="left", padx=5)

        # Botão para filtrar apenas tarefas pendentes.
        botao_pendentes = tk.Button(quadro_filtros,
                                   text="Pendentes",
                                   command=lambda: self.carregar_tarefas("Pendente"),
                                   bg="#fff59d",
                                   font=("Arial", 10),
                                   width=12)
        botao_pendentes.pack(side="left", padx=5)

        # Botão para filtrar apenas tarefas concluídas.
        botao_concluidas = tk.Button(quadro_filtros,
                                    text="Concluídas",
                                    command=lambda: self.carregar_tarefas("Concluída"),
                                    bg="#a5d6a7",
                                    font=("Arial", 10),
                                    width=12)
        botao_concluidas.pack(side="left", padx=5)

        # Carrega as tarefas do banco de dados ao inicializar a aplicação.
        self.carregar_tarefas()

    # Define o método 'selecionar_tarefa', que é chamado quando o usuário
    # seleciona uma tarefa no Treeview.
    def selecionar_tarefa(self, event):
        """
        Este método preenche os campos de entrada com os dados da tarefa
        selecionada no Treeview, permitindo que o usuário visualize e edite a tarefa.
        """
        # Obtém o item selecionado no Treeview.
        selecao = self.arvore_tarefas.selection()
        
        # Verifica se há uma seleção válida.
        if selecao:
            # Obtém o ID do item selecionado (que corresponde ao _id do MongoDB).
            item_selecionado = selecao[0]
            self.id_tarefa_selecionada = item_selecionado
            
            # Obtém os valores do item selecionado no Treeview.
            valores = self.arvore_tarefas.item(item_selecionado, "values")
            
            # Preenche os campos de entrada com os valores da tarefa selecionada.
            self.entrada_titulo.delete(0, tk.END)
            self.entrada_titulo.insert(0, valores[0])
            
            self.texto_descricao.delete("1.0", tk.END)
            self.texto_descricao.insert("1.0", valores[1])
            
            self.var_status.set(valores[2])

    # Define o método 'excluir_tarefa', responsável por remover uma tarefa do banco de dados.
    def excluir_tarefa(self):
        """
        Este método exclui a tarefa selecionada do banco de dados MongoDB.
        Ele verifica se há uma tarefa selecionada e solicita confirmação do usuário
        antes de realizar a exclusão.
        """
        # Verifica se existe uma tarefa selecionada.
        if not self.id_tarefa_selecionada:
            messagebox.showwarning("Aviso", "Nenhuma tarefa selecionada para excluir.")
            return
        
        # Solicita confirmação do usuário antes de excluir.
        confirmacao = messagebox.askyesno("Confirmar Exclusão",
                                         "Tem certeza que deseja excluir esta tarefa?")
        
        # Se o usuário confirmar, procede com a exclusão.
        if confirmacao:
            # Remove a tarefa do banco de dados usando o _id.
            self.colecao.delete_one({"_id": ObjectId(self.id_tarefa_selecionada)})
            
            # Recarrega as tarefas no Treeview.
            self.carregar_tarefas()
            
            # Limpa os campos de entrada.
            self.limpar_campos_entrada()
            
            # Redefine o identificador da tarefa selecionada.
            self.id_tarefa_selecionada = None
            
            # Exibe mensagem de sucesso.
            messagebox.showinfo("Sucesso", "Tarefa excluída com sucesso!")

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

            # Insere cada tarefa no Treeview.
            # - "" especifica que o item será inserido na raiz do Treeview, ou seja, sem um pai.
            # - tk.END insere o item no final da lista.
            # - 'values' define os valores a serem exibidos nas colunas do Treeview.
            # - 'iid' atribui um identificador exclusivo ao item no Treeview,
            # aqui convertido do '_id' do MongoDB para string.
            self.arvore_tarefas.insert("", tk.END,
                                       values=(tarefa["titulo"], tarefa["descricao"], tarefa["status"]),
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

        # Verifica se o campo título está vazio.
        # Se o título não for fornecido, exibe uma mensagem de aviso
        # ao usuário usando o messagebox.
        if not titulo:

            messagebox.showwarning("Aviso", "O título da tarefa não pode estar vazio.")  # Exibe um alerta.
            return  # Interrompe a execução do método.

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


janela_principal = tk.Tk()
app = GerenciadorTarefasApp(janela_principal)
janela_principal.mainloop()
       