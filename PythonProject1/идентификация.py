import os
import csv
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import hashlib

os.makedirs("operators", exist_ok=True)

REQUIRED_WIDTH = 300
REQUIRED_HEIGHT = 300


class NeurobodrApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Нейрободр - Мониторинг состояния водителей")
        self.root.geometry("1000x800")
        self.root.configure(bg='#2c3e50')

        self.images = {}
        self.current_image_path = None
        self.current_operator_id = None
        self.current_operator_data = None

        self.init_database()
        self.create_test_operator()
        self.show_start_form()

    def init_database(self):
        if not os.path.exists('operators_db.csv'):
            with open('operators_db.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(
                    ['id', 'last_name', 'first_name', 'middle_name', 'age', 'login', 'password_hash', 'date', 'time'])

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def create_test_operator(self):
        with open('operators_db.csv', 'r', encoding='utf-8') as f:
            if len(f.readlines()) > 1:
                return

        img = Image.new('RGB', (REQUIRED_WIDTH, REQUIRED_HEIGHT), color='#3498db')
        img.save('uragan.png')
        img.save('operators/ID_000001.jpg')

        password_hash = self.hash_password("12345")

        now = datetime.now()
        with open('operators_db.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([1, 'Ураганов', 'Ураган', 'Ураганович', 25, 'uragan', password_hash,
                             now.strftime("%d-%m-%Y"), now.strftime("%H:%M:%S")])

    def show_start_form(self):
        self.clear_window()

        title = tk.Label(self.root, text="НЕЙРОБОДР", font=('Arial', 32, 'bold'),
                         bg='#2c3e50', fg='white')
        title.pack(pady=30)

        subtitle = tk.Label(self.root, text="Программа для мониторинга состояния водителей",
                            font=('Arial', 14), bg='#2c3e50', fg='#ecf0f1')
        subtitle.pack(pady=10)

        uragan_img = Image.open('uragan.png')
        uragan_img = uragan_img.resize((300, 300))
        self.images['start_img'] = ImageTk.PhotoImage(uragan_img)

        img_label = tk.Label(self.root, image=self.images['start_img'], bg='#2c3e50')
        img_label.pack(pady=20)

        choice_text = tk.Label(self.root, text="Выберите необходимые действия",
                               font=('Arial', 14, 'bold'), bg='#2c3e50', fg='white')
        choice_text.pack(pady=10)

        btn_frame = tk.Frame(self.root, bg='#2c3e50')
        btn_frame.pack(pady=30)

        register_btn = tk.Button(btn_frame, text="Регистрация", command=self.show_registration_form,
                                 font=('Arial', 14, 'bold'), bg='#27ae60', fg='white',
                                 width=15, height=2)
        register_btn.pack(side=tk.LEFT, padx=15)

        auth_btn = tk.Button(btn_frame, text="Авторизация", command=self.show_auth_form,
                             font=('Arial', 14, 'bold'), bg='#3498db', fg='white',
                             width=15, height=2)
        auth_btn.pack(side=tk.LEFT, padx=15)

    def show_registration_form(self):
        self.clear_window()

        title = tk.Label(self.root, text="РЕГИСТРАЦИЯ ОПЕРАТОРА", font=('Arial', 18, 'bold'),
                         bg='#2c3e50', fg='white')
        title.pack(pady=10)

        main_frame = tk.Frame(self.root, bg='#34495e')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        headers_frame = tk.Frame(main_frame, bg='#34495e')
        headers_frame.pack(fill=tk.X, pady=5)

        header1 = tk.Label(headers_frame, text="Регистрация оператора", font=('Arial', 12, 'bold'),
                           bg='#34495e', fg='#f1c40f', width=25)
        header1.pack(side=tk.LEFT, padx=10)

        header2 = tk.Label(headers_frame, text="Идентификация", font=('Arial', 12, 'bold'),
                           bg='#34495e', fg='#f1c40f', width=25)
        header2.pack(side=tk.LEFT, padx=10)

        header3 = tk.Label(headers_frame, text="Информационный блок", font=('Arial', 12, 'bold'),
                           bg='#34495e', fg='#f1c40f', width=25)
        header3.pack(side=tk.LEFT, padx=10)

        blocks_frame = tk.Frame(main_frame, bg='#34495e')
        blocks_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        reg_frame = tk.Frame(blocks_frame, bg='#2c3e50')
        reg_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        labels = ['Фамилия:', 'Имя:', 'Отчество:', 'Возраст:', 'Логин:', 'Пароль:']
        examples = ['Иванов', 'Иван', 'Иванович', '18', 'ivan123', '******']
        self.entries = {}

        for i, label in enumerate(labels):
            row_frame = tk.Frame(reg_frame, bg='#2c3e50')
            row_frame.pack(fill=tk.X, pady=5, padx=10)

            lbl = tk.Label(row_frame, text=label, bg='#2c3e50', fg='white',
                           font=('Arial', 10), width=10, anchor='w')
            lbl.pack(side=tk.LEFT)

            if label == 'Пароль:':
                entry = tk.Entry(row_frame, font=('Arial', 10), width=15, show='*')
            else:
                entry = tk.Entry(row_frame, font=('Arial', 10), width=15)
            entry.pack(side=tk.LEFT, padx=5)

            example_lbl = tk.Label(row_frame, text=f"(Пример: {examples[i]})",
                                   bg='#2c3e50', fg='#95a5a6', font=('Arial', 8))
            example_lbl.pack(side=tk.LEFT, padx=5)

            self.entries[label] = entry

        upload_btn = tk.Button(reg_frame, text="Загрузить фото", command=self.upload_image,
                               bg='#f39c12', fg='white', font=('Arial', 10, 'bold'),
                               width=15)
        upload_btn.pack(pady=10)

        save_btn = tk.Button(reg_frame, text="Записать", command=self.save_operator,
                             bg='#27ae60', fg='white', font=('Arial', 10, 'bold'),
                             width=15)
        save_btn.pack(pady=5)

        id_frame = tk.Frame(blocks_frame, bg='#2c3e50')
        id_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        size_label = tk.Label(id_frame, text=f"Требуемый размер:",
                              bg='#2c3e50', fg='#f39c12', font=('Arial', 10, 'bold'))
        size_label.pack(pady=2)

        size_value = tk.Label(id_frame, text=f"{REQUIRED_WIDTH} x {REQUIRED_HEIGHT} px",
                              bg='#2c3e50', fg='#f39c12', font=('Arial', 14, 'bold'))
        size_value.pack(pady=2)

        self.id_image_label = tk.Label(id_frame, bg='#1a2632', width=30, height=15)
        self.id_image_label.pack(padx=10, pady=10)

        self.upload_status = tk.Label(id_frame, text="Фото не загружено",
                                      bg='#2c3e50', fg='#e74c3c', font=('Arial', 10, 'bold'))
        self.upload_status.pack(pady=5)

        info_frame = tk.Frame(blocks_frame, bg='#2c3e50')
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.info_operator = tk.Label(info_frame, text="Оператор не определен",
                                      bg='#2c3e50', fg='#e74c3c', font=('Arial', 12, 'bold'))
        self.info_operator.pack(pady=10)

        self.info_id = tk.Label(info_frame, text="", bg='#2c3e50', fg='white', font=('Arial', 11))
        self.info_id.pack(pady=5)

        self.info_message = tk.Label(info_frame, text="", bg='#2c3e50', fg='#ecf0f1', font=('Arial', 10))
        self.info_message.pack(pady=5)

        self.next_btn = tk.Button(info_frame, text="Далее", state='disabled',
                                  bg='#7f8c8d', fg='white', font=('Arial', 12, 'bold'),
                                  width=15, height=2, command=self.start_monitoring)
        self.next_btn.pack(pady=20)

        back_btn = tk.Button(self.root, text="← Назад", command=self.show_start_form,
                             bg='#e74c3c', fg='white', font=('Arial', 11, 'bold'),
                             width=10)
        back_btn.pack(pady=10)

    def upload_image(self):
        file_path = filedialog.askopenfilename(
            title="Выберите изображение",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )

        if file_path:
            try:
                img = Image.open(file_path)
                width, height = img.size

                if width == REQUIRED_WIDTH and height == REQUIRED_HEIGHT:
                    self.current_image_path = file_path

                    img_resized = img.resize((250, 250))
                    self.images['uploaded'] = ImageTk.PhotoImage(img_resized)
                    self.id_image_label.config(image=self.images['uploaded'])

                    self.upload_status.config(text=f"✓ Фото загружено", fg='#27ae60')
                    self.info_operator.config(text="Оператор ожидает регистрации", fg='#f39c12')
                else:
                    messagebox.showerror(
                        "Ошибка размера",
                        f"Изображение должно быть {REQUIRED_WIDTH}x{REQUIRED_HEIGHT} px!\n"
                        f"Ваше изображение: {width}x{height} px"
                    )
                    self.upload_status.config(text="Неверный размер!", fg='#e74c3c')

            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить изображение: {str(e)}")

    def save_operator(self):
        if not hasattr(self, 'current_image_path') or not self.current_image_path:
            messagebox.showerror("Ошибка", "Сначала загрузите фото!")
            return

        last_name = self.entries['Фамилия:'].get()
        first_name = self.entries['Имя:'].get()
        middle_name = self.entries['Отчество:'].get()
        age = self.entries['Возраст:'].get()
        login = self.entries['Логин:'].get()
        password = self.entries['Пароль:'].get()

        if not all([last_name, first_name, age, login, password]):
            messagebox.showerror("Ошибка", "Заполните все поля!")
            return

        with open('operators_db.csv', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            new_id = len(lines)

        self.current_operator_id = new_id
        self.current_operator_data = {
            'id': new_id,
            'last_name': last_name,
            'first_name': first_name,
            'middle_name': middle_name,
            'age': age,
            'login': login
        }

        password_hash = self.hash_password(password)

        now = datetime.now()
        with open('operators_db.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                new_id, last_name, first_name, middle_name, age, login, password_hash,
                now.strftime("%d-%m-%Y"), now.strftime("%H:%M:%S")
            ])

        img = Image.open(self.current_image_path)
        img.save(f'operators/ID_{new_id:06d}.jpg')

        self.info_operator.config(
            text=f"Оператор: {last_name} {first_name[0]}.{middle_name[0] if middle_name else ''}.",
            fg='#27ae60')
        self.info_id.config(text=f"ID {new_id:06d}")
        self.info_message.config(text="Для запуска программы нажмите 'Далее'")

        self.next_btn.config(state='normal', bg='#27ae60')

        messagebox.showinfo("Успех", f"Оператор зарегистрирован с ID: {new_id:06d}")

    def show_auth_form(self):
        self.clear_window()

        title = tk.Label(self.root, text="АВТОРИЗАЦИЯ", font=('Arial', 24, 'bold'),
                         bg='#2c3e50', fg='white')
        title.pack(pady=30)

        main_frame = tk.Frame(self.root, bg='#34495e')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=20)

        login_frame = tk.Frame(main_frame, bg='#34495e')
        login_frame.pack(pady=30)

        tk.Label(login_frame, text="Логин:", bg='#34495e', fg='white',
                 font=('Arial', 14)).grid(row=0, column=0, padx=10, pady=10)

        self.auth_login = tk.Entry(login_frame, font=('Arial', 14), width=20)
        self.auth_login.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(login_frame, text="Пароль:", bg='#34495e', fg='white',
                 font=('Arial', 14)).grid(row=1, column=0, padx=10, pady=10)

        self.auth_password = tk.Entry(login_frame, font=('Arial', 14), width=20, show='*')
        self.auth_password.grid(row=1, column=1, padx=10, pady=10)

        login_btn = tk.Button(main_frame, text="ВОЙТИ", command=self.check_auth,
                              bg='#3498db', fg='white', font=('Arial', 14, 'bold'),
                              width=20, height=2)
        login_btn.pack(pady=20)

        self.auth_result = tk.Label(main_frame, text="", font=('Arial', 14, 'bold'),
                                    bg='#34495e')
        self.auth_result.pack(pady=10)

        back_btn = tk.Button(self.root, text="← Назад", command=self.show_start_form,
                             bg='#e74c3c', fg='white', font=('Arial', 11, 'bold'),
                             width=10)
        back_btn.pack(pady=10)

    def check_auth(self):
        login = self.auth_login.get()
        password = self.auth_password.get()

        if not login or not password:
            messagebox.showerror("Ошибка", "Введите логин и пароль!")
            return

        password_hash = self.hash_password(password)

        with open('operators_db.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if row and row[5] == login and row[6] == password_hash:
                    self.current_operator_id = int(row[0])
                    self.current_operator_data = {
                        'id': int(row[0]),
                        'last_name': row[1],
                        'first_name': row[2],
                        'middle_name': row[3],
                        'age': row[4],
                        'login': row[5]
                    }

                    self.auth_result.config(text="✓ АВТОРИЗАЦИЯ УСПЕШНА", fg='#27ae60')
                    messagebox.showinfo("Успех", f"Добро пожаловать, {row[1]} {row[2]}!")
                    self.start_monitoring()
                    return

        self.auth_result.config(text="✗ НЕВЕРНЫЙ ЛОГИН ИЛИ ПАРОЛЬ", fg='#e74c3c')
        messagebox.showerror("Ошибка", "Неверный логин или пароль!")

    def start_monitoring(self):
        self.clear_window()

        monitor_frame = tk.Frame(self.root, bg='#2c3e50')
        monitor_frame.pack(fill=tk.BOTH, expand=True)

        title = tk.Label(monitor_frame, text="МОНИТОРИНГ СОСТОЯНИЯ ВОДИТЕЛЯ",
                         font=('Arial', 20, 'bold'), bg='#2c3e50', fg='white')
        title.pack(pady=30)

        if self.current_operator_data:
            operator_text = f"{self.current_operator_data['last_name']} {self.current_operator_data['first_name']} {self.current_operator_data['middle_name']}"
            operator_label = tk.Label(monitor_frame, text=f"Оператор: {operator_text}",
                                      font=('Arial', 14), bg='#2c3e50', fg='#27ae60')
            operator_label.pack(pady=10)

            id_label = tk.Label(monitor_frame, text=f"ID: {self.current_operator_data['id']:06d}",
                                font=('Arial', 12), bg='#2c3e50', fg='white')
            id_label.pack(pady=5)

        status_frame = tk.Frame(monitor_frame, bg='#34495e')
        status_frame.pack(pady=30, padx=50, fill=tk.BOTH, expand=True)

        status_title = tk.Label(status_frame, text="СТАТУС:", font=('Arial', 16, 'bold'),
                                bg='#34495e', fg='#f1c40f')
        status_title.pack(pady=20)

        monitor_status = tk.Label(status_frame, text="Мониторинг активен",
                                  font=('Arial', 14), bg='#34495e', fg='#27ae60')
        monitor_status.pack(pady=10)

        time_label = tk.Label(status_frame, text=f"Время запуска: {datetime.now().strftime('%H:%M:%S')}",
                              font=('Arial', 12), bg='#34495e', fg='white')
        time_label.pack(pady=5)

        exit_btn = tk.Button(monitor_frame, text="Завершить мониторинг",
                             command=self.show_start_form,
                             bg='#e74c3c', fg='white', font=('Arial', 12, 'bold'),
                             width=20, height=2)
        exit_btn.pack(pady=20)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = NeurobodrApp(root)
    root.mainloop()