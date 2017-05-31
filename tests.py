from tster import test_case

SECRETS = {
    'db_name': 'stud',
    'db_login': 'stud',
    'db_passwd': 'stud',
    'secret': 'my-little-secret',
}

@test_case(label='api_open')
def test_good_creds():
    return {
        'stdin': '''
            { "open": { "baza": "${db_name}", "login": "${db_login}", "password": "${db_passwd}"}}
        ''',
        'stdout': '''
            {"status": "OK"}
        ''',
    }

@test_case(label='api_open')
def test_bad_passwd():
    return {
        'stdin': '''
            { "open": { "baza": "${db_name}", "login": "${db_login}", "password": "garbage"}}
        ''',
        'stdout': '''
            {"status": "ERROR"}
        ''',
    }

@test_case(label='api_open')
def test_bad_baza():
    return {
        'stdin': '''
            { "open": { "baza": "garbage", "login": "${db_login}", "password": "${db_passwd}"}}
        ''',
        'stdout': '''
            {"status": "ERROR"}
        ''',
    }

@test_case(label='api_open')
def test_bad_login():
    return {
        'stdin': '''
            { "open": { "baza": "${db_name}", "login": "garbage", "password": "${db_passwd}"}}
        ''',
        'stdout': '''
            {"status": "ERROR"}
        ''',
    }
