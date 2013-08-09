from lib2to3.fixer_base import BaseFix
from lib2to3.pgen2 import token

class FixPatchInTests(BaseFix):
    
    _accept_type = token.STRING

    def match(self, node):
        if node.value.strip("'\"") == 'urllib2.urlopen':
            return True
        return False
    
    def transform(self, node, results):
        node.value = "'urllib.request.urlopen'"
        node.changed()
