T_INT = 'T_INT'
T_FLOAT = 'FLOAT'
T_BOOL = 'BOOL'
T_STRING = 'STRING'
T_CHAR = 'CHAR'
T_PLUS = 'PLUS'
T_MINUS = 'MINUS'
T_MUL = 'MUL'
T_DIV = 'DIV'
T_EQUALS = 'EQUALS'
T_GT = 'GREATER THAN'
T_LT = 'LESS THAN'
T_NOTEQUALS = 'NOT EQUALS'
T_LPAREN = 'LPAREN'
T_RPAREN = 'RPAREN'
T_IDENT = 'IDENT'
T_BLOCK_START = 'BLOCK_START'
T_BLOCK_END = 'BLOCK_END'
T_TYPE = ('int', 'float', 'char', 'bool', 'string')
T_DECLARATION = 'T_DECLARATION'
T_SEMI_COLON = 'SEMI COLON'
T_IF = 'T_IF'
T_FOR = 'T_FOR'


class Error:
    def __init__(self, error_name, details):
        self.error_name = error_name
        self.details = details

    def as_string(self):
        return f'{self.error_name}: {self.details}'


class IllegalCharacterError(Error):
    def __init__(self, details):
        super().__init__('Illegal Character', details)


class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __repr__(self):
        if self.value:
            return f'{self.type}: {self.value}'
        return f'{self.type}'


class Lexer:
    def __init__(self, text):
        self.text = text + '$'
        self.pos = -1
        self.current_char = None
        self.advance()

    def advance(self, value=1):
        self.pos += value
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def make_tokens(self):
        tokens = []
        error = []
        while self.current_char != '$':
            if self.current_char in list(' \n\t\r'):
                self.advance()
            elif self.current_char.isdigit():
                tokens.append(self.make_number())
            elif self.current_char == '+':
                tokens.append(Token(T_PLUS, self.current_char))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(T_MINUS, self.current_char))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(T_MUL, self.current_char))
                self.advance()
            elif self.current_char == 'f' and self.text[self.pos + 1] == 'o' and self.text[self.pos + 2] == 'r':
                tokens.append(Token(T_FOR, self.current_char + self.text[self.pos + 1] + self.text[self.pos + 2]))
                self.advance(3)
            elif self.current_char == 'i' and self.text[self.pos + 1] == 'f':
                tokens.append(Token(T_IF, self.current_char + self.text[self.pos + 1]))
                self.advance(2)
            elif self.current_char == '/':
                tokens.append(Token(T_DIV, self.current_char))
                self.advance()
            elif self.current_char == ';':
                tokens.append(Token(T_SEMI_COLON, self.current_char))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(T_LPAREN, self.current_char))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(T_RPAREN, self.current_char))
                self.advance()
            elif self.current_char == '{':
                tokens.append(Token(T_BLOCK_START, self.current_char))
                self.advance()
            elif self.current_char == '}':
                tokens.append(Token(T_BLOCK_END, self.current_char))
                self.advance()
            elif self.current_char == '+':
                tokens.append(Token(T_PLUS, self.current_char))
                self.advance()
            elif self.current_char == '>':
                tokens.append(Token(T_GT, self.current_char))
                self.advance()
            elif self.current_char == '<':
                tokens.append(Token(T_LT, self.current_char))
                self.advance()
            elif self.current_char == '!' and self.text[self.pos + 1] == '=':
                tokens.append(Token(T_NOTEQUALS, self.current_char))
                self.advance(2)
            elif self.current_char == '=':
                tokens.append(Token(T_EQUALS, self.current_char))
                self.advance()
            elif self.current_char.isalpha():
                ident = ""
                count = 0
                # self.current_char = str(self.current_char)
                while self.current_char.isalnum():
                    count += 1
                    ident += self.current_char
                    self.advance()
                if ident in ('int', 'float', 'bool', 'char', 'string'):
                    tokens.append(Token(T_DECLARATION, ident))
                else:
                    if self.text[self.pos - 4:self.pos - count - 1] in "intbooldoublefloatcharstring":
                        tokens.append(Token(T_IDENT, ident))
                    else:
                        error.append(IllegalCharacterError(f"'{ident}'"))

        return tokens, error

    def make_number(self):
        num_str = ''
        dot_count = 0

        while self.current_char.isdigit() or self.current_char == '.':
            if self.current_char == '.':
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += 1
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(T_INT, int(num_str))
        else:
            return Token(T_FLOAT, float(num_str))


def make_sybol_table(liste):
    table = []
    for i in range(len(liste)):
        tmp = {}
        if liste[i - 1].value in ['string', 'bool', 'char', 'double', 'int', 'char']:
            found = False
            for dic in table:
                if liste[i].value in dic.keys():
                    found = True
            if not found:
                tmp[liste[i].value] = {'type': liste[i - 1].value, 'portée': 'locale'}
                if liste[i - 1].value in ['string']:
                    tmp[liste[i].value]['Adresse'] = '256'
            else:
                tmp[liste[i].value] = {'type': liste[i - 1].value, 'portée': 'locale au BLOC'}
                if liste[i - 1].value in ['string']:
                    tmp[liste[i].value]['Adresse'] = '256'
            table.append(tmp)
    return table


def run(text):
    lexer = Lexer(text)
    tokens, error = lexer.make_tokens()
    table = make_sybol_table(tokens)
    return tokens, table, error
