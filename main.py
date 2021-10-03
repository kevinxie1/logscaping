#!/usr/bin/python3
import os
import config
import file_handling as fh

if __name__ == '__main__':
    for conf in config.connection:
        fh.create_base_directory(config.connection[conf]['database'])
        # derived from Files
        errors = fh.scan_files_for_errors_recursively(config.path_to_logs, config.connection[conf]['rj_config'], conf)
        primary_keys = fh.get_sql_errors(errors)
        fh.create_Primary_key_files(primary_keys, conf) # do not use in conjunction with adjustment file
        # derived from source database
        fh.create_sql_files(conf)  # use if first time correction
        fh.create_adjust_column_size_file(conf)  # use if adjusting after first time correctio
        fh.create_count_file(conf)
