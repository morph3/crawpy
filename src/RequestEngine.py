import sys
from tqdm import tqdm
import asyncio
from colorama import *
import aiohttp
import random
import string

init()
GREEN   = Fore.GREEN
RED     = Fore.RED
RESET   = Fore.RESET
BLUE    = Fore.BLUE
YELLOW  = Fore.YELLOW
MAGENTA = Fore.MAGENTA

def surpress(f):
    async def wrapper(*args, **kwargs):
        try:
            return await f(*args, **kwargs)
        except:
            pass
    return wrapper


class RequestEngine:
    def __init__(self,config):
        self.conf = config
        self.is_finished = False
        self.crafted_urls = []
        self.crafted_urls_length = 0        
        self.base_url_length = len(self.conf['base_url'])
        self.async_session = None
        self.found_urls =  [] 
        self.recursing_urls = []
        self.is_recursing = False
        self.progress_bar = None
        self.error_count = 0

        
    @surpress
    async def calibrate_fetch(self, session, url, semaphore, report):
        async with semaphore:
            async with session.request(
                                        self.conf['http_method'],
                                        url, 
                                        allow_redirects=self.conf['follow_redirects'], 
                                        headers=self.conf['headers'], 
                                        timeout=aiohttp.client.ClientTimeout(
                                        total=self.conf['timeout'])
                                        ) as response:
                status_code = response.status
                _text = await response.text()
                word_count = len(_text.split(" "))
                size_count = len(_text)
                line_count = len(_text.split("\n"))

                #sys.stdout.write(f"{status_code},{word_count},{size_count},{line_count}\n")
                report.append(f"{status_code},{word_count},{size_count},{line_count}")
                #print(report)

        return


    @surpress
    async def calibrate(self):
        # Generate random strings
        random_strs = []
        for i in range(5):
            random_strs.append(''.join(random.choice(string.ascii_letters) for i in range(random.randint(3,20))))
        random_strs[0] = random_strs[0] + ".unknown_ext"
        random_strs[-1] = random_strs[-1] + ".php"


        semaphore = asyncio.Semaphore(5)
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=self.conf['verify_ssl']) ) as session:
            tasks = []
            report = []
            for str in random_strs:
                tasks.append(self.calibrate_fetch(session, self.conf['base_url'].replace("FUZZ",str), semaphore, report))    
            await asyncio.wait(tasks)

        
        # Analyze section        
        # not sure if applying filters using line counts is a wise idea
        #line_counts = []
        status_codes = []
        word_counts = []
        size_counts = []

        # iterate for every combination
        # if all status codes are same, apply it as a filter etc.
        for r in report:
            _r = r.split(",")
            status_codes.append(int(_r[0]))
            word_counts.append(int(_r[1]))
            size_counts.append(int(_r[2]))
            #line_counts.append(_r[3])
            """
            sys.stdout.write(f"{MAGENTA}Status code:{status_codes}\n{RESET}")
            sys.stdout.write(f"{MAGENTA}Word count:{word_counts}\n{RESET}")
            sys.stdout.write(f"{MAGENTA}Size count:{size_counts}\n{RESET}")
            #sys.stdout.write(f"{MAGENTA}Line count:{line_count}\n{RESET}")
            """



        # apply them as filters
        if len(set(status_codes)) == 1:
            self.conf['filter_code'].append(status_codes[0])

        if len(set(word_counts)) == 1:
            self.conf['filter_word'].append(word_counts[0])

        if len(set(size_counts)) == 1:
            self.conf['filter_size'].append(size_counts[0])

        sys.stdout.write(f"{YELLOW}[*] Calibrated, applied filters:\n{RESET}")
        sys.stdout.write(f"{YELLOW}[*] Filter codes: {self.conf['filter_code']}\n{RESET}")
        sys.stdout.write(f"{YELLOW}[*] Filter words: {self.conf['filter_word']}\n{RESET}")
        sys.stdout.write(f"{YELLOW}[*] Filter size: {self.conf['filter_size']}\n{RESET}")

        return


    def craft_urls(self):
        self.crafted_urls = [] # makesure its cleared at first
        with open(self.conf['wordlist'], "r", encoding="latin-1") as f:
            for line in f:
                self.crafted_urls.insert(0,self.conf['base_url'].replace('FUZZ',line.replace("\n", "")))
        self.crafted_urls_length = len(self.crafted_urls)
        f.close()
        return

    def prepare_pbar(self):
        if self.progress_bar:
            self.progress_bar.reset(total=self.crafted_urls_length)
        else:
            self.progress_bar = tqdm(
                total=self.crafted_urls_length, ncols=50,desc="Fuzzing",
                bar_format="Fuzzing -> {percentage:3.2f}% {bar} {n_fmt}/{total_fmt} {rate_fmt:.5}req/s #")
        return

    def update_extensions(self):
        _updated = []
        for url in self.crafted_urls:
            _updated.insert(0,url)
            for ext in self.conf['extensions']:
                _updated.insert(-1,url+ext)

        self.crafted_urls_length = self.crafted_urls_length + self.crafted_urls_length * len(self.conf['extensions'])
        self.crafted_urls = _updated
        #sys.stdout.write(f"{self.crafted_urls} -> {self.crafted_urls_length}")
        return

    @surpress
    async def fetch(self,session, url, semaphore):
        async with semaphore:
            #sys.stdout.write(f"{GREEN}{self.conf['proxy_server']}{RESET}\n")
            async with session.request(
                                        self.conf['http_method'], 
                                        url, 
                                        allow_redirects=self.conf['follow_redirects'], 
                                        headers=self.conf['headers'], 
                                        timeout=aiohttp.client.ClientTimeout(
                                        total=self.conf['timeout']), 
                                        proxy=self.conf['proxy_server']) as response:
                self.progress_bar.update(1)
                status_code = response.status
                _text = await response.text()
                word_count = len(_text.split(" "))
                size_count = len(_text)
                line_count = len(_text.split("\n"))
                
                if (status_code in self.conf['filter_code']) or (line_count in self.conf['filter_line']) or (size_count in self.conf['filter_size']) or (word_count in self.conf['filter_word'] ):
                    pass
                else:
                    # note that alignment is not static, if we want to make it dynamic we will lose some speed so skipping now
                    info = f"[Words:{word_count}, Size:{size_count}, Lines:{line_count}]"

                    if (status_code in self.conf['recursive_codes']) and (self.is_recursing == False):
                        # for recursive scans
                        self.found_urls.append(url)
                    if(status_code in self.conf['recursive_codes']) and (self.is_recursing == True):
                        self.recursing_urls.append(url)
                    
                    if status_code < 300:
                        self.progress_bar.clear()
                        _url = f"{GREEN}[{status_code}] {url} {RESET}"
                        _url = _url.ljust(self.base_url_length+30)
                        sys.stdout.write(f"{_url}{info} \n")
                        
                        if self.conf['generate_report_enabled']:
                            self.conf['output_file'].write(f"[{status_code}] {url}\n")

                    elif status_code >= 300 and status_code < 400:
                        self.progress_bar.clear()
                        _url = f"{BLUE}[{status_code}] {url} {RESET}"
                        _url = _url.ljust(self.base_url_length+30)
                        sys.stdout.write(f"{_url}{info} \n")

                        if self.conf['generate_report_enabled']:
                            self.conf['output_file'].write(f"[{status_code}] {url}\n")
                    
                    elif status_code >= 400 and status_code < 403:
                        self.progress_bar.clear()
                        _url = f"{YELLOW}[{status_code}] {url} {RESET}"
                        _url = _url.ljust(self.base_url_length+30)
                        sys.stdout.write(f"{_url}{info} \n")

                        if self.conf['generate_report_enabled']:
                            self.conf['output_file'].write(f"[{status_code}] {url}\n")
                    
                    elif status_code >= 404:
                        self.progress_bar.clear()                     
                        _url = f"{RED}[{status_code}] {url} {RESET}"
                        _url = _url.ljust(self.base_url_length+30)
                        sys.stdout.write(f"{_url}{info} \n")

                        if self.conf['generate_report_enabled']:
                            self.conf['output_file'].write(f"[{status_code}] {url}\n")

    async def backup_filters(self):
        self.conf['filter_code'] = self.conf['filter_code_backup'].copy()
        self.conf['filter_size'] = self.conf['filter_size_backup'].copy()
        self.conf['filter_word'] = self.conf['filter_word_backup'].copy()
        return
        
    @surpress
    async def run(self):
        
        if self.conf['auto_calibrate']:
            # backup
            await self.calibrate()
            #sys.exit(1)


        self.craft_urls()
        self.update_extensions()
        self.prepare_pbar()
        semaphore = asyncio.Semaphore(self.conf['threads'])
        async with aiohttp.ClientSession( connector=aiohttp.TCPConnector(verify_ssl=self.conf['verify_ssl']) ) as session:
            tasks = []
            for url in self.crafted_urls:
                tasks.append(self.fetch(session, url, semaphore))
            await asyncio.wait(tasks)
        # Recursive mode.
        if self.conf['is_recursive']:
            self.progress_bar.clear()
            sys.stdout.write(f"\n{MAGENTA}[*] Recursive scan started{RESET}\n")
            #sys.stdout.write(f"{MAGENTA}Found urls {self.found_urls}{RESET}\n")
            
            while self.conf['recursive_depth'] != 0:
                for url in self.found_urls:
                    self.is_recursing = True

                    self.conf['base_url'] = url+"/FUZZ"
                    self.progress_bar.clear()
                    sys.stdout.write(f"\n{MAGENTA}[*] {self.conf['base_url']}{RESET}\n")

                    if self.conf['auto_calibrate']:
                        await self.backup_filters()
                        await self.calibrate()

                    self.craft_urls()
                    self.update_extensions()
                    self.prepare_pbar()
                    semaphore = asyncio.Semaphore(self.conf['threads'])
                    async with aiohttp.ClientSession( connector=aiohttp.TCPConnector( verify_ssl=self.conf['verify_ssl']) ) as session:
                        tasks = []
                        for u in self.crafted_urls:
                            tasks.append(self.fetch(session, u, semaphore))
                        await asyncio.wait(tasks)
                self.found_urls = []
                self.found_urls = self.recursing_urls.copy()
                self.conf['recursive_depth'] -= 1