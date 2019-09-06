##
##
##

from textx import metamodel_from_str
from bund.grammar.Grammar import bund_grammar
from bund.grammar.classes import bund_classes

def bund_metamodel():
    metamodel = metamodel_from_file(bund_grammar(), ignore_case=True, classes=bund_classes())
