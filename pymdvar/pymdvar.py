from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern

VARIABLE_RE = r'(\$\{)(\w+)(\})'


class VariablePattern(Pattern):
    def __init__(self, pattern, variables, md=None):
        print(type(variables))
        self.variables = variables
        super().__init__(pattern, md)

    def handleMatch(self, m):
        variable = m.group(3)
        value = ''
        if variable in self.variables:
            value = self.variables[variable]
        return value


class VariableExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {
            'enable_env': [False, 'Enable Environment variables parsing.'],
            'variables': [dict(), 'Dictionary holding variables to be used.']
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        variable = VariablePattern(VARIABLE_RE, variables=self.getConfig('variables'))
        md.inlinePatterns.register(variable, 'variable', 75)