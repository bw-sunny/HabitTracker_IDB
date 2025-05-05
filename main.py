from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.toolbar import MDTopAppBar
from kivy.lang import Builder
from kivy.properties import StringProperty
import sqlite3
from kivymd.toast import toast

# Явно загружаем KV-файлы
Builder.load_file('/Users/bezenov_v/Desktop/HabitTracker/kv/login.kv')
Builder.load_file('/Users/bezenov_v/Desktop/HabitTracker/kv/main.kv')


# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


init_db()


class LoginScreen(MDScreen):
    def try_login(self):
        email = self.ids.email.text
        password = self.ids.password.text

        if email and password:
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE email=? AND password=?', (email, password))
            user = cursor.fetchone()
            conn.close()

            if user:
                print(f"Успешный вход: email={email}")
                toast("Успешный вход!")
                self.manager.current = 'main'
            else:
                print("Неверный email или пароль")
                toast("Неверный email или пароль")
        else:
            print("Заполните все поля")
            toast("Заполните все поля")

    def switch_to_register(self):
        self.manager.current = 'register'


class RegisterScreen(MDScreen):
    def try_register(self):
        email = self.ids.reg_email.text
        password = self.ids.reg_password.text

        if email and password:
            try:
                conn = sqlite3.connect('users.db')
                cursor = conn.cursor()
                cursor.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, password))
                conn.commit()
                conn.close()
                print(f"Успешная регистрация: email={email}")
                toast("Успешная регистрация!")
                self.manager.current = 'login'
            except sqlite3.IntegrityError:
                print("Пользователь с таким email уже существует")
                toast("Пользователь с таким email уже существует")
        else:
            print("Заполните все поля")
            toast("Заполните все поля")

    def switch_to_login(self):
        self.manager.current = 'login'


class MainScreen(MDScreen):
    streak_count = StringProperty("7")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.top_bar = MDTopAppBar(
            title="HabitTracker",
            left_action_items=[["streak.svg", lambda x: self.show_streak()]],
            right_action_items=[["profile.svg", lambda x: self.show_profile()]],
            elevation=10
        )
        self.add_widget(self.top_bar)

    def show_streak(self):
        toast(f"Текущая серия: {self.streak_count} дней")

    def show_profile(self):
        toast("Профиль пользователя")

    def add_habit(self):
        toast("Добавление новой привычки")


class HabitTrackerApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"

        sm = MDScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(MainScreen(name='main'))

        return sm


if __name__ == '__main__':
    HabitTrackerApp().run()
