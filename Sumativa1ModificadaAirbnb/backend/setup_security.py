from pathlib import Path
from getpass import getpass
from pwdlib import PasswordHash
import secrets

ROOT = Path(__file__).resolve().parent
ENV = ROOT / ".env"

if ENV.exists():
    raise SystemExit(
        "Ya existe .env. No se modificaron las credenciales."
    )

password = getpass("Crea una contraseña (mínimo 12 caracteres): ")
repeat = getpass("Repite la contraseña: ")

if password != repeat:
    raise SystemExit("Las contraseñas no coinciden.")

if len(password) < 12:
    raise SystemExit("La contraseña es demasiado corta.")

hashed = PasswordHash.recommended().hash(password)
secret = secrets.token_urlsafe(48)

with ENV.open("x", encoding="utf-8") as f:
    f.write(f"ADMIN_PASSWORD_HASH={hashed}\n")
    f.write(f"JWT_SECRET={secret}\n")

print("Configuración de seguridad creada.")
print("Usuario: admin")
print("Conserva tu contraseña en un lugar seguro.")
