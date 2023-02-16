import pytest
from markdown import markdown
from pymdvar import VariableExtension


def test_empty_input():
    in_str: str = ''
    out_str: str = markdown(in_str, extensions=[VariableExtension()])
    assert in_str == out_str


@pytest.mark.parametrize('in_str, exp_str', [
    ('foo bar', '<p>foo bar</p>'),
    ('foo *test* bar', '<p>foo <em>test</em> bar</p>'),
    ('foo **test** bar', '<p>foo <strong>test</strong> bar</p>'),
    ('foo $test bar', '<p>foo $test bar</p>'),
    ('foo *${test* bar', '<p>foo <em>${test</em> bar</p>'),
    ('foo **$test}** bar', '<p>foo <strong>$test}</strong> bar</p>'),
])
def test_non_replacements(in_str, exp_str):
    out_str: str = markdown(in_str, extensions=[VariableExtension()])
    assert out_str == exp_str


@pytest.mark.parametrize('in_str, exp_str', [
    ('foo ${test} bar', '<p>foo value bar</p>'),
    ('foo *${test}* bar', '<p>foo <em>value</em> bar</p>'),
    ('foo **${test}** bar', '<p>foo <strong>value</strong> bar</p>'),
    ('foo [link](${test}/a.html) bar', '<p>foo <a href="value/a.html">link</a> bar</p>'),
    ('foo ![image](${test}/a.jpg) bar', '<p>foo <img alt="image" src="value/a.jpg" /> bar</p>'),
])
def test_simple_replacements(in_str, exp_str):
    out_str: str = markdown(in_str, extensions=[VariableExtension(variables={'test':'value'})])
    assert out_str == exp_str

