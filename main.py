
from __future__ import annotations

import os
import time
import hmac
import secrets
import sqlite3
import shutil
from uuid import uuid4
from pathlib import Path
from datetime import datetime, timedelta, timezone
from contextlib import asynccontextmanager
from threading import Lock

import joblib
import jwt
import numpy as np
import pandas as pd

from dotenv import load_dotenv
from pwdlib import PasswordHash
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field, ConfigDict

# 1. CONFIGURACIÓN GENERAL

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

SECRET = os.getenv("JWT_SECRET", "")
PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH", "")

if len(SECRET) < 32 or not PASSWORD_HASH:
    raise RuntimeError(
        "Configuración de seguridad incompleta. "
        "Ejecuta python setup_security.py"
    )

MODEL_PATH = ROOT / "models" / "modelo_rf_optimizado.joblib"
PRE_PATH = ROOT / "models" / "preprocesador.joblib"
DB_PATH = ROOT / "rentai_metrics.sqlite3"
BACKUP_DIR = ROOT / "backups"

BACKUP_DIR.mkdir(parents=True, exist_ok=True)

HASHER = PasswordHash.recommended()
BEARER = HTTPBearer(auto_error=False)

MODEL_NAME = "Random Forest optimizado"

# Protección básica contra intentos repetidos de login.
LOGIN_ATTEMPTS = {}
LOGIN_LOCK = Lock()
MAX_ATTEMPTS = 5
LOCK_SECONDS = 300

# 2. COMUNAS DE SANTIAGO

# Coordenadas aproximadas de referencia.
# No representan la ubicación exacta de una propiedad.

COMUNAS = {
    "Las Condes": (-33.41, -70.57),
    "Providencia": (-33.43, -70.61),
    "Santiago": (-33.45, -70.65),
    "Ñuñoa": (-33.46, -70.60),
    "Vitacura": (-33.39, -70.57),
    "La Reina": (-33.45, -70.54),
    "Macul": (-33.49, -70.60),
    "Estación Central": (-33.46, -70.70),
    "Recoleta": (-33.41, -70.64),
    "Independencia": (-33.42, -70.66),
    "San Miguel": (-33.50, -70.65),
    "La Florida": (-33.52, -70.60),
    "Peñalolén": (-33.49, -70.55),
    "Lo Barnechea": (-33.36, -70.52)
}

NUMERICOS = {
    "latitude",
    "longitude",
    "accommodates",
    "bedrooms",
    "beds",
    "minimum_nights",
    "number_of_reviews",
    "review_scores_rating",
    "reviews_per_month"
}

# 3. BASE DE DATOS

def conectar_db():
    conexion = sqlite3.connect(DB_PATH, timeout=10)
    conexion.execute("PRAGMA busy_timeout=10000")
    return conexion


def iniciar_db():
    with conectar_db() as conexion:
        conexion.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                model TEXT NOT NULL,
                price REAL NOT NULL,
                latency_ms REAL NOT NULL
            )
        """)


def registrar_prediccion(precio, latencia):
    with conectar_db() as conexion:
        conexion.execute(
            """
            INSERT INTO predictions
            (created_at, model, price, latency_ms)
            VALUES (?, ?, ?, ?)
            """,
            (
                datetime.now(timezone.utc).isoformat(),
                MODEL_NAME,
                precio,
                latencia
            )
        )


# 4. CATEGORÍAS DEL PREPROCESADOR

def obtener_categorias(preprocesador):
    resultado = {}

    for _, transformador, columnas in preprocesador.transformers_:
        if isinstance(transformador, str):
            continue

        objeto = transformador

        if hasattr(objeto, "steps"):
            for _, paso in reversed(objeto.steps):
                if hasattr(paso, "categories_"):
                    objeto = paso
                    break

        if not hasattr(objeto, "categories_"):
            continue

        for columna, categorias in zip(
            columnas,
            objeto.categories_
        ):
            resultado[str(columna)] = [
                str(valor)
                for valor in categorias
                if pd.notna(valor)
            ]

    return resultado

# 5. CARGA DEL MODELO

@asynccontextmanager
async def lifespan(app: FastAPI):
    iniciar_db()

    if not MODEL_PATH.is_file():
        raise RuntimeError(
            "No existe models/modelo_rf_optimizado.joblib"
        )

    if not PRE_PATH.is_file():
        raise RuntimeError(
            "No existe models/preprocesador.joblib"
        )

    # Solo cargar archivos joblib propios o confiables.
    app.state.modelo = joblib.load(MODEL_PATH)
    app.state.preprocesador = joblib.load(PRE_PATH)

    pre = app.state.preprocesador
    modelo = app.state.modelo

    if not hasattr(pre, "feature_names_in_"):
        raise RuntimeError(
            "El preprocesador no contiene los nombres "
            "de las variables de entrenamiento."
        )

    if not hasattr(modelo, "predict"):
        raise RuntimeError(
            "El modelo no permite realizar predicciones."
        )

    app.state.columnas = list(pre.feature_names_in_)
    app.state.categorias = obtener_categorias(pre)

    print("RentAI: modelo y preprocesador cargados.")
    yield


app = FastAPI(
    title="RentAI Profesional",
    version="4.0",
    lifespan=lifespan,
    docs_url=None,
    redoc_url=None
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=[
        "127.0.0.1",
        "localhost",
        "testserver"
    ]
)

app.mount(
    "/static",
    StaticFiles(directory=ROOT / "frontend"),
    name="static"
)

# 6. SEGURIDAD HTTP

@app.middleware("http")
async def seguridad_http(request: Request, call_next):
    respuesta = await call_next(request)

    respuesta.headers["X-Content-Type-Options"] = "nosniff"
    respuesta.headers["X-Frame-Options"] = "DENY"
    respuesta.headers["Referrer-Policy"] = "no-referrer"
    respuesta.headers["Cache-Control"] = "no-store"

    respuesta.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self'; "
        "connect-src 'self'; "
        "img-src 'self' data:; "
        "object-src 'none'; "
        "base-uri 'none'; "
        "frame-ancestors 'none'"
    )

    return respuesta

# 7. VALIDACIÓN DE DATOS

class LoginData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    usuario: str = Field(min_length=1, max_length=100)
    contrasena: str = Field(min_length=1, max_length=200)


class PredictData(BaseModel):
    model_config = ConfigDict(extra="forbid")

    comuna: str = Field(min_length=1, max_length=100)
    property_type: str = Field(min_length=1, max_length=200)
    room_type: str = Field(min_length=1, max_length=200)

    # Números enteros
    accommodates: int = Field(strict=True, ge=1, le=40)
    bedrooms: int = Field(strict=True, ge=0, le=30)
    beds: int = Field(strict=True, ge=0, le=80)
    minimum_nights: int = Field(strict=True, ge=1, le=365)
    number_of_reviews: int = Field(
        strict=True, ge=0, le=100000
    )

    # Números decimales
    review_scores_rating: float = Field(ge=0, le=5)
    reviews_per_month: float = Field(ge=0, le=1000)

    host_is_superhost: bool = False

# 8. AUTENTICACIÓN

def verificar_admin(
    credenciales: HTTPAuthorizationCredentials | None = Depends(
        BEARER
    )
):
    if credenciales is None:
        raise HTTPException(
            status_code=401,
            detail="Debes iniciar sesión."
        )

    if credenciales.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=401,
            detail="Tipo de autenticación inválido."
        )

    try:
        datos = jwt.decode(
            credenciales.credentials,
            SECRET,
            algorithms=["HS256"],
            audience="rentai",
            issuer="rentai"
        )
    except jwt.PyJWTError as error:
        raise HTTPException(
            status_code=401,
            detail="Sesión vencida o inválida."
        ) from error

    if datos.get("sub") != "admin":
        raise HTTPException(
            status_code=403,
            detail="Acceso denegado."
        )

    return datos


@app.post("/api/login")
def iniciar_sesion(datos: LoginData, request: Request):
    # Esta protección está diseñada para uso local.
    ip = request.client.host if request.client else "local"
    ahora_monotonic = time.monotonic()

    with LOGIN_LOCK:
        intentos = [
            instante
            for instante in LOGIN_ATTEMPTS.get(ip, [])
            if ahora_monotonic - instante < LOCK_SECONDS
        ]
        LOGIN_ATTEMPTS[ip] = intentos

        if len(intentos) >= MAX_ATTEMPTS:
            raise HTTPException(
                status_code=429,
                detail="Demasiados intentos. Espera 5 minutos."
            )

    usuario_correcto = hmac.compare_digest(
        datos.usuario, "admin"
    )

    contrasena_correcta = HASHER.verify(
        datos.contrasena,
        PASSWORD_HASH
    )

    if not (usuario_correcto and contrasena_correcta):
        with LOGIN_LOCK:
            LOGIN_ATTEMPTS.setdefault(ip, []).append(
                time.monotonic()
            )

        raise HTTPException(
            status_code=401,
            detail="Usuario o contraseña incorrectos."
        )

    with LOGIN_LOCK:
        LOGIN_ATTEMPTS.pop(ip, None)

    ahora = datetime.now(timezone.utc)

    token = jwt.encode(
        {
            "sub": "admin",
            "iss": "rentai",
            "aud": "rentai",
            "iat": ahora,
            "exp": ahora + timedelta(minutes=30),
            "jti": secrets.token_hex(16)
        },
        SECRET,
        algorithm="HS256"
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": 1800
    }

# 9. PÁGINA Y ESTADO

@app.get("/")
def pagina_principal():
    return FileResponse(ROOT / "frontend" / "index.html")


@app.get("/api/health")
def estado():
    return {
        "estado": "activo",
        "modelo_cargado": hasattr(app.state, "modelo"),
        "version": "4.0"
    }


# 10. OPCIONES DEL FORMULARIO

@app.get("/api/schema")
def obtener_formulario(
    usuario=Depends(verificar_admin)
):
    categorias = app.state.categorias

    comunas_entrenadas = categorias.get(
        "neighbourhood_cleansed", []
    )

    comunas = [
        nombre
        for nombre in COMUNAS
        if nombre in comunas_entrenadas
    ]

    return {
        "nombre": MODEL_NAME,
        "columnas": app.state.columnas,
        "comunas": comunas,
        "property_types": categorias.get(
            "property_type", []
        ),
        "room_types": categorias.get(
            "room_type", []
        )
    }

# 11. CONSTRUCCIÓN DE VARIABLES

def convertir_superhost(valor, categorias):
    opciones = categorias.get("host_is_superhost", [])

    if "t" in opciones and "f" in opciones:
        return "t" if valor else "f"

    if "True" in opciones and "False" in opciones:
        return "True" if valor else "False"

    if "true" in opciones and "false" in opciones:
        return "true" if valor else "false"

    return valor


def preparar_entrada(datos: PredictData):
    categorias = app.state.categorias

    comunas_validas = [
        nombre
        for nombre in COMUNAS
        if nombre in categorias.get(
            "neighbourhood_cleansed", []
        )
    ]

    if datos.comuna not in comunas_validas:
        raise HTTPException(
            status_code=422,
            detail="Selecciona una comuna disponible."
        )

    valores_categoricos = {
        "neighbourhood_cleansed": datos.comuna,
        "property_type": datos.property_type,
        "room_type": datos.room_type
    }

    for columna, valor in valores_categoricos.items():
        if valor not in categorias.get(columna, []):
            raise HTTPException(
                status_code=422,
                detail=f"Categoría no válida: {columna}"
            )

    latitud, longitud = COMUNAS[datos.comuna]

    valores = {
        **datos.model_dump(
            exclude={"comuna", "host_is_superhost"}
        ),
        "latitude": latitud,
        "longitude": longitud,
        "neighbourhood_cleansed": datos.comuna,
        "host_is_superhost": convertir_superhost(
            datos.host_is_superhost,
            categorias
        )
    }

    # No inventar valores para variables que el formulario
    # no solicita. El preprocesador debe poder imputarlas.
    entrada = pd.DataFrame(
        [{
            columna: valores.get(columna, np.nan)
            for columna in app.state.columnas
        }],
        columns=app.state.columnas
    )

    for columna in NUMERICOS:
        if columna in entrada.columns:
            entrada[columna] = pd.to_numeric(
                entrada[columna],
                errors="coerce"
            )

    return entrada, latitud, longitud

# 12. MOTOR INTERNO DE PREDICCIÓN

def calcular_prediccion(datos: PredictData):
    entrada, latitud, longitud = preparar_entrada(datos)

    inicio = time.perf_counter()

    try:
        transformados = (
            app.state.preprocesador.transform(entrada)
        )

        esperado = getattr(
            app.state.modelo,
            "n_features_in_",
            None
        )

        if (
            esperado is not None
            and transformados.shape[1] != esperado
        ):
            raise ValueError(
                "El modelo y el preprocesador "
                "tienen cantidades de variables distintas."
            )

        resultado = app.state.modelo.predict(
            transformados
        )

        precio = float(resultado[0])

    except Exception as error:
        raise HTTPException(
            status_code=422,
            detail=(
                "No se pudo procesar la predicción: "
                + type(error).__name__
            )
        ) from error

    if not np.isfinite(precio):
        raise HTTPException(
            status_code=422,
            detail="El modelo devolvió un valor inválido."
        )

    latencia = round(
        (time.perf_counter() - inicio) * 1000,
        2
    )

    return {
        "precio_estimado": round(max(0.0, precio), 2),
        "modelo": MODEL_NAME,
        "moneda": "CLP",
        "latencia_ms": latencia,
        "coordenadas_referencia": {
            "latitude": latitud,
            "longitude": longitud
        }
    }

# 13. ENDPOINT DE PREDICCIÓN

@app.post("/api/predict")
def predecir_precio(
    datos: PredictData,
    usuario=Depends(verificar_admin)
):
    resultado = calcular_prediccion(datos)

    registrar_prediccion(
        resultado["precio_estimado"],
        resultado["latencia_ms"]
    )

    return resultado


# 14. EXPLICACIÓN POR SENSIBILIDAD LOCAL

@app.post("/api/explain")
def explicar_prediccion(
    datos: PredictData,
    usuario=Depends(verificar_admin)
):
    if datos.bedrooms >= 30:
        raise HTTPException(
            status_code=422,
            detail="No se pueden agregar más dormitorios."
        )

    original = calcular_prediccion(datos)

    datos_modificados = datos.model_copy(
        update={"bedrooms": datos.bedrooms + 1}
    )

    modificado = calcular_prediccion(
        datos_modificados
    )

    precio_original = original["precio_estimado"]
    precio_modificado = modificado["precio_estimado"]

    diferencia = round(
        precio_modificado - precio_original,
        2
    )

    porcentaje = (
        round(diferencia / precio_original * 100, 2)
        if precio_original > 0
        else None
    )

    if diferencia > 0:
        interpretacion = (
            "El modelo estima un precio mayor "
            "con un dormitorio adicional."
        )
    elif diferencia < 0:
        interpretacion = (
            "El modelo estima un precio menor "
            "con un dormitorio adicional."
        )
    else:
        interpretacion = (
            "El modelo estima el mismo precio "
            "con un dormitorio adicional."
        )

    return {
        "metodo": "Sensibilidad local",
        "modelo": MODEL_NAME,
        "moneda": "CLP",
        "dormitorios_originales": datos.bedrooms,
        "dormitorios_simulados": datos.bedrooms + 1,
        "precio_original": precio_original,
        "precio_modificado": precio_modificado,
        "diferencia_clp": diferencia,
        "variacion_porcentual": porcentaje,
        "interpretacion": interpretacion,
        "advertencia": (
            "Es una comparación entre dos predicciones. "
            "No demuestra causalidad y no es SHAP."
        )
    }

# 15. MÉTRICAS E HISTORIAL

@app.get("/api/metrics")
def obtener_metricas(
    usuario=Depends(verificar_admin)
):
    with conectar_db() as conexion:
        cantidad, promedio = conexion.execute(
            """
            SELECT COUNT(*), AVG(latency_ms)
            FROM predictions
            """
        ).fetchone()

        registros = conexion.execute(
            """
            SELECT id, created_at, price, latency_ms
            FROM predictions
            ORDER BY id DESC
            LIMIT 20
            """
        ).fetchall()

    historial = [
        {
            "id": identificador,
            "fecha": fecha,
            "precio": round(precio),
            "latencia_ms": latencia
        }
        for identificador, fecha, precio, latencia
        in registros
    ]

    return {
        "predicciones": cantidad,
        "latencia_modelo_ms": (
            round(promedio, 2)
            if promedio is not None
            else None
        ),
        "historial": historial
    }

# 16. SISTEMA DE RESPALDOS


@app.post("/api/admin/backup")
def crear_respaldo(
    usuario=Depends(verificar_admin)
):
    fecha = datetime.now(timezone.utc).strftime(
        "%Y%m%d_%H%M%S"
    )

    nombre = f"backup_{fecha}_{uuid4().hex[:8]}"
    destino = BACKUP_DIR / nombre

    destino.mkdir(parents=True, exist_ok=False)

    try:
        with conectar_db() as origen:
            with sqlite3.connect(
                destino / "rentai_metrics.sqlite3"
            ) as copia:
                origen.backup(copia)

        shutil.copy2(
            MODEL_PATH,
            destino / MODEL_PATH.name
        )

        shutil.copy2(
            PRE_PATH,
            destino / PRE_PATH.name
        )

    except Exception as error:
        shutil.rmtree(
            destino,
            ignore_errors=True
        )

        raise HTTPException(
            status_code=500,
            detail="No se pudo crear el respaldo."
        ) from error

    return {
        "mensaje": "Respaldo creado correctamente.",
        "nombre": nombre
    }


@app.get("/api/admin/backups")
def listar_respaldos(
    usuario=Depends(verificar_admin)
):
    respaldos = sorted(
        [
            carpeta.name
            for carpeta in BACKUP_DIR.iterdir()
            if carpeta.is_dir()
        ],
        reverse=True
    )

    return {"respaldos": respaldos}
