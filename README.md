# Mossbauer

"folding.py": dobla, normaliza y calibra en velocidad un espectro de 1024 canales en archivo a una columna

"PyMossFit.py": ajusta espectro con el archivo de salida del código "folding.py". Se deben agregar tantas interacciones (singletes, dobletes, sextetes) como sean necesarias

"plotmossb2.py": gráficos calidad publicación de espectros, ajustes y modelos de interacciones.

PyMossFit-V4-1Q.ipynb y PyMossFit-V4-1Q1D.ipynb están diseñados para correr en Google Colab. Doblan espectros eNn canal optimizado con rutinas de FFT. Ajustan espectros mediante Lmfit, grafican y dan reporte de salida.
