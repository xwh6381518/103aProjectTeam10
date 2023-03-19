'''
Demo code for interacting with GPT-3 in Python.

To run this you need to 
* first visit openai.com and get an APIkey, 
* which you export into the environment as shown in the shell code below.
* next create a folder and put this file in the folder as gpt.py
* finally run the following commands in that folder

On Mac
% pip3 install openai
% export APIKEY="......."  # in bash
% python3 gpt.py

On Windows:
% pip install openai
% $env:APIKEY="....." # in powershell
% python gpt.py
'''
import openai


class GPT():
    ''' make queries to gpt from a given API '''

    def __init__(self, apikey):
        ''' store the apikey in an instance variable '''
        self.apikey = apikey
        # Set up the OpenAI API client
        openai.api_key = apikey  # os.environ.get('APIKEY')

        # Set up the model and prompt
        self.model_engine = "text-davinci-003"

    def getResponse(self, prompt):
        ''' Generate a GPT response '''
        completion = openai.Completion.create(
            engine=self.model_engine,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.8,
        )

        response = completion.choices[0].text
        return response

    # this method takes in the prompt(local time of a city) and send it to the openAI server
    # and then return the converted eastern time from chatGPT
    def get_eastern_time(self, time):
        completion = openai.Completion.create(
            engine=self.model_engine,
            prompt='convert' + time + 'to eastern time',
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.8,
        )

        eastern_time = completion.choices[0].text
        return eastern_time

    def get_local_temperature(self, location):
        ''' This method will get user input as location, and send
          a prompt to chatgpt sever and return the response from chatgpt.'''
        completion = openai.Completion.create(
            engine=self.model_engine,
            prompt='Get current temperature at ' + location + 'in Celsius degree.',
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.8,
        )
        local_temp = completion.choices[0].text
        return local_temp
    

if __name__ == '__main__':
    '''
    '''
    import os
    g = GPT(os.environ.get("APIKEY"))
    print(g.getResponse("what does openai's GPT stand for?"))
