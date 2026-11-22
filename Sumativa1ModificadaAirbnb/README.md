# RentAI Profesional

**Proyecto académico – Aprendizaje de Máquinas**

**Estudiante:** Francisco Carvajal Leiva  
**Carrera:** Ingeniería Civil Informática  
**Universidad:** Universidad Andrés Bello (UNAB)  
**Profesor:** Omar  
**Año:** 2026

---

## 1. Descripción del proyecto

RentAI Profesional es una aplicación web desarrollada en Python que utiliza técnicas de Machine Learning para estimar el precio por noche de alojamientos Airbnb en Santiago de Chile.

El proyecto integra el procesamiento y análisis de datos, entrenamiento y evaluación de modelos predictivos, desarrollo de un backend mediante FastAPI y una interfaz web para realizar predicciones.

El objetivo es aplicar algoritmos de aprendizaje automático a un problema real de estimación de precios de alojamientos turísticos.

## 2. Tecnologías utilizadas

| Tecnología | Función |
|---|---|
| Python | Lenguaje principal del proyecto |
| Pandas y NumPy | Limpieza, transformación y análisis de datos |
| Scikit-learn | Entrenamiento y evaluación de modelos |
| Random Forest | Modelo predictivo seleccionado |
| FastAPI | Desarrollo del backend |
| Uvicorn | Ejecución del servidor local |
| HTML, CSS y JavaScript | Desarrollo de la interfaz web |
| SQLite | Almacenamiento local |
| Jupyter Notebook | Entrenamiento y experimentación |
| SHAP | Interpretación de las predicciones |

## 3. Resultados del modelo

Durante el desarrollo se evaluaron distintos algoritmos de regresión y se seleccionó un modelo Random Forest optimizado.

| Métrica | Resultado aproximado |
|---|---|
| MAE | $25.687 CLP |
| RMSE | $72.952 CLP |
| R² | 0,6655 |
| WAPE | 29,98 % |

Estas métricas permiten evaluar el desempeño del modelo al estimar el precio por noche de un alojamiento.

## 4. Requisitos antes de comenzar

Para ejecutar RentAI Profesional en Windows se necesita:

- Windows 10 u 11.
- Python instalado.
- Conexión a Internet para descargar las dependencias.
- PowerShell, incluido en Windows.

**No es necesario instalar Git, Anaconda ni Visual Studio Code para ejecutar la aplicación.**

### 4.1. Instalar Python

Si Python no está instalado, descargarlo desde:

https://www.python.org/downloads/

Se recomienda Python 3.11 o 3.12 como punto de partida, sujeto a la compatibilidad con las versiones indicadas en `requirements.txt`.

Durante la instalación, habilitar la opción para agregar Python al PATH, si está disponible.

Después, cerrar y volver a abrir PowerShell.

### 4.2. Comprobar Python

Ejecutar:

```powershell
python --version
```

Si aparece un resultado similar a:

```text
Python 3.11.x
```

Python está disponible desde PowerShell.

Si aparece un error indicando que Python no se reconoce, revisar su instalación y configuración del PATH.

**Importante:** tener Python instalado no garantiza que todas las librerías sean compatibles. La instalación de dependencias se comprobará posteriormente.

---

# GUÍA DE INSTALACIÓN DESDE CERO

## 5. Descargar el proyecto desde GitHub

Este procedimiento permite descargar el proyecto sin utilizar comandos Git.

### Paso 1. Abrir el repositorio

Ingresar a:

https://github.com/FranciscoC131301/Sumativa1_Airbnb

### Paso 2. Descargar el código

En la página principal del repositorio:

1. Presionar el botón verde **Code**.
2. Seleccionar **Download ZIP**.
3. Esperar a que termine la descarga.

GitHub genera automáticamente el ZIP con el contenido de la rama seleccionada. No es necesario que exista previamente un archivo ZIP dentro del repositorio.

### Paso 3. Extraer los archivos

1. Abrir la carpeta Descargas de Windows.
2. Buscar el archivo ZIP descargado.
3. Hacer clic derecho sobre él.
4. Seleccionar **Extraer todo**.
5. Abrir la carpeta extraída.

Normalmente tendrá un nombre similar a:

```text
Sumativa1_Airbnb-main
```

### Paso 4. Encontrar la carpeta principal de RentAI

Dentro de la carpeta descargada, ingresar a:

```text
Sumativa1ModificadaAirbnb
```

En ella deben encontrarse:

```text
backend
frontend
models
notebook
resultados
requirements.txt
README.md
.gitignore
```

Esta es la carpeta desde la que se ejecutarán los comandos.

## 6. Abrir PowerShell en la carpeta correcta

Este paso es especialmente importante.

No se deben ejecutar los comandos desde `C:\WINDOWS\System32`, porque allí no se encuentran los archivos del proyecto.

### Procedimiento recomendado

1. Abrir el Explorador de archivos de Windows.
2. Entrar a la carpeta `Sumativa1ModificadaAirbnb`.
3. Hacer clic en la barra de direcciones del Explorador.
4. Borrar la dirección seleccionada.
5. Escribir:

```text
powershell
```

6. Presionar Enter.

Se abrirá PowerShell directamente en la carpeta del proyecto.

### Comprobar la ubicación

Ejecutar:

```powershell
Get-Location
```

La ruta mostrada debe terminar en:

```text
Sumativa1ModificadaAirbnb
```

Después ejecutar:

```powershell
Test-Path requirements.txt
```

El resultado esperado es:

```text
True
```

Esto confirma que PowerShell encuentra el archivo de dependencias.

También se puede ejecutar:

```powershell
dir
```

Este comando muestra las carpetas y archivos del directorio actual.

**Si aparece `False` al comprobar `requirements.txt`, no continuar todavía.** Volver al Explorador de archivos y abrir PowerShell desde la carpeta que contiene ese archivo.

## 7. Crear el entorno virtual de Python

Un entorno virtual permite instalar las librerías del proyecto sin mezclarlas con las de otros programas de Python.

Con PowerShell abierto en `Sumativa1ModificadaAirbnb`, ejecutar:

```powershell
python -m venv .venv
```

Este comando crea una carpeta llamada `.venv`.

### Comprobar que se creó

Ejecutar:

```powershell
Test-Path .venv\Scripts\python.exe
```

El resultado esperado es:

```text
True
```

**Nota:** no es necesario activar el entorno virtual manualmente.

En los siguientes pasos se utilizará directamente el Python instalado dentro de `.venv`, evitando posibles bloqueos de scripts de PowerShell.

## 8. Instalar las librerías necesarias

Ejecutar:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Este comando instala las dependencias indicadas en el archivo `requirements.txt`.

La instalación puede tardar varios minutos, dependiendo de la conexión a Internet y del computador.

### Comprobar las dependencias

Cuando termine, ejecutar:

```powershell
.\.venv\Scripts\python.exe -m pip check
```

Si aparece:

```text
No broken requirements found.
```

No se detectaron conflictos entre las dependencias instaladas.

También se puede comprobar FastAPI:

```powershell
.\.venv\Scripts\python.exe -m pip show fastapi
```

Y Uvicorn:

```powershell
.\.venv\Scripts\python.exe -m pip show uvicorn
```

Si muestran información de los paquetes, están instalados en el entorno virtual.

**Importante:** si la instalación muestra errores de compatibilidad, no continuar hasta resolverlos. Puede ser necesario utilizar otra versión de Python compatible con `requirements.txt`.

## 9. Comprobar los archivos del modelo predictivo

Antes de iniciar el servidor, verificar que los modelos entrenados se encuentren disponibles.

Ejecutar:

```powershell
Test-Path models\modelo_rf_optimizado.joblib
```

Después:

```powershell
Test-Path models\preprocesador.joblib
```

Ambos comandos deben devolver:

```text
True
```

Estos archivos contienen el modelo entrenado y el preprocesador utilizados por la aplicación.

Si alguno devuelve `False`, comprobar que la descarga incluya los archivos correspondientes dentro de `models`.

## 10. Configurar la seguridad

RentAI Profesional requiere variables de seguridad para iniciar correctamente.

Las principales son:

- `JWT_SECRET`: clave utilizada para firmar los tokens de autenticación.
- `ADMIN_PASSWORD_HASH`: hash de la contraseña del administrador.

Por seguridad, estas variables se almacenan localmente en un archivo llamado `.env`.

### Paso 1. Ejecutar la configuración

Ejecutar:

```powershell
.\.venv\Scripts\python.exe backend\setup_security.py
```

El script prepara la configuración de seguridad.

### Paso 2. Comprobar dónde se generó el archivo

Ejecutar:

```powershell
Test-Path .env
```

Si aparece:

```text
True
```

El archivo ya está en la carpeta principal.

Si aparece:

```text
False
```

Comprobar si está dentro de `backend`:

```powershell
Test-Path backend\.env
```

Si el resultado es `True`, moverlo mediante:

```powershell
Move-Item backend\.env .env
```

### Paso 3. Confirmar la ubicación

Ejecutar nuevamente:

```powershell
Test-Path .env
```

Debe aparecer:

```text
True
```

El archivo `.env` debe encontrarse en la misma carpeta que `requirements.txt`.

**No compartir ni publicar el contenido de `.env`.**

### Paso 4. Credenciales de acceso

El administrador debe utilizar una contraseña correspondiente al hash generado durante la configuración.

Si el script no solicita una contraseña ni informa cómo establecerla, la configuración de acceso requiere una revisión adicional antes de iniciar sesión.

No se recomienda publicar contraseñas predeterminadas en el repositorio.

## 11. Iniciar el servidor de RentAI

Una vez instaladas las dependencias, comprobados los modelos y configurada la seguridad, ejecutar:

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8765
```

Este comando inicia el backend de FastAPI utilizando Uvicorn.

### ¿Qué significa cada parte?

- `.\.venv\Scripts\python.exe`: utiliza Python del entorno virtual.
- `-m uvicorn`: ejecuta el servidor Uvicorn.
- `backend.main:app`: indica dónde está definida la aplicación FastAPI.
- `--host 127.0.0.1`: permite acceder desde el mismo computador.
- `--port 8765`: utiliza el puerto local 8765.

### Resultado esperado

Si el servidor inicia correctamente, aparecerán mensajes similares a:

```text
INFO: Uvicorn running on http://127.0.0.1:8765
INFO: Application startup complete.
```

Esto confirma que el servidor ha iniciado.

**Mantener PowerShell abierto mientras se utiliza la aplicación.**

## 12. Abrir RentAI Profesional

Abrir Google Chrome, Microsoft Edge u otro navegador.

Ingresar a:

http://127.0.0.1:8765

La aplicación debería mostrar su interfaz web.

Para consultar la documentación interactiva de FastAPI, si está habilitada:

http://127.0.0.1:8765/docs

### Comprobar el funcionamiento

Se recomienda verificar:

1. Que la página principal cargue correctamente.
2. Que se pueda iniciar sesión con credenciales válidas.
3. Que los campos de predicción permitan ingresar datos.
4. Que la aplicación genere una estimación.
5. Que el historial y las métricas funcionen, cuando corresponda.

Para detener el servidor, regresar a PowerShell y presionar:

```text
Ctrl + C
```

---

# EJECUCIONES POSTERIORES

## 13. Cómo volver a abrir RentAI otro día

Una vez completada la instalación inicial, no es necesario volver a descargar el proyecto ni instalar todas las librerías.

### Paso 1

Abrir la carpeta:

```text
Sumativa1ModificadaAirbnb
```

### Paso 2

Escribir `powershell` en la barra de direcciones del Explorador de archivos.

### Paso 3

Ejecutar:

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8765
```

### Paso 4

Abrir:

http://127.0.0.1:8765

No es necesario ejecutar nuevamente `setup_security.py` si `.env` ya está configurado correctamente.

---

# SOLUCIÓN DE PROBLEMAS

## 14. Error: `git` no se reconoce

Este error aparece cuando Git no está instalado o no está disponible desde PowerShell.

**Solución:** descargar el proyecto mediante **Code → Download ZIP**.

No es obligatorio utilizar `git clone`.

## 15. Error: `requirements.txt` no encontrado

Este error ocurre cuando PowerShell está ubicado en una carpeta diferente a la del proyecto.

Comprobar:

```powershell
Get-Location
```

Después:

```powershell
Test-Path requirements.txt
```

Si aparece `False`, abrir PowerShell directamente desde la carpeta `Sumativa1ModificadaAirbnb`.

## 16. Error: configuración de seguridad incompleta

Si aparece:

```text
RuntimeError: Configuración de seguridad incompleta
```

Comprobar:

```powershell
Test-Path .env
```

Si el archivo está dentro de `backend`, moverlo a la carpeta principal:

```powershell
Move-Item backend\.env .env
```

Si el archivo ya está en la raíz y el error continúa, revisar la configuración de las variables de seguridad sin mostrar ni compartir sus valores.

## 17. Error: `ModuleNotFoundError`

Este error indica que Python no puede encontrar un módulo requerido.

Comprobar que se hayan instalado las dependencias:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Ejecutar siempre la aplicación utilizando el Python del entorno virtual.

## 18. Error: el puerto 8765 está ocupado

Puede ocurrir si ya existe otra instancia del servidor utilizando ese puerto.

Revisar si RentAI está ejecutándose en otra ventana de PowerShell.

Si es así, detenerlo con `Ctrl + C` y volver a intentarlo.

## 19. Error: no se puede iniciar sesión

Comprobar que la configuración de seguridad haya generado correctamente el hash de la contraseña del administrador.

El archivo `.env` no debe modificarse manualmente sin conocer el formato que espera la aplicación.

Si no se dispone de una contraseña válida, revisar el procedimiento de creación de credenciales en `backend/setup_security.py`.

## 20. Error: Python incompatible

Algunas versiones recientes de Python pueden presentar problemas con versiones específicas de librerías científicas.

Si la instalación de dependencias falla por incompatibilidad:

1. Revisar el mensaje de error.
2. Comprobar las versiones requeridas en `requirements.txt`.
3. Instalar una versión de Python compatible.
4. Crear nuevamente el entorno virtual con esa versión.
5. Repetir la instalación de dependencias.

---

# INFORMACIÓN ADICIONAL

## 21. Estructura del proyecto

```text
Sumativa1ModificadaAirbnb/
│
├── backend/
│   ├── main.py
│   └── setup_security.py
│
├── frontend/
│
├── models/
│   ├── modelo_rf_optimizado.joblib
│   └── preprocesador.joblib
│
├── notebook/
│
├── resultados/
│
├── requirements.txt
├── README.md
└── .gitignore
```

### Descripción

**backend:** contiene la API, lógica del servidor y configuración de seguridad.

**frontend:** contiene los archivos de la interfaz web.

**models:** contiene el modelo entrenado y el preprocesador.

**notebook:** contiene los experimentos, análisis y entrenamiento de Machine Learning.

**resultados:** almacena archivos relacionados con la evaluación del modelo.

**requirements.txt:** contiene las dependencias necesarias para ejecutar la aplicación.

**README.md:** documentación e instrucciones de instalación.

**.gitignore:** permite excluir determinados archivos del control de versiones.

## 22. Seguridad del proyecto

RentAI Profesional utiliza autenticación y configuración local de credenciales.

Por motivos de seguridad:

- No publicar contraseñas ni claves privadas.
- No subir el archivo `.env` a GitHub.
- No publicar bases de datos locales con información privada.
- Utilizar credenciales propias en cada instalación.
- Mantener las dependencias actualizadas.
- Utilizar el servidor local para fines académicos y de demostración.

La dirección `127.0.0.1` permite acceder a la aplicación desde el mismo computador, sin exponer directamente el servidor a Internet.

## 23. Finalidad académica

RentAI Profesional fue desarrollado para la asignatura de Aprendizaje de Máquinas de la Universidad Andrés Bello.

Su finalidad es demostrar la aplicación de técnicas de Machine Learning a la estimación de precios de alojamientos turísticos.

Las predicciones corresponden a estimaciones estadísticas y no garantizan los valores reales del mercado.

**Autor:** Francisco Carvajal Leiva  
**Año:** 2026