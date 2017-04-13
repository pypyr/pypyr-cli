"""py.py unit tests."""
import pypyr.steps.py
import pytest


def test_py_single_code():
    """One word shell command works."""
    context = {'pycode': 'print(1+1)'}
    context = pypyr.steps.py.run_step(context)


def test_py_sequence():
    """Sequence of py code works and touches context."""
    context = {'pycode': "context['test'] = 1;"}
    pypyr.steps.py.run_step(context)

    context.update({'pycode': "context['test'] += 2"})
    pypyr.steps.py.run_step(context)

    context.update({'pycode': "context['test'] += 3"})
    pypyr.steps.py.run_step(context)

    assert context['test'] == 6, "context should be 6 at this point"


def test_py_sequence_with_semicolons():
    """Single py code string with semi - colons works."""
    context = {'pycode':
               'print(1); print(2); print(3);'}
    pypyr.steps.py.run_step(context)

    assert context == {'pycode':
                       'print(1); print(2); print(3);'}, ("context in and out "
                                                          "the same")


def test_py_sequence_with_linefeeds():
    """Single py code string with linefeeds works."""
    context = {'pycode':
               'print(1)\nprint(2)\nprint(3)'}
    pypyr.steps.py.run_step(context)


def test_pycode_error_throws():
    """pycode error should raise up to caller."""
    with pytest.raises(AssertionError):
        context = {'pycode': 'assert False'}
        pypyr.steps.py.run_step(context)


def test_no_pycode_context_throw():
    """No pycode in context should throw assert error."""
    with pytest.raises(AssertionError):
        context = {'blah': 'blah blah'}
        pypyr.steps.py.run_step(context)


def test_empty_pycode_context_throw():
    """Empty pycode in context should throw assert error."""
    with pytest.raises(AssertionError):
        context = {'pycode': None}
        pypyr.steps.py.run_step(context)