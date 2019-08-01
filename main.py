import psycopg2, sqlite3, datetime, sys

# postgresql connection information
conn_pg = psycopg2.connect(dbname='db',user='user',password='123456',host='localhost',port='5432')
cur_pg = conn_pg.cursor()

# sqlite3 connection information
conn_sqlite = sqlite3.connect('/tmp/db.sqlite3')
cur_sqlite = conn_sqlite.cursor()

# all tables, these tables should had been created in sqlite3
tbls = ['table1','table2',...]

for tbl in tbls:
    print('table:%s,' % (tbl), end=' ')
    cnt = 0
    cnt_err = 0
    cur_pg.execute('select * from %s' % (tbl))
    rows = cur_pg.fetchall()
    # get fieds name
    fld_names = [desc[0] for desc in cur_pg.description]
    for row in rows:
        values = []
        for col in row:
            if type(col) is int:
                values.append(str(col))
            elif type(col) is str:
                values.append('"'+col+'"')
            elif type(col) is bool:
                if col:
                    values.append('1')
                else:
                    values.append('0')
            elif type(col) == None.__class__:
                values.append('""')
            elif type(col) is datetime.date or type(col) is datetime.datetime or type(col) is datetime.time:
                if type(col) is datetime.datetime:
                    col = col.date()
                elif type(col) is datetime:
                    col = ''
                values.append(str(col))
            else:
                values.append(col)
        try:
            cur_sqlite.execute('insert into %s (%s) values(%s)' % (tbl,','.join(fld_names),','.join(values)))
            cnt += 1
        except Exception as e:
            print('insert into %s (%s) values(%s)' % (tbl,','.join(fld_names),','.join(values)))
            print()
            print(e)
            conn_sqlite.close()
            conn_pg.close()
            sys.exit()
            cnt_err += 1
    print('records count:%s, inserted:%s, errors:%s.' % (len(rows),cnt,cnt_err))

conn_sqlite.commit()
conn_pg.close()
conn_sqlite.close()
