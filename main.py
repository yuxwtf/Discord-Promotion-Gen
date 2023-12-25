import colorama,requests,threading,os,random,time


colorama.init()
use_proxies = False # proxyless by default
generateds = 0
fails = 0
ASKY = """

                                 __   __   ___  __        __   ___      
                                /  \ |__) |__  |__)  /\  / _` |__  |\ | 
                                \__/ |    |___ |  \ /~~\ \__> |___ | \| 

                                        made by yuxwtf with <3

"""

def UpdateHandler():
    start_time = time.time()
    global time_elapsed,generateds,fails
    while True:
        time.sleep(1)
        time_elapsed = int(time.time() - start_time)
        generations_per_second = int(generateds / time_elapsed if time_elapsed > 0 else 0)
        generations_per_minute = int(generations_per_second * 60)
        success_rate = ((generateds - fails) / generateds) * 100 if generateds > 0 else 0
        os.system(f'title OperaGen ^| Success Rate: {success_rate:.2f}% ^| Gen/m: {generations_per_minute} ^| Generated: {generateds} ^| Fails: {fails} ^| Time Elapsed: {time_elapsed}s')

class Gen:

    def __init__(self, proxy=None) -> None:
        self.session = requests.session()
        self.root = "https://api.discord.gx.games/v1/"
        if proxy != None: self.session.proxies.update(proxy)
    
    def GetToken(self):
        headers = {
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 OPR/105.0.0.0"
        }
        payload = {
            "partnerUserId": "7bb74f47de06947fca2cf6ff4036557360c12eb0d70d70d74f0fa9e0f218cd98"
        }
        req = self.session.post(self.root + "direct-fulfillment", json=payload, headers=headers)
        # print(req.status_code,req.text)
        return req.json()['token']
    
    def Token2Link(self, token):
        link = f"https://discord.com/billing/partner-promotions/1180231712274387115/{token}"
        return link
    
def load_proxies_from_file(file_path):
    proxies = []
    with open(file_path, 'r') as file:
        for line in file:
            proxies.append({'https': f'http://{line.strip()}', 'http': f'http://{line.strip()}'})
    return proxies

def Worker():
    global proxies,fails,generateds
    proxies = []
    if use_proxies: proxies = load_proxies_from_file("proxies.txt")
    while True:
        try:
            g_ = Gen(proxy=random.choice(proxies) if use_proxies else None)
            token = g_.GetToken()
            link = g_.Token2Link(token)
            print(colorama.Fore.MAGENTA + f' (+) Generated: {link}')
            with open('gens.txt', 'a') as f:
                f.write(str(link)+"\n")
                f.close()
            generateds += 1
        except:
            fails += 1
            print(colorama.Fore.YELLOW +' (X) Failed, retrying...')
            time.sleep(5)

def Main():
    os.system(f'title OperaGen ^| Awaiting User Inputs ^| github.com/yuxwtf')
    global use_proxies
    os.system('cls')
    print(colorama.Fore.MAGENTA + str(ASKY))
    threads_ = int(input(colorama.Fore.MAGENTA + '\n\n\n (>) Threads: '))
    _use_proxies = str(input(colorama.Fore.MAGENTA + ' (>) Use proxies (y/n): '))
    if _use_proxies.strip().lower() == "y": use_proxies = True
    print('\n')
    threading.Thread(target=UpdateHandler).start()
    for i in range(threads_):
        threading.Thread(target=Worker).start()


if __name__ == "__main__":
    Main()