#ターミナル上でストリームで回答生成
import os
import openai

# OpenAI APIキーを設定
openai.api_key = os.getenv("OPENAI_API_KEY")

# テキストを生成する関数
def generate_text(conversation_history):
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=conversation_history,
        stream=True  # ストリーミングを有効化
    )
    
    full_response = ""
    print("AI: ", end="", flush=True)
    
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            print(content, end="", flush=True)
            full_response += content
    
    print()  # 改行を追加
    return full_response

# メインの対話ループ
conversation_history = []
print("会話を開始します。終了するには '終了' と入力してください。")

while True:
    user_input = input("あなた: ")
    
    if user_input.lower() == "終了":
        print("会話を終了します。")
        break

    conversation_history.append({"role": "user", "content": user_input})
    generated_text = generate_text(conversation_history)
    conversation_history.append({"role": "assistant", "content": generated_text})