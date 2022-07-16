# RUNEVENT TELEGRAM BOT
#### Video Demo:  <URL HERE>
#### Description:
this is a telegram bot that is responsible for events (running events). It can create an event, add participants to an event, view the list of events, remove participants from an event, delete an event (administrator function)

## Implementation details

### N-Tier Architecture
The Backend of this project uses the [3-Tier architecture pattern](https://en.wikipedia.org/wiki/Multitier_architecture#Three-tier_architecture)

In this project these tiers are represented by:

**handlers**: A set of single-purpose functions triggered by user's request 
to a certain app route and passing provided parameters to the logic tier 

**logic:**: The engine of the app which contains all the logic, decisions making, 
processing and task scheduling.   


### Project File Structure
```
.
Dockerfile  <- docker build file
Pipfile  <- dependecies
Pipfile.lock  <- dependecies lock
README.md
application.py   <- app init 
docker-compose.yml  <- local docker config
runevent
├── base    <- project config and init functions
│   ├── __init__.py
│   ├── config.py
│   └── init.py
├── dto     <- data transfet object
│   ├── __init__.py
│   └── runevent.py
├── handlerss   <- handler layer
│   ├── __init__.py
│   └── runevent.py
├── helpers   <- utility functions
│   ├── __init__.py
│   └── keyboard.py
└── logic  <- main app logic
    ├── __init__.py
    └── runevent.py
```

### Code Correctness

* Linters: Flake8
* Formatters: black


## Installation

```shell
$ git clone https://github.com/PProkhoda/final_cs50
$ cd final_cs50/
$ pipenv sync
```

## Running the App
To run this app you will need to have Docker installed. 
Please check out [Docker documentation](https://docs.docker.com/get-docker/) for more info.  

for Production:
```sh
$ docker-compose up -d 
```

## Author

Created by [Pavel Prokhoda](https://github.com/PProkhoda) in 2022 for educational purposes