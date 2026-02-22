OPERATORS = [
    '//=', '**=', '>>=', '<<=',
    '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=', ':=',
    '==', '!=', '<=', '>=', '<<', '>>',
    '**', '//', '->', '...',
    '+', '-', '*', '/', '%', '&', '|', '^', '~', '<', '>', '=', '@',
]

DELIMITERS = ['(', ')', '[', ']', '{', '}', ',', '.', ':', ';']
PUNCT_SET = frozenset(OPERATORS + DELIMITERS)
MAX_OP_LEN = max(len(op) for op in OPERATORS)

def get_punc_type(token):
    """Return 'OPERATOR' or 'DELIMITER' or None."""
    if token in OPERATORS:
        return 'OPERATOR'
    if token in DELIMITERS:
        return 'DELIMITER'
    return None

def is_punc(token):
    return token in PUNCT_SET