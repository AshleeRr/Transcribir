# aqui manejamos la carga del audio y la transcripcion
# se usa el framework flask para crear la app web
# se usa la libreria SpeechRecognition para la transcripcion de audio a texto
from flask import Flask, request, render_template
import speech_recognition as sr

app = Flask(__name__) #Crea la app con el frameowrk flask

@app.route("/", methods=["GET", "POST"]) # Ruta principal
def index():
    transcription = "" # aqui se almancena la transcripcion
    if request.method == "POST": #verifica que el usuario mando el archivi
        audio_file = request.files["audio"]
        audio_file.save("audio.wav")  # Guarda el archivo subido

        recognizer = sr.Recognizer() # inicializa el reconocedor de voz
        try:
            with sr.AudioFile("audio.wav") as source: # carga el audio
                audio_data = recognizer.record(source)
                transcription = recognizer.recognize_google(audio_data, language="es-ES") #se selecciona el iddioma y manda el audio a google

                #manejo de errores
        except sr.UnknownValueError:
            transcription = "No se pudo entender el audio."
        except sr.RequestError:
            transcription = "Error al conectar con el servicio de Google."
    # para mostrar la transcripcion en la pagina
    # renderiza el template index.html y le pasa la transcripcion
    return render_template("index.html", transcription=transcription)

if __name__ == "__main__":
    app.run(debug=True)
