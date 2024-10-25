from random import randrange as num_aleatorio

class logica_do_jogo():
    '''
    :Descrição (pt-br):
    Classe que representa a logica do jogo da velha.
    responsavel em lidar com a matriz do jogo, os movimentos do jogador, uma resposta aos movimentos e verifica se há vencedores ou condições de fim de jogo.

    :Atributos:
    - status_jogo (bool): 
    Indica foi finalizado ou não. (True o jogo está ativo sem ganhadores ou empates. False represente uma possível vitória ou empate)
    - matriz_jogador (list): 
    Representa o estado atual da matriz do jogo (-1 representa espaço livre, 0 espaço preenchido pelo algoritmo e 1 espaço preenchido pelo jogador).
    - turno (int): 
    Indica de quem é o turno atual. (0 indica que a jogada é do algoritmo enquanto 1 é o jogador)

    *--------------------------------------*

    :Description (en):
    Class that represents the logic of the tic-tac-toe game.
    responsible for handling the game matrix, player movements, a response to movements and checking for winners or end-of-game conditions.

    :Attributes:
    - status_jogo (bool):
    Indicates whether the game has finished or not. (True indicates that the game is active with no winners or ties. False indicates a possible win or tie)
    - matriz_jogador (list):
    Represents the current state of the game matrix (-1 represents free space, 0 spaces filled by the algorithm and 1 space filled by the player).
    - turno (int):
    Indicates whose turn it is. (0 indicates that the move is by the algorithm while 1 is by the player)
    '''
    def __init__(self, status_jogo, matriz_jogador, turno):
        self._status_jogo = status_jogo
        self._matriz_jogador = matriz_jogador
        self._turno = turno

    @property
    def status_jogo(self):
        return self._status_jogo

    @status_jogo.setter
    def status_jogo(self, value):
        self._status_jogo = value

    @property
    def matriz_jogador(self):
        return self._matriz_jogador

    @matriz_jogador.setter
    def matriz_jogador(self, value):
        self._matriz_jogador = value

    @property
    def turno(self):
        return self._turno

    @turno.setter
    def turno(self, value):
        self._turno = value

    def alocar_na_matriz(self, celula_index):
        '''
        :Descrição (pt-br):
        Aloca um espaço na matriz_jogador com base no índice de célula fornecido. Esta função converte um index de uma lista linear com 9 
        posições em uma matriz 3x3 e verifica se as células estão disponíveis para preenchimento. Se for possível alocar espaço, preencha o campo
        com espaços e retorne o índice da lista. Se houver algum problema (por exemplo, a célula está cheia), retornará “N”.

        :Parâmetros:
        - celula_index (int): Índice da célula da lista linear (0 a 8) que representa o tabuleiro.

        :Retornos:
        - int: O índice da célula para ser preenchida de uma lista (0 a 8) se a jogada for válida.
        - str: Retorna `"N"` se o argumento for inválido ou se a ação adicional não for possível.

        :Regras de Negócio:
        - O jogador (representado por '1') realiza a jogada em seu turno e se a célula está disponível.
        - O bot (representado por '0') se move automaticamente em resposta ao último movimento do jogador.
        - Função `posicao_na_matriz` converte índices de listas lineares em posições de matrizes (linhas e colunas).
        - A função `bot_allocar_na_matriz` é utilizada para fazer o algoritmo do bot selecionar uma jogada válida (seja na ofensiva ou defensiva).

        :Comportamento:
        1. Verifica se o jogo está ativo (o estado do jogo é True).
        2. Converta o índice da célula (cell_index) para a posição (linha, coluna) no campo do jogo (player_matrix).
        3. Se a célula estiver vazia (-1), preencha-a com '1' no turno do jogador e retorne o índice da célula.
        4. Se for a vez do bot, o método `bot_allocar_na_matriz` é chamado para fazer um movimento em resposta ao último movimento do jogador,
        e preencher a célula '0'.
        5. Se o argumento for inválido ou se não for possível movê-lo, será retornado `"N"`.

        *--------------------------------------*

        :Description (en):
        Allocates a space in the matriz_jogador based on the cell index provided. This function converts a linear list with 9 positions into a 
        3x3 matrix and checks if the cells are available for filling. If space can be allocated, fill the field with spaces and return the list index. 
        If there is a problem (for example, the cell is filled), it returns “N”.

        :Parameters:
        - cell_index (int): Index of the cell in the linear list (0 to 8) that represents the board.

        :Returns:
        - int: The index of the filled cell in the list (0 to 8) if the move is valid.
        - str: Returns `N` if the argument is invalid or if the additional action is not possible.

        :Business Rules:
        - The player (represented by '1') makes the move on his turn and if the cell is available.
        - The bot (represented by '0') moves automatically in response to the player's last move.
        - The `position_in_matrix` function converts linear list indices into matrix positions (rows and columns).
        - The `bot_allocar_na_matriz` function is used to make the bot's algorithm select a valid move (either offensive or defensive).

        :Behavior:
        1. Checks if the game is active (the game state is True).
        2. Convert the cell index (cell_index) to the position (row, column) in the game field (player_matrix).
        3. If the cell is empty (-1), fill it with '1' on the player's turn and return the cell index.
        4. If it is the bot's turn, the `bot_allocar_na_matriz` method is called to make a move in response to the player's last move,
        and fill the cell with '0'.
        5. If the argument is invalid or if it is not possible to move it, `N` is returned.
        '''
        if self.status_jogo:
            posicao_matricial = self.posicao_na_matriz(celula_index)
            l = posicao_matricial[0]
            c = posicao_matricial[1]

            if self.matriz_jogador[l][c] == -1:

                self.matriz_jogador[l][c] = 1
                return celula_index

            elif self.turno == 0:
                jogada = self.bot_alocar_na_matriz(l, c)
                self.matriz_jogador[jogada[0]][jogada[1]] = 0

                celula_index = self.matriz_para_lista(jogada)
                return celula_index

        return "N"

    def bot_alocar_na_matriz(self, l, c):
        '''
        :Descrição (pt-br):
        Retorna um movimento valido com base na ultima movimentação do jogador. A resposta contra o jogador 
        podem ser: defensiva, ofensiva ou aleatória caso não haja uma movimentação que atrapalhe o jogador.

        :Parâmetros:
        - l (int): Índice da célula (0 a 2) que representa a linha na matriz, a qual o jogador havia preenchido.
        - c (int): Índice da célula (0 a 2) que representa a coluna na matriz, a qual o jogador havia preenchido.

        :Regras de Negócio:
        - verifica se existe uma possibilidade de ganhar, independente de qualquer movimento feito pelo jogador e retorna 
        a posição para finalizar o jogo com a vitória do algoritmo
        - Se não for possível vencer na próxima jogada, analisa possíveis movimentos de acordo com a situação atual a qual 
        o jogador está na iminência de vencer, desconsiderando lados (linhas, colunas e diagonais) a qual o jogador não pode ganhar
        - realiza um sorteio através de um gerador de números pseudo aleatório para determinar em qual lado deve ser realizar a jogada para impedir a vitória do jogador
        - Se o jogador não estiver na iminência de ganhar, verifique os lados a qual o jogador pode avançar com base em sua ultima jogada para realizar um sorteio e
        realizar uma jogada a qual atrapalhe o avanço do jogador  (ainda desconsiderando lados que não é possível a vitória do jogador)
        - Se não for possivel cria uma jogada com base na ultima movimentação do jogador, analisa qual celula da matriz está disponivel para alocar e retorna as posições para preenche-la.
    
        :Retorno:
        - Retorna as coordenadas (linha e coluna) onde o algoritimo deve alocar sua jogada.

        *--------------------------------------*

        :Description (en):
        Returns a valid move based on the player's last move. The response against the player can be: defensive, 
        offensive or random if there is no move that hinders the player.

        :Parameters:
        - l (int): Cell index (0 to 2) that represents the row in the matrix, which the player had filled.
        - c (int): Cell index (0 to 2) that represents the column in the matrix, which the player had filled.

        :Business Rules:
        - checks if there is a possibility of winning, regardless of any move made by the player and returns
        the position to end the game with the victory of the algorithm
        - If it is not possible to win in the next move, analyzes possible moves according to the current situation in which
        the player is on the verge of winning, disregarding sides (rows, columns and diagonals) in which the player cannot win
        - performs a draw using a pseudo random number generator to determine on which side the move should be made to prevent the player from winning
        - If the player is not on the verge of winning, checks the sides to which the player can advance based on his last move to perform a draw and
        perform a move that hinders the player's advance (still disregarding sides in which the player cannot win)
        - If it is not possible, creates a move based on the player's last move, analyzes which cell of the matrix is ​​available for allocation and returns the positions to fill it.

        :Return:
        - Returns the coordinates (row and column) where the algorithm should allocate its move.
        '''
        ganhar = self.chance_de_ganhar()
        if ganhar:
            return ganhar

        possiveis_movimentos = self.analisar_matriz_retornar_pontos(l, c)

        proximo_passo = [] # 0 - linha | 1 - col | 2 - diagonal | 3 - inverso
        for i in range(4):
            if possiveis_movimentos[i] == 2:
                proximo_passo.append(i)
        
        if len(proximo_passo) > 0: # Se necessario realizar uma defesa
            preencher = self.forcar_em_preencher(proximo_passo, l, c)

        else:  # Se não é necessario realizar uma defesa, apenas atrapalhe o jogador
            proximo_passo = [] # 0 - linha | 1 - col | 2 - diagonal | 3 - inverso
            for i in range(4):
                if possiveis_movimentos[i] == 1:
                    proximo_passo.append(i)

            if len(proximo_passo) > 0:
                preencher = self.forcar_em_preencher(proximo_passo, l, c)

            else:
                preencher = self.jogada_de_seguranca()

        return preencher
    
    def chance_de_ganhar(self):
        '''
        :Descrição (pt-br):
        verifica se existe uma possibilidade de ganhar em seu turno

        :Retornos:
        - list: Uma lista contendo os índices da linha e coluna para o preenchimento, se for possível vencer neste turno.
        - bool: Retorna False indicando que não é possível vencer nesta jogada.

        :Comportamento:
        - A função percorre todas as linhas, colunas e diagonais da matriz do jogo para verificar se há duas células preenchidas pelo
         algoritmo (representadas por 0) e uma célula vazia (-1), o que indica uma jogada vencedora disponível.
        - Se houver uma jogada vencedora, retorna as coordenadas (linha, coluna) dessa célula. Caso contrário, retorna False.

        *--------------------------------------*

        :Description (en):
        checks if there is a possibility of winning on your turn

        :Returns:
        - list: A list containing the row and column indexes to be filled in, if it is possible to win this turn.
        - bool: Returns False indicating that it is not possible to win this turn.

        :Behavior:
        - The function goes through all the rows, columns and diagonals of the game matrix to check if there are two cells filled in by the algorithm (represented by 0) and one empty cell (-1), which indicates a winning move available.
        - If there is a winning move, it returns the coordinates (row, column) of that cell. Otherwise, it returns False.
        '''

        for l in range(3):
            linha = 0

            for c in range(3):
                if self.matriz_jogador[l][c] == 0:
                    linha += 1
                elif self.matriz_jogador[l][c] == 1: # linha l perdida
                    linha = 0
                    break

            if linha == 2:
                for c in range(3):
                    if self.matriz_jogador[l][c] == -1: # ganhou na linha
                        return [l, c]

        for c in range(3):
            col = 0

            for l in range(3):
                if self.matriz_jogador[l][c] == 0:
                    col += 1
                elif self.matriz_jogador[l][c] == 1: # col c perdida
                    col = 0
                    break

            if col == 2:
                for l in range(3):
                    if self.matriz_jogador[l][c] == -1: # ganhou na col
                        return [l, c]

        diagonal = 0
        inversa = 0
        for i in range(3):
            if self.matriz_jogador[i][i] == 0:
                diagonal += 1
            elif self.matriz_jogador[i][i] == 1:
                diagonal = 0

            if self.matriz_jogador[i][2-i] == 0:
                inversa += 1
            elif self.matriz_jogador[i][2-i] == 1:
                inversa = 0

        if diagonal == 2 or inversa == 2:
            for i in range(3):
                if self.matriz_jogador[i][i] == -1: # Ganhou na diagonal
                    return [i, i]
                
                if self.matriz_jogador[i][2-i] == -1: # Ganhou na inversa
                    return [i, 2-i]
                
        return False

    def analisar_matriz_retornar_pontos(self, l, c):
        '''
        :Descrição (pt-br):
        Verifica se existe uma vantagem com base nos movimentos feitos pelo jogador, analisando a linha, coluna, diagonal e diagonal inversa da jogada recente.

        :Parâmetros:
        - l (int): Índice da célula (0 a 2) que representa a linha na matriz, a qual o jogador havia preenchido.
        - c (int): Índice da célula (0 a 2) que representa a coluna na matriz, a qual o jogador havia preenchido.

        :Retorno:
        - list: Uma lista de inteiros que representam as "vantagens" do jogador em diferentes direções. Cada valor da lista corresponde ao número de células
        preenchidas pelo jogador (1) nas seguintes direções:
            - [0]: Vantagem na linha da última jogada.
            - [1]: Vantagem na coluna da última jogada.
            - [2]: Vantagem na diagonal principal.
            - [3]: Vantagem na diagonal inversa.

        :Comportamento:
        - A função analisa a linha, coluna, diagonal e diagonal inversa relacionadas à última jogada feita pelo jogador
        (representada pelos índices `l` e `c`) e conta quantas células nessa linha/coluna/diagonais estão preenchidas pelo jogador (1).
        - Retorna uma lista de inteiros que indicam quantas células estão preenchidas em cada direção.
        - Quando uma direção contem o valor 0, isto indica que o jogador não tem mais como avançar naquela linha, coluna ou diagonal específica, ou seja, 
        não há vantagens em continuar nesta direção (os pontos são zerados).
        
        *--------------------------------------*

        :Description (en):
        Checks if there is an advantage based on the moves made by the player, analyzing the row, column, diagonal and reverse diagonal of the recent move.

        :Parameters:
        - l (int): Cell index (0 to 2) that represents the row in the matrix, which the player had filled.
        - c (int): Cell index (0 to 2) that represents the column in the matrix, which the player had filled.

        :Returns:
        - list: A list of integers that represent the player's "advantages" in different directions. Each value in the list corresponds to the number of cells
        filled by the player (1) in the following directions:
        - [0]: Advantage in the row of the last move.
        - [1]: Advantage in the column of the last move.
        - [2]: Advantage in the main diagonal.
        - [3]: Advantage in the reverse diagonal.

        :Behavior:
        - The function analyzes the row, column, diagonal and inverse diagonal related to the last move made by the player
        (represented by the indexes `l` and `c`) and counts how many cells in that row/column/diagonals are filled by the player (1).
        - Returns a list of integers that indicate how many cells are filled in each direction.
        - When a direction contains the value 0, this indicates that the player can no longer advance in that specific row, column or diagonal, that is,
        there is no advantage in continuing in that direction (the points are reset).
        '''
        ponto_linha = 0
        ponto_col = 0
        ponto_diagonal = 0
        ponto_diagonal_inversa = 0

        linha_perdida = False
        col_perdida = False
        diagonal_perdida = False
        diagonal_inversa_perdida = False

        for i in range(3):
            if self.matriz_jogador[l][i] == 1: # Fixa a linha e analisa as colunas
                ponto_linha += 1

            elif self.matriz_jogador[l][i] == 0:
                linha_perdida = True
            
            if self.matriz_jogador[i][c] == 1: # Fixa a colunas e analisa as linha
                ponto_col += 1

            elif self.matriz_jogador[i][c] == 0:
                col_perdida = True

            if self.matriz_jogador[i][i] == 1:
                ponto_diagonal += 1
            
            elif self.matriz_jogador[i][i] == 0:
                diagonal_perdida = True

            if self.matriz_jogador[i][2-i] == 1:
                ponto_diagonal_inversa += 1

            elif self.matriz_jogador[i][2-i] == 0:
                diagonal_inversa_perdida = True

        proximo_passo = [ponto_linha, ponto_col, ponto_diagonal, ponto_diagonal_inversa]

        if linha_perdida:
            proximo_passo[0] = 0 # Sem espaços: linha l
        if col_perdida:
            proximo_passo[1] = 0 # Sem espaços: coluna c
        if diagonal_perdida:
            proximo_passo[2] = 0 # Sem espaços: diagonal
        if diagonal_inversa_perdida:
            proximo_passo[3] = 0 # Sem espaços: inversa

        return proximo_passo

    def forcar_em_preencher(self, proximo_passo, l, c):
        '''
        :Descrição (pt-br):
        Sorteia uma jogada a qual atrapalhara o jogador.

        :Parâmetros:
        - proximo_passo (lista): Uma lista de inteiros contendo a representação dos lados. os valores podem ser:
            - 0: movimento na linha da última jogada.
            - 1: movimento na coluna da última jogada.
            - 2: movimento na diagonal principal.
            - 3: movimento na diagonal inversa.
        - l (int): Índice da célula (0 a 2) que representa a linha na matriz, a qual o jogador havia preenchido.
        - c (int): Índice da célula (0 a 2) que representa a coluna na matriz, a qual o jogador havia preenchido.

         :Comportamento:
        - A função recebe a lista `proximo_passo`, que indica as direções possíveis onde uma jogada pode ser feita para bloquear o jogador. 
        - Um valor é sorteado da lista `proximo_passo` usando a função `num_aleatorio`, que seleciona um dos lados disponíveis aleatoriamente.
        - Dependendo do lado sorteado (linha, coluna, diagonal ou diagonal inversa), a função chama uma das funções auxiliares (`analise_linha`, `analise_coluna`, `analise_diagonal`, `analise_diagonal_inversa`) para verificar quais células nessa direção estão disponíveis.
        - Após identificar as células disponíveis, outro sorteio é feito para escolher uma célula aleatória entre as disponíveis.
        - A função então retorna a linha e a coluna da célula sorteada para ser preenchid

        :Retornos:
        - list: Uma lista contendo os índices da linha e coluna para o preenchimento, respectivamente.

        *--------------------------------------*

        :Description (en):
        Draws a move that will hinder the player.

        :Parameters:
        - proximo_passo (list): A list of integers containing the representation of the sides. The values ​​can be:
            - 0: movement in the row of the last move.
            - 1: movement in the column of the last move.
            - 2: movement in the main diagonal.
            - 3: movement in the reverse diagonal.
        - l (int): Cell index (0 to 2) that represents the row in the matrix, which the player had filled.
        - c (int): Cell index (0 to 2) that represents the column in the matrix, which the player had filled.

        :Behavior:
        - The function receives the list `proximo_passo`, which indicates the possible directions where a move can be made to block the player.
        - A value is drawn from the list `proximo_passo` using the function `num_aleatorio`, which selects one of the available sides randomly.
        - Depending on the side drawn (row, column, diagonal or reverse diagonal), the function calls one of the auxiliary functions (`analise_linha`, `analise_coluna`, `analise_diagonal`, `analise_diagonal_inversa`) to check which cells in that direction are available.
        - After identifying the available cells, another draw is made to choose a random cell from those available.
        - The function then returns the row and column of the drawn cell to be filled.

        :Returns:
        - list: A list containing the row and column indices to be filled, respectively.
        '''
        focar_em = proximo_passo[num_aleatorio(0, len(proximo_passo), 1)]
        match focar_em:
                case 0:
                    sorteio = self.analise_linha(l) # fixa a linha a e analisa as colunas
                    c = sorteio[num_aleatorio(0, len(sorteio), 1)]
                    preencher = [l, c]
                case 1:
                    sorteio = self.analise_coluna(c) # fixa a coluna e analisa as linhas
                    l = sorteio[num_aleatorio(0, len(sorteio), 1)]
                    preencher = [l, c]
                case 2:
                    sorteio = self.analise_diagonal()
                    d = sorteio[num_aleatorio(0, len(sorteio), 1)]
                    preencher = [d, d]
                case 3:
                    sorteio = self.analise_diagonal_inversa()
                    i = sorteio[num_aleatorio(0, len(sorteio), 1)]
                    preencher = [i, 2-i]
        return preencher

    def jogada_de_seguranca(self):
        '''
        :Descrição (pt-br):
        Percorre por toda a matriz até encontrar uma célula vazia para retornar sua coordenadas

        :Retornos:
        - list: Uma lista contendo os índices da linha e coluna para o preenchimento, respectivamente.

        *--------------------------------------*

        :Description (en):
        It goes through the entire matrix until it finds an empty cell to return its coordinates

        :Returns:
        - list: A list containing the row and column indices to be filled, respectively.
        '''
        for l in range(3):
            for c in range(3):
                if self.matriz_jogador[l][c] == -1:
                    return [l, c]

    def analise_linha(self, l):
        '''
        :Descrição (pt-br):
        utiliza a ultima movimentação feita pelo jogador para verificar se na linha ainda tem algumas células vazias (representadas por -1)

        :Retornos:
        - list: Uma lista contendo valores inteiros de 0 a 2 indicando células vazias.

        *--------------------------------------*

        :Description (en):
        uses the last movement made by the player to check if there are still any empty cells in the line (represented by -1)

        :Returns:
        - list: A list containing integer values ​​from 0 to 2 indicating empty cells.
        '''
        espacos_disponiveis = []
        for i in range(3):
            if self.matriz_jogador[l][i] == -1:
                espacos_disponiveis.append(i)
        return espacos_disponiveis

    def analise_coluna(self, c):
        '''
        :Descrição (pt-br):
        utiliza a ultima movimentação feita pelo jogador para verificar se na coluna ainda tem algumas células vazias (representadas por -1)

        :Retornos:
        - list: Uma lista contendo valores inteiros de 0 a 2 indicando células vazias.

        *--------------------------------------*

        :Description (en):
        uses the last movement made by the player to check if there are still any empty cells in the column (represented by -1)

        :Returns:
        - list: A list containing integer values ​​from 0 to 2 indicating empty cells.
        '''
        espacos_disponiveis = []
        for i in range(3):
            if self.matriz_jogador[i][c] == -1:
                espacos_disponiveis.append(i)
        return espacos_disponiveis

    def analise_diagonal(self):
        '''
        :Descrição (pt-br):
        verifica se na diagonal principal ainda tem algumas células vazias (representadas por -1)

        :Retornos:
        - list: Uma lista contendo valores inteiros de 0 a 2 indicando células vazias.

        *--------------------------------------*

        :Description (en):
        checks if there are still some empty cells in the main diagonal (represented by -1)

        :Returns:
        - list: A list containing integer values ​​from 0 to 2 indicating empty cells.
        '''
        espacos_disponiveis = []
        for i in range(3):
            if self.matriz_jogador[i][i] == -1:
                espacos_disponiveis.append(i)
        return espacos_disponiveis

    def analise_diagonal_inversa(self):
        '''
        :Descrição (pt-br):
        verifica se na diagonal inversa ainda tem algumas células vazias (representadas por -1)

        :Retornos:
        - list: Uma lista contendo valores inteiros de 0 a 2 indicando células vazias.

        *--------------------------------------*

        :Description (en):
        checks if there are still some empty cells in the reverse diagonal (represented by -1)

        :Returns:
        - list: A list containing integer values ​​from 0 to 2 indicating empty cells.
        '''
        espacos_disponiveis = []
        for i in range(3):
            if self.matriz_jogador[i][2-i] == -1:
                espacos_disponiveis.append(i)
        return espacos_disponiveis

    def alterar_turno(self):
        '''
        :Descrição (pt-br):
        Verifica o valor atual do turno e altera entre 0 e 1, onde 0 representa o turno do algoritmo e 1 o turno do jogador.

        *--------------------------------------*

        :Description (en-us):
        Checks the current turn value and changes it between 0 and 1, where 0 represents the algorithm's turn and 1 the player's turn.
        '''
        if self.turno == 0:
            self.turno = 1
        else:
            self.turno = 0

    def analisar_matriz(self, celula):
        '''
        :Descrição (pt-br):
        A função verifica se, após a última jogada realizada em uma determinada célula, o jogador que está com a vez (indicado por `self.turno`) 
        pode vencer o jogo, seja por linha, coluna, diagonal principal ou diagonal inversa. Se o jogo for vencido, a função retorna
        um valor indicando o tipo de vitória. Caso todas as células da matriz estejam preenchidas e não haja um vencedor, a
        função indica um empate. Se nenhum desses cenários ocorrer, a função retorna `False`, indicando que o jogo continua.

        :Parâmetros:
        - celula (list): Uma lista contendo os índices da linha e da coluna (em formato `[l, c]`) onde a última jogada foi realizada.

        :Retornos:
        - str: Um valor indicando o tipo de vitória ou empate:
            - `"l{l}"`: Vitória por linha, onde `{l}` é o índice da linha.
            - `"c{c}"`: Vitória por coluna, onde `{c}` é o índice da coluna.
            - `"d"`: Vitória na diagonal principal.
            - `"i"`: Vitória na diagonal inversa.
            - `"e"`: Indica empate, caso todas as células estejam preenchidas sem um vencedor.
        - bool: Retorna False se o jogo continuar sem vitória ou empate.

        :Comportamento: 
        - A função analisa todos os lados que são referentes a célula da última jogada e verifica se todas 
        as posições nessas direções estão preenchidas pelo jogador atual (indicado por `self.turno`).
        - Caso o jogador tenha completado um dos lados, a função retorna um código correspondente ("l", "c", "d", "i").
        - Se todos os espaços da matriz estiverem preenchidos e não houver um vencedor, retorna "e" para indicar empate.
        - Se nenhum desses cenários for verdadeiro, a função retorna `False` e o jogo continua.

        *--------------------------------------*

        :Description (en):
        The function checks whether, after the last move made in a given cell, the player whose turn it is (indicated by `self.turno`)
        can win the game, whether by row, column, main diagonal or reverse diagonal. If the game is won, the function returns
        a value indicating the type of victory. If all cells of the matrix are filled and there is no winner, the
        function indicates a draw. If none of these scenarios occur, the function returns `False`, indicating that the game continues.

        :Parameters:
        - cell (list): A list containing the indexes of the row and column (in `[l, c]` format) where the last move was made.

        :Returns:
        - str: A value indicating the type of victory or draw:
        - `"l{l}"`: Victory by row, where `{l}` is the row index. - `"c{c}"`: Win by column, where `{c}` is the column index.
        - `"d"`: Win on the main diagonal.
        - `"i"`: Win on the reverse diagonal.
        - `"e"`: Indicates a draw, if all cells are filled without a winner.
        - bool: Returns False if the game continues without a win or draw.

        :Behavior:
        - The function analyzes all sides that refer to the cell of the last move and checks if all positions in these directions are filled by the current player (indicated by `self.turno`).
        - If the player has completed one of the sides, the function returns a corresponding code ("l", "c", "d", "i").
        - If all spaces in the matrix are filled and there is no winner, it returns `"e"` to indicate a draw.
        - If none of these scenarios are true, the function returns `False` and the game continues.
        '''
        l = celula[0]
        c = celula[1]

        ponto_linha = 0
        ponto_col = 0
        for i in range(3):
            if self.matriz_jogador[l][i] == self.turno:
                ponto_linha += 1
            if self.matriz_jogador[i][c] == self.turno:
                ponto_col += 1

        if ponto_col == 3:
            self.status_jogo = False
            return f"c{c}"
        elif ponto_linha == 3:
            self.status_jogo = False
            return f"l{l}"

        elif l == c:
            ponto_diagonal = 0
            for i in range(3):
                if self.matriz_jogador[i][i] == self.turno:
                    ponto_diagonal += 1

            if ponto_diagonal == 3:
                self.status_jogo = False
                return "d"
                
        elif l+c == 2:  # diagonal inversa
            ponto_diagonal = 0
            for i in range(3):
                if self.matriz_jogador[i][2-i] == self.turno:
                    ponto_diagonal += 1

            if ponto_diagonal == 3:
                self.status_jogo = False
                return "i"

        indisponivel = 0
        for linha in self.matriz_jogador:
            for coluna in linha:
                if coluna != -1:
                    indisponivel += 1

        if indisponivel == 9:
            return "e"

        return False

    def posicao_na_matriz(self, index):
        '''
        :Descrição (pt-br):
        utiliza informações de um index de uma lista linear e convertem em uma cordenada de uma matriz

        :Parâmetros:
        - index (int): um inteiro que representa a posição em uma lista linear (de 0 a 8)

        :Retornos:
        - list: Uma lista contendo os índices da linha e coluna, respectivamente.

        *--------------------------------------*

        :Description (en):
        uses information from an index of a linear list and converts it into a coordinate of a matrix

        :Parameters:
        - index (int): an integer that represents the position in a linear list (from 0 to 8)

        :Returns:
        - list: A list containing the row and column indices, respectively.
        '''
        return [index//3, index%3]

    def matriz_para_lista(self, matriz):
        '''
        :Descrição (pt-br):
        utiliza informações de coordenadas na matriz para convertem em um index de uma lista linear

        :Parâmetros:
        - matriz (list): Uma lista contendo os índices da linha e coluna, respectivamente.

        :Retornos:
        - int: um inteiro que representa a posição em uma lista linear (de 0 a 8)

        *--------------------------------------*

        :Description (en-us):
        uses coordinate information in the matrix to convert it into an index of a linear list

        :Parameters:
        - matrix (list): A list containing the row and column indices, respectively.

        :Returns:
        - int: an integer representing the position in a linear list (from 0 to 8)
        '''
        linha = matriz[0]*3
        index = linha + matriz[1]
        return index

    @classmethod
    def criar_matriz_jogador(self):
        '''
        :Descrição (pt-br):
        Esta função cria e retorna uma matriz 3x3 que representa o tabuleiro do jogo. Cada célula da matriz contém o valor `-1`, 
        indicando que o espaço está vazio e disponível para jogadas.

        :Retornos:
        - list: Uma lista de listas representando as linhas e colunas do tabuleiro. Cada célula contém o valor `-1`, que representa um espaço livre.

        *--------------------------------------*

        :Description (en):
        This function creates and returns a 3x3 matrix that represents the game board. Each cell of the matrix contains the value `-1`,
        indicating that the space is empty and available for moves.

        :Returns:
        - list: A list of lists representing the rows and columns of the board. Each cell contains the value `-1`, which represents a free space.
        '''
        matriz = []
        for l in range(3):
            linha = []
            for c in range(3):
                linha += [-1]
            matriz += [linha]
        return matriz

    def reiniciar_partida(self):
        '''
        :Descrição (pt-br):
        Esta função é responsável por reiniciar o jogo, restaurando os atributos da classe para seus 
        estados iniciais, permitindo que uma nova partida comece.

        :Comportamento:
        - O turno é redefinido para o jogador 1.
        - O status do jogo é ajustado para `True`, indicando que o jogo está em andamento.
        - A matriz que representa o tabuleiro é recriada, com todos os espaços livres (valores `-1`).

        *--------------------------------------*

        :Description (en):
        This function is responsible for restarting the game, restoring the class attributes to their initial states, allowing a new game to begin.

        :Behavior:
        - The turn is reset to player 1.
        - The game status is set to `True`, indicating that the game is in progress.
        - The matrix representing the board is recreated, with all free spaces (`-1` values).
        '''
        self.turno = 1
        self.status_jogo = True
        self.matriz_jogador = self.criar_matriz_jogador()