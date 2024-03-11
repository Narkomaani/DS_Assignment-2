# Distributed System - Assignment 2 By Jeremias Wahlsten
# 
This is my implementation of a RPC connection between a client and a server. The Server also uses Wikipedia's Opensearch API as well.
The software itself is a note making system in which the client can ask the server for notes on saved topics and create new notes.


This repository includes 2 main files:
## Server.py
It operates as a multithreaded server with 2 main functions:
  1. Adding a new note to the server based on given arguments
  2. Loading a topic matching the given argument.

## client.py
This client sided is a terminal-based menu program in which:
1. Client asks for a topic based on user input and then formats it to show it nicely.
2. Based on user input, make a request to add a new note to the server.
