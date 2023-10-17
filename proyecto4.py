import os
from pydub import AudioSegment
import numpy as np
import librosa
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler  # Añade esta línea para importar StandardScaler
from sklearn.cluster import KMeans  # Importa KMeans


def crear_lista_reproduccion(nombre_archivo, canciones):
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



#Ruta de la carpeta con los archivos de audio
carpeta_audio = "./"

# Obtener una lista de todos los archivos en la carpeta
archivos = os.listdir(carpeta_audio)

# Filtrar la lista para solo mantener archivos MP3, WAV y FLAC
archivos_audio = [archivo for archivo in archivos if archivo.endswith('.mp3') or archivo.endswith('.wav') or archivo.endswith('.flac')]

#Creamos 1 array para cada clasificacion
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

    ########### GRAFICAR
    ''''''
    # Crear un arreglo de tiempo para la gráfica de la forma de onda
    #t = np.linspace(0, duracion_ms / 1000, duracion_ms)
    t = np.linspace(0, duracion_ms / 1000, len(forma_onda))
    # Crear una gráfica de la forma de onda
    plt.figure(figsize=(10, 4))
    plt.plot(t, forma_onda)
    plt.title("Forma de Onda del Audio")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud")
    plt.grid(True)

    # Mostrar la gráfica
    plt.show()
    ''''''



# Ejemplo de uso:
crear_lista_reproduccion("clasif1.m3u", canciones1)
crear_lista_reproduccion("clasif2.m3u", canciones2)


def intentoClasificacion():
    # Clasificación básica de sentimiento basada en tempo
    X = np.array([dB]).reshape(-1, 1)  # Añade esta línea para ajustar la forma de X
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    kmeans = KMeans(n_clusters=1, n_init=10)  # Puedes ajustar el número de clusters
    kmeans.fit(X)
    labels = kmeans.predict(X)

    # Mostrar el sentimiento basado en el cluster
    sentimientos = {0: "Feliz", 1: "Triste", 2: "Neutro"}  # Puedes ajustar las etiquetas
    sentimiento_predicho = sentimientos[np.argmax(np.bincount(labels))]

    print(f"Sentimiento: {sentimiento_predicho}")
