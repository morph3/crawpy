# Crawpy

Crawpy is a web discovery tool. <br/>
It's main purpose is to have a general recon of the given URL.<br/>
Crawpy can do recursive scan, take screenshots for given status codes.


### Basic Discovery
[![asciicast](https://asciinema.org/a/jVPdNGGpafo3K4feQRoSuCpLI.svg)](https://asciinema.org/a/jVPdNGGpafo3K4feQRoSuCpLI?speed=3)

### Recursive Discovery
[![asciicast](https://asciinema.org/a/lKav0RTvViRmj8db9hyJALOfn.svg)](https://asciinema.org/a/lKav0RTvViRmj8db9hyJALOfn?speed=10)
### Screenshot Mode
![gif](https://github.com/morph3/crawpy/blob/master/screenshots/crawpy.gif)


# Installation
```
git clone https://github.com/morph3/crawpy
pip install -r requirements.txt
```

# Usage 
```
python main.py --help
usage: main.py [-h] [-u URL] [-w WORDLIST] [-t THREADS] [-r] [-x EXTENTION]
               [-to TIMEOUT] [-ss [SCREENSHOT]] [-s STATUS] [-o OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     URL
  -w WORDLIST, --wordlist WORDLIST
                        Wordlist
  -t THREADS, --threads THREADS
                        Number of threads
  -r, --recursive       Recursive scan
  -x EXTENTION, --extention EXTENTION
                        Add extentions at the end. Seperate them with comas
                        example: -x php,html,txt
  -to TIMEOUT, --timeout TIMEOUT
                        Timeout
  -ss [SCREENSHOT], --screenshot [SCREENSHOT]
                        Takes screenshot of valid requests. Default is
                        200,204,301,302,307
  -s STATUS, --status-code STATUS
                        Status codes to be checked Default is
                        200,204,301,302,307
  -o OUTPUT, --output OUTPUT
                        Output file
```

# Examples

```
python main.py -u https://morph3sec.com -w common.txt --screenshot 200
python main.py -u https://morph3sec.com -w common.txt --screenshot 200 -r --status-code 200,301 -o output.txt
```


# TODO:
```
Virtual Host Fuzzing 
Custom Header on requests 
Subnet Discovery 
Optimizations 
```
