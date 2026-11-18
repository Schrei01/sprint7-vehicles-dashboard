# Explorador de anuncios de vehículos usados — Sprint 7

Proyecto de análisis exploratorio básico y aplicación web de **Streamlit** con visualizaciones interactivas en **Plotly**. Los datos provienen del archivo `vehicles_us.csv` suministrado para el proyecto.

## Aplicación desplegada en Render

**URL pública:** PENDIENTE_DE_COMPLETAR_DESPUÉS_DEL_DESPLIEGUE

> Reemplazar el texto anterior con la URL real `https://nombre-del-servicio.onrender.com` antes de entregar el proyecto.

## Funcionalidades

- Selector de tipo de vehículo.
- Indicadores: cantidad de anuncios, precio mediano y kilometraje mediano.
- Casilla para visualizar la distribución del kilometraje mediante histograma.
- Casilla para visualizar la relación precio–kilometraje mediante diagrama de dispersión.
- Explicación del tratamiento de valores ausentes y de las limitaciones de los datos.

## Estructura

```text
proyecto_sprint7_vehiculos/
├── app.py
├── vehicles_us.csv
├── requirements.txt
├── README.md
├── .gitignore
├── render.yaml
└── notebooks/
    └── EDA.ipynb
```

## Ejecutar localmente

Requiere Python 3.10 o superior. Desde la carpeta raíz del proyecto:

```powershell
python -m venv vehicles_env
.\vehicles_env\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Si PowerShell no permite activar el entorno, ejecuta directamente:

```powershell
.\vehicles_env\Scripts\python.exe -m pip install -r requirements.txt
.\vehicles_env\Scripts\python.exe -m streamlit run app.py
```

La aplicación se abre habitualmente en `http://localhost:8501`.

## Despliegue en Render

También se incluye un `render.yaml` para crear el servicio como Blueprint desde Render (New > Blueprint), siempre que el plan gratuito esté disponible. En despliegue manual, sigue estos pasos:

1. Subir todos los archivos del proyecto a un repositorio público de GitHub.
2. Crear en Render un **New > Web Service** conectado al repositorio.
3. Seleccionar **Python** como entorno/runtime y la rama principal.
4. Configurar **Build Command**:

   ```bash
   pip install --upgrade pip && pip install -r requirements.txt
   ```

5. Configurar **Start Command**:

   ```bash
   streamlit run app.py --server.address 0.0.0.0 --server.port $PORT
   ```

6. Desplegar y verificar que la URL pública abre el dashboard.
7. Reemplazar `PENDIENTE_DE_COMPLETAR_DESPUÉS_DEL_DESPLIEGUE` con la URL real y hacer commit.

**Nota:** el comando de inicio explícito utiliza el host y puerto que Render necesita para ofrecer el servicio web públicamente.

## Análisis exploratorio

`notebooks/EDA.ipynb` incluye las comprobaciones de calidad y visualizaciones iniciales. Se evita imputar valores ausentes sin evidencia y los valores extremos se mantienen en los datos originales.

## Alcance

Este panel facilita la exploración descriptiva de los anuncios. Una asociación observada entre precio y kilometraje no demuestra causalidad, y los valores son precios anunciados, no necesariamente precios de transacciones reales.