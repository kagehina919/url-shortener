import sqlite3

class database:
    def __init__(self, **kwargs):
        self.filename = kwargs.get('filename')
        self.table = kwargs.get('table', 'credential')

    def sql_do(self, sql, *params):
        self._db.execute(sql, params)
        self._db.commit()

    def insert(self, row):
        self._db.execute('insert into {} (username, password, email) values (?, ?, ?)'.format(self._table), (row['username'], row['password'], row['email']))
        self._db.commit()

    def retrieve(self, key):
        cursor = self._db.execute('select * from {} where t1 = ?'.format(self._table), (key,))
        return dict(cursor.fetchone())

    def update(self, row):
        self._db.execute(
            'update {} set username = ? where password = ?'.format(self._table),
            (row['username'], row['password']))
        self._db.commit()

    def __iter__(self):
        cursor = self._db.execute('select * from {} order by username'.format(self._table))
        for row in cursor:
            yield dict(row)

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, fn):
        self._filename = fn
        self._db = sqlite3.connect(fn)
        self._db.row_factory = sqlite3.Row

    @filename.deleter
    def filename(self):
        self.close()

    @property
    def table(self):
        return self._table

    @table.setter
    def table(self, t):
        self._table = t

    @table.deleter
    def table(self):
        self._table = 'credential'

    def close(self):
        self._db.close()
        del self._filename


def main():
    db = database(filename = 'credential.db', table = 'credential')

    db.sql_do('drop table if exists credential')
    db.sql_do('create table credential ( username text, password text, email text )')

if __name__ == "__main__": main()