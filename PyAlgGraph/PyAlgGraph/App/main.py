from PyQt5.QtWidgets import QApplication
from App import App
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    window.setWindowTitle('PyAlgGraph')
    sys.exit(app.exec_())