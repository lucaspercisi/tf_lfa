import os
import csv
import copy

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
EPSILON = '&'


def is_sublist(sublist, list):
    return set(sublist) <= set(list)


class AFNDLine(dict):
    def __init__(self, initial=False, final=False, error=False, *args, **kwargs):
        super(AFNDLine, self).__init__(*args, **kwargs)
        self.initial = initial
        self.final = final
        self.error = error


class Constructor(object):

    def __init__(self):
        self.grammar_path = os.path.join(dir_path, 'inputs', 'tokens_GRs.txt')
        self.csv_path = os.path.join(dir_path, 'outputs', 'AFD_output.csv')
        self.afnd = dict()
        self.afd = dict()
        self.file = open(self.grammar_path, 'r')
        self.tokens = []
        self.alphabet = []  # alfabeto da linguagem
        self.initial_state = 0  # estado inicial
        self.state = 0  # estado incremento
        self.error_state = None  # estado de erro
        self.reachable = []  # lista de estados atingíveis
        self.alive = []  # lista de estados vivos
        self.test_alive = []  # lista auxiliar de testes de estados vivos
        self.epsilon_paths = []  # lista de listas com os conjuntos de epsilon transição
        self.related_states = {}  # dicionário para relacionar indeterminismos à novos estados
        self.afnd_line(self.initial_state, initial=True)  # cria o estado inicial

        # Dados da tabela de símbolos (Lucas)
        self.source_code_path = os.path.join(dir_path, 'inputs', 'sourcecode.txt')  # Local do código-fonte
        self.st = list()  # Tabela de Símbolos
        self.separators = list()  # Separadores da linguagem
        self.double_separators = list()  # Separadores da linguagem
        self.sourceCode = list(open(self.source_code_path, 'r'))  # codigo fonte inserido numa lista para criação da tabela de simbolos

    def print_afnd(self):
        print('-------------------------------------------------------------------------------------------------------')
        print('----------------------------------------------<<< AFND >>>---------------------------------------------')
        print('-------------------------------------------------------------------------------------------------------')
        for key, value in self.afnd.items():
            i = ''
            f = ''
            e = ''
            if value.initial:
                i = '->'
            if value.final:
                f = '*'
            if value.error:
                e = '(E)'
            print('{}{}{}{}: {}'.format(i, f, e, key, value))

    def print_afd(self):
        print('-------------------------------------------------------------------------------------------------------')
        print('----------------------------------------------<<< AFD >>>----------------------------------------------')
        print('-------------------------------------------------------------------------------------------------------')
        for key, value in self.afd.items():
            i = ''
            f = ''
            e = ''
            if value.initial:
                i = '->'
            if value.final:
                f = '*'
            if value.error:
                e = '(E)'
            print('{}{}{}{}: {}'.format(i, f, e, key, value))

    def update_alphabet(self, symbols=None):
        """
        Atualiza o alfabeto da linguagem
        :param symbols: list: lista de símbolos que serão adicionados ao alfabeto
        """
        if symbols and not is_sublist(symbols, self.alphabet):
            self.alphabet = list(set(self.alphabet+symbols))

    def afnd_line(self, state, initial=False, final=False, alphabet=None):
        """
        Cria uma nova linha no AFND com o estado e preenche as colunas com listas vazias em cada posição
        correspondente do alfabeto
        :param state: int: estado a ser criado
        :param initial: bool: se o estado informado é inicial
        :param final: bool: se o estado informado é final
        :param alphabet: list: lista de chars
        """
        if alphabet:
            self.update_alphabet(alphabet)  # atualiza o alfabeto

        if state not in self.afnd:  # se o estado não existe cria-se uma nova linha
            self.afnd[state] = AFNDLine(initial=initial, final=final)

        # atualiza se o estado é inicial e/ou final
        if initial:
            self.afnd[state].initial = initial
        if final:
            self.afnd[state].final = final

        for sym in self.alphabet:  # cria uma coluna para cada símbolo do alfabeto informado que ainda não existe
            if sym not in self.afnd[state]:
                self.afnd[state][sym] = []

    def afd_line(self, state, initial=False, final=False, alphabet=None):
        """
        Cria uma nova linha no AFD com o estado e preenche as colunas com listas vazias em cada posição
        correspondente do alfabeto
        :param state: int: estado a ser criado
        :param initial: bool: se o estado informado é inicial
        :param final: bool: se o estado informado é final
        :param alphabet: list: lista de chars
        """
        if alphabet:
            self.update_alphabet(alphabet)  # atualiza o alfabeto

        if state not in self.afd:  # se o estado não existe cria-se uma nova linha
            self.afd[state] = AFNDLine(initial=initial, final=final)

        # atualiza se o estado é inicial e/ou final
        if initial:
            self.afd[state].initial = initial
        if final:
            self.afd[state].final = final

        for sym in self.alphabet:  # cria uma coluna para cada símbolo do alfabeto informado que ainda não existe
            if sym not in self.afd[state]:
                self.afd[state][sym] = []

    def clean_afd(self):
        """
        Limpa o AFD e adiciona o estado de erro nos não mapeados
        """
        if not self.error_state:
            self.afd_line(self.state+1, final=True)
            self.afd[self.state+1].error = True
            self.error_state = self.state+1
            self.state += 1

        for state in list(self.afd):
            for sym in self.alphabet:  # cria uma coluna para cada símbolo do alfabeto informado que ainda não existe
                if (sym not in self.afd[state]) or (self.afd[state][sym] == []):
                    self.afd[state][sym] = self.error_state
                else:
                    self.afd[state][sym] = self.afd[state][sym][0]

    def update_afnd(self):
        """
        Preenche as lacunas vazias do AFND
        """
        for state in list(self.afnd):
            self.afnd_line(state)

    def add_afnd_step(self, origin_state, dest_state, symbol, origin_initial, origin_final, dest_initial, dest_final):
        """
        Adiciona um passo no autômato
        :param origin_state: int: estado de origem
        :param dest_state: int: estado de destino
        :param symbol: str: símbolo reconhecido
        :param origin_initial: bool: estado de origem é inicial?
        :param origin_final: bool: estado de origem é final?
        :param dest_initial: bool: estado de destino é inicial?
        :param dest_final: bool: estado de destino é final?
        """
        self.afnd_line(origin_state, origin_initial, origin_final, [symbol])
        self.afnd_line(dest_state, dest_initial, dest_final)

        self.afnd[origin_state][symbol].append(dest_state)
        self.afnd[origin_state][symbol] = list(set(self.afnd[origin_state][symbol]))

    def add_afd_step(self, origin_state, dest_state, symbol, origin_initial, origin_final, dest_initial, dest_final, replace=False):
        """
        Adiciona um passo no autômato determinístico
        :param origin_state: int: estado de origem
        :param dest_state: int: estado de destino
        :param symbol: str: símbolo reconhecido
        :param origin_initial: bool: estado de origem é inicial?
        :param origin_final: bool: estado de origem é final?
        :param dest_initial: bool: estado de destino é inicial?
        :param dest_final: bool: estado de destino é final?
        :param replace: bool: se setado sbrescreve os estados pelo novo destino em vez de apenas colocá-lo junto aos existentes
        """
        self.afd_line(origin_state, origin_initial, origin_final, [symbol])
        self.afd_line(dest_state, dest_initial, dest_final)

        if replace:
            self.afd[origin_state][symbol] = [dest_state]
        else:
            self.afd[origin_state][symbol].append(dest_state)
        self.afd[origin_state][symbol] = list(set(self.afd[origin_state][symbol]))

    def productions_to_dict(self, productions=''):
        """
        Transforma o lado direito das gramáticas em dados estruturados para que possamos trabalhar
        :param productions: str: o que vem depois de ::= na linha
        :return: dict: dicionário de valores com o padrão {produção: ESTADO}
        """
        new_data = {}
        final = False  # verifica se o estado é final (se há épsilon produção)
        productions = productions.split('|')

        for prod in productions:
            prod = prod.strip()  # elimina eventuais espaços extras entre | e a produção

            if prod:
                if prod == EPSILON:  # épsilon produção
                    final = True
                    continue
                elif prod.startswith('<'):  # épsilon transição
                    state = prod.replace('<', '').replace('>', '')
                    symbol = EPSILON
                else:  # GR linear à direita (padrão adotado)
                    symbols = prod.split('<')
                    symbol = symbols[0]

                    try:
                        state = symbols[1].replace('>', '')
                    except IndexError:  # há somente um símbolo terminal, deve ir para um estado final
                        state = '#'

                if symbol not in new_data:
                    new_data[symbol] = [state]
                elif state not in new_data[symbol]:
                    new_data[symbol].append(state)

        return new_data, final

    def _get_reachable(self, current_state):
        """
        Função recursiva que obtém os estados atingíveis.
        Vai à partir do estado inicial e coleta todos os estados atingíveis à partir dele
        depois faz o mesmo para cada um que foi coletado até testar todos os estados que aparecem
        :param current_state: int: estado atual
        """
        if current_state not in self.reachable:
            self.reachable.append(current_state)

        if current_state in self.test_alive:
            self.test_alive.remove(current_state)
            values = list(set(self.afd[current_state].values()))
            if current_state in values:
                values.remove(current_state)
            for state in values:
                self._get_reachable(state)

    def get_reachable(self, state):
        """
        Obtém apenas os estados atingíveis, partindo do estado inicial e chamando recursivamente para
        cada estado atingido
        :param state: int: estado inicial
        :return: list: lista com os números dos estados atingívis
        """
        self.test_alive = list(self.afd)
        self._get_reachable(state)
        return self.reachable

    def remove_unreachable(self):
        """
        Remove os estados inatingíveis do AFD
        """
        keep = self.get_reachable(self.initial_state)
        unreachable = list(set(self.afd.keys()).difference(keep))

        print('\nRemovendo estados inalcançáveis {}\n'.format(unreachable))

        for state in unreachable:
            del self.afd[state]

    def _get_alive(self, path=[], living_states=[]):
        """
        Chamada recursiva para obter os estados vivos do AFD, considera vivos todos os estados de um caminho que
        chega à um estado final. Faz uma busca em profundidade para obtê-los.
        :param path: list: sequência de estados que representa um caminho dentro do AFD
        :param living_states: list: próximos estados dos caminho, se chegar a um final eles estão vivos
        """
        for live in living_states:
            if self.afd[live].final and not is_sublist(path, self.alive):
                self.alive += path
        if self.test_alive:
            self.test_alive = set(self.test_alive) - set(path)
            living_states = set(living_states) - set(path)
            for state in living_states:
                path.append(state)
                self._get_alive(path, list(set(self.afd[state].values())))

    def get_alive(self, state):
        """
        Obtém os estados vivos do AFD
        :param state: int: estado inicial
        """
        self.test_alive = list(set(self.afd))
        self._get_alive([state], list(set(self.afd[state].values())))
        return self.alive

    def remove_dead(self):
        """
        Remove os estados mortos do AFD
        """
        keep = self.get_alive(self.initial_state)
        dead = list(set(self.afd.keys()).difference(keep))

        print('\nRemovendo estados mortos {}\n'.format(dead))

        for state in dead:
            del self.afd[state]

    def _get_epsilon(self, path=[], epsilon_states=[]):
        """
        Chamada recursiva para obter as transições por EPSILON entre os estados
        :param path: list: caminho atual
        :param epsilon_states: estados que estão na transição por EPSILON do último estado do caminho
        """
        if epsilon_states and not is_sublist(epsilon_states, path):  # loop de transições épsilon
            for state in epsilon_states:
                self._get_epsilon(path+[state], self.afnd[state][EPSILON])
        elif len(path) > 1:
            add = True
            for l in self.epsilon_paths:
                if is_sublist(path, l):
                    add = False
                    break

            if add:
                self.epsilon_paths.append(path)

    def get_epsilon(self):
        """
        Carrega uma lista de listas, onde cada lista interna é uma transição por épsilon entre os seus estados
        :return: list: transições por EPSILON
        """
        for state in list(self.afnd):
            self._get_epsilon([state], self.afnd[state][EPSILON])
        return self.epsilon_paths

    def remove_epsilon(self):
        """
        Remove as transições por EPSILON
        """
        if EPSILON in self.alphabet:  # verifica se há transições por EPSILON no AFND
            self.get_epsilon()  # cria os caminhos das transições

            print('\n\nRemovendo as épsilon transições {}\n\n'.format(self.epsilon_paths))

            for i in range(len(self.epsilon_paths)):
                path = self.epsilon_paths[i]

                main_state = path[0]  # o primeiro estado da transição receberá as mudanças
                for state in path[1:]:  # para cada um dos demais estados
                    for symbol in list(self.afnd[main_state]):  # as produções desse estado também serão do principal
                        if symbol != EPSILON:
                            self.afnd[main_state][symbol] = list(set(self.afnd[main_state][symbol]+self.afnd[state][symbol]))

                    for st, line in self.afd.items():  # as transições do estado de épsilon também irão ao principal
                        for sy, sts in line.items():
                            if sy != EPSILON:
                                if main_state in sts and state not in sts:
                                    self.afd[st][sy].append(state)
                        
                    if self.afnd[state].final:  # se o estado é final, o estado principal também será
                        self.afnd[main_state].final = True

            # remove as transições por EPSILON do AFND e o símbolo do alfabeto
            for state in list(self.afnd):
                del self.afnd[state][EPSILON]
            self.alphabet.remove(EPSILON)

    def fill_afnd(self):
        """
        Preenche o autômato finito com os dados informados no arquivo
        """
        print('Carregando dados do arquivo de entrada "{}" ...\n\n'.format(self.file.name))

        blocks = self.file.read().split('\n\n')  # quebra o arquivo em blocos de tokens e/ou GRs

        # identifica cada bloco se é de tokens ou uma GR
        for block in blocks:
            # tokens
            if not block.startswith('<'):
                self.tokens = block.splitlines()

                # atualiza o alfabeto com todos os caracteres contidos nos tokens
                self.update_alphabet(list("".join(self.tokens)))

                for token in self.tokens:
                    for i, symbol in enumerate(token):
                        if i == 0:  # ESTADO INICIAL TOKEN
                            self.add_afnd_step(origin_state=self.initial_state,
                                               dest_state=self.state+1,
                                               symbol=symbol,
                                               origin_initial=True,
                                               origin_final=False,
                                               dest_initial=False,
                                               dest_final=(i == len(token)-1))

                        else:  # DEMAIS ESTADOS
                            self.add_afnd_step(origin_state=self.state,
                                               dest_state=self.state+1,
                                               symbol=symbol,
                                               origin_initial=False,
                                               origin_final=False,
                                               dest_initial=False,
                                               dest_final=(i == len(token)-1))

                        self.state += 1
            # GR
            else:
                lines = block.splitlines()

                related_states = {'S': 0}  # cada estado lido da GR é relacionado a um correspondente numérico do AFND

                for i, line in enumerate(lines):
                    line_data = line.split('::=')
                    key = line_data[0].strip().replace('<', '').replace('>', '')  # elimina símbolos desnecessários

                    prod_data, final = self.productions_to_dict(line_data[1])

                    # assimila símbolos não-terminais à números de estados
                    if key not in related_states:
                        related_states[key] = self.state+1
                        self.state += 1

                    for prod, states in prod_data.items():
                        for state in states:
                            # assimila símbolos não-terminais à números de estados
                            if state not in related_states:
                                related_states[state] = self.state+1
                                self.state += 1

                            self.add_afnd_step(origin_state=related_states[key],
                                               dest_state=related_states[state],
                                               symbol=prod,
                                               origin_initial=False,
                                               origin_final=final,
                                               dest_initial=False,
                                               dest_final=True if state == '#' else False)

        self.update_afnd()  # atualiza preenchendo as colunas vazias

    def afnd_determinization(self):
        """
        Cria uma cópia do AFND e determiniza esta cópia
        """
        print('\n\nDeterminizando o AFND...\n\n')

        if not self.afd:
            self.afd = copy.deepcopy(self.afnd)  # cria uma cópia do AFND para o AFD que vamos mexer

        afd_states = list(self.afd)
        index = 0

        # vamos fazer a determinização "empurrando" os novos indeterminismos para baixo
        while index < len(afd_states):
            state = afd_states[index]
            for symbol in self.alphabet:
                state_list = self.afd[state][symbol]

                if len(state_list) not in (0, 1):  # existe indeterminismo
                    new_state = state_list
                    new_state.sort()
                    new_state = str(new_state)

                    dest_final = False

                    # se um dos estados for final o novo também será
                    for s in state_list:
                        if self.afd[s].final:
                            dest_final = True
                            break

                    # relaciona o conjunto de estados do indeterminismo com um novo estado determinizado
                    # então cria a linha correspondente à essse novo estado
                    if new_state not in self.related_states:
                        self.afd_line(self.state+1, False, dest_final)
                        self.related_states[new_state] = self.state+1
                        afd_states.append(self.state+1)
                        self.state += 1

                    for s in state_list:  # puxamos as transições dos estados que o formaram
                        for sy in self.alphabet:
                            current_states = self.afd[self.related_states[new_state]][sy]
                            extra_states = self.afd[s][sy]
                            new_states = list(set(current_states+extra_states))
                            self.afd[self.related_states[new_state]][sy] = new_states

            index += 1

        # percorremos novamente o autômato, dessa vez substituindo os indeterminismos nas produções pelos novos estados
        for state, line in self.afd.items():
            for symbol, states in line.items():
                str_state = str(states)

                if str_state in self.related_states:
                    new_state = self.related_states[str_state]
                    self.add_afd_step(origin_state=state,
                                      dest_state=new_state,
                                      symbol=symbol,
                                      origin_initial=line.initial,
                                      origin_final=line.final,
                                      dest_initial=False,
                                      dest_final=False,
                                      replace=True)

        # limpamos o AFD, removendo listas e deixando apenas o estado no valor das chaves
        # aqui também adicionamos um estado de erro e colocamos em tudo o que não é mapeado
        self.clean_afd()

    def export_csv(self):
        """
        Exporta o AFD para um arquivo CSV
        """
        print('\n\nExportando AFD para o arquivo "{}" ...'.format(self.csv_path))

        csv_file = open(self.csv_path, 'w')
        writer = csv.writer(csv_file)
        self.alphabet.sort()
        writer.writerow(['']+self.alphabet)

        for state in list(self.afd):
            state_str = '{}{}{}{}'.format('->' if self.afd[state].initial else '',
                                          '*' if self.afd[state].final else '',
                                          '(E)' if self.afd[state].error else '',
                                          state)
            writer.writerow([state_str]+[self.afd[state][symbol] for symbol in self.alphabet])

    def token_recognition(self, token=''):
        """
        Faz o reconhecimento de um token utilizando o AFD
        :param token: str: token a ser reconhecido
        :return: tuple: tupla com (token reconhecido? (bool), estado onde parou (int), mensagem com dados do reconhecimento (str))
        """
        recognized = False
        state = self.initial_state

        if not token:
            message = 'Token não informado'
            return recognized, state, message

        for letter in token:
            line = self.afd[state]

            if letter not in self.alphabet:
                message = 'Letra "{}" não pertence ao alfabeto da linguagem'.format(letter)
                return recognized, state, message

            state = line.get(letter)

        afd_data = self.afd[state]
        recognized = afd_data.final and not afd_data.error
        message = 'Inicial = {} | Final = {} | Erro = {}'.format(afd_data.initial, afd_data.final, afd_data.error)

        return recognized, state, message

    def symbol_recognition(self, state=0, symbol=''):

        _state = self.afd[state].get(symbol)
        _final = self.afd[_state].final
        return _state, _final

    # Métodos da tabela de símbolos (Lucas)
    def build_symbol_table(self):
        """
        Função build_symbol_table irá fazer a busca no autômato finito
        caracter a caracter, reconhecendo os tokesn do código fonte e verificando
        se o token é separador ou não.

        Para cada token reconhecido é adicionado ao dicinário self.st. (Symbol Table)

        Cada chave do self.st é equivalente a cada linha do código fonte.
        Cada valor do self.st contém listas do tokens reconhecidos.

        O formato da self.st: [{'line': 0, 'state': 0, 'label': 'if'}, ]

        São removidos os '\n' do código fonte antes de iniciar a construção da tabela de símbolos.
        """
        state = 0  # Estado corrente para reconhecimento do token no AF.
        temp_token = str()  # Variável para salvar rótulo do token.

        for line in range(len(self.sourceCode)):
            for i, symbol in enumerate(self.sourceCode[line]):

                try:
                    temp_token = temp_token + symbol  # Guarda simbolo para criar o rótulo.
                    state, is_final = (self.symbol_recognition(state, symbol))  # Busca tokens no AF

                    if symbol not in self.separators \
                            and symbol + self.sourceCode[line][i + 1] \
                            not in self.double_separators \
                            and is_final:

                        try:
                            if self.sourceCode[line][i + 1] in self.separators \
                                    or self.sourceCode[line][i + 1] + self.sourceCode[line][i + 2] \
                                    in self.double_separators:
                                self.st.append({'line': line, 'state': state, 'label': temp_token})  # Adiciona token reconhecido na tabela de símbolos
                                state = 0  # Reinicia o estado de busca.
                                temp_token = ''  # Limpa váriavel para guardar o rótulo.

                        except IndexError:  # Exceção para números sem símbolo separador no final.
                            state, is_final = (self.symbol_recognition(state, symbol))  # Busca tokens no AF

                    elif symbol in self.separators and is_final:

                        # Reconhece separadores duplos (ex: '==' )
                        if symbol + self.sourceCode[line][i + 1] in self.double_separators:  # and self.sourceCode[line][i + 1] == symbol:
                            pass

                        # Reconhece separadores simples (ex: ':' )
                        elif symbol + self.sourceCode[line][i + 1] not in self.separators:
                            self.st.append({'line': line, 'state': state, 'label': temp_token})
                            state = 0  # Reinicia o estado de busca.
                            temp_token = ''  # Limpa váriavel para guardar o rótulo.

                        # Reconhece separadores simples que estão juntos (ex: '):' )
                        elif symbol + self.sourceCode[line][i + 1] in self.separators and self.sourceCode[line][i + 1] != symbol:
                            self.st.append({'line': line, 'state': state, 'label': temp_token})
                            state = 0  # Reinicia o estado de busca.
                            temp_token = ''  # Limpa váriavel para guardar o rótulo.

                except IndexError:  # Exceção para os últimos simbolos de cada string.
                    self.st.append({'line': line, 'state': state, 'label': temp_token})
                    state = 0  # Reinicia o estado de busca.
                    temp_token = ''  # Limpa váriavel para guardar o rótulo.

                except KeyError:  # Excessão para ignorar espaços.
                    state = 0  # Reinicia o estado de busca.
                    temp_token = ''  # Limpa váriavel para guardar o rótulo.

    def build_separators(self):
        self.separators = ['(', ')', ':', '<', '>', '=', ' ', '"', "'"]
        self.double_separators = ['<=', '>=', '==', '!=']

    def clean_source_code(self):
        for line in range(len(self.sourceCode)):
            self.sourceCode[line] = self.sourceCode[line].replace('\n', '')

        # Não sei o por quê, mas precisou. Na quebra de linha do código fonte, adicionou uma lista.
        while '' in self.sourceCode:
            self.sourceCode.remove('')

    def show_symbol_table(self):
        for item in self.st:
            print(item)
