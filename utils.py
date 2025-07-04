from config import USUARIOS_PERMITIDOS

def usuario_permitido(update):
    username = update.effective_user.username
    if username not in USUARIOS_PERMITIDOS:
        return False
    return True