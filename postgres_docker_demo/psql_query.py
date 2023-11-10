#!/usr/bin/python
"""
Python code for reading postgres sql as per given use case scenario
"""

import psycopg2
from config import config
from tabulate import tabulate


def connect():
    """ Connect to the PostgreSQL database server from cookpad and fetch schema details """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
        print('Table schema:')
        cur.execute('''
                    SELECT *
                    FROM pg_catalog.pg_tables
                    WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema'
                    ;
        ''')
        table_detail = cur.fetchall()
        print(tabulate(table_detail, tablefmt='psql'))
        print('Exchange_rate table:')
        cur.execute('''
                    SELECT *
                    FROM exchange_rates
        ;''')
        table_detail = cur.fetchall()
        print(tabulate(table_detail, headers=['ts', 'from_currency', 'to_currency', 'rate'], tablefmt='psql'))
        print('Transactions table:')
        cur.execute('''
                    SELECT *
                    FROM transactions
        ;''')
        table_detail = cur.fetchall()
        print(tabulate(table_detail, headers=['ts', 'user_id', 'currency', 'amount'], tablefmt='psql'))
        # actual use case starts here
        print('################# TASK:1 #####################################')
        cur.execute('''
                        SELECT er.ts AS max_exchange_ts, tr.user_id, er.rate, tr.amount 
                        FROM transactions tr left join
                            (SELECT distinct on (from_currency, to_currency) er.*
                            FROM exchange_rates er
                            ORDER BY from_currency, to_currency, er.ts desc
                            ) er
                            on er.from_currency = tr.currency AND
                            er.to_currency = 'GBP'
                    ;''')
        table_detail = cur.fetchall()
        print(tabulate(table_detail, headers=['max_exchange_ts', 'user_id', 'rate', 'amount'], tablefmt='psql'))
        # use case2: Write down the same query, but this time,
        # use the latest exchange rate smaller or equal than the transaction timestamp
        print('################# TASK:2 #####################################')
        cur.execute('''
                    SELECT tr.user_id, tr.amount*er.rate as total_spent_gbp
                    FROM transactions tr left join lateral
                        (SELECT er.*
                        FROM exchange_rates er
                        WHERE er.from_currency = tr.currency and
                        DATE_TRUNC('second', er.ts) <= DATE_TRUNC('seconds', tr.ts)
                        ORDER BY tr.user_id DESC
                        LIMIT 1
                         ) er
                        ON 1=1
                    ;''')
        table_detail = cur.fetchall()
        print(tabulate(table_detail, headers=['user_id', 'total_spent_gbp'], tablefmt='psql'))
        print('################# TASK:3 #####################################')
        print('Query for TASK:3 is same as TASK:2')

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    connect()
