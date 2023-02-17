# pymdvar - Python-Markdown Variable extension

Simple extension meant to be used to convert variables to their corresponding values. Works with environment variables too. This is really just built to be used with my other project [pyssg](https://github.com/luevano/pyssg), as I need it there but I figured it could be released as an extension.

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

The basic usage requires a dictionary with the variables to be passed to the `VariableExtension` options:

```py
>>> import markdown
>>> from pymdvar import VariableExtension
>>> markdown.markdown('foo *${test}* bar', extensions=[VariableExtension(variables={'test': 'value'})])
'<p>foo <em>value</em> bar</p>'
```

if `enable_env=True` option is set, then it will read environment variables, too. Variables in `variables` take preference.

Syntax for the variables should only include the characters: `a-z`, `A-Z`, `_` and `0-9`; this limitation is set like this by personal preference, as the "variable" could be any string, could even include spaces and special chars. Variables not found are just replaced by an empty string.

Passing the extension as a string is supported:

```py
>>> import markdown
>>> markdown.markdown('foo *${test}* bar', extensions=['pymdvar'], extension_configs={'pymdvar': {'variables': {'test': 'value'}}})
'<p>foo <em>value</em> bar</p>'
```

## Options

Only supported options:

- `variables` (default `dict()`):

    Dictionary containing key-value pairs for variable-values. Example

    ```py
    variables={'test': 'value', 'key': 'value'}
    ```
- `enable_env` (default `False`):

    Enables environment variable reading.
