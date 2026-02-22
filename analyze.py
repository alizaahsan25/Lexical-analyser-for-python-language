import re
import sys
from dataclasses import dataclass
from collections import Counter
from keywords import is_keyword
from num      import get_num_type
from ID       import is_ID

@dataclass
class Token:
    type:  str
    value: str
    line:  int
    col:   int

    def __str__(self):
        return (f'({self.type:<14} {self.value!r:<40} '
                f' line {self.line:>3}, col {self.col:>3})')

_STR_PREFIX = r'(?:[bBuUrRfF]|rb|rB|Rb|RB|br|bR|Br|BR|fr|fR|Fr|FR|rf|rF|Rf|RF)?'

_TOKEN_RE = re.compile(
    r'(?P<STR_TRIPLE>'
        + _STR_PREFIX +
        r'(?:"""[\s\S]*?"""|'
        r"'''[\\s\\S]*?''')"
    r')'
    r'|(?P<STR_SINGLE>'
        + _STR_PREFIX +
        r'(?:"(?:[^"\\\n]|\\.)*"|'
        r"'(?:[^'\\\n]|\\.)*')"
    r')'
    r'|(?P<COMMENT>  \#[^\r\n]*                                )'
    r'|(?P<NEWLINE>  \r?\n                                      )'
    r'|(?P<SKIP>     [ \t]+                                     )'
    r'|(?P<NUM>'
        r'0[xX][0-9a-fA-F][0-9a-fA-F_]*'            # hex
        r'|0[bB][01][01_]*'                          # binary
        r'|0[oO][0-7][0-7_]*'                        # octal
        r'|[0-9][0-9_]*\.[0-9_]*[eE][+-]?[0-9][0-9_]*'  # float+exp
        r'|[0-9][0-9_]*\.[0-9_]*[jJ]'               # complex float
        r'|[0-9][0-9_]*\.[0-9_]*'                    # float
        r'|\.[0-9][0-9_]*'                           # leading-dot float
        r'|[0-9][0-9_]*[eE][+-]?[0-9][0-9_]*[jJ]'   # complex exp
        r'|[0-9][0-9_]*[eE][+-]?[0-9][0-9_]*'       # int+exp
        r'|[0-9][0-9_]*[jJ]'                         # complex int
        r'|[0-9][0-9_]*'                             # int
    r')'
    r'|(?P<ID>       [^\W\d]\w*                                 )'
    r'|(?P<OP3>      //=|\*\*=|>>=|<<=                          )'
    r'|(?P<OP2>      \+=|-=|\*=|/=|%=|&=|\|=|\^=|:=|==|!=|<=|>='
                    r'|<<|>>|\*\*|//|->|\.\.\.                  )'
    r'|(?P<OP1>      [+\-*/%&|^~<>=@!]                          )'
    r'|(?P<DELIM>    [(){}\[\],.:;]                              )'
    r'|(?P<UNKNOWN>  \S                                          )',
    re.VERBOSE
)

def tokenize(source: str):
    tokens = []
    errors = []
    line_no    = 1
    line_start = 0

    for mo in _TOKEN_RE.finditer(source):
        kind  = mo.lastgroup
        value = mo.group()
        col   = mo.start() - line_start + 1

        if kind == 'NEWLINE':
            line_no   += 1
            line_start = mo.end()
            continue

        if kind == 'SKIP':
            continue

        if kind == 'COMMENT':
            continue

        if kind in ('STR_TRIPLE', 'STR_SINGLE'):
            tokens.append(Token('STR', value, line_no, col))
            line_no   += value.count('\n')
            if '\n' in value:
                line_start = mo.start() + value.rfind('\n') + 1
            continue

        if kind == 'NUM':
            if len(value) > 255:
                errors.append(f'  ! Numeric constant too long ({len(value)} chars) at line {line_no}, col {col}')
                tokens.append(Token('UNKNOWN', value, line_no, col))
            else:
                sub = get_num_type(value) or 'INT'
                tokens.append(Token('NUM:' + sub, value, line_no, col))
            continue

        if kind == 'ID':
            if len(value) > 255:
                errors.append(f'  ! Identifier too long ({len(value)} chars) at line {line_no}, col {col}')
                tokens.append(Token('UNKNOWN', value, line_no, col))
                continue
            kw = is_keyword(value, line_no, col)
            if kw == 'KEYWORD':
                if value in ('True', 'False'):
                        tokens.append(Token('BOOL', value, line_no, col))
                elif value == 'None':
                        tokens.append(Token('NONE', value, line_no, col))
                else:
                        tokens.append(Token('KEYWORD', value, line_no, col))
            elif kw == 'BUILTIN':
                tokens.append(Token('BUILTIN', value, line_no, col))
            else:
                tokens.append(Token('ID', value, line_no, col))
            continue

        if kind in ('OP3', 'OP2', 'OP1'):
            tokens.append(Token('OPERATOR', value, line_no, col))
            continue

        if kind == 'DELIM':
            tokens.append(Token('DELIMITER',value, line_no, col))
            continue

        errors.append(
            f'  ! Unknown token {value!r}  →  line {line_no}, col {col}'
        )
        tokens.append(Token('UNKNOWN', value, line_no, col))

    tokens.append(Token('EOF', '', line_no, 0))
    return tokens, errors

def print_tokens(tokens):
    header = f"{'TYPE':<16} {'VALUE':<42} {'LINE':>5}  {'COL':>4}"
    sep    = '─' * len(header)
    print(header)
    print(sep)
    for tok in tokens:
        if tok.type == 'EOF':
            continue
        print(f'{tok.type:<16} {tok.value!r:<42} {tok.line:>5}  {tok.col:>4}')
    print(sep)


def print_summary(tokens):
    counts = Counter(t.type for t in tokens if t.type != 'EOF')
    print('\n TOKEN SUMMARY: ')
    for ttype, count in sorted(counts.items(), key=lambda x: -x[1]):
        print(f'  {ttype:<18}: {count}')
    total = sum(counts.values())
    print(f'  {"─"*28}')
    print(f'  {"TOTAL":<18}: {total}')


if __name__ == '__main__':
    myfile = input('Enter Python filename: ').strip()

    try:
        with open(myfile, 'r', encoding='utf-8') as f:
            source = f.read()
    except FileNotFoundError:
        print(f'Error: file not found — {myfile}')
        sys.exit(1)
    except Exception as ex:
        print(f'Error reading file: {ex}')
        sys.exit(1)

    if not source.strip():
        print(f'Error: file is empty — {myfile}')
        sys.exit(1)

    tokens, errors = tokenize(source)

    print(f'\n── Lexical Analysis: {myfile} {"─" * (40 - len(myfile))}')
    print_tokens(tokens)
    print_summary(tokens)

    if errors:
        print('\n LEXICAL ERRORS:')
        for e in errors:
            print(e)
    else:
        print('\n No lexical errors found.')

    print('\n(ENDMARKER)')
