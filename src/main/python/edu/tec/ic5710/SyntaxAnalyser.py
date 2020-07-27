from src.main.python.edu.tec.ic5710.AbstractSyntaxTree import *


def check_parse(sub_tree):
    if not sub_tree:
        return False
    else:
        return True


class SintaxAnalyser:
    founded_tokens = []
    abstract_syntax_tree = 0
    error_pointer = 0
    founded_tokens_len = 0

    def __init__(self, founded_tokens):

        self.founded_tokens = founded_tokens
        self.founded_tokens_len = len(founded_tokens)
        self.parse()

    def parse(self):

        self.abstract_syntax_tree = ProgramRootNode("PROGRAM_ROOT_NODE", "", [])
        abstract_syntax_tree_pointer = self.abstract_syntax_tree
        founded_token_pointer = 0

        if self.parse_program_root_node(founded_token_pointer):
            print("_Analysis_")
            # semantic_analyser = SemanticAnalyser(self.abstract_syntax_tree)
            # semantic_analysis_report = semantic_analyser.analyse_semantics()

        else:
            self.generate_error()

    def parse_program_root_node(self, founded_token_pointer):

        sub_tree = []
        new_pointer = founded_token_pointer
        succesful_parse = False

        sub_tree, new_pointer = self.parse_production(founded_token_pointer)

        if check_parse(sub_tree):
            self.abstract_syntax_tree.add_node(sub_tree)
            founded_token_pointer = new_pointer
            if founded_token_pointer == self.founded_tokens_len:
                return True
            else:
                return self.parse_program_root_node(founded_token_pointer)
        else:
            self.calculate_error(founded_token_pointer)
            return False

    def generate_error(self):
        tracking = ""
        syntax_error_message = "Invalid Sintax\n"
        max_tracking = 6  # Imprime 6 caracteres despues del error en el programa

        if self.error_pointer == len(self.founded_tokens):
            syntax_error_message += "Missing statement at the end\n"
        self.error_pointer -= 1

        while self.error_pointer > -1 and max_tracking > -1:
            tracking = self.founded_tokens[self.error_pointer][1] + " " + tracking
            self.error_pointer -= 1
            max_tracking -= 1
        tracking += "\x1b[1;31m <--- \x1b[1;37m"
        print(tracking)
        print(syntax_error_message)

    def parse_production(self, founded_token_pointer):

        sub_tree = []
        new_pointer = founded_token_pointer
        succesful_parse = False

        self.parse_declaration(founded_token_pointer)

        if check_parse(sub_tree):
            founded_token_pointer = new_pointer
            succesful_parse = True
        else:
            self.parse_assignation(founded_token_pointer)

            if check_parse(sub_tree):
                founded_token_pointer = new_pointer
                succesful_parse = True
            else:
                print("PROHIBIDO")
                self.parse_print(founded_token_pointer)

                if check_parse(sub_tree):
                    founded_token_pointer = new_pointer
                    succesful_parse = True

        if succesful_parse:
            return sub_tree, founded_token_pointer
        else:
            self.calculate_error(founded_token_pointer)
            return [], -1

    def calculate_error(self, founded_token_pointer):
        if founded_token_pointer > self.error_pointer:
            self.error_pointer = founded_token_pointer

    def parse_declaration(self, founded_token_pointer):

        sub_tree = DeclarationNode("DECLARATION", "DECLARATION", [])
        new_founded_token_pointer = founded_token_pointer

        sub_tree.add_node(self.create_node(founded_token_pointer))
        founded_token_pointer += 1
        print("_Declaration_")
        sub_tree_aux, new_founded_token_pointer = self.parse_assignation(founded_token_pointer)

        if check_parse(sub_tree_aux):
            puntero_token = new_founded_token_pointer
            sub_tree.add_node(sub_tree_aux)
            return sub_tree, founded_token_pointer
        self.calculate_error(founded_token_pointer)
        return [], -1

    def parse_assignation(self, founded_token_pointer):

        sub_tree = AssignationNode("ASSIGNATION", "ASSIGNATION", [])
        new_founded_token_pointer = founded_token_pointer
        print("_Assignation_")
        if self.compare_types("IDENTIFIER", founded_token_pointer):
            sub_tree.add_node(self.create_node(founded_token_pointer))
            founded_token_pointer += 1

            if self.compare_types("EQUAL_ASSIGNATION", founded_token_pointer):
                founded_token_pointer += 1
                sub_tree_aux, new_founded_token_pointer = self.parse_algebraic_operation(founded_token_pointer)

                if check_parse(sub_tree_aux):
                    founded_token_pointer = new_founded_token_pointer
                    sub_tree.add_node(sub_tree_aux)
                    if self.compare_types("SEMI_COLON", founded_token_pointer):
                        founded_token_pointer += 1

                        return sub_tree, founded_token_pointer
        self.calculate_error(founded_token_pointer)
        return [], -1

    def parse_algebraic_operation(self, founded_token_pointer):

        print("_Algebraic_")
        sub_tree = AlgebraicOperationNode("ALGEBRAIC_OPERATION", "ALGEBRAIC_OPERATION", [])

        if self.compare_types("INTEGER", founded_token_pointer) or self.compare_types("IDENTIFIER",
                                                                                      founded_token_pointer):

            sub_tree.add_node(self.create_node(founded_token_pointer))
            founded_token_pointer += 1
            while self.compare_types("OPERATOR", founded_token_pointer):

                sub_tree.add_node(self.create_node(founded_token_pointer))
                founded_token_pointer += 1
                if self.compare_types("INTEGER", founded_token_pointer) or self.compare_types("IDENTIFIER",
                                                                                              founded_token_pointer):
                    sub_tree.add_node(self.create_node(founded_token_pointer))
                    founded_token_pointer += 1
                else:
                    self.calculate_error(founded_token_pointer)
                    return [], -1
            return sub_tree, founded_token_pointer
        self.calculate_error(founded_token_pointer)
        return [], -1

    def parse_print(self, founded_token_pointer):
        sub_tree = PrintProductionNode("PRINT_PRODUCTION", "PRINT_PRODUCTION", [])

        if self.compare_types("PRINT", founded_token_pointer):
            sub_tree.add_node(self.create_node(founded_token_pointer))
            founded_token_pointer += 1

            if self.compare_types("LEFT_PARENTHESIS", founded_token_pointer):
                founded_token_pointer += 1

                if self.compare_types("IDENTIFIER", founded_token_pointer):
                    sub_tree.add_node(self.create_node(founded_token_pointer))

                    if self.compare_types("RIGHT_PARENTHESIS", founded_token_pointer):
                        founded_token_pointer += 1

                        if self.compare_types("SEMI_COLON", founded_token_pointer):
                            founded_token_pointer += 1
                            return sub_tree, founded_token_pointer
        self.calculate_error(founded_token_pointer)
        return [], -1

    def compare_types(self, token_type, founded_token_pointer):
        print(">>> Compare_: " + str(token_type) + " " + str(founded_token_pointer) + " " + self.founded_tokens[
            founded_token_pointer][0] + " " + self.founded_tokens[founded_token_pointer][1])
        print("\n")

        if founded_token_pointer < self.founded_tokens_len:
            if self.founded_tokens[founded_token_pointer][0] == token_type:
                return True
        return False

    def create_node(self, founded_token_pointer):
        token_type = self.founded_tokens[founded_token_pointer][0]
        token_value = self.founded_tokens[founded_token_pointer][1]
        node = []
        if token_type == "IDENTIFIER":
            node = IdentifierNode(token_type, token_value, [])
        elif token_type == "EQUAL_ASSIGNATION":
            node = EqualAssignationNode(token_type, token_value, [])
        elif token_type == "SEMI_COLON":
            node = SemiColonNode(token_type, token_value, [])
        elif token_type == "INTEGER":
            node = IntegerNode(token_type, token_value, [])
        elif token_type == "OPERATOR":
            node = OperatorNode(token_type, token_value, [])
        elif token_type == "PRINT":
            node = PrintNode(token_type, token_value, [])
        return node

    def print_abstract_syntax_tree(self):
        print(self.abstract_syntax_tree.children_nodes[0].children_nodes[0].type)

        abstract_syntax_tree_list = [self.abstract_syntax_tree]
        str_abstract_syntax_tree = ""

        while abstract_syntax_tree_list:

            str_abstract_syntax_tree += abstract_syntax_tree_list[0].type + "\n---> "

            for child in abstract_syntax_tree_list[0].children_nodes:
                str_abstract_syntax_tree += child.type + " "
                abstract_syntax_tree_list += [child]

            str_abstract_syntax_tree += "\n\n"
            abstract_syntax_tree_list = abstract_syntax_tree_list[1:]

        print("ABSTRACT SYNTAX TREE: \n")
        print(str_abstract_syntax_tree)