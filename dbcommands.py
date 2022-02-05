import mysql.connector
import os

class DBCommands:

    config = {
        'user': os.environ.get("DB_USER"),
        'password': os.environ.get("DB_PASS"),
        'host': os.environ.get("DB_HOST"),
        'database': os.environ.get("DB_NAME"),
        'raise_on_warnings': True
    }

    def get_account_by_name(self, name):

        lol_db = mysql.connector.connect(**self.config)
        cursor = lol_db.cursor(prepared=True)
        cursor.execute("SELECT * FROM `db_lol`.`tbl_summoner` WHERE name = %s", [name])
        results = cursor.fetchall()
        cursor.close()
        lol_db.close()

        return len(results), results

    def match_recorded(self, id):
        lol_db = mysql.connector.connect(**self.config)
        cursor = lol_db.cursor(prepared=True)
        cursor.execute("SELECT * FROM `db_lol`.`tbl_matches` WHERE match_id = %s", [id])
        results = cursor.fetchall()
        cursor.close()
        lol_db.close()

        print(len(results), id)
        return len(results) > 0

    def insert_match(self, id):
        lol_db = mysql.connector.connect(**self.config)
        cursor = lol_db.cursor(prepared=True)

        cursor.execute(
            "INSERT INTO `db_lol`.`tbl_matches` (match_id) VALUES (%s)",
            [id])

        lol_db.commit()
        cursor.close()
        lol_db.close()

    def insert_account(self, account):

        lol_db = mysql.connector.connect(**self.config)
        cursor = lol_db.cursor(prepared=True)

        cursor.execute("INSERT INTO `db_lol`.`tbl_summoner` (account_id, name, encrypted_id, puuid) VALUES (%s, %s, %s, %s)",
                       [account["accountId"], account["name"], account["id"], account["puuid"]])

        lol_db.commit()
        cursor.close()
        lol_db.close()


