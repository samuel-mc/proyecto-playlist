from pydub import AudioSegment
import numpy as np
import matplotlib.pyplot as plt

# Ruta al archivo de audio (reemplaza con tu propia ruta)
archivo_audio = "D.Gray-Man Op 1 Innocent Sorro.mp3"  # Cambia a tu archivo WAV o MP3

# Cargar el archivo de audio usando pydub
audio = AudioSegment.from_file(archivo_audio)

# Obtener información sobre el audio
duracion_ms = len(audio)
frecuencia_hz = audio.frame_rate
canal = "Mono" if audio.channels == 1 else "Estéreo"

# Calcular los decibelios (dB)
dB = audio.dBFS


# Obtener la forma de onda del audio
forma_onda = np.array(audio.get_array_of_samples())

# Crear un arreglo de tiempo para la gráfica de la forma de onda
#t = np.linspace(0, duracion_ms / 1000, duracion_ms)
t = np.linspace(0, duracion_ms / 1000, len(forma_onda))

# Mostrar información del audio
print(f"Duración: {duracion_ms} ms")
print(f"Frecuencia: {frecuencia_hz} Hz")
print(f"Canales: {canal}")
print(f"Decibelios (dB): {dB}")


# Crear una gráfica de la forma de onda
plt.figure(figsize=(10, 4))
plt.plot(t, forma_onda)
plt.title("Forma de Onda del Audio")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud")
plt.grid(True)

# Mostrar la gráfica
plt.show()