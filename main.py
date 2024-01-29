import os
import subprocess as sub
from http.server import HTTPServer, SimpleHTTPRequestHandler
from threading import Thread
import urllib, urllib.request
from lxml import etree
import io

os.chdir("/home/mat/Documents/ProgramExperiments/liferea_bs")
url = 'http://export.arxiv.org/api/query?search_query=all:electron&start=0&max_results=1'
data = urllib.request.urlopen(url).read().decode('utf-8')
data = data.split('?>', 1)[-1]

RUNNING = True
PORT = 8000
FILE = "test.atom"

def xml_val(string):
    try:
        etree.parse(io.StringIO(string))
        return "xml is good"
    except etree.XMLSyntaxError as e:
        return f"Syntax Error:\n{e}"

print(xml_val(data))

with open('test.atom', 'w') as f:
    f.write(data)

# call the arxiv api to get the feed and store that locally
# put that file as the link

def serve():
    global server
    server = HTTPServer(("0.0.0.0", PORT), SimpleHTTPRequestHandler)
    while RUNNING:
        server.handle_request()

t = Thread(target=serve)
t.start()

link = f"http://0.0.0.0:{PORT}/{FILE}"
result = sub.run(["liferea-add-feed", link], capture_output=True, text=True)


# tur off server
RUNNING = False

print(f"output: {result.stdout}")

if result.returncode == 0:
    print("all good")
else:
    print("didn't work")
