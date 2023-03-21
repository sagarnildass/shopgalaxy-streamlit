import streamlit as st
from streamlit_chat import message
import requests
import json
from PIL import Image
import requests
from io import BytesIO
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="Streamlit Chat - Demo",
    page_icon=":robot:",
    layout="wide"
)




API_URL = "https://beam.slai.io/1ck44"
headers = {
  "Accept": "*/*",
  "Accept-Encoding": "gzip, deflate",
  "Authorization": "Basic NWRjMWI2NTQ0YjFjZjEzZmNiMTM3YjM1OTc3YjRmMjE6MzU2NzY5ZGJhM2FiZDhjYjY0MGNhMTJmYzBmY2JjYjE=",
  "Connection": "keep-alive",
  "Content-Type": "application/json"
}


st.header("Shopgalaxy Product Search")

gender = st.radio(
    "Select your gender 👇",
    ["menswear", "womenswear"],
    key="gender"
    )


if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

def query(payload):
    response = requests.request("POST", API_URL, headers=headers, data=json.dumps(payload))
    return response.json()

def clear_text():
    st.session_state["input"] = ""

def get_text():
    input_text = st.text_input("You: ","", key="input")
    return input_text 


user_input = get_text()

if gender:
    payload = {
        "query":{
        "text": user_input,
        "image": None 
        },
        "query_context":'chat',
        "identifier":"Mamon",
        "gender":gender,
        "limit":"10",
        "filters":{
        "sizes": []
        }
      }
    output = query(payload)
    

    st.session_state.past.append(user_input)
    st.session_state.generated.append(output["prompt"])

    images = []
    for pred in output['predictions']:
        #print(pred['metadata']['image'])
        data = requests.get(pred['metadata']['image'])
        img = Image.open(BytesIO(data.content))
        img = img.resize((200, 200))
        images.append(img)
    st.image(images)

    if st.session_state['generated']:


        for i in range(len(st.session_state['generated'])-1, -1, -1):
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')

