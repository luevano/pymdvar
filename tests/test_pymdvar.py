import os
import pytest
from markdown import markdown
from pymdvar import VariableExtension


def test_empty_input():
    in_str: str = ''
    exp_str: str = markdown(in_str)
    out_str: str = markdown(in_str, extensions=[VariableExtension()])
    assert out_str == exp_str


@pytest.mark.parametrize('in_str, exp_str', [
    ('foo bar', '<p>foo bar</p>'),
    ('foo *test* bar', '<p>foo <em>test</em> bar</p>'),
    ('foo *PYMDVAR_TEST_1* bar', '<p>foo <em>PYMDVAR_TEST_1</em> bar</p>'),
    ('foo $test bar', '<p>foo $test bar</p>'),
    ('foo **$test}** bar', '<p>foo <strong>$test}</strong> bar</p>'),
    ('foo **$PYMDVAR_TEST_2}** bar', '<p>foo <strong>$PYMDVAR_TEST_2}</strong> bar</p>'),
    ('foo [link](${test/a.html) bar', '<p>foo <a href="${test/a.html">link</a> bar</p>'),
    ('foo ![image]($test}/a.jpg) bar', '<p>foo <img alt="image" src="$test}/a.jpg" /> bar</p>')
])
def test_no_replacements_config(in_str: str, exp_str: str, single_var_dict: dict[str, str]):
    out_str: str = markdown(in_str, extensions=[VariableExtension(variables=single_var_dict, enable_env=True)])
    assert out_str == exp_str


@pytest.mark.parametrize('in_str, exp_str', [
    ('foo *${test}* bar', '<p>foo <em></em> bar</p>'),
    ('foo *${PYMDVAR_TEST_1}* bar', '<p>foo <em></em> bar</p>'),
    ('foo [link](${test}/a.html) bar', '<p>foo <a href="/a.html">link</a> bar</p>'),
])
def test_replacements_no_config(in_str: str, exp_str: str):
    out_str: str = markdown(in_str, extensions=[VariableExtension()])
    assert out_str == exp_str


@pytest.mark.parametrize('in_str, exp_str', [
    ('foo *${test}* bar', '<p>foo <em>value</em> bar</p>'),
    ('foo *${PYMDVAR_TEST_1}* bar', '<p>foo <em>1</em> bar</p>'),
    ('foo ${value} bar', '<p>foo  bar</p>'),
    ('foo **${PYMDVAR_TEST_2}** bar', '<p>foo <strong></strong> bar</p>'),
    ('foo [link](${test}/a.html) bar', '<p>foo <a href="value/a.html">link</a> bar</p>'),
    ('foo ![image](${PYMDVAR_TEST_1}/a.jpg) bar', '<p>foo <img alt="image" src="1/a.jpg" /> bar</p>'),
    ('foo [link](${PYMDVAR_TEST_2}/a.html) bar', '<p>foo <a href="/a.html">link</a> bar</p>')
])
def test_simple_replacements(in_str: str, exp_str: str, single_var_dict: dict[str, str]):
    out_str: str = markdown(in_str, extensions=[VariableExtension(variables=single_var_dict, enable_env=True)])
    assert out_str == exp_str


@pytest.mark.parametrize('in_str, exp_str', [
    ('foo *${test}* bar', '<p>foo <em>value</em> bar</p>'),
    ('foo *${TEST}* bar', '<p>foo <em>VALUE</em> bar</p>'),
    ('foo **${SOMETHING_ELSE}** bar', '<p>foo <strong>something_else</strong> bar</p>')
])
def test_multivar_replacements(in_str: str, exp_str: str, multi_var_dict: dict[str, str]):
    out_str: str = markdown(in_str, extensions=[VariableExtension(variables=multi_var_dict)])
    assert out_str == exp_str


@pytest.mark.parametrize('in_str, exp_str', [
    ('foo *${test}* and **${TEST}** bar', '<p>foo <em>value</em> and <strong>VALUE</strong> bar</p>'),
    ('foo ![image](${PYMDVAR_TEST_1}/a.${ext}) bar', '<p>foo <img alt="image" src="/a.jpg" /> bar</p>')
])
def test_text_multivar_replacements(in_str: str, exp_str: str, multi_var_dict: dict[str, str]):
    out_str: str = markdown(in_str, extensions=[VariableExtension(variables=multi_var_dict)])
    assert out_str == exp_str


@pytest.mark.parametrize('in_str, exp_str', [
    ('foo *${test}* and **${TEST}** bar', '<p>foo <em>value</em> and <strong>VALUE</strong> bar</p>'),
    ('foo ![image](${PYMDVAR_TEST_1}/a.${ext}) bar', '<p>foo <img alt="image" src="/a.jpg" /> bar</p>')
])
def test_extension_text_mode(in_str: str, exp_str: str, multi_var_dict: dict[str, str]):
    out_str: str = markdown(in_str, extensions=['pymdvar'], extension_configs={'pymdvar': {'variables': multi_var_dict}})
    assert out_str == exp_str
