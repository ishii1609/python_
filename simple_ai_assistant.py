from openai import OpenAI
client = OpenAI(
    base_url="http://127.0.0.1:11434/v1" ,#taaki local m jo ollama  chl rh h vhn hit ho vran by default oprn ai ka use hojaega
    api_key="DUMMY_KEY"#cuz ollma doesnt need api key
)
response=client.chat.completions.create(
    model="qwen3:4b",
    messages=[
        {
        "role": "user", 
        "content": "hello llm?"
        }
        ]
)
print(response)