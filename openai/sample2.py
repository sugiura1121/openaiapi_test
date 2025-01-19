#プロンプトとしてテキストファイルを用いたい人用
import os
import openai

# OpenAI APIキーを設定
openai.api_key = os.getenv("OPENAI_API_KEY")

# テキストファイルを読み込む関数
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# テキストを生成する関数
def generate_text(conversation_history):
    response = openai.chat.completions.create(
        model = "gpt-4o",
        messages = conversation_history
    )
    return response.choices[0].message.content.strip()

# テキストファイルを読み込む
file_path = "/Users/sugiura/Documents/ai_assistant/openai/prompt.txt"  # ここに実際のファイルパスを指定
text_content = read_text_file(file_path)

# 会話履歴の初期化（テキストファイルの内容を含める）
conversation_history = [
    {"role": "system", "content": "あなたは優秀なAIです。以下のテキストの内容に基づいて回答してください：\n\n" + text_content}
]

# メインループ
while True:
    user_input = input("You:")
    if user_input.lower() == "exit":
        print("会話を終了します。")
        break

    conversation_history.append({"role": "user", "content": user_input})
    generated_text = generate_text(conversation_history)
    conversation_history.append({"role": "assistant", "content": generated_text})

    print("AI:" + generated_text)