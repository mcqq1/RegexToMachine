This academic project aims to compile regular expression into finite state automat.

We provide module 'regtomach' in which we include parser of regular expression, wrapper for abstract syntax tree and a class that represents state machine, which computes the final word.

## How to run
This project was build with Python 3.13.3.

1. Clone the repository
```shell
git clone https://github.com/mcqq1/RegexToMachine.git
cd RegexToMachine
```
2. Install dependencies (venv recommended)
```shell
python3 -m venv .venv
source .venv/bin/activate
(.venv) pip install -r requirements.txt
```
3. Run main file
```shell
(.venv) python main.py
```
