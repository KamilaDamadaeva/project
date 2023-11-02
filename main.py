import tkinter as tk
from tkinter import ttk
import sqlite3


# класс, который будет все запускать
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    # поиск записи
    def search_records(self, name):
        name = ('%' + name + '%',)
        self.db.c.execute(
            '''SELECT * FROM db WHERE name LIKE ?''', name)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row)
         for row in self.db.c.fetchall()]

    # метод отвечающий за вызов окна для поиска
    def open_search_dialog(self):
        Search()

    # удаление записей
    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM db WHERE
            id=?''', (self.tree.set(selection_item, '#1'),))
            self.db.conn.commit()  # сохранение изменений
            self.view_records()  # обновление виджета таблицы

        # обновление данных

    def update_record(self, name, tel, email, zar):
        self.db.c.execute('''UPDATE db SET name=?, tel=?, email=?, zar=? WHERE ID=?''',
                          (name, tel, email, zar, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    def open_update_dialog(self):
        Update()

    def view_records(self):
        # выбор информации из БД
        self.db.c.execute('''SELECT * FROM db''')
        # удалене всего из виджета таблицы
        [self.tree.delete(i) for i in self.tree.get_children()]
        # добавление в виджет таблицы информации из БД
        [self.tree.insert('', 'end', values=row)
         for row in self.db.c.fetchall()]

    def records(self, name, tel, email, zar):  # добавление данных
        self.db.insert_data(name, tel, email, zar)
        self.view_records()

    def open_dialog(self):  # вызов дочернего класса
        Child()

    # фон и рамки,/ панель инструментов // вверху окна, РАСТЯГИВАНИЕ ПО x
    def init_main(self):
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file='./img/add.png')
        # создание кнопки добавления
        # command - функция по нажатию
        # bg - фон
        # bd - граница
        # compound - ориентация текста (tk.CENTER , tk.LEFT , tk.RIGHT , tk.TOP или tk.BOTTOM.)
        # image - иконка кнопки
        btn_open_dialog = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.add_img, command=self.open_dialog)
        # упаковка и выравнивание по левому краю
        btn_open_dialog.pack(side=tk.LEFT)

        # Добавление Treeview
        # columns - столбцы
        # height - высота таблицы
        # show='headings' - скрытие пустой колонки таблицы
        self.tree = ttk.Treeview(self, columns=('ID', 'name', 'tel', 'email', 'zar'), height=45, show='headings')
        # добавление параметра колонок
        # width - ширина, anchor - выравнивание текста в ячейке
        self.tree.column("ID", width=30, anchor=tk.CENTER)
        self.tree.column("name", width=200, anchor=tk.CENTER)
        self.tree.column("tel", width=130, anchor=tk.CENTER)
        self.tree.column("email", width=200, anchor=tk.CENTER)
        self.tree.column("zar", width=100, anchor=tk.CENTER)

        # подписи колонок
        self.tree.heading("ID", text='ID')
        self.tree.heading("name", text='ФИО')
        self.tree.heading("tel", text='Телефон')
        self.tree.heading("email", text='E-mail')
        self.tree.heading("zar", text='Зарплата')

        # упаковка и выравнивание
        self.tree.pack(side=tk.LEFT)

        # создание кнопки изменения данных
        self.update_img = tk.PhotoImage(file='./img/update.png')
        btn_edit_dialog = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.update_img, command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        # создание кнопки удаления контакта
        self.delete_img = tk.PhotoImage(file='./img/delete.png')
        btn_delete = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.delete_img, command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        # создание кнопки поиска
        self.search_img = tk.PhotoImage(file='./img/search.png')
        btn_search = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.search_img, command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)

        # создание кнопки обновления
        self.refresh_img = tk.PhotoImage(file='./img/refresh.png')
        btn_refresh = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.refresh_img, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)


class Child(tk.Toplevel):  # повверх дочернего окна
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Добавить')
        self.geometry('400x220')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        # подписи
        label_name = tk.Label(self, text='ФИО:')
        label_name.place(x=50, y=50)
        label_select = tk.Label(self, text='Телефон')
        label_select.place(x=50, y=80)
        label_sum = tk.Label(self, text='E-mail')
        label_sum.place(x=50, y=110)
        label_zar = tk.Label(self, text='Зарплата')
        label_zar.place(x=50, y=140)

        self.entry_name = ttk.Entry(self)  # добавление строки ввода для имени
        # смена координат объекта
        self.entry_name.place(x=200, y=50)

        self.entry_email = ttk.Entry(self)  # для email
        self.entry_email.place(x=200, y=80)

        self.entry_tel = ttk.Entry(self)  # для телефона
        self.entry_tel.place(x=200, y=110)

        self.entry_zar = ttk.Entry(self)  # для зарплаты
        self.entry_zar.place(x=200, y=140)

        self.btn_cancel = ttk.Button(  # кнопка закрытия дочернего окна
            self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=300, y=170)

        self.btn_ok = ttk.Button(self, text='Добавить')  # кнопка добавления
        self.btn_ok.place(x=220, y=170)
        # срабатывание по ЛКМ
        # при нажатии кнопки вызывается метод records, которому передаюся значения из строк ввода
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_name.get(), self.entry_email.get(),
                                                                       self.entry_tel.get(), self.entry_zar.get()))


# класс для редактирования записей
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):  # кнопка
        self.title('Редактировать позицию')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_name.get(), self.entry_email.get(),
                                                                          self.entry_tel.get(), self.entry_zar.get()))
        btn_edit.bind('<Button-1>', lambda event: self.destroy(), add='+')  # закрытие окна редактирования
        self.btn_ok.destroy()

    def default_data(self):
        self.db.c.execute('''SELECT * FROM db WHERE id=?''', (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        # получение доступа к первой записи из выборки
        row = self.db.c.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_email.insert(0, row[2])
        self.entry_tel.insert(0, row[3])
        self.entry_zar.insert(0, row[4])


# поиск записи
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск')
        self.geometry('300x100')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Поиск')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)  # окно для ввода
        self.entry_search.place(x=105, y=20, width=150)
        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)  # закрытие
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Поиск')  # реакция кнопки
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')


class DB:  # создание бд
    def __init__(self):
        self.conn = sqlite3.connect('db.db')
        self.c = self.conn.cursor()  # создание курсора
        self.c.execute('''CREATE TABLE IF NOT EXISTS db (
        id INTEGER PRIMARY KEY,
        name TEXT,
        tel TEXT,
        email TEXT,
        zar text);
        ''')
        self.conn.commit()

    # добавление в БД
    def insert_data(self, name, tel, email, zar):
        self.c.execute('''INSERT INTO db (name, tel, email, zar)
         VALUES (?, ?, ?, ?)
         ''', (name, tel, email, zar))
        self.conn.commit()


if __name__ == '__main__':  # проверяет где запускается приложение
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('Телефонная книга')
    root.geometry('665x450')
    root.resizable(False, False)  # ограничение изменения размеров окна
    root.mainloop()
