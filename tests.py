from tster import test_case

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

@test_case(label='api_organizer')
def test_organizer_creation():
    return {
        'sql_setup': '''
            SELECT 0 = (SELECT count(*) FROM person);
        ''',
        'stdin': '''
            { "open": { "baza": "${db_name}", "login": "${db_login}", "password": "${db_passwd}"}}
            { "organizer": { "secret": "${secret}", "newlogin": "stefan", "newpassword": "banach"}}
            { "organizer": { "secret": "${secret}", "newlogin": "stefan", "newpassword": "muller"}}
        ''',
        'stdout': '''
            {"status": "OK"}
            {"status": "OK"}
            {"status": "ERROR"}
        ''',
        'sql_teardown': '''
            SELECT 1 = (SELECT count(*) FROM person);
            DELETE FROM person;
        '''
    }
