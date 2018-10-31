from compiler.lexical import Constructor
from compiler.sintax import LALR

# AUTÔMATO FINITO
# TODO: O Autômato está considerando o '.' como estado de erro quando tem números na frente do ponto.
constructor = Constructor()
constructor.fill_afnd()  # preenche o AFND com os dados do arquivo de entrada
constructor.print_afnd()  # imprime o AFND carregado
constructor.remove_epsilon()  # remove os EPSILON transições
constructor.print_afnd()  # imprime o AFND livre de épsilon transições
constructor.afnd_determinization()  # determiniza o afnd
constructor.print_afd()  # imprime o AFD
constructor.remove_dead()  # remove os estados mortos
constructor.remove_unreachable()  # remove os estados inatingíveis
constructor.print_afd()  # imprime o AFD finalizado

#  TABELA DE SÍMBOLOS
constructor.build_separators()  # Constroí as listas contendo os separadores da linguagem.
constructor.clean_source_code()  # Limpa o código-fonte para construção da self.ts.
constructor.build_symbol_table()  # Constrói a Tabela de Símbolos de acordo com o AF
constructor.show_symbol_table()  # Mostra Tabela de Símbolos
constructor.verify_lexical_errors()  # Exibe erros lexicos da tabela de simbolos.

# Analisador sintático LALR
lalr = LALR(st=constructor.st)
lalr.load()
lalr.analyze()
