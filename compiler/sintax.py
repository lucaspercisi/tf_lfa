import os
import xml.etree.ElementTree as ET

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)


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

    def load(self, filename='gold.xml'):
        """
        Faz a carga do arquivo do Gold para o Python
        :param filename: str: nome do arquivo de entrada
        """
        file_path = os.path.join(dir_path, 'inputs', filename)
        tree = ET.parse(file_path)
        root = tree.getroot()

        print(root.tag)