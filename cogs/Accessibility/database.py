import logging
import mysql.connector

logging.basicConfig(level=logging.INFO)

db = mysql.connector.connect(
            user="root",
            password="zqf3afr1GVQ9uae-cwe",
            host="Kraken.home",
            port="3306",
            database="Valet"
        )


class Control:
    def __init__(self):
        pass

    def initialize_server_requirements(self, svr_id, svr_members):
        """
        Initializes the server in the Valet database, adds the servers id and any important relevant information

        :param svr_id:
        :param svr_members:
        :return:
        """

        sql = "INSERT INTO registered_guilds (svr_id, svr_members) VALUES (%s, %s)"
        values = (svr_id, svr_members)
        cursor = db.cursor()
        cursor.execute(sql, values)
        db.commit()
        cursor.close()

    def update_guild_members(self, svr_id, svr_members):
        """
        Updates the table with the new information related to the server's members

        :param svr_id:
        :param svr_members:
        :return:
        """
        sql = "UPDATE registered_guilds SET svr_members = %s WHERE svr_id = %s"
        values = (svr_members, svr_id)
        cursor = db.cursor()
        cursor.execute(sql, values)
        db.commit()
        count = cursor.rowcount
        cursor.close()

    def update_premium_member_count(self, svr_id, svr_premium_member_count):
        """
        Updates the number of premium members, returns nothing

        :param svr_id:
        :param svr_premium_member_count:
        :return:
        """

        sql = "UPDATE registered_guilds SET premium_user_count = %s WHERE svr_id = %s"
        values = (svr_premium_member_count, svr_id)
        cursor = db.cursor()
        cursor.execute(sql, values)
        db.commit()
        cursor.close()

    def retrieve_premium_tier(self, svr_id) -> str:
        """
        Returns the amount of boosts the server currently has

        :param svr_id:
        :return premium_tier:
        """

        sql = "SELECT premium_tier FROM registered_guilds WHERE svr_id = %s"
        values = (svr_id,)
        cursor = db.cursor()
        cursor.execute(sql, values)
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result else None

    def retrieve_premium_subscribers(self, svr_id) -> str:
        """

        :param svr_id:
        :return:
        """
        sql = "SELECT premium_subscribers FROM registered_guilds WHERE svr_id = %s"
        values = (svr_id,)
        cursor = db.cursor()
        cursor.execute(sql, values)
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result else None

    def retrieve_premium_member_count(self, svr_id):
        """

        :param svr_id:
        :return:
        """
        sql = "SELECT premium_user_count FROM registered_guilds WHERE svr_id = %s"
        values = (svr_id,)
        cursor = db.cursor()
        cursor.execute(sql, values)
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result else None

    def retrieve_members_database(self, svr_id) -> int:
        """

        :param svr_id:
        :return:
        """
        sql = "SELECT svr_members FROM registered_guilds WHERE svr_id = %s"
        values = (svr_id,)
        cursor = db.cursor()
        cursor.execute(sql, values)
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            return None
        else:
            return int(result[0])

    def retrieve_guild_id(self, svr_id) -> int:
        sql = "SELECT svr_id FROM registered_guilds WHERE svr_id = %s"
        values = (svr_id,)
        cursor = db.cursor()
        cursor.execute(sql, values)
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            return None
        else:
            return int(result[0])
