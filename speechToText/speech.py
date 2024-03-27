import speech_recognition as sr

# Initialize the recognizer
r = sr.Recognizer()


def record():
    # Loop in case of error
    while True:
        try:
            # Use the microphone as the source for input
            with sr.Microphone() as mic:
                # Prepare the recognizer to receive input
                r.adjust_for_ambient_noise(mic, duration=0.2)

                # Listen for the user's input
                sound = r.listen(mic)

                # Using Google to recognize audio
                user_text = r.recognize_google(sound)

                return user_text

        except sr.RequestError as e:
            print("Could not request results: {0}".format(e))

        except sr.UnknownValueError:
            print("Unknown error occurred")
        except KeyboardInterrupt:
            print("Program was interrupted by a keyboard action")


def output_text(data):
    with open("output.txt", "a") as f:
        f.write(data + "\n")


while True:
    text = record()
    if text:
        output_text(text)
        print("Wrote text: ", text)