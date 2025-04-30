

class Parser:

    def __init__(self):
        cursor: int = 0

    def parse(self, input_: str):
        stack: list = []

        for idx, token in enumerate(input_):

            match token:

                case "|":
                    self.parse_alternative()

                case "{":
                    self.parse_kleen()

                case "[":
                    self.parse_optional()
                
                case _:
                    self.parse_sentence()
                

    def parse_empty(self):
        pass

    def parse_sentence(self):
        pass

    def parse_alternative(self):
        pass

    def parse_kleen(self):
        pass

    def parse_optional(self):
        pass


if __name__ == "__main__":
    parser = Parser()

    print(parser.parse("{}"))
