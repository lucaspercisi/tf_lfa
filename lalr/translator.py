"""
Coloque em TRANSLATOR o código reconhecido pelo AFD na analise léxica como chave e
o código que será utilizado pelo reconhecedor sintático LALR do item correspondente
Modo de uso:
from lalr import TRANSLATOR
cod = TRANSLATOR.get(codigo_afd, default=codigo_afd)  # se não encontrar essa chave no tradutor utiliza o mesmo código
"""
TRANSLATOR = {
    0: 0,  # (EOF)
    1: 0,  # (Error)
    2: 0,  # Whitespace
    3: 0,  # 'Comment End'
    4: 0,  # 'Comment Line'
    5: 0,  # 'Comment Start'
    6: 0,  # '-'
    7: 0,  # '--'
    8: 0,  # '!'
    9: 0,  # '!='
    10: 0,  # '%'
    11: 0,  # '&'
    12: 0,  # '&&'
    13: 0,  # '&='
    14: 0,  # '('
    15: 0,  # ')'
    16: 0,  # '*'
    17: 0,  # '*='
    18: 0,  # ','
    19: 0,  # '.'
    20: 0,  # '/'
    21: 0,  # '/='
    22: 0,  # ':'
    23: 0,  # ';'
    24: 0,  # '?'
    25: 0,  # '['
    26: 0,  # ']'
    27: 0,  # '^'
    28: 0,  # '^='
    29: 0,  # '{'
    30: 0,  # '|'
    31: 0,  # '||'
    32: 0,  # '|='
    33: 0,  # '}'
    34: 0,  # '~'
    35: 0,  # '+'
    36: 0,  # '++'
    37: 0,  # '+='
    38: 0,  # '<'
    39: 0,  # '<<'
    40: 0,  # '<<='
    41: 0,  # '<='
    42: 0,  # '='
    43: 0,  # '-='
    44: 0,  # '=='
    45: 0,  # '>'
    46: 0,  # '->'
    47: 0,  # '>='
    48: 0,  # '>>'
    49: 0,  # '>>='
    50: 0,  # auto
    51: 0,  # break
    52: 0,  # case
    53: 0,  # char
    54: 0,  # CharLiteral
    55: 0,  # const
    56: 0,  # continue
    57: 0,  # DecLiteral
    58: 0,  # default
    59: 0,  # do
    60: 0,  # double
    61: 0,  # else
    62: 0,  # enum
    63: 0,  # extern
    64: 0,  # float
    65: 0,  # FloatLiteral
    66: 0,  # for
    67: 0,  # goto
    68: 0,  # HexLiteral
    69: 0,  # Id
    70: 0,  # if
    71: 0,  # int
    72: 0,  # long
    73: 0,  # OctLiteral
    74: 0,  # register
    75: 0,  # return
    76: 0,  # short
    77: 0,  # signed
    78: 0,  # sizeof
    79: 0,  # static
    80: 0,  # StringLiteral
    81: 0,  # struct
    82: 0,  # switch
    83: 0,  # typedef
    84: 0,  # union
    85: 0,  # unsigned
    86: 0,  # void
    87: 0,  # volatile
    88: 0,  # while
    89: 0,  # <Arg>
    90: 0,  # <Array>
    91: 0,  # <Base>
    92: 0,  # <Block>
    93: 0,  # <Case Stms>
    94: 0,  # <Decl>
    95: 0,  # <Decls>
    96: 0,  # <Enum Decl>
    97: 0,  # <Enum Def>
    98: 0,  # <Enum Val>
    99: 0,  # <Expr>
    100: 0,  # <Func Decl>
    101: 0,  # <Func ID>
    102: 0,  # <Func Proto>
    103: 0,  # <Id List>
    104: 0,  # <Mod>
    105: 0,  # <Normal Stm>
    106: 0,  # <Op Add>
    107: 0,  # <Op And>
    108: 0,  # <Op Assign>
    109: 0,  # <Op BinAND>
    110: 0,  # <Op BinOR>
    111: 0,  # <Op BinXOR>
    112: 0,  # <Op Compare>
    113: 0,  # <Op Equate>
    114: 0,  # <Op If>
    115: 0,  # <Op Mult>
    116: 0,  # <Op Or>
    117: 0,  # <Op Pointer>
    118: 0,  # <Op Shift>
    119: 0,  # <Op Unary>
    120: 0,  # <Param>
    121: 0,  # <Params>
    122: 0,  # <Pointers>
    123: 0,  # <Scalar>
    124: 0,  # <Sign>
    125: 0,  # <Stm>
    126: 0,  # <Stm List>
    127: 0,  # <Struct Decl>
    128: 0,  # <Struct Def>
    129: 0,  # <Then Stm>
    130: 0,  # <Type>
    131: 0,  # <Typedef Decl>
    132: 0,  # <Types>
    133: 0,  # <Union Decl>
    134: 0,  # <Value>
    135: 0,  # <Var>
    136: 0,  # <Var Decl>
    137: 0,  # <Var Item>
    138: 0,  # <Var List>
}