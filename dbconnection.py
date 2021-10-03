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
    return psycopg2.connect(
        host=config.connection[database]['host'],
        database=config.connection[database]['database'],
        user=config.connection[database]['user'],
        password=config.connection[database]['password'])


def is_clob(con, table_name, column_name):
    list_of_clob_datatypes = ['text', 'citext']
    if get_table_col_type(con, table_name, column_name) in list_of_clob_datatypes:
        return True
    else:
        return False


def get_length(conn, table_name, column_name):
    sql = f'select max(length({column_name})) from {table_name};'
    cur = conn.cursor()
    cur.execute(sql)
    max_field_length = cur.fetchone()
    print(max_field_length)
    return max_field_length


def get_constraints(conn, table, schema):
    cur = conn.cursor()
    cur.execute(f"""SELECT pg_get_constraintdef(con.oid)
                   FROM pg_catalog.pg_constraint con
                        INNER JOIN pg_catalog.pg_class rel
                                   ON rel.oid = con.conrelid
                        INNER JOIN pg_catalog.pg_namespace nsp
                                   ON nsp.oid = connamespace
                   WHERE nsp.nspname = '{schema}'
                         AND rel.relname = '{table}';""")
    return cur.fetchall()


def get_table_names(con, schema):
    table_sql = f'''SELECT table_name FROM
        information_schema.tables
        WHERE
        table_schema = '{schema}';'''
    cur = con.cursor()
    cur.execute(table_sql)
    return cur.fetchall()
