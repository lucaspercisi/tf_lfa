import os


class SymbolTable(object):

    def __init__(self):  # Não sei
        path = os.path.abspath(__file__)  # Não sei
        dir_path = os.path.dirname(path)  # Não sei

        self.source_code_path = os.path.join(dir_path, 'codigo-fonte.txt')  # Local do código-fonte
        self.gold_lalr_path = os.path.join(dir_path, 'C-ANSI.txt')  # Local do código-fonte

        self.st = dict()  # Tabela de Símbolos
        self.separators = list()  # Separadores da linguagem
        self.double_separators = list()  # Separadores da linguagem
        self.sourceCode = list(open(self.source_code_path, 'r'))  # codigo fonte inserido numa lista para criação da tabela de simbolos
        self.gold_lalr = list(open(self.gold_lalr_path, 'r'))  # codigo fonte inserido numa lista para criação da tabela de simbolos

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
    
    São removidos os '\n' do código fonte antes de iniciar a construção da tabela de símbolos.
    '''

    def build_symbol_table(self, af):

        state = 0  # Estado corrente para reconhecimento do token no AF.
        temp_token = str()  # Variável para salvar rótulo do token.

        for line in range(len(self.sourceCode)):

            self.st[line] = list()  # Para cada linha do código fonte, uma nova lista no self.st.

            for i, symbol in enumerate(self.sourceCode[line]):

                try:
                    temp_token = temp_token + symbol  # Guarda simbolo para criar o rótulo.
                    state, is_final = (af.symbol_recognition(state, symbol))  # Busca tokens no AF

                    if symbol not in self.separators \
                            and symbol + self.sourceCode[line][i + 1] \
                            not in self.double_separators \
                            and is_final:

                        try:
                            if self.sourceCode[line][i + 1] in self.separators \
                                    or self.sourceCode[line][i + 1] + self.sourceCode[line][i + 2] \
                                    in self.double_separators:

                                self.st[line].append([state, temp_token])  # Adiciona token reconhecido na tabela de símbolos
                                state = 0  # Reinicia o estado de busca.
                                temp_token = ''  # Limpa váriavel para guardar o rótulo.

                        except IndexError:  # Exceção para números sem símbolo separador no final.
                            state, is_final = (af.symbol_recognition(state, symbol))  # Busca tokens no AF

                    elif symbol in self.separators and is_final:

                        # Reconhece separadores duplos (ex: '==' )
                        if symbol + self.sourceCode[line][i + 1] in self.double_separators:  # and self.sourceCode[line][i + 1] == symbol:
                            pass

                        # Reconhece separadores simples (ex: ':' )
                        elif symbol + self.sourceCode[line][i + 1] not in self.separators:

                            self.st[line].append([state, temp_token])
                            state = 0  # Reinicia o estado de busca.
                            temp_token = ''  # Limpa váriavel para guardar o rótulo.

                        # Reconhece separadores simples que estão juntos (ex: '):' )
                        elif symbol + self.sourceCode[line][i + 1] in self.separators and self.sourceCode[line][i + 1] != symbol:

                            self.st[line].append([state, temp_token])
                            state = 0  # Reinicia o estado de busca.
                            temp_token = ''  # Limpa váriavel para guardar o rótulo.

                except IndexError:  # Exceção para os últimos simbolos de cada string.
                    self.st[line].append([state, temp_token])
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
        for line in self.st:
            print(self.st[line])

    def gold_to_ts_translator(self):

        for l, line in enumerate(self.gold_lalr):
            if "LALR" not in line:
                continue
            while "State 1" not in self.gold_lalr[l]:
                if "        <" in self.gold_lalr[l]:
                    pass
