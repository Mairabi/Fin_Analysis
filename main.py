import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from node import DataCreator

# Пример данных для отображения


class FinancialApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Финансовый Анализ")
        self.geometry("800x600")

        self.filepaths = []
        self.data = None
        self.years = None

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

    # Здесь создаем экземпляр класса DataCreator и запускаем процедуры извлечения и расчетов
    def select_files(self):
        self.filepaths = filedialog.askopenfilenames(title="Выберите три файла", filetypes=[("Excel Files", "*.xls;*.xlsx")])
        if len(self.filepaths) != 3:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите ровно три файла")
        else:
            data_creator = DataCreator(self.filepaths)
            self.data = data_creator.get_ratios()
            self.years = data_creator.years_of_balance

            self.create_main_window()

    def create_main_window(self):
        for widget in self.winfo_children():
            widget.destroy()

        tab_control = ttk.Notebook(self)
        tab_control.pack(expand=1, fill="both")

        style = ttk.Style()
        style.configure("TNotebook.Tab", font=("Times New Roman", 14))

        for tab_name, indicators in self.data.items():
            tab_frame = ttk.Frame(tab_control)
            tab_control.add(tab_frame, text=tab_name)

            self.create_tab_content(tab_frame, indicators)

    def create_tab_content(self, parent, indicators):
        # Получаем количество годов для текущей вкладки
        current_years = self.years[:len(next(iter(indicators.values())))]

        # Создаем заголовок с годами
        for j, year in enumerate(current_years):
            year_label = tk.Label(parent, text=year, font=("Times New Roman", 12, "bold"))
            year_label.grid(row=0, column=j + 1, padx=10, pady=5)

        # Создаем строки с названиями показателей и их значениями за соответствующие годы
        for i, (indicator_name, values) in enumerate(indicators.items()):
            name_label = tk.Label(parent, text=indicator_name, font=("Times New Roman", 12), anchor="w")
            name_label.grid(row=i + 1, column=0, padx=10, pady=5, sticky="w")

            for j, value in enumerate(values):
                value_label = tk.Label(parent, text=str(value), font=("Times New Roman", 12))
                value_label.grid(row=i + 1, column=j + 1, padx=10, pady=5)


if __name__ == "__main__":
    app = FinancialApp()
    app.mainloop()
