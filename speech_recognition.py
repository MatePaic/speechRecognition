import speech_recognition as sr
import webbrowser as wb  # link za internet
import time  # za sleep koji nam služi da postavimo periodično vrijeme između dva razgovora
import playsound  # da ne ode na druge filove kao npr. iTunes..
import os  # brisenja audia u direktoriju
import random
from gtts import gTTS  # da napravi audiofile Plaea
from time import ctime  # trenutno vrijeme
from configparser import \
    ConfigParser  # za prepoznati API kljuc stranice OpenWheatherMap kojeg smo smjestili u file config.ini
import requests
from googletrans import Translator  # za prevođenje jezika
import datetime  # paket za određivanje sati i minuta pri postavljanju alarma

r = sr.Recognizer()  # inicijaliziramo klasu Recognizer()

while True:

    part = int(input(
        "What type of recognition are you interesting in(audio recorded(1), form microphone(2) or exit program(3)"))
    # dio sa snimljenih zvučnih zapisa
    if part == 1:
        language = input("Language(english, german or croatian): ")
        filename = input("What audio do you want to hear?")
        with sr.AudioFile(filename) as source:
            r.adjust_for_ambient_noise(source, duration=0.1)  # adaptacija za zvuk
            audio_data = r.record(source)
            if language == 'english':
                text = r.recognize_google(audio_data)  # prepoznaje govor u audiu
            elif language == 'german':
                text = r.recognize_google(audio_data, language='de')
            else:
                text = r.recognize_google(audio_data, language='hr')
            file = open('text_file.txt', 'w')
            file.write(text.capitalize())
            file.close()
            print(text.capitalize())  # capitalize je za veliko prvo slovo u recenici
            continue

    # dio sa mikrofona
    elif part == 2:
        def record_audio(ask=False):
            with sr.Microphone() as source:
                if ask:  # ako imamo neko pitanje pokrece se funkcija plaea_speak
                    plaea_speak(ask)
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)  # uzima ono sta govorimo i sprema dok ne dodje tisina
                voice_data = ""  # inicijalizacija varijable
                print("Recognizing Now ....")
                try:
                    if language == "english":
                        voice_data = r.recognize_google(audio)
                        print("Me: " + voice_data.capitalize())
                        if plaea == "no" and recording == "yes":
                            with open("recordedaudio.wav", "wb") as f:  # snimimo ono sto smo rekli u audio file
                                f.write(audio.get_wav_data())
                    elif language == "german":
                        voice_data = r.recognize_google(audio, language="de")
                        print("Ich: " + voice_data.capitalize())
                        if plaea == "nein" and recording == "ja":
                            with open("recordedaudiogerman.wav", "wb") as f:  # snimimo ono sto smo rekli u audio file
                                f.write(audio.get_wav_data())
                    else:
                        voice_data = r.recognize_google(audio, language="hr")
                        print("Ja: " + voice_data.capitalize())
                        if plaea == "ne" and recording == "da":
                            with open("recordedaudiohrv.wav", "wb") as f:  # snimimo ono sto smo rekli u audio file
                                f.write(audio.get_wav_data())

                except sr.UnknownValueError:  # ako se cuje preveliko suskanje ili buka ili nejasne rijeci
                    if language == "english":
                        if plaea == "yes":  # postavili smo uvjet kad zelimo pomoc
                            plaea_speak("Sorry, I did not get that")
                        else:
                            print("Sorry, I did not get that")
                    elif language == "german":
                        if plaea == "ja":
                            plaea_speak_ger("Entschuldigung, ich habe das nicht verstanden")
                        else:
                            print("Entschuldigung, ich habe das nicht verstanden")
                    else:
                        if plaea == "da":  # postavili smo uvjet kad zelimo pomoc
                            plaea_speak_cro("Oprostite nisam razumio")
                        else:
                            print("Oprostite nisam razumio")
                except sr.RequestError:  # ako nema interneta itd..
                    if plaea == "yes":  # ako smo odabrali pomoc od a ona kaze
                        plaea_speak("Sorry, my speech service is down")
                    else:
                        print("Sorry, my speech service is down")  # ako nismo odabrali pomoc od Plaea samo se napise
                return voice_data


        # za prevođenje
        def record_audio_ger(ask=False):
            with sr.Microphone() as source1:
                if ask:  # ako imamo neko pitanje pokrece se funkcija Plaea_speak
                    plaea_speak_ger(ask)
                r.adjust_for_ambient_noise(source1)
                audio1 = r.listen(source1)  # uzima ono sta govorimo i sprema dok ne dodje tisina
                voice_data_ger = ""  # inicijalizacija varijable
                print("Jetzt erkennen ....")
                try:
                    voice_data_ger = r.recognize_google(audio1, language='de')
                    print("Ich: " + voice_data_ger.capitalize())
                    if plaea == "no" and recording == "yes":
                        with open("recordedaudiogerman.wav", "wb") as f:  # snimimo ono sto smo rekli u audio file
                            f.write(audio1.get_wav_data())

                except sr.UnknownValueError:  # ako se cuje preveliko suskanje ili buka ili nejasne rijeci
                    if plaea == "yes":  # postavili smo uvjet kad zelimo pomoc
                        plaea_speak_ger("Entschuldigung, ich habe das nicht verstanden")
                    else:
                        print("Entschuldigung, ich habe das nicht verstanden")
                except sr.RequestError:  # ako nema interneta itd..
                    if plaea == "yes":  # ako smo odabrali pomoc od Plaea ona kaze
                        plaea_speak_ger("Entschuldigung, mein Sprachdienst ist ausgefallen")
                    else:
                        print(
                            "Entschuldigung, mein Sprachdienst ist ausgefallen")  # ako nismo odabrali pomoc od Plaea samo se napise
                return voice_data_ger


        def record_audio_fr(ask=False):
            with sr.Microphone() as source2:
                if ask:  # ako imamo neko pitanje pokrece se funkcija Plaea_speak
                    plaea_speak_fr(ask)
                r.adjust_for_ambient_noise(source2)
                audio2 = r.listen(source2)  # uzima ono sta govorimo i sprema dok ne dodje tisina
                voice_data_fr = ""  # inicijalizacija varijable
                print("Reconnaître maintenant ....")
                try:
                    voice_data_fr = r.recognize_google(audio2, language='fr')
                    print("Moi: " + voice_data_fr.capitalize())
                    if plaea == "no" and recording == "yes":
                        with open("recordedaudiofr.wav", "wb") as f:  # snimimo ono sto smo rekli u audio file
                            f.write(audio2.get_wav_data())

                except sr.UnknownValueError:  # ako se cuje preveliko suskanje ili buka ili nejasne rijeci
                    if plaea == "yes":  # postavili smo uvjet kad zelimo pomoc
                        plaea_speak_fr("Désolé, je n'ai pas compris")
                    else:
                        print("Désolé, je n'ai pas compris")
                except sr.RequestError:  # ako nema interneta itd..
                    if plaea == "yes":  # ako smo odabrali pomoc od Plaea ona kaze
                        plaea_speak_fr("Désolé, mon service vocal est en panne")
                    else:
                        print(
                            "Désolé, mon service vocal est en panne")  # ako nismo odabrali pomoc od Plaea samo se napise
                return voice_data_fr


        def record_audio_cro(ask=False):
            with sr.Microphone() as source3:
                if ask:  # ako imamo neko pitanje pokrece se funkcija plaea_speak
                    plaea_speak_cro(ask)
                r.adjust_for_ambient_noise(source3)
                audio3 = r.listen(source3)  # uzima ono sta govorimo i sprema dok ne dodje tisina
                voice_data_cro = ""  # inicijalizacija varijable
                print("Prepoznaje ....")
                try:
                    voice_data_cro = r.recognize_google(audio3, language='hr')
                    print("Ja: " + voice_data_cro.capitalize())
                    if plaea == "no" and recording == "yes":
                        with open("recordedaudiocro.wav", "wb") as f:  # snimimo ono sto smo rekli u audio file
                            f.write(audio3.get_wav_data())

                except sr.UnknownValueError:  # ako se cuje preveliko suskanje ili buka ili nejasne rijeci
                    if plaea == "yes":  # postavili smo uvjet kad zelimo pomoc
                        plaea_speak_cro("Oprostite, ne razumijem")
                    else:
                        print("Oprostite, ne razumijem")
                except sr.RequestError:  # ako nema interneta itd..
                    if plaea == "yes":  # ako smo odabrali pomoc od plaea ona kaze
                        plaea_speak_cro("Oprostite pao je sustav")
                    else:
                        print("Oprostite pao je sustav")  # ako nismo odabrali pomoc od plaea samo se napise
                return voice_data_cro


        def plaea_speak(audio_string):
            tts = gTTS(text=audio_string, lang="en")  # text to speech varijabla
            r = random.randint(1, 1000000)  # tako da mozemo svakom audiufilu dati random broj
            audio_file = "audio-" + str(r) + ".mp3"  # stvara audio file plaea
            tts.save(audio_file)  # snimamo audio file
            playsound.playsound(audio_file)  # pokrenemo sto prica plaea
            print(audio_string)  # printamo sto kaze plaea
            os.remove(audio_file)  # brisemo audio file u direktoriju


        # za prevođenje
        def plaea_speak_ger(audio_string1):
            tts = gTTS(text=audio_string1, lang="de")
            r = random.randint(1, 1000000)
            audio_file1 = "audioger-" + str(r) + ".mp3"
            tts.save(audio_file1)
            playsound.playsound(audio_file1)
            print(audio_string1)
            os.remove(audio_file1)


        def plaea_speak_fr(audio_string2):
            tts = gTTS(text=audio_string2, lang="fr")
            r = random.randint(1, 1000000)
            audio_file2 = "audiofr-" + str(r) + ".mp3"
            tts.save(audio_file2)
            playsound.playsound(audio_file2)
            print(audio_string2)
            os.remove(audio_file2)


        def plaea_speak_cro(audio_string3):
            tts = gTTS(text=audio_string3, lang="hr")
            r = random.randint(1, 1000000)
            audio_file3 = "audiocro-" + str(r) + ".mp3"
            tts.save(audio_file3)
            playsound.playsound(audio_file3)
            print(audio_string3)
            os.remove(audio_file3)


        def respond(voice_data):  # trazimo pomoc od Plaea
            if language == "english":
                if plaea == "yes":
                    if "hello what is your name" in voice_data:  # ako kazemo nesto od ovih recenima u iducim 6 ifovima plaea prepoznaje i odgovara
                        plaea_speak("Hello. My name is Plaea.")

                    if "what time is it" in voice_data:
                        plaea_speak(ctime())

                    if "search" in voice_data:
                        search = record_audio("What do you want to search for?")
                        url = "http://google.com/search?q=" + search
                        wb.get().open(url)
                        plaea_speak("Here is what I found for " + search)

                    if "find location" in voice_data:
                        location = record_audio("What is the location?")
                        url = "http://google.nl/maps/place/" + location + "/&amp;"
                        wb.get().open(url)
                        plaea_speak("Here is the location of " + location + ".")

                    if "weather" in voice_data:
                        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

                        config_file = 'config.ini'
                        config = ConfigParser()
                        config.read(config_file)
                        api_key = config['api_key']['key']

                        def get_weather(city):
                            result = requests.get(url.format(city, api_key))
                            if result:
                                json = result.json()
                                # (City, Country, temp_celsius, weather)
                                city = json['name']
                                country = json['sys']['country']
                                temp_kelvin = json['main']['temp']
                                temp_celsius = temp_kelvin - 273.15
                                weather = json['weather'][0]['main']
                                final = (city, country, temp_celsius, weather)
                                return final

                            else:
                                return None

                        weather = record_audio("Say the name of city: ")
                        print(get_weather(weather))

                    if "do the math" in voice_data:
                        choose_operation = str(
                            record_audio("Addition(1), subtraction(2), multiplication(3), division(4)"))
                        number1 = int(record_audio("Say the number 1"))
                        number2 = int(record_audio("Say the number 2"))
                        if choose_operation == "addition":
                            result = number1 + number2
                        elif choose_operation == "subtraction":
                            result = number1 - number2
                        elif choose_operation == "multiplication":
                            result = number1 * number2
                        else:
                            result = number1 / number2
                        plaea_speak("The final number is {}".format(result))

                    if "Translate" in voice_data:
                        choose_language = int(input("choose language(1 en to de, 2 de to en, 3 en to hr, 4 hr to en"
                                                    "5 de to hr, 6 hr to de, en to fr, 8 random"))
                        if choose_language == 1:
                            sentence = str(record_audio("say what you want to translate..."))
                            translator = Translator()
                            transleted_sentence = translator.translate(sentence, src='english', dest='german')
                            plaea_speak_ger(transleted_sentence.text)
                        elif choose_language == 2:
                            sentence = str(record_audio_ger("Sagen Sie, was Sie übersetzen möchten..."))
                            translator = Translator()
                            transleted_sentence = translator.translate(sentence, src='german', dest='english')
                            plaea_speak(transleted_sentence.text)
                        elif choose_language == 3:
                            sentence = str(record_audio("say what you want to translate..."))
                            translator = Translator()
                            transleted_sentence = translator.translate(sentence, src='english', dest='croatian')
                            plaea_speak_cro(transleted_sentence.text)
                        elif choose_language == 4:
                            sentence = str(record_audio_cro("Recite što želite prevesti"))
                            translator = Translator()
                            transleted_sentence = translator.translate(sentence, src='hr', dest='en')
                            plaea_speak(transleted_sentence.text)
                        elif choose_language == 5:
                            sentence = str(record_audio_ger("Sagen Sie, was Sie übersetzen möchten..."))
                            translator = Translator()
                            transleted_sentence = translator.translate(sentence, src='de', dest='hr')
                            plaea_speak_cro(transleted_sentence.text)
                        elif choose_language == 6:
                            sentence = str(record_audio_cro("Recite što želite prevesti"))
                            translator = Translator()
                            transleted_sentence = translator.translate(sentence, src='hr', dest='de')
                            plaea_speak_ger(transleted_sentence.text)
                        elif choose_language == 7:
                            sentence = str(record_audio("say what you want to translate"))
                            translator = Translator()
                            transleted_sentence = translator.translate(sentence, src='en', dest='fr')
                            plaea_speak_fr(transleted_sentence.text)
                        else:
                            from_lang = record_audio('From what language')
                            to_lang = record_audio('To what language')
                            sentence = str(input("say what you want to translate"))
                            translator = Translator()
                            transleted_sentence = translator.translate(sentence, src=from_lang, dest=to_lang)
                            print(transleted_sentence.text)

                    if "set alarm" in voice_data:
                        alarmHour = int(input("What hour do you want the alarm to ring"))
                        alarmMinute = int(record_audio("What minute do you want the alarm to ring"))
                        amPm = str(record_audio("am or pm?"))
                        plaea_speak("Waiting for alarm {}h {}min {}".format(alarmHour, alarmMinute, amPm))
                        if (amPm == "afternoon"):
                            alarmHour = alarmHour + 12
                        while (1 == 1):
                            if (alarmHour == datetime.datetime.now().hour and
                                    alarmMinute == datetime.datetime.now().minute):
                                print("Time to wake up")
                                playsound.playsound('Alarm-Clock Sound.mp3')
                                break

                        print("exited")

                    if "exit" in voice_data:
                        exit()


            elif language == "german":
                if "wie heißen sie" in voice_data:
                    plaea_speak_ger("Mein Name ist Plaea")
                if "wie spät ist es" in voice_data:
                    plaea_speak_ger(ctime())
                if "video" in voice_data:
                    video = record_audio_ger("Was willst du sehen?")
                    url = "https://www.youtube.com/results?search_query=" + video
                    wb.get().open(url)
                    plaea_speak_ger("Hier ist, wofür ich gefunden habe " + video + ".")
                if "fertig" in voice_data:
                    exit()


            else:
                if "kako se zoveš" in voice_data:
                    plaea_speak_cro("Moje ime je Plaea")


        # gotove funkcije
        time.sleep(0.3)  # da na terminalu svakih 0.6 dolazi napisano
        language = input("What language do you prefer?: ")
        # ako ocemo pomoc od plaea
        if language == "english":
            plaea = input("Do you need help, maybe?(yes/no)")
            if plaea == "yes":
                plaea_speak("How can I help you?")
                while 0.3:
                    voice_data = record_audio()
                    respond(voice_data)
                    if "thank you bye" in voice_data:  # ako kazemo thank you bye vraca nas na pocetak
                        break
            # ako ne želimo pomoć od plaea
            elif plaea == "no":
                recording = input("Do you want to record what will you say?(yes/no)")
                # ako zelimo da nam snimi sto kazemo
                if recording == "yes":
                    print("Plaease, say something")
                    voice_data = record_audio()
                    print("Audio Recorder Successfully \n")
                # ako ne zelimo da nam snimi sto kazemo
                else:
                    print("Please, say something")
                    while 0.3:
                        voice_data = record_audio()
                        if "leave" in voice_data:  # ako kazemo leave vraca nas na pocetak
                            break
                        if "exit" in voice_data:  # ako kazemo exit gotov program
                            exit()

        elif language == "german":
            plaea = input("Brauchen Sie vielleicht helfen?(ja/nein): ")
            if plaea == "ja":
                plaea_speak_ger("Womit kann ich Ihnen behilflich sein")
                while 0.3:
                    voice_data = record_audio()
                    respond(voice_data)
                    if "danke tschüss" in voice_data:
                        break
            elif plaea == "nein":
                recording = input("Möchten Sie aufzeichnen, was Sie sagen werden? (Ja / Nein)")
                if recording == "ja":
                    print("Bitte, sprechen Sie")
                    voice_data = record_audio()
                    print("Audiorecorder erfolgreich \n")
                # ako ne zelimo da nam snimi sto kazemo
                else:
                    print("Bitte, sprechen Sie")
                    while 0.3:
                        voice_data = record_audio()
                        if "verlassen" in voice_data:
                            break
                        if "fertig" in voice_data:
                            exit()
        else:
            plaea = input("Trebate pomoć(da/ne)")
            if plaea == "da":
                plaea_speak_cro("Kako Vam mogu pomoći")
                while 0.3:
                    voice_data = record_audio()
                    respond(voice_data)
                    if "hvala vidimo se" in voice_data:
                        break
            elif plaea == "ne":
                recording = input("Želite li snimiti što kažete(da/ne)")
                if recording == "da":
                    print("Molim pričajte")
                    voice_data = record_audio()
                    print("Uspješno snimljeno \n")
                # ako ne zelimo da nam snimi sto kazemo
                else:
                    print("Molim pričajte")
                    while 0.3:
                        voice_data = record_audio()
                        if "izađi" in voice_data:
                            break
                        if "gotovo" in voice_data:
                            exit()

    else:  # ako u pocetku ne odredimo 1 ili 2
        break
