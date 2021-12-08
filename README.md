# Crawpy
Yet another content discovery tool written in python.

What makes this tool different than others:
* It is written to work asynchronously which allows reaching to maximum limits. So it is very fast.
* Calibration mode, applies filters on its own
* Has bunch of flags that helps you fuzz in detail
* Recursive scan mode for given status codes and with depth
* Report generations, you can later go and check your results
* Multiple url scans


### An example run
[![asciicast](https://asciinema.org/a/370172.svg)](https://asciinema.org/a/370172)

### An example run with auto calibration and recursive mode enabled
[![asciicast](https://asciinema.org/a/370486.svg)](https://asciinema.org/a/370486)

### Example reports

Example reports can be found here
```
https://morph3sec.com/crawpy/example.html
https://morph3sec.com/crawpy/example.txt
```

# Installation

```
git clone https://github.com/morph3/crawpy
pip3 install -r requirements.txt 
or
python3 -m pip install -r requirements.txt
```

# Usage

```
morph3 ➜ crawpy/ [main✗] λ python3 crawpy.py --help
usage: crawpy.py [-h] [-u URL] [-w WORDLIST] [-t THREADS] [-rc RECURSIVE_CODES] [-rp RECURSIVE_PATHS] [-rd RECURSIVE_DEPTH] [-e EXTENSIONS] [-to TIMEOUT] [-follow] [-ac] [-fc FILTER_CODE] [-fs FILTER_SIZE] [-fw FILTER_WORD] [-fl FILTER_LINE] [-k] [-m MAX_RETRY]
                 [-H HEADERS] [-o OUTPUT_FILE] [-gr] [-l URL_LIST] [-lt LIST_THREADS] [-s] [-X HTTP_METHOD] [-p PROXY_SERVER]

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     URL
  -w WORDLIST, --wordlist WORDLIST
                        Wordlist
  -t THREADS, --threads THREADS
                        Size of the semaphore pool
  -rc RECURSIVE_CODES, --recursive-codes RECURSIVE_CODES
                        Recursive codes to scan recursively Example: 301,302,307
  -rp RECURSIVE_PATHS, --recursive-paths RECURSIVE_PATHS
                        Recursive paths to scan recursively, please note that only given recursive paths will be scanned initially Example: admin,support,js,backup
  -rd RECURSIVE_DEPTH, --recursive-depth RECURSIVE_DEPTH
                        Recursive scan depth Example: 2
  -e EXTENSIONS, --extension EXTENSIONS
                        Add extensions at the end. Seperate them with comas Example: -x .php,.html,.txt
  -to TIMEOUT, --timeout TIMEOUT
                        Timeouts, I suggest you to not use this option because it is procudes lots of erros now which I was not able to solve why
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
                        Output folder
  -gr, --generate-report
                        If you want crawpy to generate a report, default path is crawpy/reports/<url>.txt
  -l URL_LIST, --list URL_LIST
                        Takes a list of urls as input and runs crawpy on via multiprocessing -l ./urls.txt
  -lt LIST_THREADS, --list-threads LIST_THREADS
                        Number of threads for running crawpy parallely when running with list of urls
  -s, --silent          Make crawpy not produce output
  -X HTTP_METHOD, --http-method HTTP_METHOD
                        HTTP request method
  -p PROXY_SERVER, --proxy PROXY_SERVER
                        Proxy server, ex: 'http://127.0.0.1:8080'
```


# Examples

```
python3 crawpy.py -u https://facebook.com/FUZZ -w ./common.txt  -k -ac  -e .php,.html
python3 crawpy.py -u https://google.com/FUZZ -w ./common.txt -k -fw 9,83 -rc 301,302 -rd 2 -ac
python3 crawpy.py -u https://morph3sec.com/FUZZ -w ./common.txt -e .php,.html -t 20 -ac -k
python3 crawpy.py -u https://google.com/FUZZ -w ./common.txt  -ac -gr
python3 crawpy.py -u https://google.com/FUZZ -w ./common.txt  -ac -gr -o /tmp/test.txt
sudo python3 crawpy.py -l urls.txt -lt 20 -gr -w ./common.txt -t 20 -o custom_reports -k -ac -s
python3 crawpy.py -u https://google.com/FUZZ -w ./common.txt -ac -gr -rd 1 -rc 302,301 -rp admin,backup,support -k
```
