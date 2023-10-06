# This tool allows you to create QR codes.
__author__ = "John Acha"
__email__ = "john_acha@live.com"
__copyright__ = "Copyright © 2023"
__credits__ = "Liceli Ramos, Ken Acha, Lynn Acha"
__license__ = "GPLv3"
__version__ = "1.0"

import sys, os
import qrcode
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from io import BytesIO

basedir = os.path.dirname(__file__)

try:
    from ctypes import windll # Solo existe en Windows
    myappid = "mycompany.myproduct.subproduct.version"
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass    


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.setWindowTitle('Mikel Tool - Created by John Acha')
        self.setGeometry(100, 100, 400, 400)


        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.text_input = QLineEdit()
        self.qr_label = QLabel('Comienza a escribir para crear un código QR.')

        self.qr_label.setAlignment(Qt.AlignCenter)  # Asegurar que la etiqueta esté centrada

        self.text_input.textChanged.connect(self.generate_qr_code)
        self.layout.addWidget(self.text_input)

        self.layout.addWidget(self.qr_label)

        # Agregar un botón al final del QR
        self.save_button = QPushButton('Guardar QR')
        self.save_button.setIcon(QIcon(os.path.join(basedir, "icons", "save.svg")))
        self.save_button.clicked.connect(self.save_qr_image)
        self.layout.addWidget(self.save_button)
        self.central_widget.setLayout(self.layout)

        # Variable para almacenar la imagen QR actual
        self.current_qr_image = None

    def generate_qr_code(self):
        text = self.text_input.text()
        if text:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(text)
            qr.make(fit=True)

            # Guardar la imagen QR en un BytesIO temporal
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format="PNG")

            # Cargar la imagen desde el buffer en un QPixmap
            pixmap = QPixmap()
            pixmap.loadFromData(buffer.getvalue())

            self.qr_label.setPixmap(pixmap)
            
            # Update current_qr_image
            self.current_qr_image = img
        else:
            # Si no hay texto, muestra una imagen vacía
            self.qr_label.clear()

    def save_qr_image(self):
        if self.current_qr_image:
            options = QFileDialog.Options()
            file_name, _ = QFileDialog.getSaveFileName(self, "Guardar QR", "", "PNG Files (*.png);;All Files (*)", options=options)
            if file_name:
                self.current_qr_image.save(file_name, "PNG")
                QMessageBox.information(self, "Éxito", f"QR guardado en {file_name}")
                self.text_input.clear()  # Limpia la entrada de texto
            else:
                QMessageBox.warning(self, "Error", "No se seleccionó una ubicación de guardado.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.join(basedir, "icons", "mikel.svg")))
    window = MainWindow()
    window.show()
    app.exec_()

