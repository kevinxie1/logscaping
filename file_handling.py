import re
import os
from glob import glob
import psycopg2
import config
from dbconnection import get_postgresql_connection, get_table_names, get_constraints


def create_base_directory(dbname):
    if not os.path.exists(dbname):
        os.makedirs(dbname)


def scan_files_for_errors_recursively(path, config_name, database):
    result = [y for x in os.walk(path) for y in glob(os.path.join(x[0], f'*.{config_name}.*.txt'))]
    line_count = 0
    count = 0
    file_count = 0
    output = ''
    print('scanning...')
    for filename in result:
        if filename.endswith(".txt"):
            file_count += 1
            print(filename)
            log_pattern = re.compile("(.*) ([^\s]*)\s*\[ERROR](.*)")
            error_file = open(
                f"{config.connection[database]['database']}/{config.connection[database]['database']}_{config.error_file}",
                "a")  # append mode
            match_list = []
            error_file.write(f"{filename},\n ")
            with open(f'{filename}', "r") as file:
                error_file.write(f"{filename}\n ")
                for line in file:
                    line_count += 1
                    match = log_pattern.match(line)
                    if not match:
                        continue
                    grps = match.groups()
                    error_file.write(f"{grps[2]},\n ")
                    output += f'{grps[2]}\n'
                    count += 1
            error_file.close()
        else:
            continue
    print(f'''Scanning complete
    Scanned {line_count} lines in {file_count} files
    found {count} errors
''')
    print(f'{error_file.name} has been created holding all error lines from source files')
    return output


def deduplicate(data):
    out_data = ''
    for line in data.splitlines():
        sql = re.findall('"([^"]*)"', line)
        table = sql[0]
        if not re.search(sql[0], out_data):
            out_data += f'{line}\n'
    return out_data


def get_sql_errors(data):
    log_pattern = re.compile("(.*) ([^\s]*)\s*\[RJSql] \[main](.*)")
    output = ''
    for line in data.splitlines():
        match = log_pattern.match(line)
        if not match:
            continue
        grps = match.groups()
        if not re.search(grps[2], output):
            output += f"{grps[2]}\n"
    return output


def create_adjust_column_size_file(database):
    sql_correction = open(
        f"{config.connection[database]['database']}/{config.connection[database]['database']}_adjustment.sql",
        "w")  # append mode
    schema = config.connection[database]['schema']
    try:
        conn = get_postgresql_connection(database)
        tables = get_table_names(conn, schema)
        for table in tables:
            table = table[0]
            constraints = get_constraints(conn, table, schema)
            for constraint in constraints:
                if constraint[0].startswith('CHECK'):
                    column = constraint[0].replace('CHECK ((length(', '').split(') <= ')[0]
                    size = constraint[0].replace('CHECK ((length(', '').split(') <= ')[1][:-2]
                    sql_correction.write(
                        f'''alter table {table.upper()} alter column {column.upper()}_tmp varchar2({size});''')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    print(f'{sql_correction.name} has been created for use if you have already run the corrections.sql')


def create_sql_files(database):
    sql_correction = open(
        f"{config.connection[database]['database']}/{config.connection[database]['database']}_{config.correction_file}",
        "w")  # append mode
    schema = config.connection[database]['schema']
    try:
        conn = get_postgresql_connection(database)
        tables = get_table_names(conn, schema)
        for table in tables:
            table = table[0]
            constraints = get_constraints(conn, table, schema)
            for constraint in constraints:
                if constraint[0].startswith('CHECK'):
                    column = constraint[0].replace('CHECK ((length(', '').split(') <= ')[0]
                    size = constraint[0].replace('CHECK ((length(', '').split(') <= ')[1][:-2]
                    sql_correction.write(f'''alter table {table.upper()} add {column.upper()}_tmp varchar2({size});
update {table.upper()} set {column.upper()}_TMP = {column.upper()};
commit;
alter table {table.upper()} drop column {column.upper()};
alter table {table.upper()} rename column {column.upper()}_TMP to {column.upper()};
''')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    sql_correction.close()
    print(f'{sql_correction.name} has been created use to correct the target database')


def create_count_file(database):
    count_file = open(
        f"{config.connection[database]['database']}/{config.connection[database]['database']}_{config.count_file}",
        "w")  # append mode
    schema = config.connection[database]['schema']
    conn = get_postgresql_connection(database)
    tables = get_table_names(conn, schema)
    for table in tables[:-1]:
        count_file.write(f"select '{table}' as table,count(*) as count from {table}\n union all\n")
    count_file.write(f"select '{table}' as table,count(*) as count from {table[-1]};")
    count_file.close()
    print(f'{count_file.name} has been created use this to get a count for comparison')


def create_Primary_key_files(data, database):
    try:
        conn = get_postgresql_connection(database)
        primary_key_file = open(
            f"{config.connection[database]['database']}/{config.connection[database]['database']}_{config.primary_key_file}",
            "w")  # append mode
        for line in data.splitlines():
            sql = re.findall('"([^"]*)"', line)
            table = sql[0]
            primary_key_file.write(f'ALTER TABLE {table} ADD PRIMARY KEY ({",".join(sql[1:])});\n\n')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    primary_key_file.close()
    print(f'{primary_key_file.name} has been created')
