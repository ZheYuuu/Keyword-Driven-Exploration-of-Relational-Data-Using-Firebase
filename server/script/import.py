from firebase import firebase
import requests
import json
import sys
import mysql.connector
import logging
import pandas as pd
import re
from collections import defaultdict
import pyrebase

FirebaseConfig = dict(
    apiKey = 'AIzaSyA3kqLy7vLxG9ofiuzPo52mdRuyImdUAyE',
    authDomain = 'https://inf551-b0e88.firebaseio.com',
    databaseURL = 'https://inf551-b0e88.firebaseio.com',
    storageBucket = 'https://inf551-b0e88.appspot.com' ,
)


logging.basicConfig(filename='import.log', filemode='a',
                    format='%(name)s - %(levelname)s - %(message)s')
REP = {"-":" ",".":"", "$":"", "#":"", "[":"", "]":"", "/": " ", "'NULL'":None, "(":"", ")":"" }
REP = dict((re.escape(k), v) for k,v in REP.items())
PATTERN = re.compile("|".join(REP.keys()))

class MySQLDB:
    def __init__(self, config):
        self.config = config
        self.foreign_key_relation = {}
        self.meta_data = {}
        self.data = {}
        self.tables = []
        self.index = defaultdict(list)

    def connect(self):
        self.db = mysql.connector.connect(**self.config)
        self.cursor = self.db.cursor()

    def get_meta_data(self, name):
        db = self.config["database"]

        # Acquire meta data of columns
        sql = f'show columns from {name}'
        self.cursor.execute(sql)
        columns = self.cursor.fetchall()
        pri = []
        for i, col in enumerate(columns):
            if "PRI" in col:
                pri.append((i, col[0]))
        meta_data = {"columns": columns, "primary_key": pri}

        # Acquire foreign key relationship
        foreign_key_relation_columns = ['TABLE_SCHEMA', 'TABLE_NAME', 'COLUMN_NAME',
                                        'REFERENCED_TABLE_SCHEMA', 'REFERENCED_TABLE_NAME',
                                        'REFERENCED_COLUMN_NAME']
        foreign_key_columns = ",".join(foreign_key_relation_columns)

        sql = f"select {foreign_key_columns} from INFORMATION_SCHEMA.KEY_COLUMN_USAGE \
            where REFERENCED_TABLE_SCHEMA='{db}' \
                and REFERENCED_TABLE_NAME='{name}'"
        self.cursor.execute(sql)
        foreign_key_relation = self.cursor.fetchall()
        return meta_data, foreign_key_relation

    def get_data(self, name):
        assert name in self.meta_data, f"Table {name} has not loaded meta data."
        # columns = self.meta_data[name]['columns']
        pri = self.meta_data[name]["primary_key"]

        sql = f'select * from {name}'
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        df = pd.DataFrame(data, columns=self.cursor.column_names)
        df["idx"] = df.apply(self._get_pri, axis=1, pri=pri)
        # To Avoid Firebase's array coercion.
        # https://stackoverflow.com/questions/61449625/firebase-realtime-database-automaticlly-add-an-extra-null-when-put-data
        if name=='city':
            df['ID'] = df.apply(lambda x:'city_'+str(x["ID"]), axis=1)
            df['idx'] = df.apply(lambda x:'city_'+str(x["idx"]), axis=1)
        df = df.set_index("idx")
        data = df.astype(str).to_json(orient="index")
        return data
    
    def set_index(self, name):
        data = json.loads(self.data[name])
        for pk, entry in data.items():
            for key,val in entry.items():
                if not isinstance(val, str):
                    continue
                val = PATTERN.sub(lambda x: REP[re.escape(x.group(0))], val)
                words = val.split(" ")
                for word in words:
                    if word=='' or self._is_number(word):
                        continue
                    self.index[word.lower()].append({
                        'table': name,
                        'attribute':key,
                        'pk':pk
                    })
        return
    
    def get_index(self):
        return dict(self.index)
    
    def _is_number(self, x):
        try:
            float(x)
            return True
        except:
            return False




    def _get_pri(self, x, pri):
        pri_str = []
        for idx, attr in pri:
            pri_str.append(str(x[attr]))
        key = "_".join(pri_str)
        key = PATTERN.sub(lambda x: REP[re.escape(x.group(0))], key)
        return key.lower()

    def get_tables(self):
        sql = f'show tables'
        self.cursor.execute(sql)
        tables = self.cursor.fetchall()
        for table in tables:
            name = table[0]
            # Acquire meta data
            meta_data, foreign_key_relation = self.get_meta_data(name)
            self.meta_data[name] = meta_data
            self.foreign_key_relation[name] = foreign_key_relation
            # Acquire data
            data = self.get_data(name)
            self.data[name] = data
            # Set index
            self.set_index(name)
        return self.data

    def get_table(self, name):
        # Acquire meta data
        meta_data, foreign_key_relation = self.get_meta_data(name)
        self.meta_data[name] = meta_data
        self.foreign_key_relation[name] = foreign_key_relation
        # Acquire data
        data = self.get_data(name)
        self.data[name] = data
        return data


class FireBaseDB:
    def __init__(self, name):
        firebase = pyrebase.initialize_app(FirebaseConfig)
        self.db = firebase.database()

    def post_data(self, data, mydb_name):
        for key, val in data.items():
            self.db.child(mydb_name).child(key).set(data=json.loads(val))

    def post_index(self, index, mydb_name):
        self.db.child(mydb_name).child('index').update(data=index)



if __name__ == '__main__':
    mydb_name, firebase_name = sys.argv[1], sys.argv[2]
    # LOAD DATA FROM MySQL
    mysql_config = dict(
        host='localhost',
        user='zheyuuu',
        passwd='pwd',
        database=mydb_name
    )
    mydb = MySQLDB(mysql_config)
    mydb.connect()
    data = mydb.get_tables()
    index = mydb.get_index()
    fbdb = FireBaseDB(firebase_name)
    fbdb.post_data(data, mydb_name)
    fbdb.post_index(index, mydb_name)
