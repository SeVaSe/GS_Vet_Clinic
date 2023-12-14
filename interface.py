import queue
import sounddevice as sd
import vosk
import json
import time


from voiceBot import *

q = queue.Queue()
model = vosk.Model(r"D:\PYTHON_\PROJECT_PYTHON_\otherPY\GS_Vet_Clinic\model_small\vosk-model-small-ru-0.22")

device = sd.default.device
samplerate = int(sd.query_devices(device[0], 'input')['default_samplerate'])

def callback(indata, frames, time, status):
    q.put(bytes(indata))


def main():
    engine = pyttsx3.init()
    speaker("Добрый день! Вы позвонили в ветеринарную клинику 'Маленькие друзья'. Я робот для записи к ветеринару. Какой вопрос вас интересует?")
    engine.runAndWait()

    time.sleep(1)

    with sd.RawInputStream(samplerate=samplerate, blocksize=2000, device=device[0], dtype='int16', channels=1, callback=callback):
        rec = vosk.KaldiRecognizer(model, samplerate)
        start_time = time.time()
        current_time = time.localtime(start_time).tm_hour

        while time.time() - start_time < 7:
            data = q.get()
            if rec.AcceptWaveform(data):
                data = json.loads(rec.Result())['text']
                if "записаться на приём" in data or "хочу записаться на приём" in data or "запишите на приём" in data or\
                    "животное заболело" in data or "запишите к ветеринару" in data:

                    speaker("На данный момент наши врачи очень загружены. Есть только одна запись на прием, завтра в одинадцать утра. Вам подходит такое?")

                    time.sleep(1)
                    start_time2 = time.time()
                    while time.time() - start_time2 < 7:
                        data1 = q.get()
                        if rec.AcceptWaveform(data1):
                            data1 = json.loads(rec.Result())['text']

                            if "запиши на одиннадцать" in data1 or "запиши меня" in data1 or "давай" in data1:
                                speaker(
                                    "Вы записаны на прием, могу я задать вам пару вопросов о питомце? Это нужно, чтобы ветеринар знал, на "
                                    "что обратить внимание на приёме")

                                start_time3 = time.time()
                                while time.time() - start_time3 < 5:
                                    data2 = q.get()
                                    if rec.AcceptWaveform(data2):
                                        data2 = json.loads(rec.Result())['text']
                                        if "задай вопрос" in data2 or "да ты можешь" in data2 or "давай задавай" in data2 or "задавай вопрос" in data2:
                                            speaker("Скажите, какой у вас питомец")

                                            start_time4 = time.time()
                                            while True:
                                                data3 = q.get()
                                                if rec.AcceptWaveform(data3):
                                                    data3 = json.loads(rec.Result())['text']
                                                    if " " not in data3:
                                                        speaker("Какой у вашего животного вес ?")

                                                        time.sleep(3)
                                                        speaker("Спасибо, ваши ответы записаны. Ждем вас в нашей клинике, до свидания!")
                                                        return
                                                else:
                                                    print(rec.PartialResult())
                                        elif "не надо" in data2 or "не хочу" in data2 or "нельзя" in data2:
                                            speaker("Я вас понял. Ждем вас на приеме, до свидания!")
                                            return  # Выход из цикла, можно добавить дополнительные действия при необходимости
                                    else:
                                        print(rec.PartialResult())

                        else:
                            print(rec.PartialResult())

                    speaker("Перезвоните нам позже, как будет хорошая связь")
                    return
                elif "нет ничего не хочу" in data or "нет" in data or "не надо" in data or\
                    "ничего не интересует" in data or "отказ" in data:
                    speaker("Очень жаль, что я не смог вам помочь. Всего доброго, до свидания!")
                    return
                else:
                    speaker("К сожалению, я не могу вам помочь в этом вопросе")

                    if 8 <= current_time <= 22:
                        speaker("Перевожу на оператора")
                    else:
                        speaker("Отдел технической поддержки работает с 8 утра до 10 вечера, я не могу вас перевести на оператора. Позвоните нам в рабочее время!")
                    return
            else:
                print(rec.PartialResult())

        speaker("Не услышал вашего ответа. Перезвоните позже, когда будет время")

if __name__ == '__main__':
    main()
