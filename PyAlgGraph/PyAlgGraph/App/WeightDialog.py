from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton

class WeightDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(800, 600)
        
        self.setWindowTitle("Asignar peso al vértice")
        self.layout = QVBoxLayout()
        self.label = QLabel("Ingrese el peso del vértice:")
        self.text_field = QLineEdit()
        self.button = QPushButton("Aceptar")
        self.button.clicked.connect(self.accept)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.text_field)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

    def get_weight(self):
        
        if self.text_field.text() == "":
            return 0
        else:
            return int(self.text_field.text())