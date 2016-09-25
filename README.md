# Tak-sim
## Simulator for the game of Tak

Tak is a board game based on its fictional counterpart that is mentioned in **The Wise Man's Fear** by **Patrick Rothfuss** (The second book in the Kingkiller Chronicles). You can find details of the game [here](http://cheapass.com/tak/). The formal set of rules can be found [here](http://www.cheapass.com/sites/default/files/TAKBetaRules9-9.pdf).

This simulator has been created for the fall 2016 course COL333 (Artificial Intelligence). All the best for your tournament!

## How to use

To run the server:
```bash
python server.py <port no.>
```

Optional arguments:  
-n \<n> : Board size (Default: 5)  
-TL \<time limit> : Time limit in seconds for each player (Default: 120) 
 
To run an AI player:
```bash 
python client.py <server ip> <server port> <run.sh>
```

Optional arguments:  
-n \<n> : Board size (Default: 5)  
-mode \<MODE> : This can be 'GUI' (which visualizes the game state as a Tkinter window), 'CUI' (which shows a simple command line visualisation of the game state) or 'None' (no game state visualization). Default: 'GUI'
 
run.sh should be a bash script which runs your code.

Note: If you are running both client instances on the same machine it is recommended you set the mode of at least one of them to CUI or None. Two Tkinter GUI instances tend to clog the CPU.

The AI player will first receive a space-separated string
'\<Player no.> \<board size> \<time limit>' which it should read from stdin, and it should then read/write moves from stdin / to stdout respectively. Debug messages can be written to stderr.
