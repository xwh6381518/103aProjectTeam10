'''
gptwebapp shows how to create a web app which ask the user for a prompt
and then sends it to openai's GPT API to get a response. You can use this
as your own GPT interface and not have to go through openai's web pages.

We assume that the APIKEY has been put into the shell environment.
Run this server as follows:

On Mac
% pip3 install openai
% pip3 install flask
% export APIKEY="......."  # in bash
% python3 gptwebapp.py

On Windows:
% pip install openai
% pip install flask
% $env:APIKEY="....." # in powershell
% python gptwebapp.py
'''
from flask import request, redirect, url_for, Flask
from gpt import GPT
import os

app = Flask(__name__)
gptAPI = GPT(os.environ.get('APIKEY'))

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q789789uioujkkljkl...8z\n\xec]/'


@app.route('/')
def index():
    ''' display a link to the general query page '''
    print('processing / route')
    return f'''
        <body bgcolor="#ffffe0">
        <h1>Team 10 CA01</h1> 
        <h2><a href="/about">About</a></h2>
        <h2><a href="/team">Team 10</a></h2>
        <br/><br/>
        <h2>GPT Demo</h2>
        <a href="/gptdemo">Ask questions to GPT</a><br/><br/>
        <h2>Wenhao Xie</h2>
        <a href="/time">Convert time of any city in the world to eastern time GPT</a>
        <br/><br/>
        <h2>Zhihan Li</h2>
        <a href="/temp"> Get local temperature from ChatGPT.</a>
        <br/><br/>
        <h2>Barry Wen</h2>
        <a href="/currency">Convert a currency to another</a>
        <br/><br/>
        </body>
    '''


@app.route('/gptdemo', methods=['GET', 'POST'])
def gptdemo():
    ''' handle a get request by sending a form 
        and a post request by returning the GPT response
    '''
    if request.method == 'POST':
        prompt = request.form['prompt']
        answer = gptAPI.getResponse(prompt)
        return f'''
        <h1>GPT Demo</h1>
        <pre style="bgcolor:yellow">{prompt}</pre>
        <hr>
        Here is the answer in text mode:
        <div style="border:thin solid black">{answer}</div>
        Here is the answer in "pre" mode:
        <pre style="border:thin solid black">{answer}</pre>
        <a href={url_for('gptdemo')}> make another query</a>
        '''
    else:
        return '''
        <h1>GPT Demo App</h1>
        Enter your query below
        <form method="post">
            <textarea name="prompt"></textarea>
            <p><input type=submit value="get response">
        </form>
        '''


@app.route('/time', methods=['GET', 'POST'])
def time():
    ''' handle a get request by sending a form 
        and a post request by returning the GPT response
    '''
    if request.method == 'POST':
        prompt = request.form['prompt']
        answer = gptAPI.get_eastern_time(prompt)
        return f'''
        <h2>Convert Time</h2>
        <pre style="bgcolor:yellow">{prompt}</pre>
        <hr>
        Here is the answer in text mode:
        <div style="border:thin solid black">{answer}</div>
        Here is the answer in "pre" mode:
        <pre style="border:thin solid black">{answer}</pre>
        <a href={url_for('time')}> Try another city</a>
        '''
    else:
        return '''
        <h2>Time Convert App</h2>
        <p div style=font-size:22px>
        Please enter your local time below(e.g. Tokyo 8am Friday)
        </p>
        <form method="post">
            <textarea name="prompt"></textarea>
            <p><input type=submit value="get response">
        </form>
        <br/><br/><a href="/">Back</a>
        '''


@app.route('/temp', methods=['GET', 'POST'])
def temp():
    ''' handle a get request by sending a form 
        and a post request by returning the GPT response
    '''
    if request.method == 'POST':
        prompt = request.form['prompt']
        answer = gptAPI.get_local_temperature(prompt)
        return f'''
        <body bgcolor="#F0FFF0">
        <h2>Get current temperature of entered location</h2>
        <pre style="bgcolor:yellow;font-size:20px">{prompt}</pre>
        <p div style=font-size:22px>
        Here is the answer from ChatGPT:
        </p>
        <div style="border:thin solid black;font-size:20px">{answer}</div>
        <a href={url_for('temp')}> Try another city</a>
        </body>
        '''
    else:
        return '''
        <body bgcolor="#F0FFF0">
        <h2>Local Temperature App</h2>
        <p div style=font-size:22px>
        Please enter a location/city where you want to know it current temperature: (e.g. Waltham)
        </p>
        <form method="post">
            <textarea name="prompt"></textarea>
            <p><input type=submit value="get response">
        </form>     
        <br/><br/><a href="/">Back</a>
        </body>
        '''


@app.route('/currency', methods=['GET', 'POST'])
def currency():
    ''' handle a get request by sending a form 
        and a post request by returning the GPT response
    '''
    if request.method == 'POST':
        from_currency = request.form['from']
        amount = request.form['amount']
        to_currency = request.form['to']
        answer = gptAPI.currency_convertor(from_currency, amount, to_currency)
        return f'''
        <h1>Currency Convertor</h1>
        <pre style="bgcolor:yellow">{answer}</pre>
        <hr>
        Here is the answer in text mode:
        <div style="border:thin solid black">{answer}</div>
        Here is the answer in "pre" mode:
        <pre style="border:thin solid black">{answer}</pre>
        <a href={url_for('currency')}>Try another currency</a>
        '''
    else:
        return '''
        <h1>Currency Convertor</h1>
        <p div style=font-size:20px>
        Enter your query below
        </p>
        <form method="post">
            <textarea name="from">From currency: </textarea>
            <textarea name="amount">Amount: </textarea>
            <textarea name="to">To currency: </textarea>
            <p><input type=submit value="get response">
        </form>
        <br/><br/><a href="/">Back</a>
        '''


@app.route('/about')
def about():
    return '''
    <body bgcolor="#C1EEC1">
    <h1> This is the first creative assignment webpage of CS103A Spring Team 10.</h1>
    <h2> Our team created three methods for users to interact with gpt.</h2>
    <br/><br/>
    <h2> Wenhao Xie </h2>
    <p div style=font-size:22px> I added a method get_eastern_time(time), which accept a string of time 'e.g. Tokyo 8am Friday', 
     and ask chatgpt to convert it to eastern time.</p>

    <h2> Zhihan Li </h2>
    <p div style=font-size:22px> I added a method called get_local_temperature(location). It take user input string as location 'e.g. Columbus',
    and ask chatgpt the current temperatuer of this location.</p>

    <h2> Barry Wen </h2>
    <p div style=font-size:22px> I added a method called currency_convertor(from_currency, amount, to_currency). 
    It takes three user inputs to help user convert the currency to another one by chatGPT.</p>

    <br/><br/><a href="/">Back</a>
    </body>
    '''


@app.route('/team')
def team():
    return '''
    <body bgcolor="#f3f3f3">
    <h1> CS103A Team 10</h>
    <br/><br/>

    <h2> Wenhao Xie </h2>
    <p div style=font-size:22px> 1st year MS4 student from China. I am the captain of the team and I wrote the /time page
    as well as my parts in /about and team page</p> 

    <h2> Zhihan Li </h2>
    <p div style=font-size:22px> 1st year MS3 student. I made the /temp page and 
    I wrote the short introduction on both /about and /team page.</p>

    <h2> Barry Wen </h2>
    <p div style=font-size:22px> 1st year MS4 student. BS in Real Estate and MS in Computer Science. I am a member of Team 10. 
    I wrote the /currency page and my part in /about and /team page.</p>
    
    <br/><br/><a href="/">Back</a>
    </body>
    '''


if __name__ == '__main__':
    # run the code on port 5001, MacOS uses port 5000 for its own service :(
    app.run(debug=True, port=5001)
