class UserNotFound(Exception):
    user_id: int

    def __init__(self, user_id: int, *args):
        super().__init__(*args)
        self.user_id = user_id

    def __str__(self):
        return f"No se encontró el usuario con el ID '{self.user_id}'."


class UserAlreadyExists(Exception):
    email: str

    def __init__(self, email: str, *args):
        super().__init__(*args)
        self.email = email

    def __str__(self):
        return f"El usuario con el correo '{self.email}' ya existe."


class InvalidLoginData(Exception):
    def __init__(self, *args):
        super().__init__(*args)

    def __str__(self):
        return f"Contraseña o email inválidos. Contraseña debe tener mínimo 8 caracteres, una mayúscula, una minúscula, un número y un carácter especial"
