from PyQt5 import QtWidgets
from db import Session, User, hash_pw, check_pw, valid_pw

def show_register_dialog(parent=None):
    dialog = QtWidgets.QDialog(parent)
    dialog.setWindowTitle("Register")
    dialog.setFixedSize(300, 200)

    layout = QtWidgets.QVBoxLayout(dialog)
    username_input = QtWidgets.QLineEdit()
    password_input = QtWidgets.QLineEdit()
    deepl_input = QtWidgets.QLineEdit()

    username_input.setPlaceholderText("Username")
    password_input.setPlaceholderText("Password")
    password_input.setEchoMode(QtWidgets.QLineEdit.Password)
    deepl_input.setPlaceholderText("DEEPL_API_KEY")

    layout.addWidget(username_input)
    layout.addWidget(password_input)
    layout.addWidget(deepl_input)

    submit_btn = QtWidgets.QPushButton("Register")
    layout.addWidget(submit_btn)

    def handle_register():
        username = username_input.text().strip()
        password = password_input.text().strip()
        deepl_key = deepl_input.text().strip()

        if not username or not password or not deepl_key:
            QtWidgets.QMessageBox.warning(dialog, "Error", "Tüm alanlar zorunlu.")
            return

        if not valid_pw(password):
            QtWidgets.QMessageBox.warning(dialog, "Error", "Şifre ≥8 karakter ve en az 1 rakam içermeli.")
            return

        session = Session()
        if session.query(User).filter_by(username=username).first():
            QtWidgets.QMessageBox.warning(dialog, "Error", "Kullanıcı adı zaten kayıtlı.")
            return

        user = User(username=username, password_hash=hash_pw(password), deepl_key=deepl_key)
        session.add(user)
        session.commit()

        QtWidgets.QMessageBox.information(dialog, "Başarılı", "Kayıt başarılı. Giriş yapabilirsiniz.")
        dialog.accept()

    submit_btn.clicked.connect(handle_register)

    return dialog.exec_() == QtWidgets.QDialog.Accepted

def show_login_dialog(parent=None):
    dialog = QtWidgets.QDialog(parent)
    dialog.setWindowTitle("Login")
    dialog.setFixedSize(300, 160)

    layout = QtWidgets.QVBoxLayout(dialog)
    username_input = QtWidgets.QLineEdit()
    password_input = QtWidgets.QLineEdit()

    username_input.setPlaceholderText("Username")
    password_input.setPlaceholderText("Password")
    password_input.setEchoMode(QtWidgets.QLineEdit.Password)

    layout.addWidget(username_input)
    layout.addWidget(password_input)

    submit_btn = QtWidgets.QPushButton("Login")
    layout.addWidget(submit_btn)

    result = {"user": None}

    def handle_login():
        username = username_input.text().strip()
        password = password_input.text().strip()

        if not username or not password:
            QtWidgets.QMessageBox.warning(dialog, "Error", "Kullanıcı adı ve şifre zorunlu.")
            return

        session = Session()
        user = session.query(User).filter_by(username=username).first()

        if not user or not check_pw(password, user.password_hash):
            QtWidgets.QMessageBox.critical(dialog, "Error", "Giriş başarısız.")
            return

        result["user"] = user
        dialog.accept()

    submit_btn.clicked.connect(handle_login)

    return result["user"] if dialog.exec_() == QtWidgets.QDialog.Accepted else None