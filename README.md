# ope3-logistica

## Estructura del Repositorio

* `data`: Contiene los datos del problema.
  * `raw`: Contiene los datos originales del enunciado.
  * `inputs`: Contiene los datos del enunciados formateados para usarlos en el modelo.
  * `outputs`: Carpeta donde se guardan las salidas del modelo en caso de salvarlas.

* `logistica`: Esta carpeta contiene todos los módulos con funciones y clases que permiten ejecutar el programa de optimización.
  * `componentes.py`: Contiene la definición de las clases Camion y Pedido.
  * `ruteo.py`: Contiene la definición de la clase principal Ruteo.
  * `metaheuristicas.py`: Contiene las funciones de optimización y visualización de resultados.
  * `utils.py`: Contiene functiones varias.

* `notebooks`: Contiene notebooks diferentes con distintas modalidades de ejecución del programa.
  * `optimizacion_diaria_directa.ipynb`: Permite correr la optimización para todos los pedidos de 1 día, de manera directa (sin los detalles y extensión del notebook `optimizacion_diaria.ipynb`).
  * `optimizacion_multiple`: Permite correr la optimización para todos los pedidos en múltiples días de manera directa. Genera una solución optimizada para cada columna con el nombre `pedido` de la hoja `pedidos` del archivo de inputs.
  * `pruebas`: pruebas varias de código.

* `optimizacion_diaria.ipynb`: Notebook que permite correr la optimización de todos los pedidos de 1 día a partir de los datos en `data/inputs` y en detalle.

    El siguiente botón se puede usar para correr este notebook directamente en Google Colab, sin la necesidad de instalar Python o cualquier librería.

    [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/JuanCruzC97/ope3-logistica/blob/main/optimizacion_diaria.ipynb)

