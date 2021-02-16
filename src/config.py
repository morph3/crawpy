# -*- coding: utf-8 -*-
config = {
        'is_recursive' : False,
        'generate_report_enabled' : False,
        'output_file_txt' : None,
        'output_file_html' : None,
        'html_report' : "",
        
        'wordlist' : "",
        'threads' : 20, # default, asynchronous so 
        'timeout' : 0,
        'extensions' : [], #list of extensipons
        'base_url' : "",
        'directories' : [],
        'http_method' : "GET",
        'screenshot_mode' : False,
        'screenshot_codes' : [],
        'verify_ssl' : True,
        'follow_redirects' : False,
        'recursive_codes' : [],
        'recursive_depth' : -1,
        'auto_calibrate' : False,
        # Matchers 
        'filter_code' : [],
        'filter_string' : [],
        'filter_size' : [],
        'filter_word' : [],
        'filter_line' : [],
        'filter_code_backup' : [],
        'filter_size_backup' : [],
        'filter_word_backup' : [],
        'proxy_server': None,
        'headers' : {
            'User-Agent' : 'crawpy/1.3 - github.com/morph3',
        }
}
