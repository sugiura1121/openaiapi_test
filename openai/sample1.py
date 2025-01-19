#テキストでプロンプトを与えるコード
import openai

#以下にapiキーを設定してください
openai.api_key = "your-api-key"

# GPT-3またはGPT-4を使用してテキストを生成する関数
def generate_text(prompt):
    response = openai.chat.completions.create(
        model="gpt-4o",  # または "gpt-4" などのモデル名
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()


# プロンプトを設定
prompt = input("ここにテキストを入力してください:")

# テキストを生成
generated_text = generate_text(prompt)

# 結果を表示
print(generated_text)