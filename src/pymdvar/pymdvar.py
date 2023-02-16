from os import getenv
from re import Match
from typing import Any
from xml.etree.ElementTree import Element
from markdown import Markdown
from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern

VAR_RE: str = r'(\$\{)([a-zA-Z_]*)(\})'


class VarPattern(Pattern):
    # need to redefine as an extra attribute needs to be passed
    def __init__(self, pattern: Any,
                 vars: dict[str, str],
                 enable_env: bool,
                 md: Markdown | None = None) -> None:
        self.vars: dict[str, str] = vars
        self.enable_env: bool = enable_env
        super().__init__(pattern, md)

    def handleMatch(self, m: Match[str]) -> str | Element | None:
        # for some reason the group is offest by 1
        var: str | Any = m.group(3)
        value: str = ''

        if var in self.vars:
            value = self.vars[var]
        else:
            if self.enable_env:
                value = getenv(var, '')
        return value


class VariableExtension(Extension):
    def __init__(self, **kwargs: Any) -> None:
        self.config: dict[str, list[Any | str]] = {
            'enable_env': [False, 'Enable environment variables parsing.'],
            'variables': [dict(), 'Dictionary holding variables to be used.']
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md: Markdown) -> None:
        vars: dict[str, str] | Any = self.getConfig('variables', dict())
        enable_env: bool = self.getConfig('enable_env', False)
        var_pattern: VarPattern = VarPattern(VAR_RE, vars, enable_env)
        md.inlinePatterns.register(var_pattern, 'variable', 175)


def makeExtension(*args: Any, **kwargs: Any):
    return VariableExtension(*args, **kwargs)
