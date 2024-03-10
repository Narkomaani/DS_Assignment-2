import sys
from xmlrpc.server import SimpleXMLRPCServer
import xml.etree.ElementTree as ET

from socketserver import ThreadingMixIn

import random
import time

import requests

# NOTE: 
# sxmlrpc doesen't parse data, so an 
# approach like this where user input is unsanitized
# should not be used in production 
database_location = "db.xml"
database = ET.parse(database_location)
db = database.getroot() # should this be somewhere else?

# class with python ready made multithreaded server
class SimpleThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

# Create server
with SimpleThreadedXMLRPCServer(('localhost', 8000)) as server:
    
    # Registers the XML-RPC introspection functions aka
    # system.listMethods,  system.methodHelp and 
    # system.methodSignature.
    server.register_introspection_functions()

    # Enables MultiCall() method to server
    server.register_multicall_functions()

    @server.register_function
    def wikipediaSearch(search):
        if (type(search) != str):
            raise TypeError("parameter invalid, give the topic as a string")
        

        URL = "https://en.wikipedia.org/w/api.php"
        ARGS = {
                "action": "opensearch",
                "namespace": "0",
                "search": search,
                "limit": "3",
                "format": "xml"
                }
        
        data = ET.fromstring(requests.get(url=URL,params=ARGS).content)

        URLs = []
        for itemElement in data.iterfind("Item"):
            if itemElement.find("Url"):
                URLs.append(itemElement.find("Url").text)

        return URLs

    @server.register_function
    def saveNote(args):
        # 1. see if you can find an existing topic
        #   if not, make a new topic
        # add the note and its data to the topic


        # creating a new note
        noteElement = ET.Element("note", attrib={"name": args["note"]})

        textElement = ET.Element("text")
        textElement.text = args["text"]
        noteElement.append(textElement)
            
        timeElement = ET.Element("time")
        timeElement.text = args["time"]
        noteElement.append(timeElement)
        # URLs = [].__sizeof__
        URLs = wikipediaSearch(args["topic"])
        if URLs.__sizeof__ != 0:
            urlElement = ET.Element("timestamp")
            urlElement.text = URLs
            noteElement.append(urlElement)

        # Check if topic already exists
        for topic in db.iter():
            if topic.get("name") == args["topic"]:
                topic.append(noteElement)
                database.write("db.xml")
                return "Your note has been saved!"
        
        topicElement = ET.Element("topic", attrib={"name": args["topic"]})
        topicElement.append(noteElement)
        db.append(topicElement)

        database.write("db.xml")
        return "A new topic has been created and saved"
    
    @server.register_function
    def loadTopic(topic):
        
        if (type(topic) != str):
            raise TypeError("parameter invalid, give the topic as a string")
        
        for section in db.findall("topic"):
            if section.attrib["name"] == topic:
                return ET.tostring(section, encoding="unicode")
        
        raise LookupError("Unable to find given topic")
    
    @server.register_function
    def sayHi():
        r = random.randint(2, 10)
        print('sleeping {} seconds before return'.format(r))
        time.sleep(r)
        print("The client asked to says hi!")
        return "Server says Hi!"
    
    @server.register_function
    def sleep():
        r = random.randint(2, 10)
        print('sleeping {} seconds'.format(r))
        time.sleep(r)
        return 'slept {} seconds, exiting'.format(r)
    
    @server.register_function
    def argumentti(arg):
        return arg

    # Run the server's main loop
    try:
        print("Server thread started.")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        server.shutdown()
        sys.exit(0)