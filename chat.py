from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont

COMPANY_NAMES = ["Apple", "Google", "Microsoft", "Amazon", "Facebook", "Tesla", "Netflix", "Twitter", "Uber", "Airbnb"]

def main():
    app = QApplication([])
    window = QWidget()
    window.setGeometry(100, 100, 300, 300)
    window.setWindowTitle("Charlie's Form Generator")

    main_layout = QVBoxLayout()

    # Add company selection dropdown item
    company_label = QLabel("Select a company:")
    main_layout.addWidget(company_label)

    company_combo = QComboBox()
    company_combo.setEditable(True)
    company_combo.addItems(COMPANY_NAMES)
    main_layout.addWidget(company_combo)

    spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
    main_layout.addItem(spacer)

    # Add Get Data button
    button = QPushButton("Get Data")
    button.clicked.connect(on_clicked)
    main_layout.addWidget(button)

    window.setLayout(main_layout)

    window.show()
    app.exec_()

def on_clicked():
    print("Hello World")

if __name__ == '__main__':
    main()
