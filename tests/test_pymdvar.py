import pytest
from markdown import markdown
from pymdvar import VariableExtension


def test_empty_input():
    in_str = ''
    out_str = markdown(in_str, extensions=[VariableExtension()])
    print(in_str)
    print(out_str)
    assert in_str == out_str


@pytest.mark.parametrize('in_str, exp_str', [
    ('foo bar', '<p>foo bar</p>'),
    ('foo *test* bar', '<p>foo <em>test</em> bar</p>'),
    ('foo **test** bar', '<p>foo <strong>test</strong> bar</p>')
])
def test_non_replacements(in_str, exp_str):
    out_str = markdown(in_str, extensions=[VariableExtension()])
    assert out_str == exp_str


@pytest.mark.parametrize('in_str, exp_str', [
    ('foo ${test} bar', '<p>foo value bar</p>'),
    ('foo *${test}* bar', '<p>foo <em>value</em> bar</p>'),
    ('foo **${test}** bar', '<p>foo <strong>value</strong> bar</p>')
])
def test_simple_replacements(in_str, exp_str):
    out_str = markdown(in_str, extensions=[VariableExtension(variables={'test':'value'})])
    assert out_str == exp_str

