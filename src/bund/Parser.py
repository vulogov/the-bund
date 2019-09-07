##
##
##
import bund
import dpath.util

class Parser(object):
    def __init__(self):
        self.mm = bund.grammar.MetaModel.bund_metamodel()
        self.d  = {}
    def load_namespace(self, buffer)

if __name__ == '__main__':
    p = Parser()
    p.load_namespace(open("../examples/3.bund").read())
