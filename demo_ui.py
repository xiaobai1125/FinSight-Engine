import streamlit as st
import requests
import json

# 强制使用 localhost 避免代理问题
API_URL = "http://localhost:8000/api/v1/chat"

st.set_page_config(page_title="FinSight Engine", page_icon="🤖")
st.title("🤖 FinSight 企业知识库")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        try:
            # 强制忽略代理
            session = requests.Session()
            session.trust_env = False

            resp = session.post(API_URL, json={"query": prompt, "use_agent": True})
            if resp.status_code == 200:
                data = resp.json()
                ans = data['answer']
                if data['tool_used']:
                    ans += f"\n\n🛠️ **Tool Used:** `{data['tool_used']}`"
                st.write(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})
            else:
                st.error(f"Error: {resp.text}")
        except Exception as e:
            st.error(f"Connection Failed: {e}")