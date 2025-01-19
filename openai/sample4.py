#返答の、。ごとに音声化する。ストリーミングで音声再生する。
import os
import openai
from gtts import gTTS
from pygame import mixer
import time
import queue
import threading

# OpenAI APIキーを設定
openai.api_key = os.getenv("OPENAI_API_KEY")

# 音声再生用のキュー
audio_queue = queue.Queue()

# 音声再生用スレッド関数
def audio_player_thread():
    mixer.init()
    while True:
        audio_file = audio_queue.get()
        if audio_file == "STOP":
            mixer.music.stop()
            mixer.music.unload()
            mixer.quit()
            break
        
        mixer.music.load(audio_file)
        mixer.music.play()
        while mixer.music.get_busy():
            time.sleep(0.1)
        mixer.music.unload()
        os.remove(audio_file)
        audio_queue.task_done()

# テキストを音声に変換する関数
def text_to_speech(text, index):
    if text.strip():
        tts = gTTS(text=text, lang='ja')
        filename = f"temp_{index}.mp3"
        tts.save(filename)
        audio_queue.put(filename)

# テキストを生成する関数
def generate_text(conversation_history):
    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=conversation_history,
        stream=True
    )
    
    full_response = ""
    current_segment = ""
    segment_count = 0
    print("AI: ", end="", flush=True)
    
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            print(content, end="", flush=True)
            current_segment += content
            full_response += content
            
            # 「、」や「。」で区切って音声化
            if "、" in content or "。" in content:
                text_to_speech(current_segment, segment_count)
                segment_count += 1
                current_segment = ""
    
    # 残りのテキストを音声化
    if current_segment:
        text_to_speech(current_segment, segment_count)
    
    print()
    return full_response

# メインの対話ループ
def main():
    # 音声再生用スレッドの開始
    audio_thread = threading.Thread(target=audio_player_thread, daemon=True)
    audio_thread.start()
    
    conversation_history = []
    print("会話を開始します。終了するには '終了' と入力してください。")

    while True:
        user_input = input("あなた: ")
        
        if user_input.lower() == "終了":
            audio_queue.put("STOP")
            print("会話を終了します。")
            break

        conversation_history.append({"role": "user", "content": user_input})
        generated_text = generate_text(conversation_history)
        conversation_history.append({"role": "assistant", "content": generated_text})
        
        # すべての音声再生が終わるまで待機
        audio_queue.join()

if __name__ == "__main__":
    main() 