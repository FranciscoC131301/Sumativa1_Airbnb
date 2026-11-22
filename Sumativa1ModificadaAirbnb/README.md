# RentAI Profesional

**Proyecto académico – Aprendizaje de Máquinas**

**Estudiante:** Francisco Carvajal Leiva  
**Universidad:** Universidad Andrés Bello (UNAB)  
**Profesor:** Omar

## 1. Descripción

RentAI Profesional es una aplicación web que utiliza Machine Learning para estimar el precio por noche de alojamientos Airbnb en Santiago de Chile, considerando sus características y ubicación.

## 2. Tecnologías utilizadas

- **Python:** procesamiento de datos y entrenamiento.
- **Scikit-learn:** desarrollo y evaluación de modelos predictivos.
- **Pandas y NumPy:** análisis de datos.
- **FastAPI:** desarrollo del backend.
- **HTML, CSS y JavaScript:** interfaz web.
- **SQLite:** almacenamiento local.
- **Jupyter Notebook:** entrenamiento y análisis de resultados.

## 3. Modelos y resultados

Se evaluaron diferentes algoritmos de regresión, seleccionando un **Random Forest optimizado** para la aplicación.

Resultados del modelo seleccionado:

| Métrica | Resultado |
|---|---|
| MAE | $25.687 CLP |
| RMSE | $72.952 CLP |
| R² | 0,6655 |
| WAPE | 29,98 % |

Se utilizaron validación cruzada, optimización de hiperparámetros y análisis SHAP para interpretar predicciones.

## 4. Funcionalidades

- Predicción del precio por noche.
- Interfaz web para ingresar características del alojamiento.
- Autenticación de usuarios.
- Historial de predicciones.
- Consulta de métricas y análisis de resultados.

## 5. Instalación y ejecución

Instalar las dependencias desde la carpeta principal:

```bash
pip install -r requirements.txt
```

Iniciar la aplicación:

```bash
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8765
```

Acceder a la aplicación en:

`http://127.0.0.1:8765`

La ejecución requiere disponer de los archivos del modelo entrenado y configurar las variables de entorno necesarias.

## 6. Seguridad

El proyecto utiliza autenticación, validación de datos y un archivo `.gitignore` para evitar publicar credenciales, bases de datos locales y respaldos.

## 7. Finalidad académica

Proyecto desarrollado para la asignatura **Aprendizaje de Máquinas**, con fines educativos. Las predicciones son estimaciones estadísticas y no garantizan precios reales de mercado.
