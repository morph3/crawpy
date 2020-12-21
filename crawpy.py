import time
import sys
import argparse
from colorama import *
import src.config
import os
from src.RequestEngine import RequestEngine
from src.Banner import Banner
#from src.Interact import Interact
import asyncio
import aiohttp


def flush_input():
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        import termios    #for linux/unix
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)


if __name__ == "__main__":
    base_path = os.path.abspath(os.path.dirname(__file__))

    init()
    GREEN   = Fore.GREEN
    RED     = Fore.RED
    RESET   = Fore.RESET
    BLUE    = Fore.BLUE
    YELLOW  = Fore.YELLOW

    parser = argparse.ArgumentParser()

    # Mandatory options
    parser.add_argument("-u", "--url", dest="url",help="URL")
    parser.add_argument("-w", "--wordlist", dest="wordlist", help="Wordlist")
    
    # Optional options
    parser.add_argument("-t", "--threads", dest="threads", help="Size of the semaphore pool",default=50)
    parser.add_argument("-r", "--recursive", dest="recursive",default=[],help="Recursive scan, specify status codes\n Example: 200,301,302")
    parser.add_argument("-rd", "--recursive-depth", dest="recursive_depth",default=-1, type=int,help="Recursive scan depth,Example: 2")
    

    parser.add_argument("-e", "--extension", dest="extensions",default=[],help="Add extensions at the end. Seperate them with comas \n Example: -x .php,.html,.txt")
    parser.add_argument("-to", "--timeout", dest="timeout",default=5, help="Timeouts, I suggest you to not use this option because it is procudes lots of erros now which I was not able to solve why")
    parser.add_argument("-ss", "--screenshot", dest="screenshot", default=[],help="Takes screenshot of valid requests.\nDefault is 200,204,301,302,307")
    parser.add_argument("-follow", "--follow-redirects", dest="follow_redirects",action='store_true', help="Follow redirects")
    
    # Filter options
    parser.add_argument("-ac","--auto-calibrate", dest="auto_calibrate", action='store_true', help="Automatically calibre filter stuff")
    
    parser.add_argument("-fc","--filter-code", dest="filter_code", default=[], help="Filter status code")
    parser.add_argument("-fs","--filter-size", dest="filter_size", default=[], help="Filter size")
    parser.add_argument("-fw","--filter-word", dest="filter_word", default=[], help="Filter words")
    parser.add_argument("-fl","--filter-line", dest="filter_line", default=[], help="Filter line")

    parser.add_argument("-k", "--ignore-ssl", dest="verify_ssl",action='store_false',help="Ignore untrusted SSL certificate")
    parser.add_argument("-m","--max-retry", dest="max_retry", default=3,help="Max retry")
    parser.add_argument("-H","--headers", dest="headers", action='append', help="Headers, you can set the flag multiple times.For example: -H \"X-Forwarded-For: 127.0.0.1\", -H \"Host: foobar\" ")

    parser.add_argument("-o","--output", dest="output_file", default=f"{base_path}/reports/", help="Output file" )
    parser.add_argument("-gr","--generate-report", dest="generate_report", action="store_true", help="If you want crawpy to generate a report, default path is crawpy/reports/<url>.txt" )

    parser.add_argument("-X","--http-method", dest="http_method", default="GET",help="HTTP request method")
    parser.add_argument("-p","--proxy", dest="proxy_server",help="Proxy server, ex: 'http://127.0.0.1:8080'")


    args = parser.parse_args()

    if len(sys.argv) < 2:
        parser.print_usage()
        sys.exit(0)

    Banner().greet()


    conf = src.config.config
    # initialize


    conf['base_url'] = args.url
    conf['wordlist'] = args.wordlist
    conf['threads'] = int(args.threads)
    conf['http_method'] = args.http_method
    conf['timeout'] = args.timeout
    conf['verify_ssl'] = args.verify_ssl
    conf['follow_redirects'] = args.follow_redirects
    conf['recursive_depth'] = args.recursive_depth
    conf['auto_calibrate'] = args.auto_calibrate
    conf['proxy_server'] = args.proxy_server

    # output
    if args.generate_report:
        conf['generate_report_enabled'] = True
        if "reports/" in args.output_file:
            _url = args.url.replace("://","_").replace(".","_").replace("FUZZ","").replace("/","") # i know this is ugly but it works
            conf['output_file'] = open(f"{args.output_file}{_url}.txt","w")  
        else:
            conf['output_file'] = open(f"{args.output_file}","w") 

    if args.headers != None:
        for header in args.headers:
            conf['headers'][header.split(':')[0]] = header.split(':')[1]


    if len(args.filter_word) > 0:
        conf['filter_word'] = [int(_) for _ in args.filter_word.split(",")]

    if len(args.filter_code) > 0:
        conf['filter_code'] = [int(_) for _ in args.filter_code.split(",")]

    if len(args.filter_size) > 0:
        conf['filter_size'] = [int(_) for _ in args.filter_size.split(",")]

    if len(args.filter_line) > 0:
        conf['filter_line'] = [int(_) for _ in args.filter_line.split(",")]

    # extension
    if len(args.extensions) > 0:
        conf['extensions'] = args.extensions.split(",")

    if len(args.recursive) > 0:
        conf['is_recursive'] = True
        conf['recursive_codes'] = [int(_) for _ in args.recursive.split(",")]
        conf['filter_code_backup'] = conf['filter_code'].copy()
        conf['filter_size_backup'] = conf['filter_size'].copy()
        conf['filter_word_backup'] = conf['filter_word'].copy()
        
        if args.recursive_depth == -1:
            sys.stdout.write(f"{RED}[!] You must enter a recursion depth! {RESET}\n")
            sys.exit(1)

    # screenshot 
    if len(args.screenshot) > 0:
        conf['screenshot_mode'] = True
        screenshot_codes = args.screenshot.split(",")
    else:
        conf['screenshot_mode'] = False



    #info section
    sys.stdout.write(f"{BLUE}[*] Url: {conf['base_url']} \n{RESET}")
    sys.stdout.write(f"{BLUE}[*] Wordlist: {conf['wordlist']}\n{RESET}")
    sys.stdout.write(f"{BLUE}[*] Semaphore pool: {conf['threads']}\n{RESET}")
    sys.stdout.write(f"{BLUE}[*] Extensions: {conf['extensions']}\n{RESET}")
    sys.stdout.write(f"{BLUE}[*] Follow redirects: {conf['follow_redirects']}\n{RESET}")
    sys.stdout.write(f"{BLUE}[*] HTTP Method {conf['http_method']}\n{RESET}")
    sys.stdout.write(f"{BLUE}[*] Headers {conf['headers']}\n{RESET}")
    
    # Matchers
    if len(conf['filter_word']) > 0:
        sys.stdout.write(f"{YELLOW}[*] Filter words: {conf['filter_word']}\n{RESET}")
    if len(conf['filter_code']) > 0:
        sys.stdout.write(f"{YELLOW}[*] Filter codes: {conf['filter_code']}\n{RESET}")
    if len(conf['filter_size']) > 0:
        sys.stdout.write(f"{YELLOW}[*] Filter size: {conf['filter_size']}\n{RESET}")
    if len(conf['filter_line']) > 0:
        sys.stdout.write(f"{YELLOW}[*] Filter line: {conf['filter_line']}\n{RESET}")

    if conf['proxy_server']:
        sys.stdout.write(f"{YELLOW}[*] Proxy server: {conf['proxy_server']}{RESET}\n")
    if conf['screenshot_mode']:
        sys.stdout.write(f"{GREEN}[*] Screenshot mod is enabled for status codes : {screenshot_codes} {RESET}\n")
    if conf['is_recursive']:
        sys.stdout.write(f"{YELLOW}[!] Recursive scan enabled with depth {conf['recursive_depth']}{RESET}\n")
    if conf['generate_report_enabled']:
        sys.stdout.write(f"{YELLOW}[!] Generate report enabled, writing: {conf['output_file'].name}{RESET}\n")

    if os.name != 'nt':
        os.system("stty -echo")
    

    requester = RequestEngine(conf)
    loop = asyncio.get_event_loop()
    #loop.set_debug(1)
    sys.stdout.write(f"{BLUE}-------------\n{RESET}")
    
    try:
        loop.run_until_complete(requester.run())

    except KeyboardInterrupt:
        sys.stdout.write(f"{RED}[!] Keyboard interrupt recieved, exiting ...{RESET}\n")
        pass
    except:
        pass


    if os.name != 'nt':
        os.system("stty echo")    
    
    if conf['generate_report_enabled']:
        conf['output_file'].close()

    flush_input()


    # screenshot section
    """
    # Maybe do this in run func
    if conf['screenshot_mode']:
        if len(requester.screenshot_urls) < 1:
            sys.stdout.write(f"{RED}[!]Not found any url , quiting...\n{RESET}")
            sys.exit(1)
        crawpy_ss = Interact("firefox")
        for url in requester.screenshot_urls:
            if str(url.status_code) in screenshot_codes:
                crawpy_ss.clip(url.url)

    """
    """
    # output section
    if output != "":
        import os
        he.handler.info("Output file is {}".format(os.getcwd()+"/"+output))
        with open(output,"w") as f:
            for resp in he.handler.found_resps:
                f.write(f"[{resp.status_code}] {resp.urls} \n")
            f.close()
    """
