import os

class SymbolTable(object):

    def __init__(self):
        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path)

        self.source_code_path = os.path.join(dir_path, 'codigo-fonte.txt')
        self.st = dict()  # tabela de simbolos
        self.separators = list()  # separadores da linguagem
        # self.sy_separators = list()  # separadores da linguagem que tambem são simbolos
        # self.sy_ignored = list()
        self.sourceCode = list(open(self.source_code_path, 'r'))  # codigo fonte inserido numa lista para criação da tabela de simbolos

        self.build_separators()
        self.clean_source_code()

    def build_symbol_table(self, af):
        state = 0

        for line in range(len(self.sourceCode)):
            self.st[line] = []
            for symbol in self.sourceCode[line]:
                pass

# TODO: Finalizar laço principal
                # if symbol not in self.separators:
                #     state = (af.symbol_recognition(state, symbol))
                # else:
                #     af.afd[state][symbol].
                #     self.st[line].append([state])
                #     state = 0


    def show_symbol_table(self):
        for line in self.st:
            print(self.st[line])

    def build_separators(self):
        self.separators = ['(', ')', ':', '<', '>']
        # self.separators = [' ']

    def clean_source_code(self):
        for line in range(len(self.sourceCode)):
            self.sourceCode[line] = self.sourceCode[line].replace(' ', '')
            self.sourceCode[line] = self.sourceCode[line].replace('\n', '')
