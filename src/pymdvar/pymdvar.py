from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern

VARIABLE_RE = r'\$\{(\w+)\}'


class VariablePattern(Pattern):
    def handleMatch(self, m):
        variable = m.group(2)
        return variable


def makeExtension(*args, **kwargs):
    return VariableExtension(*args, **kwargs)


class VariableExtension(Extension):
    def extendMarkdown(self, md):
        md.inlinePatterns.register(VariablePattern(VARIABLE_RE), 'var', 175)