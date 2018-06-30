import csv
import copy

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

    def __init__(self, filename):
        self.afnd = dict()
        self.afd = dict()
        self.file = open(filename, 'r')
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

    def add_afd_step(self, origin_state, dest_state, symbol, origin_initial, origin_final, dest_initial, dest_final):
        """
        Adiciona um passo no autômato determinístico
        :param origin_state: int: estado de origem
        :param dest_state: int: estado de destino
        :param symbol: str: símbolo reconhecido
        :param origin_initial: bool: estado de origem é inicial?
        :param origin_final: bool: estado de origem é final?
        :param dest_initial: bool: estado de destino é inicial?
        :param dest_final: bool: estado de destino é final?
        """
        self.afd_line(origin_state, origin_initial, origin_final, [symbol])
        self.afd_line(dest_state, dest_initial, dest_final)

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
                    except IndexError:  # há somente um símbolo terminal, deve ir para um estado de erro padrão
                        state = '#'

                new_data[symbol] = state

        return new_data, final

    def _get_reachable(self, current_state, stop=False):
        """
        Função recursiva que obtém os estados atingíveis
        :param current_state: int: estado atual
        :param stop: bool: flag para parar a recursão, é passado se o estado atual é um estado de erro, então pára
        """
        if current_state not in self.reachable:
            self.reachable.append(current_state)
        if stop is False:
            values = list(set(self.afd[current_state].values()))
            if current_state in values:
                values.remove(current_state)
            for state in values:
                self._get_reachable(state, self.afd[state].error)

    def get_reachable(self, state):
        """
        Obtém apenas os estados atingíveis, partindo do estado inicial e chamando recursivamente para
        cada estado atingido
        :param state: int: estado inicial
        :return: list: lista com os números dos estados atingívis
        """
        self._get_reachable(state)
        return self.reachable

    def remove_unreachable(self):
        """
        Remove os estados inatingíveis do AFD
        """
        keep = self.get_reachable(self.initial_state)
        unreachable = list(set(self.afd.keys()).difference(keep))

        print('\n\nRemovendo estados inalcançáveis {}\n'.format(unreachable))

        for state in unreachable:
            del self.afd[state]

    def _get_alive(self, path=[], reachable_states=[]):
        """
        Chamada recursiva para obter os estados vivos do AFD, considera vivos todos os estados de um caminho que
        chega à um estado final
        :param path: list: sequência de estados que representa um caminho dentro do AFD
        :param reachable_states: list: estados atingíveis pelo último estado do caminho
        """
        for reach in reachable_states:
            if self.afd[reach].final and not is_sublist(path, self.alive):
                self.alive += path
        if self.test_alive:
            self.test_alive = set(self.test_alive) - set(path)
            reachable_states = set(reachable_states) - set(path)
            for state in reachable_states:
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

        print('\nRemovendo estados mortos {}\n\n'.format(dead))

        for state in dead:
            del self.afd[state]

    def _get_epsilon(self, path=[], epsilon_states=[]):
        """
        Chamada recursiva para obter as transições por EPSILON entre os estados
        :param path: list: caminho atual
        :param epsilon_states: estados que estão na transição por EPSILON do último estado do caminho
        """
        if epsilon_states:
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

    def get_epsilon(self, state):
        """
        Carrega uma lista de listas, onde cada lista interna é uma transição por épsilon entre os seus estados
        :param state: int: estado inicial
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
            for state in list(self.afnd):  # cria os caminhos das transições
                self.get_epsilon(state)

            print('\n\nRemovendo as épsilon transições {}\n\n'.format(self.epsilon_paths))

            for path in self.epsilon_paths:
                main_state = path[0]  # o primeiro estado da transição receberá as mudanças
                for state in path[1:]:  # para cada um dos demais estados
                    for symbol in list(self.afnd[main_state]):  # as produções desse estado irão para o principal
                        self.afnd[main_state][symbol] = list(set(self.afnd[main_state][symbol]+self.afnd[state][symbol]))
                    for st, line in self.afnd.items():  # os caminhos que levam ao estado agora levarão ao principal
                        for symbol in list(line):
                            if state in self.afnd[st][symbol]:
                                self.afnd[st][symbol].remove(state)
                                if main_state not in self.afnd[st][symbol]:
                                    self.afnd[st][symbol].append(main_state)

                    if self.afnd[state].final:  # se o estado é final, o estado principal também será
                        self.afnd[main_state].final = True

                    # excluímos o estado
                    del self.afnd[state]

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

                    for prod, state in prod_data.items():

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

        changed = self._afnd_determinization()  # determiniza o afnd
        while changed:  # continua a determinização enquanto houver alterações no autômato
            changed = self._afnd_determinization()

        self.clean_afd()  # limpa o AFD e adiciona o estado de erro

    def _afnd_determinization(self):
        """
        Determiniza o AFND
        """
        changed = False

        for state in list(self.afd):
            for symbol in list(self.afd[state]):
                state_list = self.afd[state][symbol]

                if len(state_list) not in (0, 1):  # existe indeterminismo
                    changed = True

                    new_state = state_list
                    new_state.sort()
                    new_state = str(new_state)

                    dest_final = False

                    # se um dos estados for final o novo também será
                    for s in state_list:
                        if self.afd[s].final:
                            dest_final = True
                            break

                    if new_state not in self.related_states:
                        self.related_states[new_state] = self.state+1
                        self.state += 1

                    self.add_afd_step(origin_state=state,
                                      dest_state=self.related_states[new_state],
                                      symbol=symbol,
                                      origin_initial=self.afd[state].initial,
                                      origin_final=self.afd[state].final,
                                      dest_initial=False,
                                      dest_final=dest_final)

                    for s in state_list:
                        for sy in list(self.afd[s]):
                            states = self.afd[s][sy]
                            self.afd[self.related_states[new_state]][sy] = list(set(self.afd[self.related_states[new_state]][sy]+states))

                    self.afd[state][symbol] = [self.related_states[new_state]]

        return changed

    def export_csv(self, path_to_file):
        """
        Exporta o AFD para um arquivo CSV
        :param path_to_file: str: caminho do arquivo
        """
        print('\n\nExportando AFD para o arquivo "{}" ...'.format(path_to_file))

        csv_file = open(path_to_file, 'w')
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
