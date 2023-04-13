from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import pandas as pd

import CompanyReader
from get_bk_data import get_data

# df = CompanyReader.setup_df()
df = pd.read_csv('contacts.csv')
COMPANY_NAMES = df['Customer'].to_list()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Charlie's Form Generator")
        self.setGeometry(100, 100, 300, 300)

        main_layout = QVBoxLayout()

        # Add company selection dropdown item
        company_label = QLabel("Select a company:")
        main_layout.addWidget(company_label)

        self.company_combo = QComboBox()
        self.company_combo.setEditable(True)
        self.company_combo.addItems(COMPANY_NAMES)
        self.company_combo.lineEdit().setPlaceholderText("Enter a company name...")
        self.company_combo.setCurrentIndex(-1)  # Deselect any item    
        main_layout.addWidget(self.company_combo)

        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(spacer)

        # Add Get Data button
        self.get_data_button = QPushButton("Get Data")
        self.get_data_button.clicked.connect(self.on_get_data_clicked)
        main_layout.addWidget(self.get_data_button)

        self.central_widget = QWidget()
        self.central_widget.setLayout(main_layout)
        self.setCentralWidget(self.central_widget)

    def on_get_data_clicked(self):
        # Check if a company has been selected
        if self.company_combo.currentText() == "":
            QMessageBox.warning(self, "Error", "Please select a company.")
            return

        # Get the selected company name
        selected_company = self.company_combo.currentText()
        get_data(selected_company)

        # Find the row for the selected company and print each column on a new line
        selected_row = df.loc[df['Customer'] == selected_company]
        for column in selected_row:
            column_name = column
            column_value = selected_row[column].iloc[0]
            print(f"{column_name}: {column_value}")

        # Create success message label
        success_label = QLabel("Company contact data successfully fetched")
        success_label.setStyleSheet("color: green; font-weight: bold")

        # Create QFormLayout for the selected row
        form_layout = QFormLayout()

        # Iterate through each column of the selected row and add a QLineEdit widget to the form layout
        for column in selected_row:
            # Get the column name and value for the selected row
            column_name = column
            column_value = selected_row[column].iloc[0]

            # Create a QLineEdit widget and set the column name as the placeholder text
            line_edit = QLineEdit()
            line_edit.setPlaceholderText(column_name)
            line_edit.setText(str(column_value))
            line_edit.setAlignment(Qt.AlignLeft)  # Align the text to the left
            line_edit.setMinimumWidth(200)  # Set the minimum width of the widget
            form_layout.addRow(column_name, line_edit)

        # Create layout for success message, form layout, and generate forms button
        layout = QVBoxLayout()
        layout.addWidget(success_label)
        layout.addLayout(form_layout)
        layout.addStretch()

        # Create Generate Forms button
        generate_forms_button = QPushButton("Generate Forms")
        generate_forms_button.clicked.connect(self.on_generate_forms_clicked)
        layout.addWidget(generate_forms_button)

        # Create widget and set it as the central widget of the main window
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Hide current widgets
        self.company_combo.hide()
        self.get_data_button.hide()


    def on_generate_forms_clicked(self):
        # Add code to generate forms here
        pass

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
