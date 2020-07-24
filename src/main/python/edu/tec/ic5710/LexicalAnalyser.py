import re  # Biblioteca que maneja regex de Python

class Scanner:

    def __init__(self, program):

        # Contiene el programa leido del programa.txt
        self.program = program

        # Contiene los identificadores de las palabras clave del Java Tropicalizado al Español.
        self.integer_token = r'[0-9]+'
        self.print_token = r'imprime'
        self.id_token = r'[a-z]+'
        self.Left_parenthesis_token = r'\('
        self.Right_parenthesis_token = r'\)'
        self.semi_colon_token = r';'
        self.operator_token = r'-|\+|/|\*|\+|='
        self.error_token = r'[\S]+'

        # Se crea un regex con todos los posibles tokens para formar la gramatica
        self.grammar = r'(' + self.integer_token + ')|(' + self.print_token + ')|(' \
                         + self.Left_parenthesis_token + ')|(' + self.Right_parenthesis_token + ')|(' \
                         + self.semi_colon_token + ')|(' + self.operator_token + ')|(' \
                         + self.id_token + ')|(' + self.error_token + ')'

        self.founded_tokens = []
        self.wrong_token = []
        self.error = False

        self.find_tokens()
        self.show_tokens()

    def find_tokens(self):

        # Imprime el programa ingresado.
        print(self.program)
        # Prepara la gramatica para hacer match
        self.grammar = re.compile(self.grammar)

        matches = self.grammar.finditer(self.program)

        # Recorre los matches encontrados para asignarles su respectivo tipo.
        for match in matches:
            if type(match.group(1)) == str:
                self.founded_tokens += [["INTEGER", match.group(1)]]
            elif type(match.group(2)) == str:
                self.founded_tokens += [["PRINT", match.group(2)]]
            elif type(match.group(3)) == str:
                self.founded_tokens += [["LEFT_PARENTHESIS", match.group(3)]]
            elif type(match.group(4)) == str:
                self.founded_tokens += [["RIGHT_PARENTHESIS", match.group(4)]]
            elif type(match.group(5)) == str:
                self.founded_tokens += [["SEMI_COLON", match.group(5)]]
            elif type(match.group(6)) == str:
                self.founded_tokens += [["OPERATOR", match.group(6)]]
            elif type(match.group(7)) == str:
                self.founded_tokens += [["IDENTIFIER", match.group(7)]]
            elif type(match.group(8)) == str:
                self.founded_tokens += [["ERROR", match.group(8)]]
            elif type(match.group(9)) == str:
                print("ERROR: Token not recognized." + match.group(9))
                self.error = True

    def show_tokens(self):

        count = 0
        print("Founded tokens: \n")

        for token in self.founded_tokens:
            print(str(count) + " " + str(token))
            count += 1
        print()