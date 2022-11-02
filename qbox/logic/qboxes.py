import sqlite3
import datetime


FIRST_DAY = datetime.date(1, 1, 1)


class QuestBox():

    def __init__(self, db_name='quest_box.db'):
        self.db_name = db_name

        self._create_table('void', [
            'id INTEGER PRIMARY KEY AUTOINCREMENT',
            'quest TEXT',
        ])
        self._create_table('pandora', [
            'id INTEGER PRIMARY KEY AUTOINCREMENT',
            'quest TEXT',
            'was_born VARCHAR(10)',
        ])
        self._create_table('serif_wall', [
            'id INTEGER PRIMARY KEY AUTOINCREMENT',
            'quest TEXT',
            'deadline VARCHAR(10)',
        ])
        self._create_table('panihida', [
            'id INTEGER PRIMARY KEY AUTOINCREMENT',
            'lifetime INT',
            'was_closed VARCHAR(10)',
        ])

    def _process_sql(self, request):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            print(f"logging:    {request}")
            result = cursor.execute(request).fetchall()
            connection.commit()
        return result

    def _create_table(self, table_name, fields):
        fields = ', '.join(fields)
        self._process_sql(f"CREATE TABLE IF NOT EXISTS {table_name}\
            ({fields});")

    def add_quest(self, quest):
        request_body = f"INSERT INTO void(quest) VALUES('{quest}')"
        self._process_sql(request_body)

    def activate_quest(self, quest):
        add_request = f"INSERT INTO pandora(quest, was_born) \
            VALUES('{quest}', '{datetime.date.today()}')"
        remove_request = f"DELETE FROM void WHERE quest='{quest}'"
        for request in (add_request, remove_request):
            self._process_sql(request)

    def shedule_quest(self, quest, date):
        add_request = f"INSERT INTO serif_wall(quest, deadline) \
            VALUES('{quest}', '{date}')"
        remove_request = f"DELETE FROM void WHERE quest='{quest}'"
        for request in (add_request, remove_request):
            self._process_sql(request)

    def delete_quest(self, quest, table_name):
        request = f"DELETE FROM {table_name} WHERE quest='{quest}'"
        self._process_sql(request)

    def return_quest(self, quest, table_name):
        self.add_quest(quest)
        self.delete_quest(quest, table_name)

    def close_pandora_quest(self, quest):
        fetch_request = f"SELECT was_born FROM pandora \
            WHERE quest='{quest}'"
        result = self._process_sql(fetch_request)
        if not result:
            raise KeyError(f"No quest={quest} in database")
        today_date = datetime.date.today()
        was_born = datetime.datetime.strptime(result[0][0], "%Y-%m-%d").date()
        lifetime = (today_date - was_born).days + 1
        add_request = f"INSERT INTO panihida(lifetime, was_closed) \
            VALUES({lifetime}, '{today_date}')"
        self._process_sql(add_request)
        self.delete_quest(quest, 'pandora')

    def close_serif_quest(self, quest):
        today_date = datetime.date.today()
        add_request = f"INSERT INTO panihida(lifetime, was_closed) \
            VALUES(0, '{today_date}')"
        self._process_sql(add_request)
        self.delete_quest(quest, 'serif_wall')

    def get_statistics(self, left_border=FIRST_DAY,
                       right_border=datetime.date.today()):
        fetch_request = f"SELECT * FROM panihida\
            WHERE was_closed BETWEEN '{left_border}' and '{right_border}'"
        result = self._process_sql(fetch_request)
        result = [sample[1:] for sample in result]
        return result

    def get_table(self, table_name):
        fetch_request = f"SELECT * FROM {table_name}"
        result = self._process_sql(fetch_request)
        result = [sample[1:] for sample in result]
        return result
