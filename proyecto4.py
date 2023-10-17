import os
from pydub import AudioSegment
import numpy as np
import librosa
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler  # Añade esta línea para importar StandardScaler
from sklearn.cluster import KMeans  # Importa KMeans


def crear_lista_reproduccion(nombre_archivo, canciones):
    """
    Crea un archivo de lista de reproducción M3U.

    :param nombre_archivo: Nombre del archivo M3U (por ejemplo, "mi_lista.m3u").
    :param canciones: Una lista de rutas de archivos de canciones a incluir en la lista de reproducción.
    """
    try:
        with open(nombre_archivo, 'w') as archivo_m3u:
            # Escribir la cabecera del archivo M3U
            archivo_m3u.write("#EXTM3U\n")

            # Agregar cada canción a la lista de reproducción
            for cancion in canciones:
                archivo_m3u.write(f"#EXTINF:0,{cancion}\n")
                archivo_m3u.write(cancion + "\n")
                
        print(f"Lista de reproducción '{nombre_archivo}' creada con éxito.")
    except Exception as e:
        print(f"Error al crear la lista de reproducción: {str(e)}")





# Ruta al archivo de audio (reemplaza con tu propia ruta)
archivo_audio = "darkSide.mp3"  # Cambia a tu archivo WAV o MP3

# Definir la ruta de la carpeta con los archivos de audio
carpeta_audio = "./"

# Obtener una lista de todos los archivos en la carpeta
archivos = os.listdir(carpeta_audio)

# Filtrar la lista para solo mantener archivos MP3 y WAV
archivos_audio = [archivo for archivo in archivos if archivo.endswith('.mp3') or archivo.endswith('.wav') or archivo.endswith('.flac')]


canciones1 = []
canciones2 = []


# Procesar cada archivo de audio
for archivo_audio in archivos_audio:
    print(f"Procesando archivo {archivo_audio}...")

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
    # Convertir el array de audio a punto flotante entre -1 y 1
    forma_onda_bpm = forma_onda / 2**15  # Si tu audio es de 16 bits

    # Calcular el promedio de la forma de onda
    promedio = np.mean(forma_onda)
    # Calcular el tempo (BPM) de la canción
    tempo, _ = librosa.beat.beat_track(y=forma_onda_bpm, sr=frecuencia_hz)

    # Crear un arreglo de tiempo para la gráfica de la forma de onda
    #t = np.linspace(0, duracion_ms / 1000, duracion_ms)
    t = np.linspace(0, duracion_ms / 1000, len(forma_onda))

    # Mostrar información del audio
    print(f"Duración: {duracion_ms} ms")
    print(f"Frecuencia: {frecuencia_hz} Hz")
    print(f"Canales: {canal}")
    print(f"Decibelios (dB): {dB}")
    print(f"Tempo (BPM): {tempo}")
    print(f"Promedio de la forma de onda: {promedio}\n\n")
    if(promedio >= 0.5):
        canciones1.append(os.path.join(carpeta_audio, archivo_audio))
    else:
        canciones2.append(os.path.join(carpeta_audio, archivo_audio))


# Ejemplo de uso:
crear_lista_reproduccion("clasif1.m3u", canciones1)
crear_lista_reproduccion("clasif2.m3u", canciones2)
