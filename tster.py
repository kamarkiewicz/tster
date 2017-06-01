#!/usr/bin/python3
import itertools, json, logging, subprocess, sys, string
import secrets, tests

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def io_cleaner(data):
    ''' This should parse your stdin/stdout in a way that is valid in spec.
        The approach allows to have prettified jsons in tests. '''
    if isinstance(data, str):
        data = iter(json.loads(line) for line in data.strip().splitlines() if line.strip())
    return '\n'.join(json.dumps(e) for e in data)

def test_case(label='unknown'):
    ''' Decorator for registering tests. '''
    def func_wrapper(func):
        def test_case_wrapper():
            data = {
                'testname': func.__name__,
                'label': str(label),
            }
            data.update(func())
            for streamtype in ['stdin', 'stdout']:
                assert streamtype in data, "Your test does not contain {} data".format(streamtype)
                data[streamtype] = string.Template(data[streamtype]).substitute(secrets.SECRETS)
                data[streamtype] = io_cleaner(data[streamtype])
            return data
        return test_case_wrapper
    return func_wrapper

def collect_test_cases(module):
    ''' Pythonic mambo-jumbo for collecting your tests from tests.py module. '''
    from types import FunctionType
    return iter(getattr(module, e, None) for e in dir(module)
            if isinstance(getattr(module, e, None), FunctionType)
            and getattr(module, e, None).__name__ is 'test_case_wrapper')

def exec_program(program, stdin):
    ''' Runs your program with stdin filled from the test. '''
    stdout = subprocess.check_output(program, input=stdin.encode(), shell=True)
    return stdout.decode()

def compare_row(expected_row, data_row):
    return set(expected_row.items()) ^ set(data_row.items())

def compare(expected, data):
    expected = [json.loads(line) for line in expected.splitlines()]
    data = [json.loads(line) for line in data.splitlines()]
    assert len(expected) == len(data)
    for i, expected_row, data_row in zip(itertools.count(), expected, data):
        diff = compare_row(expected_row, data_row)
        if diff: yield (i, diff)

def main(args):
    ''' Test runner! '''
    from pprint import pprint

    RES_PENDING = '\33[1m{label}::{testname}\33[0m\t ... '
    RES_OK, RES_FAIL = '\33[1m\33[32mOK\33[0m', '\33[1m\33[31mFAIL\33[0m'

    assert len(args) > 1, 'first argument should be a path to your program'

    PROGRAM = args[1]
    LABEL = next(iter(args[2:]), None) # optional second argument
    PSQL_TOOL = ('PGHOST=localhost PGUSER={db_login} PGPASSWORD={db_passwd} ' +
                 'psql -v ON_ERROR_STOP=1 {db_name}').format(**secrets.SECRETS)

    for test in collect_test_cases(tests):
        data = test()
        if LABEL and LABEL != data['label']: continue
        print(RES_PENDING.format(**data), end='')
        try:
            if 'sql_setup' in data:
                exec_program(PSQL_TOOL, data['sql_setup'])
            result = exec_program(PROGRAM, data['stdin'])
            if 'sql_teardown' in data:
                exec_program(PSQL_TOOL, data['sql_teardown'])
            mismatches = list(compare(data['stdout'], result))
            print('[ {} ]'.format(RES_OK if not mismatches else RES_FAIL))
            if mismatches:
                pprint(mismatches)
        except Exception as e:
            print('[ {} ]'.format(RES_FAIL))
            logger.exception(e)

if __name__ == "__main__":
    main(sys.argv)
