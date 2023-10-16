from moviepy.editor import AudioFileClip
import matplotlib.pyplot as plt
import numpy as np

def calculate_rms(audio_array):
    return np.sqrt(np.mean(np.square(audio_array)))

def analyze_audio(file_path):
    audio_clip = AudioFileClip(file_path)
    
    # Obtener información del archivo de audio
    channels = audio_clip.reader.nchannels
    sample_rate = audio_clip.fps
    duration = audio_clip.duration
    
    print(f"Channels: {channels}")
    print(f"Sample Rate: {sample_rate}")
    print(f"Duration: {duration} seconds")

    # Crear una gráfica de la forma de onda
    audio_array = audio_clip.to_soundarray(fps=sample_rate, nbytes=2)

    time = np.arange(0, audio_array.shape[0]) / sample_rate

    plt.figure(figsize=(10, 4))
    plt.title("Forma de Onda")
    plt.plot(time, audio_array[:, 0])  # Canal izquierdo
    if channels == 2:
        plt.plot(time, audio_array[:, 1], alpha=0.5)  # Canal derecho si es estéreo
    plt.xlabel("Tiempo (segundos)")
    plt.ylabel("Amplitud")
    plt.show()

    # Calcular los decibeles RMS
    rms = calculate_rms(audio_array)

    print(f"Decibeles RMS: {rms} dB")

if __name__ == "__main__":
    file_path = "Period.mp3"  # Nombre del archivo en la misma carpeta
    analyze_audio(file_path)
