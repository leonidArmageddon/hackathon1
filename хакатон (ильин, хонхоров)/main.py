import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
from PIL import Image, ImageTk

class OnlineStoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Онлайн магазин мебели")

        # База для данных товаров
        self.products = [
            {'id': 1, 'name': 'Стул', 'price': 499},
            {'id': 2, 'name': 'Стол', 'price': 5000},
            {'id': 3, 'name': 'Шкаф', 'price': 9999},
            {'id': 4, 'name': 'Кровать', 'price': 6999},
            {'id': 5, 'name': 'Кресло', 'price': 3999},
        ]

        # База данных для пользователей
        self.users = [
            {'id': 1, 'name': 'User 1', 'password': 'password1', 'cart': [], 'profile_picture': None},
            {'id': 2, 'name': 'User 2', 'password': 'password2', 'cart': [], 'profile_picture': None},
        ]

        # Создание виджетов
        self.label = tk.Label(root, text="Онлайн Магазин", font=('Helvetica', 16))
        self.label.pack(pady=10)

        self.login_button = tk.Button(root, text="Вход", command=self.login)
        self.login_button.pack()

        self.register_button = tk.Button(root, text="Регистрация", command=self.register)
        self.register_button.pack()

        self.search_entry = tk.Entry(root, width=30)
        self.search_entry.pack()

        self.search_button = tk.Button(root, text="Поиск", command=self.search_products)
        self.search_button.pack()

        self.product_listbox = tk.Listbox(root, selectmode=tk.SINGLE, height=5)
        for product in self.products:
            self.product_listbox.insert(tk.END, f"{product['name']} - {product['price']} ₽")
        self.product_listbox.pack(pady=20)

        self.add_to_cart_button = tk.Button(root, text="Добавить в корзину", command=self.add_to_cart)
        self.add_to_cart_button.pack()

        self.open_cart_button = tk.Button(root, text="Открыть корзину", command=self.open_cart)
        self.open_cart_button.pack()

        self.profile_button = tk.Button(root, text="Профиль", command=self.open_or_update_profile)
        self.profile_button.pack()

        self.profile_window = None

    def login(self):
        username = simpledialog.askstring("Вход", "Введите ваше имя пользователя:")
        password = simpledialog.askstring("Вход", "Введите ваш пароль:")

        if not username or not password:
            messagebox.showerror("Ошибка", "Пожалуйста, заполните оба поля!")
            return

        user = [user for user in self.users if user['name'] == username and user['password'] == password]
        if user:
            self.user = user[0]
            messagebox.showinfo("Успех", f"Добро пожаловать, {self.user['name']}!")
            self.open_cart_button.config(state=tk.NORMAL)
        else:
            messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль!")

    def register(self):
        username = simpledialog.askstring("Регистрация", "Введите ваше имя пользователя:")
        password = simpledialog.askstring("Регистрация", "Введите ваш пароль:")

        if not username or not password:
            messagebox.showerror("Ошибка", "Пожалуйста, заполните оба поля!")
            return

        if [user for user in self.users if user['name'] == username]:
            messagebox.showerror("Ошибка", "Имя пользователя уже существует!")
            return

        new_user = {'id': len(self.users) + 1, 'name': username, 'password': password, 'cart': [], 'profile_picture': None}
        self.users.append(new_user)
        self.user = new_user
        messagebox.showinfo("Успех", f"Регистрация прошла успешно, {self.user['name']}!")
        self.open_cart_button.config(state=tk.NORMAL)

    def search_products(self):
        search_term = self.search_entry.get()
        filtered_products = [product for product in self.products if search_term.lower() in product['name'].lower()]
        self.product_listbox.delete(0, tk.END)
        for product in filtered_products:
            self.product_listbox.insert(tk.END, f"{product['name']} - {product['price']} ₽")

    def add_to_cart(self):
        if not self.user:
            messagebox.showerror("Ошибка", "Пожалуйста, войдите в аккаунт или зарегистрируйтесь, чтобы добавить товары в корзину!")
            return

        selected_index = self.product_listbox.curselection()
        if selected_index:
            product = self.products[selected_index[0]]
            self.user['cart'].append(product)
            messagebox.showinfo("Добавлено!", f"{product['name']} добавлен в вашу корзину!")

    def open_cart(self):
        if not self.user:
            messagebox.showerror("Ошибка", "Пожалуйста, войдите в аккаунт или зарегистрируйтесь, чтобы открыть корзину!")
            return

        cart_window = tk.Toplevel(self.root,)
        cart_window.title("Корзина")

        cart_label = tk.Label(cart_window, text=f"Твоя корзина, {self.user['name']}", font=('Helvetica', 14))
        cart_label.pack(pady=10)

        cart_listbox = tk.Listbox(cart_window, selectmode=tk.SINGLE, height=5)
        for item in self.user['cart']:
            cart_listbox.insert(tk.END, f"{item['name']} - {item['price']} ₽")
        cart_listbox.pack(pady=10)

        remove_button = tk.Button(cart_window, text="Удалить из корзины", command=lambda: self.remove_from_cart(cart_listbox))
        remove_button.pack()

        calculate_total_button = tk.Button(cart_window, text="Посчитать общую стоимость", command=lambda: self.calculate_total(cart_listbox))
        calculate_total_button.pack()

        cancel_button = tk.Button(cart_window, text="Отмена", command=cart_window.destroy)
        cancel_button.pack()

    def remove_from_cart(self, cart_listbox):
        selected_index = cart_listbox.curselection()
        if selected_index:
            removed_product = self.user['cart'].pop(selected_index[0])
            messagebox.showinfo("Удалено", f"{removed_product['name']} был удален из вашей корзины!")
            self.update_cart_listbox(cart_listbox)

    def calculate_total(self, cart_listbox):
        total_price = sum(product['price'] for product in self.user['cart'])
        messagebox.showinfo("Общая цена", f"Общая стоимость вашей корзины: {total_price:.2f} ₽")
        cart_listbox.destroy()

    def update_cart_listbox(self, cart_listbox):
        cart_listbox.delete(0, tk.END)
        for item in self.user['cart']:
            cart_listbox.insert(tk.END, f"{item['name']} - {item['price']} ₽")

    def open_or_update_profile(self):
        if not self.user:
            messagebox.showinfo("Ошибка", "Пожалуйста, войдите в аккаунт или зарегистрируйтесь, чтобы открыть профиль!")
            return

        if self.profile_window and tk.Toplevel.winfo_exists(self.profile_window):
            self.update_profile_window()
        else:
            self.open_profile()

    def open_profile(self):
        self.profile_window = tk.Toplevel(self.root)
        self.profile_window.title(f"Ваш профиль, {self.user['name']}")

        self.name_label = tk.Label(self.profile_window, text="Имя: " + self.user['name'], font=('Helvetica', 14))
        self.name_label.pack(pady=10)

        self.profile_picture_label = tk.Label(self.profile_window, text="Изображение профиля:")
        self.profile_picture_label.pack()

        self.update_profile_picture_label()

        change_name_button = tk.Button(self.profile_window, text="Изменить имя профиля", command=self.change_name)
        change_name_button.pack()

        upload_picture_button = tk.Button(self.profile_window, text="Загрузить фото", command=self.upload_picture)
        upload_picture_button.pack()

        close_button = tk.Button(self.profile_window, text="Закрыть", command=self.profile_window.destroy)
        close_button.pack()

    def update_profile_window(self):
        self.name_label.config(text="Имя: " + self.user['name'])
        self.update_profile_picture_label()

    def update_profile_picture_label(self):
        if self.user['profile_picture']:
            image = Image.open(self.user['profile_picture'])
            image = image.resize((100, 100))
            photo = ImageTk.PhotoImage(image)
            self.profile_picture_label.image = photo
            self.profile_picture_label.config(image=photo)
            self.profile_picture_label.pack()

    def change_name(self):
        new_name = simpledialog.askstring("Изменить имя профиля", "Введите ваше имя:")
        if new_name:
            self.user['name'] = new_name
            self.update_profile_window()

    def upload_picture(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.user['profile_picture'] = file_path
            self.update_profile_window()


if __name__ == "__main__":
    root = tk.Tk()
    app = OnlineStoreApp(root)
    root.mainloop()
