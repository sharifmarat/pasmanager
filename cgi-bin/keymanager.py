#!/usr/bin/env python3

import sqlite3
import sys

class KeyManager:
    def __init__(self, dbfile):
        self.__connection = sqlite3.connect(dbfile)
        self.__cursor = self.__connection.cursor();

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__cursor.close()
        self.__connection.close()

    def createTable(self):
        with self.__connection:
            self.__cursor.execute("""
                create table if not exists "keys" (
                    id text primary key not null
                        check(
                            typeof("id") = "text" 
                            AND length("id") <= 64),
                    cipher text not null
                        check(
                            typeof("cipher") = "text"
                            AND length("cipher") <= 1048576));""");

    def getCipher(self, id):
        try:
            self.__cursor.execute('select cipher from keys where id=?', (id,))
            cipher = self.__cursor.fetchone()
            if not cipher:
                return None
            else:
                return cipher[0]
        except sqlite3.IntegrityError as e:
            print(e, file=sys.stderr)
            return None
        except sqlite3.OperationalError as e:
            print(e, file=sys.stderr)
            return None

    def addCipher(self, id, cipher):
        try:
            with self.__connection:
                self.__cursor.execute('insert into keys values(?, ?)', (id, cipher))
            return True
        except sqlite3.IntegrityError as e:
            print(e, file=sys.stderr)
            return False

