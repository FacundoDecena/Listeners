import sys
from antlr4 import *
from CLexer import CLexer
from CParser import CParser
from antlr4.TokenStreamRewriter import *
from os import walk

from Functions import Functions
from constant import *


def find_c_files(root):
    files = []
    for (dirpath, _, filenames) in walk(top=root):
        for filename in filenames:
            if filename.endswith('.c') or filename.endswith('.h'):
                files.append(dirpath + "/" + filename)
    return files


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
            stream.fill()
            rewriter = TokenStreamRewriter(tokens=stream)
            parser = CParser(stream)
            tree = parser.compilationUnit()
            function = Functions()
            ptw = ParseTreeWalker()
            ptw.walk(function, tree)
            if len(function.functions) > 0:
                print("Funciones:")
                for function in function.functions:
                    if function[FUNCTION_LINES] > MAX_SAFE_LINES:
                        print("Atencion: Esta funcion tiene más de", MAX_SAFE_LINES, "lineas, puede ser posible "
                                                                                     "dividirla en subfunciones")
                        rewriter.insertBefore("default", function[FUNCTION_START], "/* Es posible que esta funcion "
                                                                                   "pueda ser refactorizada */ \n")
                        ugly_code = rewriter.getText("default", 0, 9000)
                        almost_pretty_code = ugly_code.replace(";", ";\n")
                        almost_pretty_code = almost_pretty_code.replace("{", "{\n")
                        almost_pretty_code = almost_pretty_code.replace("}", "}\n")
                        print(almost_pretty_code)

                    print("\t", function)
            else:
                print("No se encontraron funciones")
        except UnicodeDecodeError:
            print('Salteando archivo por un error de tipo "UnicodeDecodeError"')

    print("\nCantidad de archivos", len(files))


if __name__ == '__main__':
    main(sys.argv)
