from PySide6.QtWidgets import QMainWindow, QMessageBox  # Importar QMessageBox para mostrar mensajes de error
from PySide6.QtCore import Slot
from views.qt.login import Ui_MainWindow
from views.register_windows import RegisterWindow
from controllers.usuario_controller import UsuarioController

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Conectar los botones a sus funciones respectivas
        self.ui.login_button.clicked.connect(self.slot_on_button_login_clicked)
        self.ui.register_button.clicked.connect(self.slot_on_button_crear_cuenta_clicked)

        self.usuario_controller = UsuarioController()

        # Variable para almacenar la posición de la última ventana mostrada
        self.last_position = None

    @Slot()
    def slot_on_button_login_clicked(self):  
        print("Hemos pulsado el botón de login")
        name = self.ui.email_editline.text().strip()  # Usar .strip() para eliminar espacios
        password = self.ui.password_editline.text()

        # Verificar si los campos están vacíos
        if not name or not password:
            QMessageBox.warning(self, "Error de Login", "Por favor, completa todos los campos.")
            return

        # Verificar credenciales del usuario
        if self.usuario_controller.verificar_usuario(name, password):
            QMessageBox.information(self, "Bienvenido", f"Bienvenido {name}!")  
            print(f"Bienvenido {name}")
        else:
            QMessageBox.warning(self, "Error de Login", "Nombre de usuario o contraseña incorrectos.")  # Mensaje de error
            print("Error al iniciar sesión")

    @Slot()
    def slot_on_button_crear_cuenta_clicked(self):
        """Oculta la ventana de login y muestra la de registro en la última posición registrada"""
        print("Hemos pulsado el botón de registro")

        # Guardar la posición actual de login antes de ocultarla
        self.last_position = self.pos()
        self.hide()

        # Crear y configurar la ventana de registro
        self.registro_window = RegisterWindow(parent=self)  # Pasa `self` como parent
        self.registro_window.setWindowTitle("Registro - La Estantería de Don Librote")

        # Mover la ventana de registro a la última posición registrada
        if self.last_position:
            self.registro_window.move(self.last_position)

        # Mostrar la ventana de registro
        self.registro_window.show()

        # Al cerrar registro, guardar su posición actual y volver a mostrar login
        self.registro_window.destroyed.connect(self.update_position_and_show_login)

    @Slot()
    def update_position_and_show_login(self):
        """Actualiza la última posición registrada y vuelve a mostrar la ventana de login"""
        # Guardar la posición actual de la ventana de registro si está visible
        if self.registro_window:
            self.last_position = self.registro_window.pos()

        # Mover login a la última posición registrada y mostrarlo
        if self.last_position:
            self.move(self.last_position)

        self.show()
