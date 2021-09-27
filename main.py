import re
import os
from glob import glob
import psycopg2
import config
from dbconnection import get_postgresql_connection, is_clob, fetch_table_count


def scan_files_for_errors_recursively(path):
    result = [y for x in os.walk(path) for y in glob(os.path.join(x[0], '*.txt'))]
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
            error_file = open(config.error_file, "w")  # append mode
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
        output += f"{grps[2]}\n"
    return output


def create_sql_files(data, database):
    try:
        conn = get_postgresql_connection()
        sql_file = open(f"{config.connection[database]['database']}_{config.correction_file}", "w")  # append mode
        sql_file2 = open(f"{config.connection[database]['database']}_{config.count_file}", "w")  # append mode

        for line in data.splitlines():
            sql = re.findall('"([^"]*)"', line)
            table = sql[0]
            if line[-1]:
                sql_file2.write(f'''select count(*) from {table} ;''')
            else:
                sql_file2.write(f'''select count(*) from {table} 
union all
''')
            if len(sql) == 2:
                column = sql[1]
                sql_file.write(f'''alter table {table} add {column}_tmp varchar2({config.varchar_size});
    update {table} set {column}_tmp = {column};
    commit;
    alter table {table} drop column {column};
    alter table {table} rename column {column}_tmp to {column};
    ''')
                sql_file.write(f'ALTER TABLE {table} ADD PRIMARY KEY ({column})\n\n')
            else:
                for column in sql[1:]:
                    if is_clob(conn, table, column):
                        sql_file.write(f'''alter table {table} add {column}_tmp varchar2(4000);
    update {table} set {column}_tmp = {column};
    commit;
    alter table {table} drop column {column};
    alter table {table} rename column {column}_tmp to {column};
    ''')
                sql_file.write(f'ALTER TABLE {table} ADD PRIMARY KEY ({",".join(sql[1:])})\n\n')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        sql_file.close()
        print(f'{sql_file.name} has been created')
        print("closing connection")


if __name__ == '__main__':
     errors = scan_files_for_errors_recursively(config.path_to_logs)
     primary_keys = get_sql_errors(errors)
     # create_sql_files(deduplicate(primary_keys), 'db1')
     # fetch_table_count('db1')

     for line in primary_keys.splitlines():
        if line[-1]:
            print("last")
        else:
            print('not last')