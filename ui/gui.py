import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Menu


def agent_login(window, active_agent, result):
    def action_login():
        error_message.config(text="")
        if username.get() == "":
            error_message.config(text="Please input your username", foreground="Red")
        elif password.get() == "":
            error_message.config(text="Please input your password", foreground="Red")
        else:
            active_agent.login(username.get(), password.get(), result)
            if result.code == "00":
                print("Login OK")
                # First instructions
                area.destroy()
                window.geometry("800x600")
            else:
                error_message.config(text=result.message[1], foreground="Red")

    window.title("PyBank")
    window.geometry("500x500")

    area = ttk.LabelFrame(window, text="Agent login")
    area.grid(column=0, row=0, padx=100, pady=100)

    username_label = ttk.Label(area, text="Username")
    username_label.grid(column=0, row=0, padx=20, pady=10)

    username = tk.StringVar()
    username_text = ttk.Entry(area, width=30, textvariable=username)
    username_text.grid(column=1, row=0, padx=20, pady=10)

    password_label = ttk.Label(area, text="Password")
    password_label.grid(column=0, row=1, padx=20, pady=10)

    password = tk.StringVar()
    password_text = ttk.Entry(area, width=30, show='*', textvariable=password)
    password_text.grid(column=1, row=1, padx=20, pady=10)

    login = ttk.Button(area, text="Login", command=action_login)
    login.grid(column=0, row=2, padx=50, pady=50, columnspan=2)

    error_message = ttk.Label(area)
    error_message.grid(column=0, row=3, padx=20, pady=20, columnspan=2)
