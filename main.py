from my_compiler import parser



if __name__ == "__main__":
    parser = parser.Parser("{{")
    ast = parser.parse_expression()
    print(ast)
