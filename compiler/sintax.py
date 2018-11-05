import os
import xml.etree.ElementTree as ET

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)

ACTION_TYPES = {
    '1': 'shift',
    '2': 'reduce',
    '3': 'goto',
    '4': 'accept'
}


class Action(object):
    def __init__(self, action, state):
        self.action = action
        self.state = state

    def __repr__(self):
        return '{} -> {}'.format(self.action, self.state)

    def __str__(self):
        return "{} -> {}".format(self.action, self.state)


class Production(object):
    def __init__(self, nonterminal, size, symbols=[]):
        self.nonterminal = nonterminal
        self.size = size
        self.symbols = symbols

    def __repr__(self):
        return '{} | {}'.format(self.nonterminal, ' '.join(map(str, self.symbols)))

    def __str__(self):
        return '{} | {}'.format(self.nonterminal, ' '.join(map(str, self.symbols)))


class LALR(object):
    def __init__(self, st={}):
        """
        Analisador sintático LALR
        :param ts: tabela de símbolos
        """
        self.st = st  # tabela de símbolos
        self.stack = []  # pilha
        self.table = {}  # tabela do analisador
        self.dict = {}  # tradutor código -> elemento
        self.productions = {}  # produções da gramática LC
        # dicionário tradutor de número de estado do AF para número do LALR
        self.translator = {
            186: 59,  # int
            202: 53,  # float
            193: 64,  # void
            192: 45,  # char
            209: 60,  # return
            171: 58,  # if
            204: 65,  # while
            199: 52,  # else
            181: 55,  # for
            173: 51,  # do
            203: 43,  # break
            213: 48,  # continue
            207: 63,  # switch
            190: 44,  # case
            212: 50,  # default
            157: 34,  # <
            147: 40,  # >
            71: 18,  # :
            72: 11,  # (
            73: 12,  # )
            141: 37,  # =
            76: 39,  # ==
            78: 36,  # <=
            80: 41,  # >=
            82: 6,  # !=
            156: None,  # ' NÃO MAPEADO, NÃO USAMOS STRINGS, NÃO MUDEI PARA NÃO TER QUE REFAZER O TRADUTOR
            148: None,  # " NÃO MAPEADO, NÃO USAMOS STRINGS, NÃO MUDEI PARA NÃO TER QUE REFAZER O TRADUTOR
            87: 25,  # {
            88: 29,  # }
            89: 21,  # [
            90: 22,  # ]
            91: 19,  # ;
            155: 31,  # +
            146: 3,  # -
            149: 13,  # *
            152: 16,  # /
            96: 15,  # ,
            98: 33,  # +=
            100: 38,  # -=
            102: 14,  # *=
            104: 17,  # /=
            106: 24,  # ^=
            108: 10,  # &=
            110: 28,  # |=
            111: 20,  # ?
            113: 27,  # ||
            115: 9,  # &&
            117: 42,  # >>
            119: 35,  # <<
            120: 7,  # %
            151: 26,  # |
            145: 23,  # ^
            150: 8,  # &
            153: 5,  # !
            125: 30,  # ~
            127: 32,  # ++
            129: 4,  # --
            130: 96,  # variável
            143: 96,  # variável
            139: 96,  # variável
            159: 96,  # variável
            160: 96,  # variável
            142: 96,  # variável
            158: 96,  # variável
            154: 96,  # variável
            138: 96,  # variável
            140: 96,  # variável
            144: 96,  # variável
            161: 96,  # variável
            162: 96,  # variável
            163: 96,  # variável
            164: 96,  # variável
            165: 96,  # variável
            166: 96,  # variável
            167: 96,  # variável
            168: 96,  # variável
            169: 96,  # variável
            170: 96,  # variável
            172: 96,  # variável
            174: 96,  # variável
            175: 96,  # variável
            176: 96,  # variável
            177: 96,  # variável
            178: 96,  # variável
            179: 96,  # variável
            180: 96,  # variável
            182: 96,  # variável
            183: 96,  # variável
            184: 96,  # variável
            185: 96,  # variável
            187: 96,  # variável
            188: 96,  # variável
            189: 96,  # variável
            191: 96,  # variável
            194: 96,  # variável
            195: 96,  # variável
            196: 96,  # variável
            197: 96,  # variável
            198: 96,  # variável
            200: 96,  # variável
            201: 96,  # variável
            205: 96,  # variável
            206: 96,  # variável
            208: 96,  # variável
            210: 96,  # variável
            211: 96,  # variável
            137: 49,  # int
            136: 54,  # float
            214: 1,  # erro
            0: 0  # EOF
        }

    def analyze(self):
        """
        Efetua a análise sintática
        :return: bool: True quando foi aceito, False não
        """
        i = 0  # posição atual na fita ou TS
        self.stack.append(0)  # empilha o estado inicial

        while True:
            try:
                item = self.st[i]
            except IndexError:
                print('\nFim inesperado do código fonte')
                return

            try:
                translated_state = self.translator[item.get('state')]  # estado traduzido AFD -> LALR
                action_obj = self.table[self.stack[-1]][translated_state]
            except KeyError:
                print('\nErro de sintaxe na linha {}, token "{}"'.format(item.get('line'), item.get('label')))
                return

            action = action_obj.action
            next_state = action_obj.state

            if action == 'shift':  # empilha
                """
                A ação empilha o código do token (state) seguido do estado da ação atual
                Em seguida, movimenta a leitura na fita (TS)
                """
                self.stack.append(item.get('state'))
                self.stack.append(next_state)
                i += 1

            elif action == 'reduce':  # redução
                """
                Retira da pilha o dobro do tamanho da produção indicada na ação
                Em seguida empilha o não terminal que dá nome à regra que contém a produção junto com estado indicado
                para o salto na linha do estado que ficou na pilha e a coluna do não terminal
                """
                prod = self.productions.get(next_state)
                size = prod.size * 2
                # size = prod.size+1

                for i in range(0, size):
                    self.stack.pop()

                curr_state = self.stack[-1]
                self.stack.append(int(prod.nonterminal))
                self.stack.append(self.table[curr_state][int(prod.nonterminal)].state)

                # Verifica se após redução encontrou o 'aceite'
                translated_state = self.translator[item.get('state')]
                if self.table[self.stack[-1]][translated_state].action == 'accept':
                    print('\nAceite')
                    return

            elif action == 'goto':  # salto
                self.stack.append(action)
                self.stack.append(next_state)
                self.stack.pop()
                self.stack.pop()

            elif action == 'accept':
                print('\nAceite')
                return

    def is_terminal(self, sy):
        """
        Verifica se o símbolo informado é terminal
        :param sy: str: símbolo
        :return: boolean: True se for terminal
        """
        return not sy.istitle()  # no arquivo, os não-terminais tem nomes com letra maiúscula no início das palavras

    def load(self, filename='gold.xml'):
        """
        Faz a carga do arquivo do Gold para o Python
        :param filename: str: nome do arquivo de entrada
        """
        file_path = os.path.join(dir_path, 'inputs', filename)
        tree = ET.parse(file_path)
        root = tree.getroot()

        # símbolos
        for sy in root.iter('Symbol'):
            self.dict[int(sy.get('Index'))] = sy.get('Name')

        # produções
        for prod in root.iter('Production'):
            nonterm = prod.get('NonTerminalIndex')
            size = int(prod.get('SymbolCount'))
            symbols = []
            for sy in prod.iter('ProductionSymbol'):
                symbols.append(int(sy.get('SymbolIndex')))
            self.productions[int(prod.get('Index'))] = Production(nonterm, size, symbols)

        # estados e ações do LALR
        for state in root.iter('LALRState'):
            curr_state = int(state.get('Index'))
            self.table[curr_state] = {}
            for action in state.iter('LALRAction'):
                action_symbol = int(action.get('SymbolIndex'))
                action_obj = Action(ACTION_TYPES[action.get('Action')], int(action.get('Value')))
                self.table[curr_state][action_symbol] = action_obj
