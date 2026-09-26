import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
import random
import difflib
import re

# -----------------------------------
# CONFIGURACIÓN
# -----------------------------------

duration = 5
sample_rate = 44100

# -----------------------------------
# PALABRAS POR NIVEL
# -----------------------------------

words_by_level = {
    "facil": [
        "gato",
        "perro",
        "manzana",
        "leche",
        "sol"
    ],

    "medio": [
        "banano",
        "escuela",
        "amigo",
        "ventana",
        "amarillo"
    ],

    "dificil": [
        "tecnologia",
        "universidad",
        "informacion",
        "pronunciacion",
        "imaginacion"
    ]
}

# -----------------------------------
# TRADUCCIONES
# -----------------------------------

translations = {
    "gato": "cat",
    "perro": "dog",
    "manzana": "apple",
    "leche": "milk",
    "sol": "sun",

    "banano": "banana",
    "escuela": "school",
    "amigo": "friend",
    "ventana": "window",
    "amarillo": "yellow",

    "tecnologia": "technology",
    "universidad": "university",
    "informacion": "information",
    "pronunciacion": "pronunciation",
    "imaginacion": "imagination"
}

# -----------------------------------
# SELECCIONAR NIVEL
# -----------------------------------

print("-----------------------------------")
print("       PRÁCTICA DE INGLÉS")
print("-----------------------------------")

print("\nSelecciona un nivel:")
print("1. Fácil")
print("2. Medio")
print("3. Difícil")

option = input("\nEscribe 1, 2 o 3: ")

if option == "1":
    level = "facil"

elif option == "2":
    level = "medio"

elif option == "3":
    level = "dificil"

else:
    print("Opción no válida.")
    exit()

# -----------------------------------
# ELEGIR PALABRA DEL NIVEL
# -----------------------------------

target_spanish = random.choice(words_by_level[level])

# Buscar su traducción
target_english = translations[target_spanish]

print("\n-----------------------------------")
print("Nivel:", level.upper())
print("-----------------------------------")

print("\nTu palabra es:")
print("👉", target_spanish)

print("\nAhora di en INGLÉS la traducción de esta palabra.")
print("Tienes", duration, "segundos.")

# -----------------------------------
# GRABAR VOZ
# -----------------------------------

print("\nHabla ahora...")

recording = sd.rec(
    int(duration * sample_rate),
    samplerate=sample_rate,
    channels=1,
    dtype="int16"
)

sd.wait()

wav.write("output.wav", sample_rate, recording)

print("\nGrabación completa.")
print("Comprobando pronunciación...")

# -----------------------------------
# RECONOCIMIENTO DE VOZ
# -----------------------------------

recognizer = sr.Recognizer()

with sr.AudioFile("output.wav") as source:
    audio = recognizer.record(source)

try:

    recognized_text = recognizer.recognize_google(
        audio,
        language="en-US"
    )

    # -----------------------------------
    # LIMPIAR TEXTO
    # -----------------------------------

    recognized = recognized_text.lower().strip()
    target = target_english.lower().strip()

    recognized = re.sub(r"[^\w\s]", "", recognized)
    target = re.sub(r"[^\w\s]", "", target)

    # -----------------------------------
    # COMPARAR
    # -----------------------------------

    similarity = difflib.SequenceMatcher(
        None,
        recognized,
        target
    ).ratio()

    percentage = similarity * 100

    # -----------------------------------
    # RESULTADO
    # -----------------------------------

    print("\n-----------------------------------")
    print("          RESULTADO")
    print("-----------------------------------")

    print("Nivel:", level.upper())
    print("Palabra en español:", target_spanish)
    print("Traducción correcta:", target_english)
    print("Lo que dijiste:", recognized_text)

    print(f"\nCoincidencia: {percentage:.1f}%")

    # -----------------------------------
    # VALIDACIÓN
    # -----------------------------------

    if recognized == target:

        print("\n✓ ¡Excelente!")
        print("La palabra fue reconocida correctamente.")

    elif percentage >= 75:

        print("\n~ ¡Casi perfecto!")
        print("La palabra fue reconocida de forma muy parecida.")

    elif percentage >= 45:

        print("\n⚠ Pronunciación regular.")
        print("Intenta hablar más despacio y vocalizar mejor.")

    else:

        print("\n✗ Pronunciación incorrecta.")
        print("Vuelve a intentarlo.")

    # -----------------------------------
    # RESPUESTA CORRECTA
    # -----------------------------------

    print("\nRespuesta correcta:", target_english)

except sr.UnknownValueError:

    print("\n✗ No se pudo reconocer tu pronunciación.")
    print("Habla más fuerte y claramente.")

except sr.RequestError as e:

    print("\nError con el servicio de reconocimiento:")
    print(e)