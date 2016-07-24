import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class Form(QDialog):
    
    def __init__(self):
        super().__init__()
        self.create_widgets()
        self.setWindowTitle('Simple Form')    
        
    def create_widgets(self):
        self.first_name = QLineEdit()
        self.first_name.setFixedWidth(300)
        self.first_name.textChanged.connect(self.update_full_name)
        self.first_name.textChanged.connect(self.validate_names)
        self.first_name.textChanged.connect(self.enable_buttons)

        self.last_name = QLineEdit()
        self.last_name.setFixedWidth(300)
        self.last_name.textChanged.connect(self.update_full_name)
        self.last_name.textChanged.connect(self.validate_names)
        self.last_name.textChanged.connect(self.enable_buttons)

        self.full_name = QLabel()
        self.error_message = QLabel()
        self.error_message.setStyleSheet('color: red')
        self.error_message.hide()

        fields = QFormLayout()
        fields.addRow("First Name", self.first_name)
        fields.addRow("Last Name", self.last_name)
        fields.addRow("Full Name", self.full_name)
        fields.addRow(None, self.error_message)

        self.send_button = QPushButton("Send")
        self.send_button.setEnabled(False)
        self.send_button.clicked.connect(self.send)

        self.clear_button = QPushButton("Clear")
        self.clear_button.setEnabled(False)
        self.clear_button.clicked.connect(self.reset_names)

        close_button = QPushButton("&Close")
        close_button.clicked.connect(qApp.quit)
        close_button.setDefault(True)

        buttons = QHBoxLayout()
        buttons.addStretch(1)
        buttons.addWidget(self.send_button)
        buttons.addWidget(self.clear_button)
        buttons.addWidget(close_button)

        vb = QVBoxLayout()
        vb.addLayout(fields)
        vb.addStretch(1)
        vb.addLayout(buttons)
        
        # vb.setSizeConstraint(QLayout.SetFixedSize)
        self.setLayout(vb)    

    def update_full_name(self):
        full_name = (self.first_name.text().strip()
                     + ' ' +
                     self.last_name.text().strip()).upper().strip()  

        self.full_name.setText(full_name)

    @staticmethod
    def is_valid_name(name):
        return all(c.isalnum() or c in ' -' for c in name)

    def validate_names(self):
        msg1 = msg2 = None 

        if not self.is_valid_name(self.first_name.text()):
            msg1 = 'first name' 

        if not self.is_valid_name(self.last_name.text()):
            msg2 = 'last name'

        msg = ' & '.join(filter(None, [msg1, msg2]))

        if msg:
            self.error_message.setText('Invalid {}!'.format(msg))
            self.error_message.setVisible(True)
        else:
            self.error_message.setText(None)
            self.error_message.setVisible(False)

    def enable_buttons(self):
        fn = self.first_name.text()
        ln = self.last_name.text()

        if fn or ln: 
            self.clear_button.setEnabled(True)
        else:
            self.clear_button.setEnabled(False)

        if (fn.strip() and ln.strip() and 
            self.is_valid_name(fn) and self.is_valid_name(ln)):
           self.send_button.setEnabled(True)
        else:
           self.send_button.setEnabled(False)

    def reset_names(self):
        self.first_name.setText('')
        self.last_name.setText('')
           
    def send(self):
        msg = "The name {}\nwas sent to the server.".format(self.full_name.text())
        QMessageBox.information(self, 'Success!', msg)
        self.reset_names()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    f = Form()
    f.show()
    sys.exit(app.exec_())

