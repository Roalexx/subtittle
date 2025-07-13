from PyQt5 import QtWidgets
from db import Session, User, hash_pw, check_pw, valid_pw

class RegisterDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Register")
        self.setFixedSize(300, 200)
        self.user, self.pw, self.key = None, None, None
        v = QtWidgets.QVBoxLayout(self)
        self.u = QtWidgets.QLineEdit(); self.u.setPlaceholderText("Username")
        self.p = QtWidgets.QLineEdit(); self.p.setPlaceholderText("Password"); self.p.setEchoMode(QtWidgets.QLineEdit.Password)
        self.k = QtWidgets.QLineEdit(); self.k.setPlaceholderText("DEEPL_API_KEY")
        v.addWidget(self.u); v.addWidget(self.p); v.addWidget(self.k)
        btn = QtWidgets.QPushButton("Create"); btn.clicked.connect(self.save)
        v.addWidget(btn)

    def save(self):
        if not valid_pw(self.p.text()):
            QtWidgets.QMessageBox.warning(self,"Err","Şifre ≥8 ve ≥1 rakam içermeli.")
            return
        s = Session()
        if s.query(User).filter_by(username=self.u.text()).first():
            QtWidgets.QMessageBox.warning(self,"Err","Kullanıcı zaten var.")
            return
        user = User(username=self.u.text(),
                    password_hash=hash_pw(self.p.text()),
                    deepl_key=self.k.text())
        s.add(user); s.commit()
        QtWidgets.QMessageBox.information(self,"OK","Kaydedildi.")
        self.accept()

class LoginDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login"); self.setFixedSize(300,150)
        self.user=None; v=QtWidgets.QVBoxLayout(self)
        self.u=QtWidgets.QLineEdit(); self.u.setPlaceholderText("Username")
        self.p=QtWidgets.QLineEdit(); self.p.setPlaceholderText("Password"); self.p.setEchoMode(QtWidgets.QLineEdit.Password)
        v.addWidget(self.u); v.addWidget(self.p)
        b=QtWidgets.QPushButton("Login"); b.clicked.connect(self.auth); v.addWidget(b)

    def auth(self):
        s=Session(); u=s.query(User).filter_by(username=self.u.text()).first()
        if not u or not check_pw(self.p.text(), u.password_hash):
            QtWidgets.QMessageBox.critical(self,"Err","Hatalı giriş."); return
        self.user=u; self.accept()