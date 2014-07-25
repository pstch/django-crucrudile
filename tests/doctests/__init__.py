from nose.tools import assert_equal

from sphinx.cmdline import main

def test_run_sphinx_doctests():
    assert_equal(
        main(['-N', '-E', '-b', 'doctest', 'docs', 'var/docs_doctests']),
        0
    )
