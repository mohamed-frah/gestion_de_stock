import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database import ProductDatabase

class DashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tableau de bord de gestion des stocks")
        self.database = ProductDatabase("localhost", "root", "root", "store")

        # Utilisation du thème "clam"
        self.style = ttk.Style()
        self.style.theme_use("clam")

        

        self.create_widgets()
        self.fetch_products_callback()
        
        self.product_tree.bind("<ButtonRelease-1>", self.display_selected_product_info)

    def create_widgets(self):
        # Treeview pour l'affichage des produits
        self.product_tree = ttk.Treeview(self.root, columns=("ID", "Name", "Description", "Price", "Quantity", "Category"), show='headings')
        self.product_tree.heading("ID", text="ID")
        self.product_tree.heading("Name", text="Nom")
        self.product_tree.heading("Description", text="Description")
        self.product_tree.heading("Price", text="Prix")
        self.product_tree.heading("Quantity", text="Quantité")
        self.product_tree.heading("Category", text="Catégorie")

        # Ajout des barres de défilement
        y_scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.product_tree.yview)
        x_scrollbar = ttk.Scrollbar(self.root, orient="horizontal", command=self.product_tree.xview)
        self.product_tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

        y_scrollbar.pack(side="right", fill="y")
        x_scrollbar.pack(side="bottom", fill="x")

        self.product_tree.pack(expand=True, fill="both")

        # Labels et Entry pour saisir les informations du produit
        ttk.Label(self.root, text="Nom:").pack()
        self.name_entry = ttk.Entry(self.root)
        self.name_entry.pack()

        ttk.Label(self.root, text="Description:").pack()
        self.description_entry = ttk.Entry(self.root)
        self.description_entry.pack()

        ttk.Label(self.root, text="Prix:").pack()
        self.price_entry = ttk.Entry(self.root)
        self.price_entry.pack()

        ttk.Label(self.root, text="Quantité:").pack()
        self.quantity_entry = ttk.Entry(self.root)
        self.quantity_entry.pack()

        ttk.Label(self.root, text="Catégorie:").pack()
        self.category_combobox = ttk.Combobox(self.root, values=[1, 2, 3])
        self.category_combobox.pack()

        # Boutons pour ajouter, mettre à jour et supprimer un produit
        self.add_button = ttk.Button(self.root, text="Ajouter le produit", command=self.add_product_callback)
        self.add_button.pack(side=tk.BOTTOM, pady=10)

        self.update_button = ttk.Button(self.root, text="Modifier le produit sélectionné", command=lambda: self.update_product_callback(self.name_entry.get(), self.description_entry.get(), self.price_entry.get(), self.quantity_entry.get(), self.category_combobox.get()))
        self.update_button.pack(side=tk.BOTTOM, pady=10)

        self.delete_button = ttk.Button(self.root, text="Supprimer le produit sélectionné", command=self.delete_product_callback)
        self.delete_button.pack(side=tk.BOTTOM, pady=10)



    def add_product_callback(self):
    # Ajout d'un produit à la base de données
        name = self.name_entry.get()
        description = self.description_entry.get()
        price = self.price_entry.get()
        quantity = self.quantity_entry.get()
        category = self.category_combobox.get()
        

        if not name or not description or not price or not quantity or not category:
            messagebox.showwarning("Attention", "Tous les champs doivent être remplis.")
            return
        
        try:
            price = int(price)
            quantity = int(quantity)
        except ValueError:
            messagebox.showwarning("Attention", "Le prix doit être un nombre et la quantité un entier.")
            return

    # Appel à la base de données
        if self.database.add_product(name, description, price, quantity, category):
            messagebox.showinfo("Succès", "Produit ajouté avec succès")
            self.fetch_products_callback()  # Actualiser l'affichage
        else:
            messagebox.showerror("Erreur", "Impossible d'ajouter le produit")


    def delete_product_callback(self):
        # Suppression du produit sélectionné de la base de données
        selected_item = self.product_tree.selection()[0]
        product_id = self.product_tree.item(selected_item)['values'][0]
        
        if self.database.delete_product(product_id):
            messagebox.showinfo("Succès", "Produit supprimé avec succès")
            self.fetch_products_callback()  # Actualiser l'affichage
        else:
            messagebox.showerror("Erreur", "Impossible de supprimer le produit")


    def update_product_callback(self,name, description, price, quantity, category):
        selected_item = self.product_tree.selection()
        if selected_item:  # Vérifiez qu'un élément est bien sélectionné
            selected_item = selected_item[0]
            product_id = self.product_tree.item(selected_item)['values'][0]

            new_values = {'name': name, 'description': description, 'price': int(price), 'quantity': int(quantity), 'category': int(category)}

            
            if self.database.update_product(product_id, **new_values):
                messagebox.showinfo("Succès", "Produit mis à jour avec succès")
                self.fetch_products_callback()
            else:
                messagebox.showerror("Erreur", "La mise à jour du produit a échoué")
        else:
            messagebox.showwarning("Sélectionnez un produit", "Veuillez sélectionner un produit à mettre à jour")


    def fetch_products_callback(self):
        # Récupération et affichage des produits
        for i in self.product_tree.get_children():
            self.product_tree.delete(i)
        
        products = self.database.fetch_products()
        for product in products:
            self.product_tree.insert('', 'end', values=product)

    def display_selected_product_info(self, event):
        # Display the information of the selected product in entry widgets
        selected_item = self.product_tree.selection()
        if selected_item:
            selected_item = selected_item[0]
            product_info = self.product_tree.item(selected_item, 'values')

            # Update the entry widgets with the selected product information
            self.name_entry.delete(0, 'end')
            self.name_entry.insert(0, product_info[1])

            self.description_entry.delete(0, 'end')
            self.description_entry.insert(0, product_info[2])

            self.price_entry.delete(0, 'end')
            self.price_entry.insert(0, product_info[3])

            self.quantity_entry.delete(0, 'end')
            self.quantity_entry.insert(0, product_info[4])

            self.category_combobox.set(product_info[5])


def main():
    root = tk.Tk()
    app = DashboardApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()