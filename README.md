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
