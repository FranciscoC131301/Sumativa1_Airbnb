# RentAI Profesional

**Proyecto académico – Aprendizaje de Máquinas**

**Estudiante:** Francisco Carvajal Leiva  
**Universidad:** Universidad Andrés Bello (UNAB)  
**Carrera:** Ingeniería Civil Informática  
**Profesor:** Omar  
**Año:** 2026

## 1. Descripción del proyecto

RentAI Profesional es una aplicación web desarrollada en Python que utiliza técnicas de Machine Learning para estimar el precio por noche de alojamientos Airbnb en Santiago de Chile, considerando las características y ubicación de las propiedades.

El proyecto integra análisis de datos, entrenamiento de modelos predictivos, desarrollo de un backend mediante FastAPI y una interfaz web interactiva.

## 2. Tecnologías utilizadas

- **Python:** desarrollo y procesamiento de datos.
- **Pandas y NumPy:** análisis y preparación de datos.
- **Scikit-learn:** entrenamiento y evaluación de modelos.
- **Random Forest:** modelo predictivo seleccionado.
- **FastAPI y Uvicorn:** backend y servidor local.
- **HTML, CSS y JavaScript:** desarrollo del frontend.
- **SQLite:** almacenamiento local.
- **Jupyter Notebook:** entrenamiento y análisis de resultados.
- **SHAP:** interpretación de las predicciones.

## 3. Modelos y resultados

Se compararon diferentes algoritmos de regresión y se seleccionó un modelo Random Forest optimizado mediante validación cruzada.

Resultados aproximados del modelo seleccionado:

| Métrica | Resultado |
|---|---|
| MAE | $25.687 CLP |
| RMSE | $72.952 CLP |
| R² | 0,6655 |
| WAPE | 29,98 % |

También se realizaron análisis de convergencia de redes neuronales y explicaciones individuales mediante SHAP.

## 4. Funcionalidades

- Estimación del precio por noche de alojamientos.
- Interfaz web para ingresar características de propiedades.
- Autenticación de usuarios.
- Historial de predicciones.
- Consulta de métricas.
- Validación de datos y mecanismos básicos de seguridad.

## 5. Instalación y ejecución

**Requisitos previos:** Python, Git y conexión a Internet para instalar las dependencias.

### Paso 1. Descargar el repositorio

Abrir PowerShell y ejecutar:

```powershell
git clone https://github.com/FranciscoC131301/Sumativa1_Airbnb.git
cd Sumativa1_Airbnb
cd Sumativa1ModificadaAirbnb
```

### Paso 2. Crear y activar un entorno virtual

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Paso 3. Instalar las dependencias

```powershell
python -m pip install -r requirements.txt
```

### Paso 4. Configurar la seguridad

Ejecutar:

```powershell
python backend/setup_security.py
```

El proyecto requiere las variables de seguridad `JWT_SECRET` y `ADMIN_PASSWORD_HASH`.

El archivo `.env` debe quedar en la carpeta principal del proyecto, junto a `requirements.txt`.

Si el script lo crea dentro de `backend`, ejecutar:

```powershell
Move-Item backend\.env .env
```

Cada usuario debe generar sus propias credenciales. El archivo `.env` no se incluye en GitHub por seguridad.

### Paso 5. Iniciar la aplicación

```powershell
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8765
```

### Paso 6. Abrir RentAI Profesional

Ingresar desde el navegador a:

http://127.0.0.1:8765

Documentación de la API:

http://127.0.0.1:8765/docs

Para detener el servidor, presionar `Ctrl + C` en PowerShell.

## 6. Estructura del proyecto

```text
Sumativa1_Airbnb/
│
└── Sumativa1ModificadaAirbnb/
    ├── backend/
    │   ├── main.py
    │   ├── __init__.py
    │   └── setup_security.py
    │
    ├── frontend/
    │   ├── index.html
    │   ├── app.js
    │   └── style.css
    │
    ├── models/
    │   ├── modelo_rf_optimizado.joblib
    │   └── preprocesador.joblib
    │
    ├── notebook/
    │   └── Entrenamiento_nuevo.ipynb
    │
    ├── resultados/
    │
    ├── requirements.txt
    ├── README.md
    └── .gitignore
```

## 7. Seguridad

El proyecto incorpora autenticación, validación de entradas y configuración local de credenciales.

Por seguridad, no se publican archivos `.env`, contraseñas, tokens, bases de datos locales ni respaldos privados.

La aplicación se ejecuta en `127.0.0.1`, por lo que corresponde a una ejecución local y no a un servicio publicado en Internet.

## 8. Finalidad académica

RentAI Profesional fue desarrollado para la asignatura de Aprendizaje de Máquinas de la Universidad Andrés Bello.

Su finalidad es demostrar la aplicación de técnicas de aprendizaje automático en la estimación de precios de alojamientos turísticos. Los resultados son estimaciones estadísticas y no garantizan precios reales de mercado.

**Autor:** Francisco Carvajal Leiva  
**Año:** 2026
