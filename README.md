# pymdvar - Python-Markdown Variable extension

Simple extension meant to be used to convert variables to their corresponding values. Works with environment variables too.

It uses the `${variable}` syntax. For example, given `variable=value`, the following text:

```md
Foo ${variable} bar
```

Becomes:

```html
<p>Foo value bar</p>
```

## Install

`pymdvar` can be installed via `pip`:

```sh
python -m pip install pymdvar
```

## Usage

The basic usage requires a dictionary with the variables to be passed to the `VariableExtension`:

```py
>>> import markdown
>>> from pymdvar import VariableExtension
>>> markdown.markdown('foo *${test}* bar', extensions=[VariableExtension(variables={'test': 'value'})])
'<p>foo <em>value</em> bar</p>'
```

if `enable_env=True` is passed, then it will read environment variables, too. Variables in `variables` take preference.

Only `a-z`, `A-Z`, `_` and `0-9` characters are accepted.

Passing the extension as a string is supported:

```py
>>> import markdown
>>> markdown.markdown('foo *${test}* bar', extensions=['pymdvar'], extension_configs={'pymdvar': {'variables': {'test': 'value'}}})
'<p>foo <em>value</em> bar</p>'
```