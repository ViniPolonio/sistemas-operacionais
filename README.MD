Sistema de Monitoramento de Computadores em Rede

Este projeto implementa um sistema de monitoramento que coleta dados de CPU, memória, disco e rede em máquinas virtuais (2 Linux e 1 Windows) usando SSH, Telnet e FTP.
📋 Requisitos
💻 Máquinas Monitoradas

    2 VMs Linux (com SSH e FTP ativos)

    1 VM Windows (com Telnet e FTP ativos)

    Todas na mesma rede

📚 Bibliotecas Python (no host principal)
bash

pip install paramiko

    paramiko já inclui suporte a SSH e SFTP. O Python padrão fornece ftplib e telnetlib.

⚙️ Configuração das VMs
🐧 Para Linux (Ubuntu/Debian)
bash

sudo apt update
sudo apt install openssh-server vsftpd -y
sudo systemctl enable --now ssh
sudo systemctl enable --now vsftpd

    Certifique-se de que o firewall permita SSH (porta 22) e FTP (porta 21).

🪟 Para Windows

    Ativar Telnet:

        Painel de Controle > Programas > Ativar/desativar recursos do Windows

        Marque Telnet Client e Telnet Server

    Configurar Firewall:
    powershell

    netsh advfirewall firewall add rule name="Allow Telnet" dir=in action=allow protocol=TCP localport=23
    netsh advfirewall firewall add rule name="Allow FTP" dir=in action=allow protocol=TCP localport=21

    Instalar um servidor FTP (ex: FileZilla Server)

🚀 Como Executar

    Edite main.py e ajuste:
    python

machines = [
    MachineMonitor('192.168.1.101', 'linux', 'usuario_linux', 'senha_linux'),
    MachineMonitor('192.168.1.102', 'linux', 'usuario_linux2', 'senha_linux2'),
    MachineMonitor('192.168.1.103', 'windows', 'usuario_windows', 'senha_windows')
]

    Substitua IPs, usuários e senhas conforme suas VMs.

Execute o monitoramento:
bash

    python main.py

🔧 Funcionamento

✔ Coleta automática de:

    Uso de CPU (%)

    Uso de memória (%)

    Espaço em disco (%)

    Dados de rede (opcional)

✔ Logs são gerados em:

    Linux: /tmp/monitor_log.txt

    Windows: C:\monitor_log.txt

✔ Reinicialização segura:

    Scripts são injetados na inicialização (cron no Linux / Registro no Windows).
