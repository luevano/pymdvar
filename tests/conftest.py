import pytest


@pytest.fixture
def single_var_dict():
    return {'test': 'value'}


@pytest.fixture
def multi_var_dict():
    return {'ext': 'jpg',
            'test': 'value',
            'TEST': 'VALUE',
            'SOMETHING_ELSE': 'something_else'}
