from regtomach.parser import Parser


def main():
    parser = Parser("{A|[CD]B}")

    syntax_tree = parser.generate_syntax_tree()

    print(syntax_tree)
    syntax_tree.save_to_png()


if __name__ == "__main__":
    main()
