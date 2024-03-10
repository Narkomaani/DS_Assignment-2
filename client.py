import xmlrpc.client
import datetime
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed


server = xmlrpc.client.ServerProxy("http://localhost:8000", allow_none=True)

# A method to extract xml from server return and print it nicely
def printTopic(xml):
    topic = ET.fromstring(xml)
    print("Notes for " + topic.get("name"))
    for note in topic.findall("note"):
        print("Note:", note.get("name"))
        for element in note.findall("text"):
            print(element.text, end="")
        for element in note.findall("timestamp"):
            print(element.text)

    return

# get topic from db and parse it
def getTopic(): 
    try:
        topic = str(input("Give the name of the topic:\n"))
    except:
        print("error with given input, try again.")
        return

    try: 
        print("Waiting for server reply...")
        topic = server.loadTopic(topic)
        printTopic(topic)
        
    except xmlrpc.client.Fault as e:
        print("A fault occurred")
        print("Fault code: %d" % e.faultCode)
        print("Fault string: %s" % e.faultString)
        return
    except Exception as e:
        print("Server error:", e)
        return

    return

# sends a request with user input args
def saveNewTopic():

    try:
        topic = str(input("Give the topic of the note:\n"))
        note = str(input("Give the name for your note:\n"))
        text = str(input("Give the text of the note:\n"))
        timestamp = datetime.datetime.now().strftime("%m/%d/%y - %H:%M:%S")
    except:
        print("error with given input, try again.")
        return

    args = {"topic": topic, 
           "note": note, 
           "text": text, 
           "time": timestamp
           }

    try: 
        
        print(server.saveNote(args))
    except xmlrpc.client.Error as e:
        print("Server error:", e)
        pass
    except Exception as e:
        print("Client error:", e)
        pass
    return

def sayHI():
    return server.sayHi()

def ThreadingTestaus():
    with ThreadPoolExecutor() as executor:
        sayHi = {executor.submit(sayHI) for _ in range(4)}
        for future in as_completed(sayHi):
            sleep_time = future.result()
            print(sleep_time)

    return

def listMethods():
    try: 
        print(server.system.listMethods)
    except xmlrpc.client.Error as e:
        print("Server error:", e)
        pass
    except Exception as e:
        print("Client error:", e)
        pass
    return

def valikko():
    print("""Select one:
        1) load a topic
        2) save a new note
        3) List every method
        4) Thread test
        0) exit the program
        """)
    try:
        valinta = int(input(""))
    except Exception as e:
        return -1
    return valinta 

def main():
    valinta = 1

    print("Welcome to my Notebook software\nMade by Jeremias Wahlsten")
    
    # Menu loop
    while valinta != 0:
        valinta = valikko()

        if valinta == 1:
            getTopic()
        elif valinta == 2:
            saveNewTopic()
        elif valinta == 3:
            listMethods()
        elif valinta == 4:
            ThreadingTestaus()
        elif valinta == 0:
            continue
        else:
            print("unknown input, try again")
    
    print("Exiting software...")
    return

main()