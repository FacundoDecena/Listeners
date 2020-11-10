import sys
from antlr4 import *
from CLexer import CLexer
from CParser import CParser
from CListener import CListener
from os import walk

from Functions import Functions


def find_c_files(root):
    f = []
    for (dirpath, _, filenames) in walk(top=root):
        for filename in filenames:
            if filename.endswith('.c') or filename.endswith('.h'):
                f.append(dirpath+"/"+filename)
    return f


def main(argv):
    input_stream_root = argv[1]
    files = find_c_files(input_stream_root)
    for file in files:
        print()
        print("File name: " + file)
        try:
            input_stream = FileStream(file)
            lexer = CLexer(input_stream)
            stream = CommonTokenStream(lexer)
            parser = CParser(stream)
            tree = parser.compilationUnit()
            function = Functions()
            ptw = ParseTreeWalker()
            ptw.walk(function, tree)
            print("Functions:", function.functions)
            print("Structs:", function.structs)
        except UnicodeDecodeError:
            print("UnicodeDecodeError caught, skipping file")
    print("Cantidad de archivos", len(files))


if __name__ == '__main__':
    main(sys.argv)
