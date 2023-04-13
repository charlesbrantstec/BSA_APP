from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QComboBox
import CompanyReader

# COMPANY_NAMES = ["Apple", "Google", "Microsoft", "Amazon", "Facebook", "Tesla", "Netflix", "Twitter", "Uber", "Airbnb"]
df = CompanyReader.setup_df()
COMPANY_NAMES = df['Customer'].to_list()

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
    company_combo.lineEdit().setPlaceholderText("Enter a company name...")
    company_combo.setCurrentIndex(-1)  # Deselect any item
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

if __name__ == 'main':
    main()

main()