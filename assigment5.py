from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.uic import loadUi
import sys
import re
from PyQt5.QtGui import QKeySequence, QPixmap
from PyQt5.QtWidgets import QShortcut

class ValidationForm(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("validation_form.ui", self)
        self.shortcutQuit = QShortcut(QKeySequence("Q"), self)
        self.shortcutQuit.activated.connect(self.close)

        self.btnSave.clicked.connect(self.validateForm)
        self.pushButton_2.clicked.connect(self.clearForm)

    def validateForm(self):
        name = self.LeName.text().strip()
        email = self.LeEmail.text().strip()
        age = self.LeAge.text().strip()
        phone_raw = self.LePhoneNumber.text().strip().replace(" ", "")
        address = self.TeAddress.toPlainText().strip()
        gender = self.CbGender.currentText()
        education = self.CbEducation.currentText()

        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        if phone_raw.startswith("+62"):
            phone = "62" + phone_raw[3:]
        elif phone_raw.startswith("62"):
            phone = phone_raw
        elif phone_raw.startswith("0"):
            phone = "62" + phone_raw[1:]
        else:
            phone = "62" + phone_raw

        # Validasi
        if not name or not email or not age or not address or not gender or not education:
            msg = QMessageBox()
            msg.setWindowTitle("Validation Error")
            msg.setText("All fields are required.")
            msg.setIconPixmap(QPixmap("warning_icon.png").scaled(64, 64))
            msg.exec_()
            return

        if not name[0].isupper():
            msg = QMessageBox()
            msg.setWindowTitle("Validation Error")
            msg.setText("Name must start with a capital letter.")
            msg.setIconPixmap(QPixmap("warning_icon.png").scaled(64, 64))
            msg.exec_()
            return

        if not re.match(email_pattern, email):
            msg = QMessageBox()
            msg.setWindowTitle("Validation Error")
            msg.setText("Please enter a valid email address.")
            msg.setIconPixmap(QPixmap("warning_icon.png").scaled(64, 64))
            msg.exec_()
            return

        if not age.isdigit():
            msg = QMessageBox()
            msg.setWindowTitle("Validation Error")
            msg.setText("Age must be numeric.")
            msg.setIconPixmap(QPixmap("warning_icon.png").scaled(64, 64))
            msg.exec_()
            return

        if not phone.isdigit() or len(phone) != 13:
            msg = QMessageBox()
            msg.setWindowTitle("Validation Error")
            msg.setText("Phone number must be exactly 13 digits.")
            msg.setIconPixmap(QPixmap("warning_icon.png").scaled(64, 64))
            msg.exec_()
            return

        # Jika lolos semua validasi
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Success")
        msg.setText("Profile saved successfully!")
        msg.setIconPixmap(QPixmap("success_icon.png").scaled(64, 64))
        msg.setStandardButtons(QMessageBox.Ok)
        response = msg.exec_()

        if response == QMessageBox.Ok:
            self.clearForm()

    def clearForm(self):
        self.LeName.clear()
        self.LeEmail.clear()
        self.LeAge.clear()
        self.LePhoneNumber.setText("+62")
        self.TeAddress.clear()
        self.CbGender.setCurrentIndex(0)
        self.CbEducation.setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ValidationForm()
    window.show()
    sys.exit(app.exec_())
