"""
This module offers a simple way to connect and perform operations on a PostgreSQL database.
"""

import psycopg as pg
import logging

from typing import Optional


class Postgres:
    def __init__(self, user: str, database: str, password: str, host: str) -> None:
        if not (user and database and password and host):
            logging.error(
                f"Failed connection attempt to database {database} with parameters: user={user}, host={host}. Either invalid or empty parameters"
            )
            raise Exception(
                "Invalid/Empty database connection parameters (user, database, host, password)."
            )

        self._user = user
        self._database = database
        self._password = password
        self._host = host
        self.__conn: pg.Connection

    def connect(self) -> None:
        self.__conn = pg.connect(
            f"dbname={self._database} user={self._user} password={self._password} host={self._host}"
        )
        logging.info(f"Called connect method on postgres database {self._database}")

    def close(self) -> None:
        self.__conn.close()
        logging.info(f"Closed connection to database {self._database}")

    def query(self, query: str, params: Optional[any] = None) -> any:
        logging.info(f"Queried the database {self._database} > {query}")

        if not self.__conn:
            raise Exception("Not connected to database.")

        with self.__conn.cursor() as curr:
            curr.execute(query, params)

            try:
                return curr.fetchall()
            except Exception:
                return None

    def create_database(self, name: str, template: Optional[str] = None) -> None:
        self.__conn.rollback()
        self.__conn.autocommit = True
        q = f"CREATE DATABASE {name}"

        if template is not None and len(template) > 0:
            q += f" TEMPLATE {template}"

        self.__conn.execute(q)
        self.__conn.autocommit = False
        logging.info(f"Attempted to create new database named {name}")

    def drop_database(self, name: str) -> None:
        self.__conn.rollback()
        self.__conn.autocommit = True
        self.__conn.execute(f"DROP DATABASE IF EXISTS {name};")
        self.__conn.autocommit = False
        logging.info(f"Attempted to drop database named {name}")

    def clear_table(
        self, name: str, cascade: bool = False, restart_id: bool = False
    ) -> None:
        try:
            self.transaction()
            q = f"TRUNCATE {name}"

            if restart_id:
                q += "RESTART IDENTITY"
            if cascade:
                q += "CASCADE"

            self.query(q)
        except Exception as e:
            self.rollback()
            raise Exception(f"Não foi possível limpar a base de dados. Detalhe: {e}.")
        finally:
            self.commit()
        logging.info(f"Attempted to clear database {name}")

    def transaction(self) -> None:
        self.__conn.transaction()
        logging.info(f"Started transaction on database {self._database}")

    def commit(self) -> None:
        self.__conn.commit()
        logging.info(f"Called commit on  database {self._database}")

    def rollback(self) -> None:
        self.__conn.rollback()
        logging.info(f"Called rollback on database {self._database}")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback) -> None:
        self.close()


def get_all_database_names(conn: Postgres) -> list[str]:
    try:
        dbs = conn.query(
            "SELECT datname FROM pg_database WHERE datistemplate = FALSE;", None
        )
        return [db[0] for db in dbs]
    except Exception as e:
        logging.warn(
            f"Could not retrieve the names of the avaiable databases. Detail: {e}"
        )
        return []
