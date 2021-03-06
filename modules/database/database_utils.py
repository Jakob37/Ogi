import sqlite3

import ogi_config

from modules.utils import date_utils

ENTRY_TABLE = 'time_entries'
PROJECT_TABLE = 'projects'
CATEGORY_TABLE = 'categories'
WORK_TYPE_TABLE = 'work_types'
DAY_TABLE = 'days'

ENTRY_FIELDS = [('date_stamp', 'TEXT'),
                ('time_stamp', 'TEXT'),
                ('log_type', 'TEXT'),
                ('focus', 'INTEGER'),
                ('duration', 'INTEGER'),
                ('message', 'TEXT'),
                ('project', 'TEXT'),
                ('name_id', 'INTEGER PRIMARY KEY'),
                ('work_type', 'TEXT')]
PROJECT_FIELDS = [('name', 'TEXT PRIMARY KEY'),
                  ('category', 'TEXT')]
CATEGORY_FIELDS = [('name', 'TEXT PRIMARY KEY')]
WORK_TYPE_FIELDS = [('name', 'TEXT PRIMARY KEY')]
DAY_FIELDS = [('name_id', 'INTEGER PRIMARY KEY'),
              ('date_stamp', 'TEXT'),
              ('description', 'TEXT'),
              ('focus_project', 'TEXT'),
              ('alertness', 'INTEGER'),
              ('sleep_time', 'NUMERIC'),
              ('external_pressure', 'INTEGER'),
              ('internal_pressure', 'INTEGER'),
              ('clarity', 'INTEGER')]


# ENTRY_FIELDS = [
#                 ('id', 'INTEGER PRIMARY KEY'),
#                 ('date_stamp', 'TEXT'),
#                 ('time_stamp', 'TEXT'),
#                 ('log_type', 'TEXT'),
#                 ('focus', 'INTEGER'),
#                 ('duration', 'INTEGER'),
#                 ('message', 'TEXT'),
#                 ('project', 'TEXT'),
#                 ('work_type', 'TEXT')
#                 ]
# PROJECT_FIELDS = [
#                   ('id', 'INTEGER PRIMARY KEY'),
#                   ('name', 'TEXT PRIMARY KEY'),
#                   ('category', 'TEXT')
#                  ]
# CATEGORY_FIELDS = [
#                    ('id', 'INTEGER PRIMARY KEY'),
#                    ('name', 'TEXT PRIMARY KEY')
#                   ]
# WORK_TYPE_FIELDS = [
#                     ('id', 'INTEGER PRIMARY KEY'),
#                     ('name', 'TEXT PRIMARY KEY')
#                    ]
# DAY_FIELDS = [
#               ('id', 'INTEGER PRIMARY KEY'),
#               ('date_stamp', 'TEXT'),
#               ('description', 'TEXT'),
#               ('focus_project', 'TEXT'),
#               ('alertness', 'INTEGER'),
#               ('sleep_time', 'NUMERIC'),
#               ('external_pressure', 'INTEGER'),
#               ('internal_pressure', 'INTEGER'),
#               ('clarity', 'INTEGER')
#               ]


def setup_database(database_path, dry_run=False):

    print("Hello database!")

    conn = sqlite3.connect(database_path)
    c = conn.cursor()

    # create_entry_table = get_create_table_command(ENTRY_TABLE, ENTRY_FIELDS, primary_key='name_id')
    create_entry_table = get_create_table_command(ENTRY_TABLE, ENTRY_FIELDS)
    create_category_table = get_create_table_command(CATEGORY_TABLE, CATEGORY_FIELDS)
    create_project_table = get_create_table_command(PROJECT_TABLE, PROJECT_FIELDS)
    create_work_type_table = get_create_table_command(WORK_TYPE_TABLE, WORK_TYPE_FIELDS)
    create_day_table = get_create_table_command(DAY_TABLE, DAY_FIELDS)

    c.execute(create_entry_table)
    c.execute(create_category_table)
    c.execute(create_project_table)
    c.execute(create_work_type_table)
    c.execute(create_day_table)

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


def get_create_table_command(table_name, field_tuples):

    """
    Expects an open SQLite cursor, table name and a list of name/type tuples
    Valid SQLite types are:

    INTEGER, REAL, TEXT, BLOB, NULL
    """

    database_str = 'CREATE TABLE {name} ({fields})'

    field_strings = ['{} {}'.format(field[0], field[1]) for field in field_tuples]

    # if primary_key is not None:
    #     field_strings.append('{} INTEGER PRIMARY KEY'.format(primary_key))

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

    params = (time_entry.date,
              time_entry.time,
              time_entry.log_type,
              time_entry.focus,
              time_entry.duration,
              time_entry.message,
              time_entry.project,
              time_entry.work_type,)
    command_str = 'INSERT INTO {table_name} VALUES (?, ?, ?, ?, ?, ?, ?, NULL, ?)'.format(table_name=ENTRY_TABLE)

    if verbose:
        print("Command to be executed: '{}'".format(command_str))

    cursor.execute(command_str, params)
    conn.commit()
    conn.close()


def insert_work_type_entry_into_database(work_type_entry):

    conn = get_connection()
    cursor = conn.cursor()

    command_str = 'INSERT INTO {table_name} VALUES (?)' \
        .format(table_name=WORK_TYPE_TABLE)

    params = (work_type_entry.name,)

    cursor.execute(command_str, params)
    conn.commit()
    conn.close()


def insert_day_entry_into_database(day_entry):

    conn = get_connection()
    cursor = conn.cursor()

    command_str = 'INSERT INTO {table_name} VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)'.format(table_name=DAY_TABLE)

    params = (day_entry.date,
              day_entry.description,
              day_entry.focus,
              day_entry.alertness,
              day_entry.sleep_time,
              day_entry.external_pressure,
              day_entry.internal_pressure,
              day_entry.clarity)

    cursor.execute(command_str, params)
    conn.commit()


def list_entries_in_table(cursor, table_name):

    for row in cursor.execute('SELECT * FROM {}'.format(table_name)):
        string_values = [str(val) for val in row]
        print('\t'.join(string_values))


def get_categories_as_strings(sep="\t"):

    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM categories')
    category_strings = sql_tuples_to_delimited_strings(c.fetchall(), delim=sep)
    conn.close()
    return category_strings


def get_work_types_as_strings(sep="\t"):

    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM work_types')
    work_type_strings = sql_tuples_to_delimited_strings(c.fetchall(), delim=sep)
    conn.close()
    return work_type_strings


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


def get_today_day_entries():

    current_date = date_utils.get_current_date()

    today_entries = list()
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM days WHERE date_stamp = {}'.format(current_date))
    for entry in c:
        today_entries.append(entry)
    conn.commit()
    conn.close()
    return today_entries


def update_project_name(original_name, updated_name):

# UPDATE users SET role=99 WHERE name='Fred'

    raise NotImplementedError('Tables needs to be set up with numbers as primary tables')

    alter_proj_command = 'ALTER PROJECT at {proj_table} WHERE name_id = {orig_name}'
    alter_time_entry_command = 'UPDATE {time_entry_table} SET project={new_name} WHERE project = {orig_name}'

    conn = get_connection()
    c = conn.cursor()

    c.execute(alter_proj_command)
    c.execute(alter_time_entry_command)

    conn.commit()
    conn.close()





