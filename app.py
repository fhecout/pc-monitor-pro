import os
import time
import platform
import psutil
import socket
import subprocess
from datetime import datetime
import speedtest

# Variáveis de controle
uso_cpu_alto_contador = 0
ping_alto_contador = 0

def obter_nome_arquivo():
    hoje = datetime.now().strftime("%Y-%m-%d")
    return os.path.join("monitoramentos", f"monitoramento-{hoje}.txt")

def log(texto):
    agora = datetime.now().strftime("%H:%M:%S")
    with open(obter_nome_arquivo(), "a", encoding="utf-8") as f:
        f.write(f"{agora} - {texto}\n")

conexao_ativa = True  # status inicial presumido

def testar_ping():
    global ping_alto_contador, conexao_ativa
    try:
        saida = subprocess.check_output(["ping", "-n", "1", "8.8.8.8"], stderr=subprocess.STDOUT, universal_newlines=True)

        for linha in saida.splitlines():
            if "tempo=" in linha or "time=" in linha:
                partes = linha.split()
                for parte in partes:
                    if parte.startswith("tempo=") or parte.startswith("time="):
                        valor = ''.join(filter(str.isdigit, parte))
                        tempo = int(valor)
                        log(f"📶 Ping Google: {tempo} ms")

                        if tempo > 100:
                            ping_alto_contador += 1
                            log("⚠️ Alerta: ping > 100ms")
                        else:
                            ping_alto_contador = 0

                        if not conexao_ativa:
                            log("📈 Conexão restabelecida")
                            conexao_ativa = True
                        return

        log("📶 Ping sem resposta (pacote perdido)")
        if conexao_ativa:
            log("📉 Conexão perdida")
            conexao_ativa = False

    except subprocess.CalledProcessError:
        log("🚨 Sem resposta do ping (possível queda de internet)")
        if conexao_ativa:
            log("📉 Conexão perdida")
            conexao_ativa = False
    except Exception as e:
        log(f"Erro no ping: {e}")



def testar_velocidade():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download = st.download() / 1024 / 1024
        upload = st.upload() / 1024 / 1024
        ping = st.results.ping
        log(f"🌐 Velocidade: Download={download:.2f}Mbps, Upload={upload:.2f}Mbps, Ping={ping:.1f}ms")
        log("="*90)
    except Exception as e:
        log(f"Erro na velocidade: {e}")
        log("="*90)

        
        
        
                                                                                                                                                 

def obter_temperaturas():
    try:
        output = subprocess.check_output(['wmic', 'path', 'Win32_TemperatureProbe', 'get', 'CurrentReading,Description'], universal_newlines=True)
        linhas = output.strip().splitlines()[1:]  # pula o cabeçalho
        resultado = []
        for linha in linhas:
            if not linha.strip():
                continue
            partes = linha.strip().split()
            if len(partes) >= 2 and partes[0].isdigit():
                valor_kelvin = int(partes[0])
                celsius = (valor_kelvin - 2732) / 10
                desc = " ".join(partes[1:])
                resultado.append(f"{desc}: {celsius:.1f}°C")
        return "\n".join(resultado) if resultado else "Temperaturas não disponíveis"
    except Exception as e:
        return f"Erro ao obter temperatura: {e}"



def obter_voltagem():
    try:
        output = subprocess.check_output(['wmic', 'path', 'Win32_VoltageProbe', 'get', 'Name,CurrentReading'], universal_newlines=True)
        linhas = output.strip().splitlines()[1:]  # pula o cabeçalho
        resultado = []
        for linha in linhas:
            if not linha.strip():
                continue
            partes = linha.strip().split()
            if len(partes) >= 2 and partes[-1].isdigit():
                valor = int(partes[-1])
                nome = " ".join(partes[:-1])
                resultado.append(f"{nome}: {valor} mV")
        return "\n".join(resultado) if resultado else "Voltagens não disponíveis"
    except Exception as e:
        return f"Erro ao obter voltagem: {e}"


def verificar_disco():
    log("💽 Uso de discos:")
    for part in psutil.disk_partitions(all=False):
        try:
            uso = psutil.disk_usage(part.mountpoint)
            total_gb = uso.total // (1024 ** 3)
            usado_gb = uso.used // (1024 ** 3)
            log(f"  {part.device} - {usado_gb}GB usados / {total_gb}GB ({uso.percent}%)")
        except PermissionError:
            log(f"  {part.device} - Permissão negada")
        except Exception as e:
            log(f"  {part.device} - Erro: {e}")


def verificar_cpu():
    global uso_cpu_alto_contador
    uso_cpu = psutil.cpu_percent()
    log(f"🧠 Uso de CPU: {uso_cpu}%")

    if uso_cpu > 85:
        uso_cpu_alto_contador += 1
        if uso_cpu_alto_contador >= 180:
            log("🔥 ALERTA GRAVE: CPU > 85% por mais de 3 minutos")
    else:
        uso_cpu_alto_contador = 0

    processos = sorted(psutil.process_iter(['pid', 'name', 'cpu_percent']), key=lambda p: p.info['cpu_percent'], reverse=True)
    log("🔍 Top 5 processos por uso de CPU:")
    for p in processos[1:6]:
        try:
            log(f"    {p.info['name']} (PID {p.info['pid']}): {p.info['cpu_percent']}%")
        except:
            continue

def verificar_memoria():
    mem = psutil.virtual_memory()
    log(f"📊 Memória RAM: {mem.percent}% usada ({mem.used // (1024**2)}MB de {mem.total // (1024**2)}MB)")

def verificar_uptime():
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    agora = datetime.now()
    tempo_ativo = agora - boot_time
    log(f"🕒 Uptime: {tempo_ativo} (desde {boot_time.strftime('%d/%m/%Y %H:%M:%S')})")

def verificar_temperatura_voltagem():
    log("🌡️ Temperatura:")
    # log(obter_hwinfo())
    log("🔋 Voltagem:")
    # log(obter_voltagem())

def garantir_pasta():
    os.makedirs("monitoramentos", exist_ok=True)

def monitorar():
    garantir_pasta()
    log("🚀 Iniciando monitoramento...")

    segundos = 0
    while True:
        if segundos % 5 == 0:
            testar_ping()
            verificar_cpu()
            verificar_disco()
            verificar_memoria()
            verificar_uptime()
            # verificar_temperatura_voltagem()

        if segundos % 5 == 0:
            testar_velocidade()

        time.sleep(1)
        segundos += 1

if __name__ == "__main__":
    try:
        monitorar()
    except KeyboardInterrupt:
        log("🛑 Monitoramento encerrado manualmente.")
    except Exception as e:
        log(f"💥 Erro geral: {e}")
