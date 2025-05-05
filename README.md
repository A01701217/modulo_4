# modulo_4
M4_Interacción_inteligente_H_S


Manual : Procesador de Audio Version7.py

1.	Inicio de la aplicación
  o	Ejecuta el script y se abrirá la ventana principal.
  o	Verás dos gráficas: la superior muestra la señal en el tiempo y la inferior la FFT de la señal original (en azul).
2.	Cargar Audio
  o	Haz clic en el botón "Cargar".
  o	Selecciona un archivo de audio compatible (ej. WAV, MP3, AAC).
  o	La señal original y su FFT se actualizarán en las gráficas.
3.	Aplicar Filtro
  o	Presiona "Aplicar Filtro".
  o	Se te pedirán tres datos mediante cuadros de diálogo:
   	Tipo de filtro: Escribe low para pasa-bajas, high para pasa-altas o band para pasa-banda.
   	Frecuencia de corte: Por ejemplo, se sugiere 1000 Hz.
   	Orden del filtro: Se sugiere un valor de 4.
  o	Si eliges band, se solicitará una segunda frecuencia (ej. 3400 Hz).
  o	La señal filtrada se dibujará en rojo sobre la señal original, y la FFT se actualizará mostrando ambos conjuntos de datos.
4.	Resetear
  o	Haz clic en "Resetear" para eliminar el filtro aplicado y volver a ver solo la señal original y su FFT.
5.	Guardar Audio Filtrado
  o	Presiona "Guardar" para guardar el audio filtrado en un archivo WAV.
  o	Elige la ruta y el nombre del archivo en el cuadro de diálogo.


Tarea Dos 
Filtro de Kalman (SORT)

 describe las principales matrices y el vector de estado que utiliza el filtro de Kalman en el algoritmo SORT para visión computacional en mi caso solo use 4 dimensiones 

1) Vector de estado (dim_x = 7)
x = [ x, y, s, r, ẋ, ẏ, ṡ ]^T
x, y: centro del bounding box
s   : escala (área = ancho·alto)
r   : relación de aspecto (ancho/alto)
ẋ, ẏ, ṡ: velocidades de x, y y s

2) Matriz de transición F (velocidad constante, r fijo)
F = [
  [1, 0, 0, 0, 1, 0, 0],
  [0, 1, 0, 0, 0, 1, 0],
  [0, 0, 1, 0, 0, 0, 1],
  [0, 0, 0, 1, 0, 0, 0],
  [0, 0, 0, 0, 1, 0, 0],
  [0, 0, 0, 0, 0, 1, 0],
  [0, 0, 0, 0, 0, 0, 1],
]

3) Matriz de observación H (mapea estado [x, y, s, r])
H = [
  [1, 0, 0, 0, 0, 0, 0],
  [0, 1, 0, 0, 0, 0, 0],
  [0, 0, 1, 0, 0, 0, 0],
  [0, 0, 0, 1, 0, 0, 0],
]

4) Inicialización del filtro
kf = KalmanFilter(dim_x=7, dim_z=4)
kf.F = F
kf.H = H

5) Ciclo de tracking por cada frame:
a) Predict:
   kf.predict()
b) Update (si hay detección):
   z = [x, y, s, r]^T  (calculado a partir de [x1,y1,x2,y2])
   kf.update(z)

Video https://drive.google.com/file/d/1ukx_LHkrOedCawWtMnAeKrWE2Luafwyu/view?usp=sharing

Manual de uso de Tarea2KalmanFilter.py

Requisitos:
- Python 3.8+
- GPU con CUDA (opcional pero recomendado)
- Instalar paquetes:
    pip install ultralytics sort numpy opencv-python torch

Archivos necesarios:
- Tarea2KalmanFilter.py
- sort.py (implementación de SORT)
- yolov8m.pt (peso de modelo YOLOv8)
- Video de prueba (modulo_4/Prueba2.mp4)

Pasos de ejecución:
1) Coloca todos los archivos en la misma carpeta.
2) Abre una terminal y navega a esa carpeta.
3) Ejecuta:
       python Tarea2KalmanFilter.py
4) El script lanzara una ventana con el video:
   - Rectángulos verdes = cajas detectadas y trackeadas (ID fijo).
   - Rectángulos amarillos = predicciones futuras del filtro de Kalman.
5) Para salir, presiona la tecla ‘q’ en la ventana de video.

Descripción burda de lo que hace:
El programa usa YOLOv8 para detectar objetos en cada cuadro de un video,  
luego aplica un filtro de Kalman simple (SORT) para seguir cada objeto  
midiendo su posición y velocidad, y muestra tanto las detecciones reales  
como las predicciones que hacen el seguimiento más estable. 
