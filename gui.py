import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from decimal import Decimal

# Пример данных для отображения
data = {
    "Абс. фин. устойчивость": {
        "Показатель 1": [Decimal("1.1"), Decimal("2.2")],
        "Показатель 2": [Decimal("3.3"), Decimal("4.4")]
    },
    "Фин. устойчивость": {
        "Показатель 3": [Decimal("5.5"), Decimal("6.6")],
        "Показатель 4": [Decimal("7.7"), Decimal("8.8")]
    },
    "Ликвидность": {
        "Показатель 5": [Decimal("9.9"), Decimal("10.10")],
        "Показатель 6": [Decimal("11.11"), Decimal("12.12")]
    },
    "Рентабельность": {
        "Показатель 7": [Decimal("13.13"), Decimal("14.14")],
        "Показатель 8": [Decimal("15.15"), Decimal("16.16")]
    },
    "Оборачиваемость": {
        "Показатель 9": [Decimal("17.17"), Decimal("18.18")],
        "Показатель 10": [Decimal("19.19"), Decimal("20.20")]
    }
}


class FinancialApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Финансовый Анализ")
        self.geometry("800x600")

        self.filepaths = []

        self.create_welcome_window()

    def create_welcome_window(self):
        welcome_frame = tk.Frame(self)
        welcome_frame.pack(expand=True, fill=tk.BOTH)

        welcome_label = tk.Label(welcome_frame, text="Добро пожаловать.\nВыберите необходимые файлы",
                                 font=("Times New Roman", 25), justify="center", anchor='center')
        welcome_label.pack(pady=50)

        select_button = tk.Button(welcome_frame, text="Выбрать файлы", font=("Times New Roman", 14),
                                  command=self.select_files, width=15, height=2)
        select_button.pack(pady=25)

    def select_files(self):
        self.filepaths = filedialog.askopenfilenames(title="Выберите три файла", filetypes=[("Excel Files", "*.xls;*.xlsx")])
        if len(self.filepaths) != 3:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите ровно три файла")
        else:
            self.create_main_window()

    def create_main_window(self):
        for widget in self.winfo_children():
            widget.destroy()

        tab_control = ttk.Notebook(self)
        tab_control.pack(expand=1, fill="both")

        style = ttk.Style()
        style.configure("TNotebook.Tab", font=("Times New Roman", 14))

        for tab_name, indicators in data.items():
            tab_frame = ttk.Frame(tab_control)
            tab_control.add(tab_frame, text=tab_name)

            self.create_tab_content(tab_frame, indicators)

    def create_tab_content(self, parent, indicators):
        for i, (indicator_name, values) in enumerate(indicators.items()):
            name_label = tk.Label(parent, text=indicator_name, font=("Times New Roman", 12), anchor="w")
            name_label.grid(row=i, column=0, padx=10, pady=5, sticky="w")

            value_2021_label = tk.Label(parent, text=str(values[0]), font=("Times New Roman", 12))
            value_2021_label.grid(row=i, column=1, padx=10, pady=5)

            value_2020_label = tk.Label(parent, text=str(values[1]), font=("Times New Roman", 12))
            value_2020_label.grid(row=i, column=2, padx=10, pady=5)


if __name__ == "__main__":
    app = FinancialApp()
    app.mainloop()
