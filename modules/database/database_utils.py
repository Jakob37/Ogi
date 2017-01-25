import sqlite3

import ogi_config

ENTRY_TABLE = 'time_entries'
PROJECT_TABLE = 'projects'
CATEGORY_TABLE = 'categories'

ENTRY_FIELDS = [('date_stamp', 'TEXT'),
                ('time_stamp', 'TEXT'),
                ('log_type', 'TEXT'),
                ('focus', 'INTEGER'),
                ('duration', 'INTEGER'),
                ('message', 'TEXT'),
                ('project', 'TEXT')]

PROJECT_FIELDS = [('name', 'TEXT PRIMARY KEY'),
                  ('category', 'TEXT')]

CATEGORY_FIELDS = [('name', 'TEXT PRIMARY KEY')]


def setup_database(database_path, dry_run=False):

    print("Hello database!")

    conn = sqlite3.connect(database_path)
    c = conn.cursor()

    create_entry_table = get_create_table_command(ENTRY_TABLE, ENTRY_FIELDS, primary_key='name_id')
    create_category_table = get_create_table_command(CATEGORY_TABLE, CATEGORY_FIELDS)
    create_project_table = get_create_table_command(PROJECT_TABLE, PROJECT_FIELDS)

    c.execute(create_entry_table)
    c.execute(create_category_table)
    c.execute(create_project_table)

    if not dry_run:
        conn.commit()
    else:
        print("Dry run, changes not committed")

    conn.close()


def get_connection():

    conf = ogi_config.get_config()
    db_path = conf.get('file_paths', 'sql_path')

    conn = sqlite3.connect(db_path)
    return conn


def close_connection(conn, commit_changes):

    if commit_changes:
        conn.commit()

    conn.close()


def get_create_table_command(table_name, field_tuples, primary_key=None):

    """
    Expects an open SQLite cursor, table name and a list of name/type tuples
    Valid SQLite types are:

    INTEGER, REAL, TEXT, BLOB, NULL
    """

    database_str = 'CREATE TABLE {name} ({fields})'

    field_strings = ['{} {}'.format(field[0], field[1]) for field in field_tuples]

    if primary_key is not None:
        field_strings.append('{} INTEGER PRIMARY KEY'.format(primary_key))

    field_str = ', '.join(field_strings)

    return database_str.format(name=table_name, fields=field_str)


def insert_category_into_database(category_entry):

    conn = get_connection()
    cursor = conn.cursor()

    command_str = 'INSERT INTO {table_name} VALUES (?)'\
        .format(table_name=CATEGORY_TABLE)

    params = (category_entry.name,)

    print(command_str)
    print(params)

    cursor.execute(command_str, params)
    conn.commit()
    conn.close()


def insert_project_into_database(project_entry):

    conn = get_connection()
    cursor = conn.cursor()

    params = (project_entry.name, project_entry.category)

    command_str = 'INSERT INTO {table_name} VALUES (?, ?)'\
        .format(table_name=PROJECT_TABLE)

    cursor.execute(command_str, params)
    conn.commit()
    conn.close()


def insert_time_entry_into_database(time_entry, verbose=False):

    conn = get_connection()
    cursor = conn.cursor()

    params = (time_entry.date, time_entry.time, time_entry.log_type, time_entry.focus, time_entry.duration, time_entry.message, time_entry.project)
    command_str = 'INSERT INTO {table_name} VALUES (?, ?, ?, ?, ?, ?, ?, NULL)'.format(table_name=ENTRY_TABLE)

    if verbose:
        print("Command to be executed: '{}'".format(command_str))

    cursor.execute(command_str, params)
    conn.commit()
    conn.close()


def list_entries_in_table(cursor, table_name):

    for row in cursor.execute('SELECT * FROM {}'.format(table_name)):
        string_values = [str(val) for val in row]
        print('\t'.join(string_values))


def get_categories_as_strings(sep="\t"):

    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM categories')
    category_strings = sql_tuples_to_delimited_strings(c.fetchall(), delim=sep)
    return category_strings


def get_projects_as_strings(sep="\t"):

    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM projects')
    project_strings = sql_tuples_to_delimited_strings(c.fetchall(), delim=sep)
    return project_strings


def get_time_entries_as_strings(sep="\t"):

    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM time_entries')
    time_entry_strings = sql_tuples_to_delimited_strings(c.fetchall(), delim=sep)
    conn.close()
    return time_entry_strings


def sql_tuples_to_delimited_strings(sql_tuples, delim="\t"):

    del_strings = list()

    for tup in sql_tuples:
        str_tup = [str(elem) for elem in tup]
        del_string = delim.join(str_tup)
        del_strings.append(del_string)

    return del_strings


def get_last_time_entry_string():

    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM time_entries WHERE name_id = (SELECT MAX(name_id) FROM time_entries)')
    entry_string = sql_tuples_to_delimited_strings(c.fetchall(), delim='\t')
    conn.close()
    return entry_string[0]


def delete_last_time_entry():

    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM time_entries WHERE name_id = (SELECT MAX(name_id) FROM time_entries)')
    conn.commit()
    conn.close()
