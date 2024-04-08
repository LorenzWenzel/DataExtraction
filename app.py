import asyncio
import os
from flask import Flask
from main import main
import logging

# if os.name == 'nt':
#     # Setze das Event-Loop-Policy für Windows
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

def sync_main():
    return asyncio.run(main())

#Setzt eine Route/API auf 0.0.0.0, die main asynchron ausführt. 
@app.route('/')
def hello():
    #return sync_main()
    return main()

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
