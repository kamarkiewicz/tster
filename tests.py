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
        'sql_teardown': '''
            SELECT assert(1, (SELECT count(*) FROM person)::integer);
        '''
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
