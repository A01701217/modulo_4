import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

import librosa
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.signal import butter, filtfilt


class AudioProcessor:
    def __init__(self, master):
        master.title("Procesador de Audio - Minimal con Overlay")
        master.geometry("800x600")

        # Variables de audio
        self.audio_data = None
        self.sample_rate = None
        self.filtered_data = None

        # Frame superior con botones
        btn_frame = tk.Frame(master)
        btn_frame.pack(side="top", fill="x", padx=5, pady=5)
        tk.Button(btn_frame, text="Cargar", command=self.load_audio).pack(
            side="left", padx=5
        )
        tk.Button(btn_frame, text="Aplicar Filtro", command=self.apply_filter)
        tk.Button(btn_frame).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Resetear", command=self.reset).pack(
            side="left", padx=5
        )
        tk.Button(btn_frame, text="Guardar", command=self.save_audio).pack(
            side="left", padx=5
        )

        # Etiqueta informativa con sugerencias
        sug = (
            "Sugerencias:\n• Tipo de filtro: low (pasa-bajas), high (pasa-altas) o band (pasa-banda)\n"
            "• Frecuencia de corte recomendada: 300-3400 Hz\n• Orden sugerido: 4"
        )
        tk.Label(master, text=sug, justify="left").pack(side="top", pady=5)

        # Figura para gráfica (dos subgráficas)
        self.fig, (self.ax_wave, self.ax_fft) = plt.subplots(2, 1, figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master)
        self.canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

    def load_audio(self):
        """Carga un archivo de audio y dibuja su señal y FFT."""
        file_path = filedialog.askopenfilename(
            title="Seleccione un archivo de audio",
            filetypes=[
                ("Audio files", "*.wav *.mp3 *.aac"),
                ("Todos los archivos", "*.*"),
            ],
        )
        if file_path:
            try:
                self.audio_data, self.sample_rate = librosa.load(file_path, sr=None)
                self.filtered_data = None  # Se resetea el filtrado previo
                self.update_plots()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{e}")

    def update_plots(self):
        """Dibuja la gráfica de la señal en el tiempo y su FFT, mostrando siempre la original y sobre ella el filtro (si existe)."""
        if self.audio_data is None:
            return

        # Limpia ambas gráficas
        self.ax_wave.clear()
        self.ax_fft.clear()

        # Graficar señal original
        t = np.arange(len(self.audio_data)) / self.sample_rate
        self.ax_wave.plot(t, self.audio_data, label="Original", color="blue")

        # Si existe señal filtrada, superponerla
        if self.filtered_data is not None:
            self.ax_wave.plot(t, self.filtered_data, label="Filtrado", color="red")

        self.ax_wave.set_title("Señal de Audio")
        self.ax_wave.set_xlabel("Tiempo (s)")
        self.ax_wave.set_ylabel("Amplitud")
        self.ax_wave.legend()
        self.ax_wave.grid(True, alpha=0.3)

        # Calcular y graficar FFT de la señal original
        fft_orig = np.fft.fft(self.audio_data)
        freqs_orig = np.fft.fftfreq(len(self.audio_data), 1 / self.sample_rate)
        mask_orig = freqs_orig >= 0
        self.ax_fft.plot(
            freqs_orig[mask_orig],
            np.abs(fft_orig)[mask_orig],
            label="FFT Original",
            color="blue",
        )

        # Si existe filtrado, calcular y graficar su FFT
        if self.filtered_data is not None:
            fft_filt = np.fft.fft(self.filtered_data)
            freqs_filt = np.fft.fftfreq(len(self.filtered_data), 1 / self.sample_rate)
            mask_filt = freqs_filt >= 0
            self.ax_fft.plot(
                freqs_filt[mask_filt],
                np.abs(fft_filt)[mask_filt],
                label="FFT Filtrado",
                color="red",
            )

        self.ax_fft.set_title("Transformada de Fourier (FFT)")
        self.ax_fft.set_xlabel("Frecuencia (Hz)")
        self.ax_fft.set_ylabel("Magnitud")
        self.ax_fft.legend()
        self.ax_fft.grid(True, alpha=0.3)

        self.fig.tight_layout()
        self.canvas.draw()

    def apply_filter(self):
        """
        Solicita parámetros con sugerencias y aplica un filtro Butterworth a la señal.
        Se sobrepone el resultado en la gráfica.
        """
        if self.audio_data is None:
            messagebox.showwarning("Advertencia", "Primero cargue un archivo de audio.")
            return

        # Solicita tipo de filtro (low, high o band)
        filter_type = simpledialog.askstring(
            "Filtro",
            "Ingrese el tipo de filtro:\n- low (Pasa-bajas)\n- high (Pasa-altas)\n- band (Pasa-banda)\nEjemplo: low",
        )
        if not filter_type:
            return

        # Solicitar frecuencia(s) de corte y orden con sugerencia
        cutoff = simpledialog.askfloat(
            "Frecuencia de corte",
            "Ingrese la frecuencia de corte (Hz) [sugerencia: 1000]:",
        )
        order = simpledialog.askinteger(
            "Orden", "Ingrese el orden del filtro [sugerencia: 4]:"
        )
        if cutoff is None or order is None:
            return

        nyquist = self.sample_rate / 2
        try:
            if filter_type.lower() == "band":
                cutoff2 = simpledialog.askfloat(
                    "Frecuencia de corte 2",
                    "Ingrese la segunda frecuencia de corte (Hz) [sugerencia: 3400]:",
                )
                if cutoff2 is None:
                    return
                wn = [min(cutoff, cutoff2) / nyquist, max(cutoff, cutoff2) / nyquist]
            else:
                wn = cutoff / nyquist

            b, a = butter(order, wn, btype=filter_type.lower())
            self.filtered_data = filtfilt(b, a, self.audio_data)
            self.update_plots()
        except Exception as e:
            messagebox.showerror("Error", f"Error al aplicar filtro:\n{e}")

    def reset(self):
        """Elimina el filtro para mostrar únicamente la señal original."""
        if self.audio_data is None:
            return
        self.filtered_data = None
        self.update_plots()

    def save_audio(self):
        """Guarda la señal filtrada en un archivo WAV."""
        if self.filtered_data is None:
            messagebox.showwarning("Advertencia", "No hay audio filtrado para guardar.")
            return
        file_path = filedialog.asksaveasfilename(
            defaultextension=".wav",
            filetypes=[("Archivo WAV", "*.wav")],
            title="Guardar audio filtrado",
        )
        if file_path:
            try:
                sf.write(file_path, self.filtered_data, self.sample_rate)
                messagebox.showinfo("Guardado", "Archivo guardado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = AudioProcessor(root)
    root.mainloop()
