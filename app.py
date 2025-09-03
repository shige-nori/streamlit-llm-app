import streamlit as st
st.title("ジャンル別専門家チャットボット")
st.divider()
st.write("専門家のジャンルを選択し、その分野に関する質問をしてください。")

selected_item = st.radio(
    "動作モードを選択してください。",
    ["健康", "歴史"]
)
st.divider()

if selected_item == "健康":
    # システムメッセージの作成
    system_message = {
    "role": "system",
    "content": """あなたは健康の専門家です。
                ユーザーからの質問に100文字以内で回答してください。
                健康以外の質問の場合は、専門外ですと返答してください"""
    }
    user_message = st.text_input(label="健康に関する質問を入力してください。")
    
elif selected_item == "歴史":
    # システムメッセージの作成
    system_message = {
    "role": "system",
    "content": """あなたは歴史の専門家です。
                ユーザーからの質問に100文字以内で回答してください。
                歴史以外の質問の場合は、専門外ですと返答してください"""
    }
    user_message = st.text_input(label="歴史に関する質問を入力してください。")

if st.button("実行"):
    # 入力チェック
    if not user_message:
        st.error("質問内容を入力してください。")
    else:
        st.divider()

        from openai import OpenAI
        # 環境変数OPENAI_API_KEYを読み込む(ローカル用)
        # from dotenv import load_dotenv
        # load_dotenv()

        # OpenAIクライアントの初期化(ローカル用)
        # client = OpenAI(timeout=10.0)
        
        # StreamlitのSecretsからAPIキーを読み込む
        api_key = st.secrets["OPENAI_API_KEY"]

        # 読み込んだAPIキーを使ってクライアントを初期化
        client = OpenAI(api_key=api_key)

        # ユーザーメッセージの作成
        question_message = {
            "role": "user",
            "content": user_message
        }

        # OpenAI APIへリクエストを送信し、回答を取得（例外処理付き）
        try:
            first_completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    system_message,
                    question_message
                ],
                temperature=0.5
            )
            # 回答を表示
            response = first_completion.choices[0].message.content
            st.write(f"回答: {response}")
        except Exception as e:
            st.error(f"APIリクエスト中にエラーが発生しました: {e}")