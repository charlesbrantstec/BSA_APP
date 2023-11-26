from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView

class HelloWorld(QMainWindow):
    def __init__(self):
        super().__init__()
        self.browser = QWebEngineView()
        self.browser.load(QUrl.fromLocalFile(r"C:\Users\12158\Desktop\BSA_APP\html\job-portal-website-template\index.html")) # Replace with the correct path
        self.setCentralWidget(self.browser)

if __name__ == '__main__':
    app = QApplication([])
    window = HelloWorld()
    window.show()
    app.exec_()
