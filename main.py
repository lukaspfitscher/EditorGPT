import time
import openai
import sys

openai.api_key = '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'
conversation = []
first_response = True
response = ''
filename = sys.argv[1]
last_two_chars = ''

while True:
 with open(filename,'rb') as file:
  try:file.seek(-2,2)
  except: pass
  last_two_chars = file.read()

 if(last_two_chars == b'pl'):

  #remove 'lp'
  with open(filename, 'rb+') as file:
   file.seek(-2, 2)
   file.truncate()

  #read last 4000 signs
  with open(filename,'r') as f:
    f.seek(0,2) 
    end_pos = f.tell() 
    f.seek(max(0,end_pos-4000)) 
    prompt = f.read()

  print('\033[2;36;40m'+'waiting for response'+'\033[0m')
  conversation.append({'role':'user','content':prompt})
  for api_response in openai.ChatCompletion.create(
     model='gpt-3.5-turbo',
     messages=conversation,
     stream = True):

   #first streaming response contains no content just the role
   if api_response["choices"][0]["finish_reason"] == "stop":
    print('\033[2;35;40m'+'finished'+'\033[0m'+'\n',end = '')
    break
   elif first_response == True:
    first_response = False
    conversation.append({'role':'assistant','content':''})
    with open(filename, 'a') as file:
     file.write('\n\n')
    #removes the 'waiting for response' and replace it with 'GPT' fancy!
    sys.stdout.write("\033[F") # Move cursor up one line
    sys.stdout.write("\033[K") # Clear to the end of the line
    print('\033[2;33;40m'+'gpt is responding in file'+'\033[0m'+'\n',end = '')

   else:
    snip = api_response["choices"][0]["delta"]["content"]

    with open(filename, 'a') as file:
     file.write(snip)

    #print(snip,end = '')
    conversation[-1]['content'] += snip
  first_response = True
 time.sleep(0.2)
