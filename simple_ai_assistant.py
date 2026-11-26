from openai import OpenAI
from dotenv import load_dotenv
import json
from tools import TOOLS, FUNCTION_NAME_TO_FUNCTION_MAP #module ko .py extension k stth ni likhte
import os
load_dotenv() #looks for .env file by default and loads env variables
client = OpenAI(
    base_url=os.getenv("BASE_URL") ,#taaki local m jo ollama  chl rh h vhn hit ho vran by default oprn ai ka use hojaega
    api_key=os.getenv("API_KEY")#cuz ollma doesnt need api key
)
messages=[]
MAX_STEPS=5
messages.append({"role": "system", "content": "You are a helpful assistant.and you will answer in very short like 1-2 lines "})
while(True):
    user_input=input("\n User: ")
    messages.append({"role": "user", "content": user_input})

  #tool-call-chaining
    for step in range(MAX_STEPS):
       response=client.chat.completions.create(
       model=os.getenv("MODEL"),
       messages=messages ,  
       tools=TOOLS    
       )

   
       msg=response.choices[0].message
       if not msg.tool_calls:
          break 
       messages.append(msg) 
       
       for tool_call in msg.tool_calls:
          func_name=tool_call.function.name
          func_args={}
          try:
             func_args=json.loads(tool_call.function.arguments) 
             fn=FUNCTION_NAME_TO_FUNCTION_MAP[func_name]
             result=fn(**func_args)
          except Exception as e:
             result=f"Error while calling tool {func_name} with arguments {func_args}: {str(e)}"  
        
          messages.append({
            "role":"tool",
            "tool_id":tool_call.id,
            "content":str(result)
          })
    
    else:
       fallback="sorry couldnt complete within step limit"  
       messages.append({
        "role":"assistant",
        "content":fallback
      })
       print("\n Assistant: "+ fallback)
       continue    

    messages.append({
    "role":"assistant",
    "content":msg.content
    })#python m while k bhr access ho skt avariablre so am accessing msg

    print("\n Assistant: "+ msg.content)
    