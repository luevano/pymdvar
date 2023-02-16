from os import getenv
from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern

VARIABLE_RE = r'(\$\{)([a-zA-Z_]*)(\})'


class VariablePattern(Pattern):
    # need to redefine as an extra attribute needs to be passed
    def __init__(self, pattern, variables, enable_env, md=None):
        self.variables = variables
        self.enable_env = enable_env
        super().__init__(pattern, md)

    def handleMatch(self, m):
        # for some reason the group is offest by 1
        variable = m.group(3)
        value = ''

        if variable in self.variables:
            value = self.variables[variable]
        else:
            if self.enable_env:
                value = getenv(variable, '')
        return value


class VariableExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {
            'enable_env': [False, 'Enable environment variables parsing.'],
            'variables': [dict(), 'Dictionary holding variables to be used.']
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        variables = self.getConfig('variables', dict())
        enable_env = self.getConfig('enable_env', False)
        variable_pattern = VariablePattern(VARIABLE_RE, variables, enable_env)
        md.inlinePatterns.register(variable_pattern, 'variable', 175)


def makeExtension(*args, **kwargs):
    return VariableExtension(*args, **kwargs)
