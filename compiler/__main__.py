from compiler.lexical import Constructor
from compiler.sintax import LALR

# AUTÔMATO FINITO
# TODO: O Autômato está considerando o '.' como estado de erro quando tem números na frente do ponto.
constructor = Constructor()
constructor.fill_afnd()  # preenche o AFND com os dados do arquivo de entrada
# constructor.print_afnd()  # imprime o AFND carregado
constructor.remove_epsilon()  # remove os EPSILON transições
# constructor.print_afnd()  # imprime o AFND livre de épsilon transições
constructor.afnd_determinization()  # determiniza o afnd
# constructor.print_afd()  # imprime o AFD
constructor.remove_dead()  # remove os estados mortos
constructor.remove_unreachable()  # remove os estados inatingíveis
# constructor.print_afd()  # imprime o AFD finalizado

# recognizing_test_tokens = [
#     'int',
#     'float',
#     'void',
#     'char',
#     'return',
#     'if',
#     'while',
#     'else',
#     'for',
#     'do',
#     'break',
#     'continue',
#     'switch',
#     'case',
#     'default',
#     '<',
#     '>',
#     ':',
#     '(',
#     ')',
#     '=',
#     '==',
#     '<=',
#     '>=',
#     '!=',
#     "'",
#     "'",
#     '"',
#     '"',
#     '{',
#     '}',
#     '[',
#     ']',
#     ';',
#     '+',
#     '-',
#     '*',
#     '/',
#     ',',
#     '+=',
#     '-=',
#     '*=',
#     '/=',
#     '^=',
#     '&=',
#     '|=',
#     '?',
#     '||',
#     '&&',
#     '>>',
#     '<<',
#     '%',
#     '|',
#     '^',
#     '&',
#     '!',
#     '~',
#     '++',
#     '--',
#     'a',
#     'b',
#     'c',
#     'd',
#     'e',
#     'f',
#     'g',
#     'h',
#     'i',
#     'j',
#     'k',
#     'l',
#     'm',
#     'n',
#     'o',
#     'p',
#     'q',
#     'r',
#     's',
#     't',
#     'u',
#     'v',
#     'w',
#     'x',
#     'y',
#     'z',
#     '_',
#     'a',
#     'b',
#     'c',
#     'd',
#     'e',
#     'f',
#     'g',
#     'h',
#     'i',
#     'j',
#     'k',
#     'l',
#     'm',
#     'n',
#     'o',
#     'p',
#     'q',
#     'r',
#     's',
#     't',
#     'u',
#     'v',
#     'w',
#     'x',
#     'y',
#     'z',
#     'A',
#     'B',
#     'C',
#     'D',
#     'E',
#     'F',
#     'G',
#     'H',
#     'I',
#     'J',
#     'K',
#     'L',
#     'M',
#     'N',
#     'O',
#     'P',
#     'Q',
#     'R',
#     'S',
#     'T',
#     'U',
#     'V',
#     'W',
#     'X',
#     'Y',
#     'Z',
#     'A',
#     'B',
#     'C',
#     'D',
#     'E',
#     'F',
#     'G',
#     'H',
#     'I',
#     'J',
#     'K',
#     'L',
#     'M',
#     'N',
#     'O',
#     'P',
#     'Q',
#     'R',
#     'S',
#     'T',
#     'U',
#     'V',
#     'W',
#     'X',
#     'Y',
#     'Z',
#     'variavel_',
#     '1',
#     '88',
#     '564',
#     '-120',
#     '-5.18',
#     '0.0',
#     '1000.0000037'
# ]
#
# afd_finals = []
# recognizing_finals = []
#
# for key, line in constructor.afd.items():
#     if line.final:
#         afd_finals.append(key)
#
# for token in recognizing_test_tokens:
#     # print('\nReconhecendo token [ {} ]'.format(token))
#     recognized, state, message = constructor.token_recognition(token)
#     # print(recognized, state, message)
#     if recognized and state not in recognizing_finals:
#         print(state, ':', ', #', token)
#         recognizing_finals.append(state)
#     elif not recognized:
#         print(recognized, state, message)
#
# print('Estados não reconhecidos')
# print(set(afd_finals)-set(recognizing_finals))

#  TABELA DE SÍMBOLOS
constructor.build_separators()  # Constroí as listas contendo os separadores da linguagem.
constructor.clean_source_code()  # Limpa o código-fonte para construção da self.ts.
constructor.build_symbol_table()  # Constrói a Tabela de Símbolos de acordo com o AF
constructor.show_symbol_table()  # Mostra Tabela de Símbolos
constructor.verify_error_state()

# Analisador sintático LALR
lalr = LALR(st=constructor.st)
lalr.load()
lalr.analyze()
