import sqlite3

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


def insert_category_into_database(cursor, category_entry):

    category_values = str(category_entry).split('\t')
    category_value_string = ','.format(category_values)

    command_str = 'INSERT INTO {table_name} VALUES ({values})'\
        .format(table_name=CATEGORY_TABLE, values=category_value_string)

    cursor.execute(command_str)


def insert_project_into_database(cursor, project_entry):

    project_name = project_entry.name
    project_cat = project_entry.category

    value_string = '{name}, {category}'.format(name=project_name, category=project_cat)

    command_str = 'INSERT INTO {table_name} VALUES {{values}}'\
        .format(table_name=PROJECT_TABLE, values=value_string)

    cursor.execute(command_str)


def insert_time_entry_into_database(cursor, time_entry):

    values = str(time_entry).split('\t')
    value_string = ', '.format(values)

    command_str = 'INSERT INTO {table_name} VALUES ({values}, NULL)'\
        .format(table_name=ENTRY_TABLE, values=value_string)

    cursor.execute(command_str)


def list_entries_in_table(cursor, table_name):

    for row in cursor.execute('SELECT * FROM {}'.format(table_name)):
        string_values = [str(val) for val in row]
        print('\t'.join(string_values))
