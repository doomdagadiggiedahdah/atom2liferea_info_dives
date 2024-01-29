import io
import os
from lxml import etree
import subprocess as sub
from threading import Thread
import urllib, urllib.request
from http.server import HTTPServer, SimpleHTTPRequestHandler
os.chdir("/home/mat/Documents/ProgramExperiments/liferea_bs")

## search queries
topic = ""
while topic == "":
    topic = input("what do you want to learn about?\n").replace(" ", "%20")

num_results = input("how many results do you want? Pressing enter gives 25\n")
if num_results == "":
    num_results = 25

## fun defs
url = f"http://export.arxiv.org/api/query?search_query=all:{topic}&start=0&max_results={num_results}"
running = True # server runs until updated False
data = urllib.request.urlopen(url).read().decode('utf-8')
data = data.split('?>', 1)[-1]
file = "feed.atom"
port = 8000
link = f"http://0.0.0.0:{port}/{file}"

## functions
def xml_val(string):
    try:
        etree.fromstring(string)
        return True
    except etree.XMLSyntaxError as e:
        f"Syntax Error:\n{e}"
        return False

def serve():
    global server
    server = HTTPServer(("0.0.0.0", port), SimpleHTTPRequestHandler)
    while running:
        server.handle_request()

## run it
if xml_val(data):
    with open(file, 'w') as f:
        f.write(data)

    t = Thread(target=serve)
    t.start()
    result = sub.run(["liferea-add-feed", link], capture_output=True, text=True)
    running = False # close server

    # check if liferea accepted
    if result.returncode == 0:
        print("added to feed")
    else:
        print("not added to feed")
else:
    print("bad xml, try again")

# another thing would be getting from multiple sources
