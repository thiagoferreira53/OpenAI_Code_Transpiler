import os
import openai
import argparse
from datetime import datetime

import time
start_time = time.time()

#openai.api_key = os.getenv("OPENAI_API_KEY")
my_key = "put_your_key_here"

parser = argparse.ArgumentParser(description="Request")

parser.add_argument("-frm", help="inform the language the script is written in", type=str)
parser.add_argument("-to", help="inform the language the script should be translated to", type=str)
parser.add_argument("-request", help="inform the script you want to be translated", type=str)
parser.add_argument("-o", help="optimize the code", action='store_true')

args = parser.parse_args()

with open(args.request) as f:
    content = f.readlines()

openai.api_key = my_key
if(args.o):
    request = "#### Translate and optimize the " + args.frm + " code into " + args.to + "\n### " + \
            args.frm + "\n\n"+ ''.join(content) + "\n\n### " + args.to
else:
  request = "#### Translate the " + args.frm + " code into " + args.to + "\n### " + \
            args.frm + "\n\n"+ ''.join(content) + "\n\n### " + args.to

print(request)

response = openai.Completion.create(
  model="code-davinci-002",
  prompt=str(request),
  temperature=0,
  max_tokens=2000,
  top_p=0.8,
  frequency_penalty=0.1,
  presence_penalty=0.5,
  stop=["###"]
)

print("##########OPENAI API RESPONSE##########")
print(response)
print("#######################################")



with open("translated_code.txt", 'w') as file:
    file.write("ID: " + response.id + "\nModel: "+response.model + \
               "\nExecuton Time: " + str(round(time.time() - start_time, 2))+" seconds")
    file.write("\nPrompt Tokens: " + str(response.usage.prompt_tokens)+ \
               "\nResponse Tokens: " + str(response.usage.completion_tokens) + \
               "\nTotal Tokens: " + str(response.usage.completion_tokens))
    file.write("\nRESULT: " + response.choices[0].text)
    
