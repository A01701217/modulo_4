import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from scipy.signal import butter, filtfilt
import librosa
import soundfile as sf
from scipy import signal

class AudioProcessor:
    def __init__(self, master):
        master.title("Procesador de Audio - Minimal")
        master.geometry("800x600")

        # Variables para almacenar datos de audio
        self.audio_data = None
        self.sample_rate = None
        self.filtered_data = None

        # Frame superior con botones
        btn_frame = tk.Frame(master)
        btn_frame.pack(side="top", fill="x", padx=5, pady=5)
        tk.Button(btn_frame, text="Cargar", command=self.load_audio).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Aplicar Filtro", command=self.apply_filter).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Resetear", command=self.reset).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Guardar", command=self.save_audio).pack(side="left", padx=5)

        # Figura para la gráfica de la señal y la FFT (dos subgráficas)
        self.fig, (self.ax_wave, self.ax_fft) = plt.subplots(2, 1, figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master)
        self.canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

    def load_audio(self):
        """Carga un archivo de audio y dibuja la señal original junto con su FFT."""
        file_path = filedialog.askopenfilename(
            title="Seleccione un archivo de audio", 
            filetypes=[("Audio files", "*.wav *.mp3 *.aac"), ("Todos los archivos", "*.*")]
        )
        if file_path:
            try:
                self.audio_data, self.sample_rate = librosa.load(file_path, sr=None)
                self.filtered_data = None  # Reinicia cualquier filtrado previo
                self.plot_audio(self.audio_data, "Señal Original")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{e}")

    def plot_audio(self, data, title_wave):
        """Dibuja la señal en el tiempo y su FFT en la misma figura."""
        self.ax_wave.clear()
        self.ax_fft.clear()

        # Señal en el dominio del tiempo
        t = np.arange(len(data)) / self.sample_rate
        self.ax_wave.plot(t, data)
        self.ax_wave.set_title(title_wave)
        self.ax_wave.set_xlabel("Tiempo (s)")
        self.ax_wave.set_ylabel("Amplitud")

        # Cálculo y gráfica de la FFT (solo frecuencias positivas)
        fft_vals = np.fft.fft(data)
        freqs = np.fft.fftfreq(len(data), 1/self.sample_rate)
        mask = freqs >= 0
        self.ax_fft.plot(freqs[mask], np.abs(fft_vals)[mask])
        self.ax_fft.set_title("FFT")
        self.ax_fft.set_xlabel("Frecuencia (Hz)")
        self.ax_fft.set_ylabel("Magnitud")

        self.fig.tight_layout()
        self.canvas.draw()

    def apply_filter(self):
        """
        Pide los parámetros del filtro y aplica un filtro Butterworth
        a la señal cargada.
        """
        if self.audio_data is None:
            messagebox.showwarning("Advertencia", "Primero cargue un archivo de audio.")
            return

        # Solicitar al usuario el tipo de filtro: low, high o band
        filter_type = simpledialog.askstring("Filtro", "Tipo de Filtro (low, high, band):")
        if not filter_type:
            return

        # Solicitar la frecuencia de corte (en Hz) y el orden del filtro
        cutoff = simpledialog.askfloat("Frecuencia de corte", "Frecuencia de corte (Hz):")
        order = simpledialog.askinteger("Orden", "Orden del filtro:")
        if cutoff is None or order is None:
            return

        nyquist = self.sample_rate / 2
        try:
            if filter_type.lower() == 'band':
                # Para un filtro de banda se solicitan dos frecuencias de corte
                cutoff2 = simpledialog.askfloat("Frecuencia de corte 2", "Frecuencia de corte 2 (Hz):")
                if cutoff2 is None:
                    return
                wn = [min(cutoff, cutoff2)/nyquist, max(cutoff, cutoff2)/nyquist]
            else:
                wn = cutoff / nyquist

            b, a = butter(order, wn, btype=filter_type.lower())
            self.filtered_data = filtfilt(b, a, self.audio_data)
            self.plot_audio(self.filtered_data, f"Señal Filtrada ({filter_type})")
        except Exception as e:
            messagebox.showerror("Error", f"Error al aplicar filtro:\n{e}")

    def reset(self):
        """Vuelve a mostrar la señal original y elimina el filtrado."""
        if self.audio_data is None:
            return
        self.filtered_data = None
        self.plot_audio(self.audio_data, "Señal Original")

    def save_audio(self):
        """Guarda la señal filtrada en un archivo WAV."""
        if self.filtered_data is None:
            messagebox.showwarning("Advertencia", "No hay audio filtrado para guardar.")
            return
        file_path = filedialog.asksaveasfilename(
            defaultextension=".wav",
            filetypes=[("Archivo WAV", "*.wav")],
            title="Guardar audio filtrado"
        )
        if file_path:
            try:
                sf.write(file_path, self.filtered_data, self.sample_rate)
                messagebox.showinfo("Guardado", "Archivo guardado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")

if __name__ == '__main__':
    root = tk.Tk()
    app = AudioProcessor(root)
    root.mainloop()
