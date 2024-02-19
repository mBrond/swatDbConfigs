#créditos: https://gist.github.com/snorfalorpagus/8578272#file-mdb2sqlite-py-L69
import pyodbc
import sqlite3
from collections import namedtuple
import re
import os


def mdb2sqlite(filename_in="", filename_out=""):
    """
    Converte um banco de dados mdb (Microsoft Acess) para sqlite
    :param filename_in: Caminho do banco de dados .mdb. Se vazio,
    :param filename_out: Caminho do banco de dados .sqlite
    :return: Arquivo Sqlite no caminho de filename_out
    """

    path = os.getcwd()
    if filename_in == "":
        filename_in = path+"\\HWSD.mdb"
    elif ".mdb" not in filename_in:
        filename_in = filename_in+"\\"+"HWSD.mdb"
    elif "\\" not in filename_in:
        filename_in = path+"\\"+filename_in

    cnxn = pyodbc.connect('Driver={{Microsoft Access Driver (*.mdb, *.accdb)}};Dbq={};'.format(filename_in))

    #decode utf 16
    cnxn.setdecoding(pyodbc.SQL_WCHAR, encoding='latin-1')

    cursor = cnxn.cursor()

    conn = sqlite3.connect(filename_out)

    c = conn.cursor()

    Table = namedtuple('Table', ['cat', 'schem', 'name', 'type'])

    # get a list of tables
    tables = []
    for row in cursor.tables():
        if row.table_type == 'TABLE':
            t = Table(row.table_cat, row.table_schem, row.table_name, row.table_type)
            tables.append(t)

    for t in tables:
        print(t.name)

        # SQLite tables must being with a character or _
        t_name = t.name
        if not re.match('[a-zA-Z]', t.name):
            t_name = '_' + t_name

        # get table definition
        columns = []
        for row in cursor.columns(table=t.name):
            print
            '    {} [{}({})]'.format(row.column_name, row.type_name, row.column_size)
            col_name = re.sub('[^a-zA-Z0-9]', '_', row.column_name)
            columns.append('{} {}({})'.format(col_name, row.type_name, row.column_size))
        cols = ', '.join(columns)

        # create the table in SQLite
        c.execute('DROP TABLE IF EXISTS "{}"'.format(t_name))
        c.execute('CREATE TABLE "{}" ({})'.format(t_name, cols))

        # copy the data from MDB to SQLite
        cursor.execute('SELECT * FROM "{}"'.format(t.name))
        for row in cursor:
            values = []
            for value in row:
                if value is None:
                    values.append(None)
                else:
                    if isinstance(value, bytearray):
                        value = sqlite3.Binary(value)
                    else:
                        value = u'{}'.format(value)
                    values.append(value)
            v = ', '.join(['?'] * len(values))
            sql = 'INSERT INTO "{}" VALUES(' + v + ')'
            c.execute(sql.format(t_name), values)

    conn.commit()
    conn.close()