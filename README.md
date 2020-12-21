# Crawpy
Yet another content discovery tool written in python.

What makes this tool different than others:
* It is written to work asynchronously which allows reaching to maximum limits so it is very fast.
* Calibration mode, applies filters on its own
* Has bunch of flags that helps you fuzz in detail
* Recursive scan mode for given status codes
* Report generation 

TODO: mass fuzz
TODO: screenshot mode, serv them with http

### An example run
[![asciicast](https://asciinema.org/a/370172.svg)](https://asciinema.org/a/370172)

### An example run with auto calibration and recursive mode enabled
[![asciicast](https://asciinema.org/a/370486.svg)](https://asciinema.org/a/370486)


# Installation
```
git clone https://github.com/morph3/crawpy
pip3 install -r requirements.txt 
or
python3 -m pip install -r requirements.txt
```

# Usage
```
usage: crawpy.py [-h] [-u URL] [-w WORDLIST] [-t THREADS] [-r RECURSIVE] [-rd RECURSIVE_DEPTH] [-e EXTENSIONS] [-to TIMEOUT] [-ss SCREENSHOT] [-follow] [-ac] [-fc FILTER_CODE] [-fs FILTER_SIZE] [-fw FILTER_WORD] [-fl FILTER_LINE] [-k]   
                 [-m MAX_RETRY] [-H HEADERS] [-o OUTPUT_FILE] [-gr] [-X HTTP_METHOD] [-p PROXY_SERVER]

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     URL
  -w WORDLIST, --wordlist WORDLIST
                        Wordlist
  -t THREADS, --threads THREADS
                        Size of the semaphore pool
  -r RECURSIVE, --recursive RECURSIVE
                        Recursive scan, specify status codes Example: 200,301,302
  -rd RECURSIVE_DEPTH, --recursive-depth RECURSIVE_DEPTH
                        Recursive scan depth,Example: 2
  -e EXTENSIONS, --extension EXTENSIONS
                        Add extensions at the end. Seperate them with comas Example: -x .php,.html,.txt
  -to TIMEOUT, --timeout TIMEOUT
                        Timeouts, I suggest you to not use this option because it is procudes lots of erros now which I was not able to solve why
  -ss SCREENSHOT, --screenshot SCREENSHOT
                        Takes screenshot of valid requests. Default is 200,204,301,302,307
  -follow, --follow-redirects
                        Follow redirects
  -ac, --auto-calibrate
                        Automatically calibre filter stuff
  -fc FILTER_CODE, --filter-code FILTER_CODE
                        Filter status code
  -fs FILTER_SIZE, --filter-size FILTER_SIZE
                        Filter size
  -fw FILTER_WORD, --filter-word FILTER_WORD
                        Filter words
  -fl FILTER_LINE, --filter-line FILTER_LINE
                        Filter line
  -k, --ignore-ssl      Ignore untrusted SSL certificate
  -m MAX_RETRY, --max-retry MAX_RETRY
                        Max retry
  -H HEADERS, --headers HEADERS
                        Headers, you can set the flag multiple times.For example: -H "X-Forwarded-For: 127.0.0.1", -H "Host: foobar"
  -o OUTPUT_FILE, --output OUTPUT_FILE
                        Output file
  -gr, --generate-report
                        If you want crawpy to generate a report, default path is crawpy/reports/<url>.txt
  -X HTTP_METHOD, --http-method HTTP_METHOD
                        HTTP request method
  -p PROXY_SERVER, --proxy PROXY_SERVER
                        Proxy server, ex: 'http://127.0.0.1:8080'
```


# Examples
```
python3 crawpy.py -u https://facebook.com/FUZZ -w ./common.txt  -k -ac  -e .php,.html
python3 crawpy.py -u https://google.com/FUZZ -w ./common.txt  -k -fw 9,83 -r 301,302 -rd 2
python3 crawpy.py -u https://morph3sec.com/FUZZ -w ./common.txt -e .php,.html -t 20 -ac -k
python3 crawpy.py -u https://google.com/FUZZ -w ./common.txt  -ac -gr
python3 crawpy.py -u https://google.com/FUZZ -w ./common.txt  -ac -gr -o /tmp/test.txt
```

