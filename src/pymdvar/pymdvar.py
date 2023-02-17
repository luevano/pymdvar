import os
from re import Match
from typing import Any
from xml.etree.ElementTree import Element
from markdown import Markdown
from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern

VAR_RE: str = r'(\$\{)([a-zA-Z_0-9]*)(\})'


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
        if var in self.vars:
            return self.vars[var]
        if self.enable_env:
            if var in os.environ:
                return os.environ[var]
        return ''


class VariableExtension(Extension):
    def __init__(self, **kwargs: Any) -> None:
        self.config: dict[str, list[Any | str]] = {
            'enable_env': [False, 'Enable environment variables parsing.'],
            'variables': [dict(), 'Dictionary holding variables to be used.']
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md: Markdown) -> None:
        vars: dict[str, str] | Any = self.getConfig('variables')
        enable_env: bool = self.getConfig('enable_env')
        var_pattern: VarPattern = VarPattern(VAR_RE, vars, enable_env)
        md.inlinePatterns.register(var_pattern, 'variable', 175)
