from tqdm import tqdm
import requests
from requests.auth import HTTPDigestAuth


user = None
password = None

with open("config.txt") as f:
    for linha in f:
        if linha.startswith("user="):
            user = linha.split("=",1)[1].strip()
        elif linha.startswith("password="):
            password = linha.split("=",1)[1].strip()


with open('ips.txt') as f:
    ips = [linha.strip() for linha in f if linha.strip()]
resp= []

for i in tqdm(ips, desc="Verificando Ips", unit="ip"):
    Collect = f"http://{i}/cgi-bin/magicBox.cgi?action=getSoftwareVersion"
    try:
        res = requests.get(Collect, auth=HTTPDigestAuth(user, password), timeout=5)
        if res.status_code ==200:
            softver = res.text.strip()
            resp.append((i,res.text))
        elif res.status_code ==404:
            resp.append((i,"Erro 404: Link Não existe, ou IP incorreto"))
        elif res.status_code == 502:
            resp.append((i,"Erro 502: Aparelho ocupado ou reiniciando"))
        else:
            resp.append((i,f"Erro HTTP{res.status_code}"))
    except Exception as e:
        resp.append((i,f"Erro HTTP{e}"))

with open("Versão_Facial_p_IP","w") as f:
    f.write("IP,Versao_Firmware\n")
    for ip,softver in resp:
        f.write(f"{ip},{softver}\n")

