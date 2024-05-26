import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class EquationSolver(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Solver ecuație gradul 3')
        self.setGeometry(100, 100, 600, 400)

        self.coefficient_labels = []
        self.coefficient_lineedits = []

        coefficients_layout = QVBoxLayout()

        for i in range(4):
            label_text = f'Coeficient a{i}: ' if i != 3 else 'Coeficient b: '
            coefficient_label = QLabel(label_text)
            self.coefficient_labels.append(coefficient_label)

            coefficient_lineedit = QLineEdit()
            self.coefficient_lineedits.append(coefficient_lineedit)

            coefficients_layout.addWidget(coefficient_label)
            coefficients_layout.addWidget(coefficient_lineedit)

        solve_button = QPushButton('Rezolvă')
        solve_button.clicked.connect(self.solve_equation)

        self.result_label = QLabel()

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.axes = self.figure.add_subplot(111)

        main_layout = QVBoxLayout()
        main_layout.addLayout(coefficients_layout)
        main_layout.addWidget(solve_button)
        main_layout.addWidget(self.result_label)
        main_layout.addWidget(self.canvas)

        self.setLayout(main_layout)

    def solve_equation(self):
        coefficients = []
        for lineedit in self.coefficient_lineedits:
            coefficients.append(float(lineedit.text()))

        a0, a1, a2, b = coefficients

        if a0 == 0:
            self.result_label.setText('Eroare: a0 trebuie să fie diferit de 0')
            return

        p = a2 - ((a1 ** 2) / (3 * a0))
        q = b - ((a1 * a2) / (3 * a0)) + ((2 * (a1 ** 3)) / (27 * (a0 ** 2)))

        delta = (q ** 2) / 4 + (p ** 3) / 27

        if delta > 0:
            u = (-q / 2 + (delta ** 0.5)) ** (1 / 3)
            v = (-q / 2 - (delta ** 0.5)) ** (1 / 3)
            x1 = u + v
            x2 = -(u + v) / 2 + 1j * (u - v) * (3 ** 0.5) / 2
            x3 = -(u + v) / 2 - 1j * (u - v) * (3 ** 0.5) / 2

            result = f'Soluțiile sunt: {x1}, {x2}, {x3}'
        elif delta == 0:
            if p == 0:
                x = (-q / 2) ** (1 / 3)
                result = f'Soluția multiplă este: {x}'
            else:
                x1 = (3 * q / p - ((p / 3) ** 0.5)) ** (1 / 3) + \
                     (3 * q / p + ((p / 3) ** 0.5)) ** (1 / 3) - a1 / (3 * a0)
                result = f'Soluția triplă este: {x1}'
        else:
            phi = ((-q / 2) ** 2 + (delta ** 0.5) ** 2) ** (1 / 2)
            teta = (q / 2) / phi
            omega = (delta ** 0.5) / phi
            x1 = 2 * phi * (omega ** (1 / 3)) * (1 - 1j * (3 ** 0.5) / 2)
            x2 = 2 * phi * (omega ** (1 / 3)) * (1 + 1j * (3 ** 0.5) / 2)
            x3 = -phi * (omega ** (1 / 3))
            result = f'Soluțiile sunt: {x1}, {x2}, {x3}'

        self.result_label.setText(result)

        # Plot the function
        x_values = np.linspace(-10, 10, 400)
        y_values = a0 * x_values ** 3 + a1 * x_values ** 2 + a2 * x_values + b
        self.axes.clear()
        self.axes.plot(x_values, y_values, color='blue')
        self.axes.grid(True)
        self.axes.set_title('Graficul funcției')

        self.canvas.draw()

        # Set the size of the canvas
        self.canvas.setFixedSize(400, 300)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = EquationSolver()
    window.show()
    sys.exit(app.exec_())
