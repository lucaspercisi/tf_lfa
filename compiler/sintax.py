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
            176: 59,  # int
            197: 53,  # float
            189: 64,  # void
            183: 45,  # char
            202: 60,  # return
            162: 58,  # if
            200: 65,  # while
            187: 52,  # else
            179: 55,  # for
            167: 51,  # do
            196: 43,  # break
            207: 48,  # continue
            204: 63,  # switch
            184: 44,  # case
            206: 50,  # default
            142: 34,  # <
            139: 40,  # >
            71: 18,  # :
            72: 11,  # (
            73: 12,  # )
            149: 37,  # =
            76: 39,  # ==
            78: 36,  # <=
            80: 41,  # >=
            82: 6,  # !=
            83: 25,  # {
            84: 29,  # }
            85: 21,  # [
            86: 22,  # ]
            87: 19,  # ;
            147: 31,  # +
            137: 3,  # -
            140: 13,  # *
            133: 16,  # /
            92: 15,  # ,
            94: 33,  # +=
            96: 38,  # -=
            98: 14,  # *=
            100: 17,  # /=
            102: 24,  # ^=
            104: 10,  # &=
            106: 28,  # |=
            107: 20,  # ?
            109: 27,  # ||
            111: 9,  # &&
            113: 42,  # >>
            115: 35,  # <<
            116: 7,  # %
            152: 26,  # |
            146: 23,  # ^
            145: 8,  # &
            148: 5,  # !
            121: 30,  # ~
            123: 32,  # ++
            125: 4,  # --
            126: 57,  # variável
            141: 57,  # variável
            135: 57,  # variável
            151: 57,  # variável
            138: 57,  # variável
            150: 57,  # variável
            143: 57,  # variável
            136: 57,  # variável
            153: 57,  # variável
            144: 57,  # variável
            154: 57,  # variável
            155: 57,  # variável
            156: 57,  # variável
            157: 57,  # variável
            158: 57,  # variável
            159: 57,  # variável
            160: 57,  # variável
            161: 57,  # variável
            163: 57,  # variável
            164: 57,  # variável
            165: 57,  # variável
            166: 57,  # variável
            168: 57,  # variável
            169: 57,  # variável
            170: 57,  # variável
            171: 57,  # variável
            172: 57,  # variável
            173: 57,  # variável
            174: 57,  # variável
            175: 57,  # variável
            177: 57,  # variável
            178: 57,  # variável
            180: 57,  # variável
            181: 57,  # variável
            182: 57,  # variável
            185: 57,  # variável
            186: 57,  # variável
            188: 57,  # variável
            190: 57,  # variável
            191: 57,  # variável
            192: 57,  # variável
            193: 57,  # variável
            194: 57,  # variável
            195: 57,  # variável
            198: 57,  # variável
            199: 57,  # variável
            201: 57,  # variável
            203: 57,  # variável
            205: 57,  # variável
            134: 49,  # int
            132: 54,  # float
            208: 1,  # erro
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

            print('Fita:', self.translator[item.get('state')])
            print('Pilha:', self.stack)
            print('Tabela:', self.table[self.stack[-1]])

            try:
                translated_state = self.translator[item.get('state')]  # estado traduzido AFD -> LALR
                action_obj = self.table[self.stack[-1]][translated_state]
            except KeyError:
                print('\nErro de sintaxe na linha {}, token "{}"'.format(item.get('line'), item.get('label')))
                return
            else:
                print('Ação:', action_obj, '\n---')

            action = action_obj.action
            next_state = action_obj.state

            if action == 'shift':  # empilha
                """
                A ação empilha o código do token (state) seguido do estado da ação atual
                Em seguida, movimenta a leitura na fita (TS)
                """
                self.stack.append(translated_state)
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

                for xx in range(0, size):
                    self.stack.pop()

                curr_state = self.stack[-1]
                self.stack.append(int(prod.nonterminal))
                self.stack.append(self.table[curr_state][int(prod.nonterminal)].state)

            elif action == 'goto':  # salto
                pass

            elif action == 'accept':
                print('\nAceite')
                return

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
