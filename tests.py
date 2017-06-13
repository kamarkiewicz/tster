from tster import test_case

SQL_FUNCTIONS = '''
CREATE OR REPLACE FUNCTION assert(expected anyelement, got anyelement)
RETURNS SETOF void AS $$
BEGIN
  IF got!=expected THEN
    RAISE EXCEPTION 'got % results, expected %', got, expected;
  END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION truncate_tables()
RETURNS void AS $$
DECLARE
    statements CURSOR FOR
        SELECT tablename FROM pg_tables
        WHERE tableowner = CURRENT_USER AND schemaname = 'public';
BEGIN
    FOR stmt IN statements LOOP
        EXECUTE 'TRUNCATE TABLE ' || quote_ident(stmt.tablename) || ' CASCADE;';
    END LOOP;
END;
$$ LANGUAGE plpgsql;
'''

SQL_TRUNCATE_ALL_TABLES = SQL_FUNCTIONS + '''
    SELECT truncate_tables();
'''

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
        'sql_setup': SQL_TRUNCATE_ALL_TABLES,
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
    }

@test_case(label='api_event')
def test_inserting_event_with_unique_eventname():
    return {
        'sql_setup': SQL_TRUNCATE_ALL_TABLES,
        'stdin': '''
            { "open": { "baza": "${db_name}", "login": "${db_login}", "password": "${db_passwd}"}}
            {"organizer": {"secret": "${secret}", "newlogin": "Donald_Grump11", "newpassword": "admin"}}
            {"event": {"login": "Donald_Grump11", "password": "admin", "eventname": "Konwent", "start_timestamp": "2016-01-20 10:00:00", "end_timestamp": "2016-02-01 18:00:00"}}
            {"event": {"login": "Donald_Grump11", "password": "admin", "eventname": "Konwent", "start_timestamp": "2017-01-20 16:00:00", "end_timestamp": "2017-02-01 18:00:00"}}
        ''',
        'stdout': '''
            {"status": "OK"}
            {"status": "OK"}
            {"status": "OK"}
            {"status": "ERROR"}
        ''',
    }

@test_case(label='api_talk')
def test_accepting_the_proposal():
    return {
        'sql_setup': SQL_TRUNCATE_ALL_TABLES,
        'stdin': '''
            { "open": { "baza": "${db_name}", "login": "${db_login}", "password": "${db_passwd}"}}
            {"organizer": {"secret": "${secret}", "newlogin": "org", "newpassword": "qwerty"}}
            {"user": {"login": "org", "password": "qwerty", "newlogin": "usr1", "newpassword": "qwerty1"}}
            {"proposal": {"login": "usr1", "password": "qwerty1", "talk": "ptalk#u1#t1", "title": "title#u1#t1", "start_timestamp": "2017-01-01 06:15:00"}}
            {"talk": {"login": "org", "password": "qwerty", "speakerlogin": "usr1", "talk": "ptalk#u1#t1", "title": "title#u1#t1", "start_timestamp": "2017-01-01 06:15:00", "room": "958", "initial_evaluation": "5", "eventname": ""}}
        ''',
        'stdout': '''
            {"status": "OK"}
        ''' * 5
    }

@test_case(label='random')
def test_batch():
    return {
        'sql_setup': SQL_TRUNCATE_ALL_TABLES,
        'stdin': open('random.txt').read(),
        'stdout': '''
            {"status": "OK"}
        ''' * 1013
    }

@test_case(label='public_test')
def public_test():
    return {
        'sql_setup': SQL_TRUNCATE_ALL_TABLES,
        'stdin': open('public_test.json').read(),
        'stdout': open('public_test_out.json').read()
    }

@test_case(label='abandoned_talks')
def public_test_with_abandoned_talks():
    return {
        'sql_setup': SQL_TRUNCATE_ALL_TABLES,
        'stdin': open('public_test.json').read() + '''
            {"abandoned_talks": {"login": "org", "password": "qwerty", "limit": 0}}
            {"abandoned_talks": {"login": "org", "password": "qwerty", "limit": 2}}
            {"abandoned_talks": {"login": "usr0", "password": "qwerty0", "limit": 0}}
            {"abandoned_talks": {"login": "usr007", "password": "qwerty007", "limit": 0}}
        ''',
        'stdout': open('public_test_out.json').read() + '''
            {"status":"OK", "data":[{"number":5,"room":"0","start_timestamp":"2017-01-01 02:15:00","talk":"talk#u1#t0","title":"title#u1#t0"},{"number":5,"room":"1","start_timestamp":"2017-01-01 03:15:00","talk":"talk#u1#t1","title":"title#u1#t1"},{"number":5,"room":"1","start_timestamp":"2017-01-01 05:15:00","talk":"talk#u2#t1","title":"title#u2#t1"},{"number":5,"room":"1","start_timestamp":"2017-01-01 09:15:00","talk":"talk#u4#t1","title":"title#u4#t1"},{"number":5,"room":"0","start_timestamp":"2017-01-01 10:15:00","talk":"talk#u5#t0","title":"title#u5#t0"},{"number":5,"room":"1","start_timestamp":"2017-01-01 11:15:00","talk":"talk#u5#t1","title":"title#u5#t1"},{"number":5,"room":"0","start_timestamp":"2017-01-01 14:15:00","talk":"talk#u7#t0","title":"title#u7#t0"},{"number":5,"room":"1","start_timestamp":"2017-01-01 15:15:00","talk":"talk#u7#t1","title":"title#u7#t1"},{"number":5,"room":"1","start_timestamp":"2017-01-01 17:15:00","talk":"talk#u8#t1","title":"title#u8#t1"},{"number":5,"room":"2","start_timestamp":"2017-08-01 02:15:00","talk":"talk#u15#t2","title":"title#u15#t2"},{"number":5,"room":"3","start_timestamp":"2017-08-01 03:15:00","talk":"talk#u15#t3","title":"title#u15#t3"},{"number":3,"room":"1","start_timestamp":"2017-08-01 01:15:00","talk":"talk#u15#t1","title":"title#u15#t1"},{"number":2,"room":"0","start_timestamp":"2017-08-01 00:15:00","talk":"talk#u15#t0","title":"title#u15#t0"},{"number":1,"room":"5","start_timestamp":"2017-08-01 05:15:00","talk":"talk#u15#t5","title":"title#u15#t5"}]}
            {"status":"OK", "data":[{"number":5,"room":"0","start_timestamp":"2017-01-01 02:15:00","talk":"talk#u1#t0","title":"title#u1#t0"},{"number":5,"room":"1","start_timestamp":"2017-01-01 03:15:00","talk":"talk#u1#t1","title":"title#u1#t1"}]}
            {"status":"ERROR"}
            {"status":"ERROR"}
        '''
    }
