import sys, time
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLineEdit, QLabel, 
                             QCheckBox, QTextEdit, QMessageBox, QGridLayout, QComboBox)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class ChartWindow(QMainWindow):
    def __init__(self, stats):
        super().__init__()
        self.setWindowTitle("Сравнительный анализ погрешностей")
        self.resize(1000, 900)
        
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        layout = QVBoxLayout(self.main_widget)
        
        # Создаем фигуру с двумя областями для рисования
        self.figure = Figure(figsize=(10, 12))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        self.plot_all(stats)

    def plot_all(self, stats):
        # Очищаем фигуру и создаем два подграфика
        self.figure.clear()
        
        # Определяем количество активных графиков
        dist_names = list(stats.keys())
        num_plots = len(dist_names)
        
        for idx, d_name in enumerate(dist_names):
            # Создаем подграфик (строки, колонки, индекс)
            ax = self.figure.add_subplot(num_plots, 1, idx + 1)
            
            # Для каждого значения X рисуем отдельную линию
            for x_val, data in stats[d_name].items():
                ax.plot(data['n'], data['error'], marker='o', label=f"X = {x_val}")
            
            ax.set_xscale('log')
            ax.set_title(f"Распределение: {d_name}", fontsize=14, fontweight='bold', color='#3A8DFF')
            ax.set_xlabel("Количество предметов (N) - лог. шкала")
            ax.set_ylabel("Погрешность (%)")
            ax.grid(True, which="both", alpha=0.3)
            ax.legend(title="Макс. стоимость X")

        self.figure.tight_layout(pad=5.0) # Чтобы графики не наезжали друг на друга
        self.canvas.draw()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Backpack Solver Project")
        self.resize(1000, 800)
        
        # Словарь для хранения результатов расчётов
        self.results_storage = {}
        self.generated_items = [] #хранилище для "сырых" данных
        self.current_items_dict = {} # Хранилище: {'Равномерное': [...], 'Нормальное': [...]}

        self.setStyleSheet("""
            QMainWindow { background-color: #121212; }
            QLabel { color: #BBBBBB; font-size: 14pt; font-weight: bold; }
            QLineEdit, QComboBox { 
                background-color: #1E1E1E; color: #FFFFFF; 
                border: 1px solid #444; padding: 5px; 
                border-radius: 4px; font-size: 14pt;
            }
            QComboBox QAbstractItemView { /*ЭТО НАСТРОЙКИ ИМЕННО ЭЛЕМЕНТОВ ВЫПАДАЮЩЕГО СПИСКА*/
                background-color: #252526;       /* Фон всего списка */
                color: #BBBBBB;                  /* Цвет текста элементов */
                selection-background-color: #3A8DFF; /* Цвет фона при наведении (выборе) */
                selection-color: #FFFFFF;        /* Цвет текста при наведении */
                border: 1px solid #3A8DFF;       /* Рамка вокруг выпадающего списка */
            }
            QCheckBox { color: #FFFFFF; font-size: 13pt; }
            QTextEdit { 
                background-color: #181818; color: #00FF00; 
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 13pt; border: 2px solid #3A8DFF; 
                border-radius: 8px; padding: 10px;
            }
            QPushButton { 
                background-color: #3A8DFF; color: white; 
                font-size: 13pt; font-weight: bold; 
                border-radius: 5px; padding: 10px 25px; 
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # Блок управления
        top_wrapper = QHBoxLayout()
        grid = QGridLayout() #сетка/невидимая таблица
        grid.setSpacing(20)

        grid.addWidget(QLabel("Кол-во (N):"), 0, 0)
        self.edit_n = QLineEdit()
        grid.addWidget(self.edit_n, 0, 1)
        grid.addWidget(QLabel("Макс. цена (X):"), 0, 2)
        self.edit_max_price = QLineEdit()
        grid.addWidget(self.edit_max_price, 0, 3)

        grid.addWidget(QLabel("Алгоритмы:"), 1, 0)
        self.check_bb = QCheckBox("Ветвей и границ")
        self.check_greedy = QCheckBox("Жадный")
        grid.addWidget(self.check_bb, 1, 1)
        grid.addWidget(self.check_greedy, 1, 2)

        grid.addWidget(QLabel("Данные:"), 2, 0)
        self.check_uniform = QCheckBox("Равномерное")
        self.check_normal = QCheckBox("Нормальное")
        grid.addWidget(self.check_uniform, 2, 1)
        grid.addWidget(self.check_normal, 2, 2)

        top_wrapper.addLayout(grid)
        top_wrapper.addStretch()
        main_layout.addLayout(top_wrapper)

        # Кнопка и Фильтр
        action_layout = QHBoxLayout()
        
        self.btn_solve = QPushButton("Запустить расчёт")
        self.btn_solve.clicked.connect(self.solve_task)
        
        # СОЗДАЕМ кнопку генерации
        self.btn_generate = QPushButton("Сгенерировать данные")
        self.btn_generate.clicked.connect(self.generate_data)
        
        self.combo_filter = QComboBox()
        self.combo_filter.setFixedWidth(400)
        self.combo_filter.addItem("Сначала запустите расчёт...")
        self.combo_filter.currentIndexChanged.connect(self.update_display)
        
        # ДОБАВЛЯЕМ кнопки в горизонтальный слой
        action_layout.addWidget(self.btn_generate) # Теперь она появится слева
        action_layout.addWidget(self.btn_solve)
        action_layout.addSpacing(20)
        action_layout.addWidget(QLabel("Просмотр результатов:"))
        action_layout.addWidget(self.combo_filter)
        action_layout.addStretch()
        
        main_layout.addLayout(action_layout)

        # --- Вывод ---
        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)
        main_layout.addWidget(self.result_output)

        self.btn_charts = QPushButton("Построить графики")
        self.btn_charts.clicked.connect(self.show_charts)
        action_layout.addWidget(self.btn_charts)

    # Новый метод:
    def show_charts(self):
        try:
            from solver import branch_boundary_method, greedy_algo
            from utils import uniform_distribution, normal_distribution
            
            # Твои условия по N и X
            n_values = [10, 100, 1000, 100000]
            x_values = [10, 100, 1000, 10000, 100000]
            w = 1
            
            # Структура: { 'Равномерное': { X_value: { 'n': [], 'err': [] } } }
            stats = {}

            active_dists = []
            if self.check_uniform.isChecked(): active_dists.append(("Равномерное", uniform_distribution))
            if self.check_normal.isChecked(): active_dists.append(("Нормальное", normal_distribution))

            if not active_dists:
                QMessageBox.warning(self, "Внимание", "Выберите хотя бы один тип данных!")
                return

            # Прогресс-бар или просто текст в консоль, так как расчет будет долгим
            print("Запуск масштабного тестирования...")

            for d_name, d_func in active_dists:
                stats[d_name] = {}
                for x in x_values:
                    stats[d_name][x] = {"n": [], "error": []}
                    for n in n_values:
                        items = d_func(n, x)
                        
                        # Точное решение (Эталон)
                        _, _, exact_p = branch_boundary_method([i.copy() for i in items], w)
                        # Жадное решение
                        _, _, greedy_p = greedy_algo([i.copy() for i in items], w)
                        
                        error = ((exact_p - greedy_p) / exact_p * 100) if exact_p > 0 else 0
                        
                        stats[d_name][x]["n"].append(n)
                        stats[d_name][x]["error"].append(error)

            self.chart_win = ChartWindow(stats)
            self.chart_win.show()
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Критическая ошибка расчетов: {str(e)}")
    
    def generate_data(self):
        try:
            from utils import uniform_distribution, normal_distribution
            
            n = int(self.edit_n.text())
            x = int(self.edit_max_price.text())
            
            # Очищаем старое хранилище при новой генерации
            self.current_items_dict = {}
            msg = "Сгенерировано:\n"
            
            if self.check_uniform.isChecked():
                self.current_items_dict['Равномерное'] = uniform_distribution(n, x)
                msg += f"- Равномерное ({n} шт.)\n"
                
            if self.check_normal.isChecked():
                self.current_items_dict['Нормальное'] = normal_distribution(n, x)
                msg += f"- Нормальное ({n} шт.)\n"
                
            if not self.current_items_dict:
                QMessageBox.warning(self, "Внимание", "Выберите тип данных для генерации!")
                return

            self.result_output.setText(msg + "Данные готовы к решению.")
            self.combo_filter.clear()
            self.combo_filter.addItem("Сначала решите задачу...")
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка генерации: {str(e)}")

    def solve_task(self):
        try:
            from solver import branch_boundary_method, greedy_algo

            # 1. Проверяем наличие данных
            if not self.current_items_dict:
                QMessageBox.warning(self, "Внимание", "Сначала сгенерируйте данные!")
                return

            # Читаем актуальное N из поля ввода
            try:
                current_n = int(self.edit_n.text())
            except ValueError:
                QMessageBox.warning(self, "Внимание", "Введите корректное число N!")
                return

            # Проверяем алгоритмы
            algos = []
            if self.check_bb.isChecked(): algos.append(("Ветвей и границ", branch_boundary_method))
            if self.check_greedy.isChecked(): algos.append(("Жадный", greedy_algo))

            if not algos:
                QMessageBox.warning(self, "Внимание", "Выберите хотя бы один алгоритм!")
                return

            w = 1
            self.results_storage = {} 
            self.combo_filter.clear()
            self.combo_filter.addItem("Показать всё")

            active_dists = []
            if self.check_uniform.isChecked() and 'Равномерное' in self.current_items_dict:
                active_dists.append('Равномерное')
            if self.check_normal.isChecked() and 'Нормальное' in self.current_items_dict:
                active_dists.append('Нормальное')

            if not active_dists:
                QMessageBox.warning(self, "Внимание", "Выбранные типы данных не соответствуют сгенерированным!")
                return

            for d_name in active_dists:
                # ВАЖНО: Берем только первые current_n предметов из хранилища
                # Это позволяет менять N без повторной генерации
                full_list = self.current_items_dict[d_name]
                
                # Если пользователь ввел N больше, чем было сгенерировано — выдаем предупреждение
                if current_n > len(full_list):
                    QMessageBox.warning(self, "Предупреждение", 
                                        f"Вы ввели N={current_n}, но сгенерировано было только {len(full_list)}. "
                                        "Будет использован весь доступный массив.")
                    raw_items = full_list
                else:
                    raw_items = full_list[:current_n] # Срез списка до нужного количества
                
                # Копия для эталона
                items_for_exact = [item.copy() for item in raw_items]
                exact_items, exact_w, exact_p = branch_boundary_method(items_for_exact, w)
                
                for a_name, a_func in algos:
                    items_for_algo = [item.copy() for item in raw_items]
                    
                    start = time.perf_counter()
                    res_items, final_w, final_p = a_func(items_for_algo, w)
                    dt = time.perf_counter() - start
                    
                    if a_name == "Ветвей и границ":
                        error_str = "0.000% (Точное решение)"
                    else:
                        if exact_p > 0:
                            relative_error = ((exact_p - final_p) / exact_p) * 100
                            error_str = f"{relative_error:.4f}%"
                        else:
                            error_str = "0.000%"

                    key = f"{a_name} ({d_name}) | N={len(raw_items)}"
                    self.combo_filter.addItem(key)
                    
                    text = f"РЕЗУЛЬТАТ: {key}\n"
                    text += f"Выполнено за: {dt:.6f} сек.\n"
                    text += f"Относительная погрешность: {error_str}\n"
                    text += "-" * 45 + "\n"
                    for i in res_items:
                        text += f"ID: {i['index']:03} | Вес: {i['weight']:.9f} | Цена: {i['price']:.5f}\n"
                    text += "-" * 45 + "\n"
                    text += f"ИТОГОВЫЙ ВЕС:  {final_w:.15f}\n"
                    text += f"ИТОГОВАЯ ЦЕНА: {final_p:.9f}\n"
                    
                    self.results_storage[key] = text

            self.update_display()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при расчёте: {str(e)}")

    def update_display(self): #фильтрация
        choice = self.combo_filter.currentText()
        if choice == "Показать всё":
            all_text = "\n\n".join(self.results_storage.values())
            self.result_output.setText(all_text)
        elif choice in self.results_storage:
            self.result_output.setText(self.results_storage[choice])