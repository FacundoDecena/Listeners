from CListener import *
from CParser import *


class Functions(CListener):
    def __init__(self):
        self.functions = []
        self.structs = []
        self.function = False
        self.text = ""

    def enterFunctionDefinition(self, ctx: CParser.FunctionDefinitionContext):
        self.function = True

    def exitFunctionDefinition(self, ctx: CParser.FunctionDefinitionContext):
        length = ctx.stop.line - ctx.start.line
        self.functions.append((self.text, ctx.start.line, ctx.stop.line, length))
        self.function = False

    def enterDeclarator(self, ctx: CParser.DeclaratorContext):
        if self.function:
            self.text = ctx.start.text
            if self.text == '(':
                self.text = "No se pudo recuperar el nombre de la funcion"
            self.function = False
