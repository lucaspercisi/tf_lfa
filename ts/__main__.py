import os

class SymbolTable(object):

    def __init__(self):  # Não sei
        path = os.path.abspath(__file__)  # Não sei
        dir_path = os.path.dirname(path)  # Não sei

        self.source_code_path = os.path.join(dir_path, 'codigo-fonte.txt')  # Local do código-fonte
        self.st = dict()  # Tabela de simbolos
        self.separators = list()  # Separadores da linguagem
        self.sourceCode = list(
            open(self.source_code_path, 'r'))  # codigo fonte inserido numa lista para criação da tabela de simbolos

        self.build_separators()  # Constroí as listas contendo os separadores da linguagem.
        self.clean_source_code()  # Limpa o código-fonte para construção da self.ts.

    '''
    Função build_symbol_table irá fazer a busca no autômato finito
    caracter a caracter, reconhecendo os tokesn do código fonte e verificando
    se o token é separador ou não.
    
    Para cada token reconhecido é adicionado ao dicinário self.st. (Symbol Table)
    
    Cada chave do self.st é equivalente a cada linha do código fonte. 
    Cada valor do self.st contém listas do tokens reconhecidos.
    
    O formato da self.ts: {linha : [[estado_reconhecedor, rótulo], ..., [estado_reconhecedor, rótulo]]}
    
    São removidos todos os espaços em branco e quebras de linha do código fonte antes de iniciar a construção da tabela de símbolos.
    '''
    def build_symbol_table(self, af):

        state = 0  # Estado corrente para reconhecimento do token no AF.
        temp_token = str()  # Variável para salvar rótulo do token.

        for line in range(len(self.sourceCode)):

            self.st[line] = list()  # Para cada linha do código fonte, uma nova lista no self.st.

            for i, symbol in enumerate(self.sourceCode[line]):

                try:
                    temp_token = temp_token + symbol  # Guarda simbolo para criar o rótulo.

                    if symbol not in self.separators:

                        state, state_is_final = (af.symbol_recognition(state, symbol))  # Busca tokens no AF

                        # TODO: Arrumar o retorno da variável .final do AF
                        if self.sourceCode[line][i + 1] in self.separators:  # and state_is_final:
                            self.st[line].append([state, temp_token])  # Adiciona token reconhecido na tabela de símbolos
                            state = 0  # Reinicia o estado de busca.
                            temp_token = ''  # Limpa váriavel para guardar o rótulo.
                        # else:
                        #     print("Erro: Linha {}, Estado final: {}, Estado: {}".format((line, state_is_final, state)))

                    elif symbol in self.separators:

                        state, state_is_final = (af.symbol_recognition(state, symbol))

                        # TODO: Arrumar o retorno da variável .final do AF para condicial correta
                        # Reconhece separadores de símbolo único (ex: ':' )
                        if self.sourceCode[line][i + 1] not in self.separators:  # and state_is_final:
                            self.st[line].append([state, temp_token])
                            state = 0  # Reinicia o estado de busca.
                            temp_token = ''  # Limpa váriavel para guardar o rótulo.

                        # TODO: Reconhecer separadores juntos de símbolo e token diferentes (ex: '):' )
                        elif self.sourceCode[line][i + 1] in self.separators and self.sourceCode[line][i + 1] != symbol:
                            self.st[line].append([state, temp_token])
                            state = 0  # Reinicia o estado de busca.
                            temp_token = ''  # Limpa váriavel para guardar o rótulo.

                        # TODO: Reconhecer separadores juntos de mesmo token e simbolos iguais (ex: '==' )
                        elif self.sourceCode[line][i + 1] in self.separators and self.sourceCode[line][i + 1] == symbol:
                            pass

                        # TODO: Reconhecer separadores juntos de mesmo token e simbolos diferentes (ex: '!=' )
                        else:
                            pass

                except IndexError:  # Último simbolo de cada linha
                    self.st[line].append([state, temp_token])
                    state = 0  # Reinicia o estado de busca.
                    temp_token = ''  # Limpa váriavel para guardar o rótulo.

    def build_separators(self):
        self.separators = ['(', ')', ':', '<', '>']

    def clean_source_code(self):
        for line in range(len(self.sourceCode)):
            self.sourceCode[line] = self.sourceCode[line].replace(' ', '')
            self.sourceCode[line] = self.sourceCode[line].replace('\n', '')

    def show_symbol_table(self):
        for line in self.st:
            print(self.st[line])

