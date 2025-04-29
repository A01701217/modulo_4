import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

import librosa
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.signal import butter, filtfilt


class AudioApp:
    def __init__(self, master):
        # Título y tamaño de la ventana
        master.title("Procesador de Audio")
        master.geometry("800x600")

        # Inicializo variables
        self.data = None  # aquí guardo la señal cargada
        self.filtered = None  # aquí guardaré la señal filtrada
        self.fs = None  # frecuencia de muestreo

        # Creo un frame para los botones de acción
        frm = tk.Frame(master)
        frm.pack(padx=5, pady=5, fill="x")
        # Botones
        for txt, cmd in [
            ("Cargar", self.load),
            ("Filtro", self.apply_filter),
            ("Reset", self.reset),
            ("Guardar", self.save),
        ]:
            tk.Button(frm, text=txt, command=cmd).pack(side="left", padx=4)

        # Área para las dos gráficas: tiempo y frecuencia
        self.fig, (self.ax_w, self.ax_f) = plt.subplots(2, 1, figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def load(self):
        # seleccionar archivo de audio, carga con librosa y dibuja la señal original.

        path = filedialog.askopenfilename(
            filetypes=[("Audio", "*.wav *.mp3"), ("Todos", "*.*")]
        )
        if not path:
            return
        try:
            #  devuelve un ndarray y la frecuencia de muestreo
            self.data, self.fs = librosa.load(path, sr=None)
        except Exception as e:
            return messagebox.showerror("Error al cargar", e)

        self.filtered = None  # reinicio cualquier filtrado previo
        self._plot()  # dibujo la señal cargada

    def _plot(self):
        # señal en el dominio del tiempo y su FFT.

        # Tiempo en segundos para el eje x
        t = np.arange(len(self.data)) / self.fs
        # resetear gráfica de tiempo
        self.ax_w.clear()
        if self.filtered is None:
            #  original en azul
            self.ax_w.plot(t, self.data, label="Original", color="blue")
        else:
            # Original abajp y señal filtrada en naranja
            self.ax_w.plot(t, self.data, label="Original", color="blue", alpha=0.5)
            self.ax_w.plot(
                t, self.filtered, label="Filtrado", color="orange", alpha=0.8
            )
        self.ax_w.set(
            title="Señal en el tiempo", xlabel="Tiempo (s)", ylabel="Amplitud"
        )
        self.ax_w.legend()

        # resetear gráfica de frecuencia
        self.ax_f.clear()
        # FFT de la señal original
        X = np.fft.rfft(self.data)
        f = np.fft.rfftfreq(len(self.data), 1 / self.fs)
        self.ax_f.plot(f, np.abs(X), label="FFT Original", color="blue", alpha=0.5)
        # FFT de la señal filtrada
        if self.filtered is not None:
            Y = np.fft.rfft(self.filtered)
            self.ax_f.plot(
                f, np.abs(Y), label="FFT Filtrado", color="orange", alpha=0.8
            )

        self.ax_f.set(title="FFT", xlabel="Frecuencia (Hz)", ylabel="Magnitud")
        self.ax_f.legend()

        # Ajuste de espacios y dibujar
        self.fig.tight_layout()
        self.canvas.draw()

    def apply_filter(self):
        # Pide  tipo de filtro y parámetros, aplica Butterworth.

        if self.data is None:
            return messagebox.showwarning("Aviso", "Primero cargue audio")
        # Tipo de filtro: low, high o band
        tp = simpledialog.askstring("Tipo", "low, high o band:")
        if not tp:
            return
        # Frecuencia de corte y orden
        c1 = simpledialog.askfloat("Corte", "Frecuencia de corte (Hz):")
        o = simpledialog.askinteger("Orden", "Orden del filtro:")
        if None in (c1, o):
            return

        # Normalización para la función butter
        wn = c1 / (self.fs / 2)
        if tp.lower() == "band":
            # Si es banda, pido segunda frecuencia
            c2 = simpledialog.askfloat("Corte 2", "Frecuencia de corte 2 (Hz):")
            if c2 is None:
                return
            wn = sorted([c1, c2])
            wn = [w / (self.fs / 2) for w in wn]

        # Diseño y aplicación del filtro
        b, a = butter(o, wn, btype=tp.lower())
        self.filtered = filtfilt(b, a, self.data)
        self._plot()  # actualizo gráficas

    def reset(self):
        # Vuelve a la señal original sin filtro aplicado.
        if self.data is not None:
            self.filtered = None
            self._plot()

    def save(self):
        # Guarda la señal filtrada en un WAV si está disponible.
        if self.filtered is None:
            return messagebox.showwarning("Aviso", "No hay audio filtrado")
        p = filedialog.asksaveasfilename(defaultextension=".wav")
        if not p:
            return
        try:
            sf.write(p, self.filtered, self.fs)  # guardo el archivo
            messagebox.showinfo("Guardado", "Archivo guardado correctamente")
        except Exception as e:
            messagebox.showerror("Error al guardar", e)


if __name__ == "__main__":
    root = tk.Tk()
    AudioApp(root)
    root.mainloop()
