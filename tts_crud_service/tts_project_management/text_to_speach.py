from gtts import gTTS


class GoogleTextToSpeach:
    def __init__(self) -> None:
        pass

    def create_tts(self, slow: bool, text="not given", sequense=1) -> dict:
        """TTS mp3 파일을 생성해서 생성정보를 리턴합니다. 파일 명명규칙 : f"GTTS \"{text}\" {str(sequense).zfill(3)}"""
        tts = gTTS(text=text, slow=slow, lang="ko")

        tts.save(f"audio_outputs/GTTS {text} {str(sequense).zfill(3)}")

        data = {
            "sequense": sequense,
            "name": f'GTTS "{text}" {str(sequense).zfill(3)}',
            # TODO
            "saved_path": "path str",
        }
        return data
