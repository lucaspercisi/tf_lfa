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
                print('Fim inesperado do código fonte')
                return

            try:
                action_obj = self.table[self.stack[-1]][item.get('state')]
            except IndexError:
                print('Erro de sintaxe na linha {}'.format(item.get('line')))
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
                size = prod.size*2

                for i in range(0, size+1):
                    self.stack.pop()

                curr_state = self.stack[-1]
                self.stack.append(prod.nonterminal)
                self.stack.append(self.table[curr_state][prod.nonterminal].state)
            elif action == 'goto':  # salto
                self.stack.append(action)
                self.stack.append(next_state)
                self.stack.pop()
                self.stack.pop()
            else:  # 'accept' aceite
                print('Aceite')
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
