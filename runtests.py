#!/usr/bin/env python
# pylint: disable=W0142,C0111
"""
#TODO: Missing module docstring
"""
import os
import sys
import nose


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")


def run_nose_main():
    print("#### Running tests using nose test runner...")
    print("#### (Disable with {}=1)".format(run_nose_main.disable_with))
    return nose.main()
    print("#### Done running tests with Django test runner.")


def run_sphinx_main():
    print("#### Running tests using Sphinx doctest builder...")
    print("#### (Disable with {}=1)".format(run_sphinx_main.disable_with))
    import sphinx
    return sphinx.main(['-E', '-b', 'doctest', 'docs', 'var/docs_doctests'])
    print("#### Done running tests using Sphinx doctest builder.")

run_nose_main.disable_with = "NO_NOSE_TESTS"
run_sphinx_main.disable_with = "NO_SPHINX_TESTS"


def fails(runner, *args, **kwargs):
    try:
        return bool(runner(*args, **kwargs))
    except SystemExit as ex:
        return ex.code
    except Exception as ex:
        print("## {} failed with : {}".format(runner, ex))
        return True
    return False


def safely_run_if_enabled(runner):
    if os.environ.get(runner.disable_with) != '1':
        return not fails(runner)


def try_tests(tests):
    for test in tests:
        yield safely_run_if_enabled(test)


TESTS = [
    run_nose_main,
    run_sphinx_main
]


def runtests():
    print("## django-crucrudile test runner script")
    results = list(try_tests(TESTS))
    print("## Test results : {}".format(
        dict(
            zip(
                (test.__name__ for test in TESTS),
                results)
        )
    ))
    if not all(results):
        print("## Error: (at least) a test runner failed !")
        sys.exit(1)
    else:
        print("## OK")

if __name__ == '__main__':
    print("## django-crucrudile test runner script")
    runtests()
