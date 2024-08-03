import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv
import os
from openai import OpenAI
load_dotenv()
API_KEY = os.environ['OPENAI_API_KEY']

client = OpenAI(api_key=API_KEY)
# 음성 엔진 초기화
engine = pyttsx3.init()
# 음성 속성 설정 (옵션)
engine.setProperty('rate', 150)  # 음성 속도 (기본값은 200)
engine.setProperty('volume', 1.0)  # 볼륨 (기본값은 1.0, 0.0에서 1.0 사이)

# 음성 인식기 객체 생성
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# respond 함수 정의
def respond(source):  # source를 매개변수로 받아서 사용하도록 수정
    recognizer.adjust_for_ambient_noise(source)
    print("말씀해 주세요...")

    audio = recognizer.listen(source, timeout=10)
    if audio:
        text2 = recognizer.recognize_google(audio, language="ko-KR")
        print(f"인식된 텍스트: {text2}")

        # OpenAI API 호출
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "너는 쓰레기 분리수거 전문가야. 한국어로 설명하고 최대한 한 줄 이내로 설명해줘."},
                {"role": "user", "content": text2}
            ]
        )
        response_content = response.choices[0].message.content  # 수정된 부분
        if response_content:
            engine.say(response_content)
            engine.runAndWait()
            print(response_content)
            print("계속")
            respond(source)  # 수정된 부분
    else:
        request()  # 이 부분은 변경하지 않았습니다.


# request 함수 정의
def request():
    with sr.Microphone() as source:
        print("음성을 입력하세요...")

        recognizer.adjust_for_ambient_noise(source)

        try:
            while True:
                print("듣고 있습니다...")
                audio = recognizer.listen(source)
                
                try:
                    text1 = recognizer.recognize_google(audio, language="ko-KR")
                    print(f"인식된 텍스트: {text1}")

                    if "쓰레기통" in text1:
                        engine.say("네 말씀해주세요.")
                        engine.runAndWait()
                        respond(source)
                
                except sr.UnknownValueError:
                    print("음성을 이해할 수 없습니다.")
                except sr.RequestError as e:
                    print(f"Google Speech Recognition 서비스에 요청할 수 없습니다; {e}")

        except KeyboardInterrupt:
            print("프로그램이 종료되었습니다.")

# 프로그램 시작
request()
