import os


class Action(object):
    def __init__(self, action, state):
        self.action = action
        self.state = state

    def __repr__(self):
        return 'Action( {} -> {} )'.format(self.action, self.state)

    def __str__(self):
        return "{} -> {}".format(self.action, self.state)


class LALR(object):
    def __init__(self, ts={}, tape=[]):
        """
        Analisador sintático LALR
        :param ts: tabela de símbolos
        :param tape: fita de saída da análise léxica
        """
        self.ts = ts  # tabela de símbolos
        self.tape = tape  # fita de saída da análise léxica
        self.stack = []  # pilha
        self.table = {}  # tabela do analisador
        self.dict = {}  # tradutor código -> elemento

    def analyze(self):
        """
        Efetua a análise sintática
        :return: bool: True quando foi aceito, False não
        """
        i = 0  # posição atual na fita
        self.stack.append(0)  # empilha o estado inicial

        while True:
            try:
                elem = self.dict[self.tape[i]]
            except IndexError:
                return False  # terminou a fita e não reconheceu
            action_obj = self.table[self.stack[-1]][elem]
            action = action_obj.action
            next_state = action_obj.state

            if action == 's':  # empilha
                self.stack.append(elem)
                self.stack.append(next_state)
                i += 1
            elif action == 'r':  # redução
                # TODO: Implementar redução: parece que precisa das regras aqui e dos conjuntos first/follow
                self.stack.pop()
                self.stack.pop()
            elif action == 'g':  # salto
                self.stack.append(action)
                self.stack.append(next_state)
            else:  # aceite
                return True

    def load(self, filename='input.txt'):
        """
        Faz a carga do arquivo do Gold para o Python
        :param filename: str: nome do arquivo de entrada
        """
        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path)
        file_path = os.path.join(dir_path, filename)
        file = open(file_path, 'r')

        state = 'begin'  # estado inicial da "máquina de estados"
        curr_state = None  # auxiliar para guardar o estado da tabela enquanto guarda suas ações

        # laço que funciona como uma máquina de estados, cada estado extrai um tipo de informação da linha
        for line in file.readlines():
            line = line.strip().replace("'", "")
            data = list(filter(None, line.split(' ')))
            if len(data) >= 2 and data[0].startswith('<') and data[1].endswith('>'):
                data[0] += data[1]
                del data[1]
            if state == 'begin':  # estado inicial
                if line == 'Terminals':  # mudança de estado
                    state = 'terminals'
                    continue
            elif state == 'terminals':  # lendo terminais
                if line == 'Nonterminals':  # mudança de estado
                    state = 'nonterminals'
                    continue
                if len(data) == 2:
                    code = data[0].strip()
                    symbol = data[1].strip()
                    if code.isdigit():
                        self.dict[int(code)] = symbol
            elif state == 'nonterminals':  # lendo não terminais
                if line == 'Rules':  # mudança de estado
                    state = 'rules'
                    continue
                if len(data) == 2:
                    code = data[0].strip()
                    symbol = data[1].strip()
                    if code.isdigit():
                        self.dict[int(code)] = symbol
            elif state == 'states':  # lendo estados da tabela do analisador
                if line.startswith('State'):
                    curr_state = data[1]
                    if data[1] not in self.table:
                        self.table[data[1]] = {}
                elif len(data) == 3:
                    if data[0] not in self.table[curr_state]:
                        self.table[curr_state][data[0]] = Action(data[1], data[2])
            else:  # cai aqui quando o estado for "rules", não estamos carregando as regras
                if line == 'LALR States':  # mudança de estado
                    state = 'states'
                    continue