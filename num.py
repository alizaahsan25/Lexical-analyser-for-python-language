import re
_PATTERNS = [
    ('FLOAT_EXP',  r'^[0-9][0-9_]*\.[0-9_]*[eE][+-]?[0-9][0-9_]*$'),  
    ('FLOAT',      r'^[0-9][0-9_]*\.[0-9_]*$|^\.[0-9][0-9_]*$'),      
    ('COMPLEX',    r'^[0-9][0-9_]*(\.[0-9_]*)?[jJ]$'),                
    ('HEX',        r'^0[xX][0-9a-fA-F][0-9a-fA-F_]*$'),           
    ('BINARY',     r'^0[bB][01][01_]*$'),                            
    ('OCTAL',      r'^0[oO][0-7][0-7_]*$'),                        
    ('INT_EXP',    r'^[0-9][0-9_]*[eE][+-]?[0-9][0-9_]*$'),           
    ('INT',        r'^[0-9][0-9_]*$'),                                    
]

def get_num_type(token):
    """Return numeric sub-type string if token is a number, else None."""
    for num_type, pattern in _PATTERNS:
        if re.match(pattern, token):
            return num_type
    return None

def is_number(token, line, col):
    """Return 'NUM:<subtype>' string if numeric literal, else None."""
    num_type = get_num_type(token)
    if num_type:
        return 'NUM:' + num_type
    return None