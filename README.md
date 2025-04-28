# PC Monitor Pro 🖥️

<div align="center">
  <img src="https://img.shields.io/badge/status-finalizado-success" alt="Status do Projeto"/>
  <img src="https://img.shields.io/badge/licença-MIT-green" alt="Licença"/>
  <img src="https://img.shields.io/badge/python-3.6+-blue" alt="Python Version"/>
</div>

## 📋 Sobre o Projeto

PC Monitor Pro é uma ferramenta robusta de monitoramento de sistema desenvolvida em Python. Ela oferece monitoramento em tempo real do seu computador, incluindo uso de CPU, memória, disco, conexão de internet e muito mais. Ideal para administradores de sistema e usuários que precisam manter um olho constante no desempenho de suas máquinas.

## ✨ Funcionalidades Principais

- 🔄 Monitoramento em tempo real
  - CPU: Uso geral e top 5 processos
  - Memória RAM
  - Discos: Espaço usado e disponível
  - Conexão de Internet: Ping, download e upload
  - Uptime do sistema

- 📊 Alertas Automáticos
  - Notificação de CPU alta (>85% por 3+ minutos)
  - Alerta de ping elevado (>100ms)
  - Monitoramento de quedas de conexão

- 📝 Logs Detalhados
  - Registros diários automáticos
  - Formato de data e hora para fácil análise
  - Armazenamento organizado por data

## 🚀 Tecnologias Utilizadas

- Python 3.6+
- Bibliotecas:
  - psutil (monitoramento do sistema)
  - speedtest-cli (teste de velocidade)
  - datetime (gestão de tempo)
  - subprocess (execução de comandos)

## 🛠️ Instalação

```bash
# Clone o repositório
git clone https://github.com/fhecout/pc-monitor-pro.git

# Entre no diretório
cd pc-monitor-pro

# Instale as dependências
pip install -r requirements.txt

# Execute o programa
python app.py
```

## 🖥️ Pré-requisitos

- Python 3.6 ou superior
- Sistema Operacional: Windows
- Conexão com a Internet
- Privilégios de administrador (para algumas funcionalidades)

## 📊 Exemplo de Saída

```
12:30:45 - 🚀 Iniciando monitoramento...
12:30:46 - 📶 Ping Google: 25 ms
12:30:47 - 🧠 Uso de CPU: 45%
12:30:48 - 💽 Uso de discos:
12:30:49 - 📊 Memória RAM: 60% usada (8192MB de 16384MB)
12:30:50 - 🌐 Velocidade: Download=100.25Mbps, Upload=50.30Mbps, Ping=25.1ms
```

## 📬 Contato

Felipe Couto - [@fhecout](https://twitter.com/fhecout)

Link do Projeto: [https://github.com/fhecout/pc-monitor-pro](https://github.com/fhecout/pc-monitor-pro)

---

⭐️ Se este projeto te ajudou, considere dar uma estrela! 
