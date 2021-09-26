import re
import os
from glob import glob


def scan_files_for_errors_recursively(path, output_file):
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
            error_file = open(output_file, "w")  # append mode
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
        if not re.search(sql[0],out_data):
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


def create_sql_file(data, output_file, out_file_multi):
    sql_file2 = open(out_file_multi, "w")  # append mode
    sql_file = open(output_file, "w")  # append mode
    for line in data.splitlines():
        sql = re.findall('"([^"]*)"', line)
        table = sql[0]
        if len(sql) == 2:
            column = sql[1]
            sql_file.write(f'''alter table {table} add {column}_tmp varchar2(4000);
update {table} set {column}_tmp = {column};
commit;
alter table {table} drop column {column};
alter table {table} rename column {column}_tmp to {column};
''')
            sql_file.write(f'ALTER TABLE {table} ADD PRIMARY KEY ({column})\n\n')
        else:
            for column in sql[1:]:
                sql_file2.write(f'''alter table {table} add {column}_tmp varchar2(4000);
update {table} set {column}_tmp = {column};
commit;
alter table {table} drop column {column};
alter table {table} rename column {column}_tmp to {column};
''')
            sql_file2.write(f'ALTER TABLE {table} ADD PRIMARY KEY ({",".join(sql[1:])})\n\n')
    sql_file.close()
    print(f'{output_file} has been created')
    sql_file2.close()
    print(f'{out_file_multi} has been created')


if __name__ == '__main__':
    errors = scan_files_for_errors_recursively('C:/Users/william/Downloads/BMClog', 'errors_summary.txt')
    # print(errors)
    primary_keys = get_sql_errors(errors)
    # print(primary_keys)
    create_sql_file(deduplicate(primary_keys), 'correction.sql', 'corrections_Multi.sql')
