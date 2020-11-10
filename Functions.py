from CListener import *
from CParser import *

class Functions(CListener):
    def __init__(self):
        self.functions = []
        self.structs = []
        self.function = False
        self.startLine=0

    def enterFunctionDefinition(self, ctx: CParser.FunctionDefinitionContext):
        self.function = True

    def exitFunctionDefinition(self, ctx: CParser.FunctionDefinitionContext):
        # self.functions.append((ctx.start.text, ctx.))
        # print(ctx.get)
        self.function = False

    def enterDeclarator(self, ctx: CParser.DeclaratorContext):
        if self.function:
            print(ctx.start.line)
            self.startLine = ctx.start.line
            self.function = False
