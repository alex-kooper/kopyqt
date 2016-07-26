import sys

from PyQt5.QtWidgets import (
    QApplication,
    qApp,
    QFormLayout,
    QHBoxLayout,
    QVBoxLayout,
    QLayout,
    QDialog,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton
)


class Form(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Simple Form')
        
        self.first_name = self._create_name_field()
        self.last_name = self._create_name_field()
        self.full_name = QLabel()
        self.error_message = self._create_error_field()

        fields = QFormLayout()
        fields.addRow('First Name', self.first_name)
        fields.addRow('Last Name', self.last_name)
        fields.addRow('Full Name', self.full_name)
        fields.addRow(None, self.error_message)

        self.send_button = self._create_button('Send', self.send)
        self.clear_button = self._create_button('Clear', self.reset_names)
        close_button = self._create_button('&Close', qApp.quit, is_enabled=True, is_default=True)

        buttons = QHBoxLayout()
        buttons.addStretch(1)
        buttons.addWidget(self.send_button)
        buttons.addWidget(self.clear_button)
        buttons.addWidget(close_button)

        vb = QVBoxLayout()
        vb.addLayout(fields)
        vb.addStretch(1)
        vb.addLayout(buttons)
        
        vb.setSizeConstraint(QLayout.SetFixedSize)
        self.setLayout(vb)    

    def update_full_name(self):
        full_name = (self.first_name.text().strip() + ' ' +
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

    def _create_name_field(self):
        le = QLineEdit()

        le.setFixedWidth(300)
        le.textChanged.connect(self.update_full_name)
        le.textChanged.connect(self.validate_names)
        le.textChanged.connect(self.enable_buttons)

        return le

    @staticmethod
    def _create_error_field():
        em = QLabel()
        em.setStyleSheet('color: red')
        em.hide()
        return em

    @staticmethod
    def _create_button(name, callback, is_enabled=False, is_default=False):
        b = QPushButton(name)
        b.setEnabled(is_enabled)
        b.setDefault(is_default)
        b.clicked.connect(callback)
        return b


if __name__ == '__main__':
    app = QApplication(sys.argv)
    f = Form()
    f.show()
    sys.exit(app.exec_())
