import os
from pydub import AudioSegment
from pydub.playback import play
from pydub.utils import mediainfo
import pyloudnorm
import numpy as np
import matplotlib.pyplot as plt

def analyze_audio(file_path):
    audio = AudioSegment.from_file(file_path)
    
    # Obtener información general del archivo de audio
    audio_info = mediainfo(file_path)
    channels = audio.channels
    sample_rate = audio.frame_rate
    duration = len(audio) / 1000.0  # Duración en segundos
    
    print(f"Channels: {channels}")
    print(f"Sample Rate: {sample_rate}")
    print(f"Duration: {duration} seconds")

    # Convertir el objeto AudioSegment a un arreglo numpy de punto flotante
    audio_data = np.array(audio.get_array_of_samples()) / (2 ** 15)  # Normalizar a punto flotante
    
    # Calcular los LUFS
    meter = pyloudnorm.Meter(sample_rate)
    loudness = meter.integrated_loudness(audio_data)
    print(f"Integrated LUFS: {loudness} LUFS")

    # Reproducir el audio
    play(audio)

    # Crear una gráfica de la forma de onda
    plt.figure(figsize=(10, 4))
    plt.title("Forma de Onda")
    plt.plot(audio_data)
    plt.xlabel("Muestra")
    plt.ylabel("Amplitud")
    plt.show()

if __name__ == "__main__":
    file_name = "Period.mp3"  # Nombre del archivo en la misma carpeta
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    analyze_audio(file_path)
