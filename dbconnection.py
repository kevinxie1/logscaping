import psycopg2
import config


def table_exists(con, table_str):
    exists = False
    try:
        cur = con.cursor()
        cur.execute("select exists(select relname from pg_class where relname='" + table_str + "')")
        exists = cur.fetchone()[0]
        print(exists)
    except psycopg2.Error as e:
        print(e)
    finally:
        cur.close()
    return exists


def fetch_table_counts(dbname):
    pass

def fetch_table_count(conn,table_name):
    pass


def get_table_col_names(con, table_str):
    col_names = []
    try:
        cur = con.cursor()
        cur.execute(f"select * from {table_str} LIMIT 0")
        for desc in cur.description:
            col_names.append(desc[0])
        cur.close()
    except psycopg2.Error as e:
        print(e)
    finally:
        cur.close()
    return col_names


def get_table_col_type(con, table_name, column_name):
    data_type = ''
    try:
        cur = con.cursor()
        cur.execute(
            f"select data_type FROM information_schema.columns WHERE  table_name = '{table_name}' and column_name='{column_name}'")
        data_type = cur.fetchone()
    except psycopg2.Error as e:
        print(e)
    finally:
        cur.close()
    return data_type[0]


def get_postgresql_connection(database):
    config.connection[database]['user'],
    conn = psycopg2.connect(
        host=config.connection[database]['host'],
        database=config.connection[database]['database'],
        user=config.connection[database]['user'],
        password=config.connection[database]['password'])
    return conn


def is_clob(con, table_name, column_name):
    list_of_clob_datatypes = ['text', 'citext']
    if get_table_col_type(con, table_name, column_name) in list_of_clob_datatypes:
        return True
    else:
        return False

