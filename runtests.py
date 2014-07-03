#!/usr/bin/env python
# pylint: disable=W0142,C0111
"""
#TODO: Missing module docstring
"""
import os
import sys

from colorama import (
    Fore as F,
    Back as B,
    Style as S,
)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")


def bright(text):
    print(S.BRIGHT + text + S.RESET_ALL)


def dim(text):
    print(S.DIM + text + S.RESET_ALL)


def error(text):
    print(S.BRIGHT + F.RED, end='')
    print(text, end='')
    print(S.RESET_ALL)


def success(text):
    print(S.BRIGHT + F.GREEN, end='')
    print(text, end='')
    print(S.RESET_ALL)


def format_results(text):
    print(
        str(text).replace(
            "True",
            F.GREEN + "True" + F.RESET
        ).replace(
            "False",
            F.RED + "False" + F.RESET
        )
    )


def run_nose_main():
    bright("#### Running tests using nose test runner...")
    dim("#### (Disable with {}=1)".format(run_nose_main.disable_with))
    print(S.DIM, end='')
    import nose
    return nose.main()
    print(S.RESET_ALL, end='')
    bright("#### Done running tests with Django test runner.")


def run_sphinx_main():
    bright("#### Running tests using Sphinx doctest builder...")
    dim("#### (Disable with {}=1)".format(run_sphinx_main.disable_with))
    import sphinx
    print(S.DIM, end='')
    return sphinx.main(
        ['-N', '-E', '-b', 'doctest', 'docs', 'var/docs_doctests']
    )
    print(S.RESET_ALL, end='')
    bright("#### Done running tests using Sphinx doctest builder.")

run_nose_main.disable_with = "NO_NOSE_TESTS"
run_sphinx_main.disable_with = "NO_SPHINX_TESTS"


def fails(runner, *args, **kwargs):
    runner_name = runner.__name__

    def _error(text):
        error(text.format(runner_name))

    def _success(text):
        success(text.format(runner_name))

    try:
        failed = bool(runner(*args, **kwargs))
        if failed:
            _error("## {} failed by returning True")
        else:
            _success("## {} succeeded by returning False")
    except SystemExit as ex:
        if ex.code:
            _error("## {} failed with SystemExit(True)")
            return True
        else:
            _success("## {} succeeded with SystemExit(False)")
            return False
    except Exception as ex:
        _error("## {} failed with : {}")
        return True


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
    results = dict(
        zip(
            (test.__name__ for test in TESTS),
            list(try_tests(TESTS))
        )
    )

    format_results("## Test results : {}".format(
        results
    ))

    if not all(results.values()):
        error("## Error: (at least) a test runner failed !")
        error("## Failed test runners :")
        for name, result in results.items():
            if not result:
                error("## - {}".format(name))
        sys.exit(1)
    else:
        success("## OK")

if __name__ == '__main__':
    print("## django-crucrudile test runner script")
    runtests()
