
import mysql.connector
from mysql.connector import Error
from tkinter import messagebox

class ProductDatabase:
    def __init__(self, host, user, passwd, database):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.database = database

    def connect(self):
        try:
            return mysql.connector.connect(
                host=self.host,
                user=self.user,
                passwd=self.passwd,
                database=self.database
            )
        except Error as err:
            messagebox.showerror("Erreur", f"Une erreur s'est produite: {err}")
            return None

    def fetch_products(self):
        try:
            conn = self.connect()
            if conn is not None:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM product")
                rows = cursor.fetchall()
                return rows
        except Error as err:
            messagebox.showerror("Erreur", f"Une erreur s'est produite lors de la récupération des produits: {err}")
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
        return []


    def add_product(self, name, description, price, quantity, category):
        try:
            conn = self.connect()
            if conn is not None:
                cursor = conn.cursor()
                query = "INSERT INTO product (name, description, price, quantity, id_category) VALUES (%s, %s, %s, %s, %s)"
                values = (name, description, price, quantity, category)
                cursor.execute(query, values)
                conn.commit()
                return True
        except Error as err:
            messagebox.showerror("Erreur", f"Une erreur s'est produite lors de l'ajout: {err}")
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
        return False



    def delete_product(self, product_id):
        try:
            conn = self.connect()
            if conn is not None:
                cursor = conn.cursor()
                query = "DELETE FROM product WHERE id = %s"
                cursor.execute(query, (product_id,))
                conn.commit()
                return True
        except Error as err:
            messagebox.showerror("Erreur", f"Une erreur s'est produite lors de la suppression: {err}")
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
        return False


    def update_product(self, product_id, name, description, price, quantity, category):
        try:
            conn = self.connect()
            if conn is not None:
                cursor = conn.cursor()
                query = """
                UPDATE product
                SET name = %s, description = %s, price = %s, quantity = %s, id_category = %s
                WHERE id = %s
                """
                values = (name, description, price, quantity, category, product_id)
                cursor.execute(query, values)
                conn.commit()
                return True
        except Error as err:
            messagebox.showerror("Erreur", f"Une erreur s'est produite lors de la mise à jour: {err}")
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
        return False

