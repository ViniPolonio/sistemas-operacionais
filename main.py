import threading
import paramiko
import ftplib
import telnetlib
import time
from datetime import datetime

class MachineMonitor:
    def __init__(self, host, os_type, username, password):
        self.host = host
        self.os_type = os_type
        self.username = username
        self.password = password
        self.ftp = None
        self.ssh = None
        self.telnet = None
        
    def connect(self):
        if self.os_type == 'linux':
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(self.host, username=self.username, password=self.password)
            self.ftp = ftplib.FTP(self.host)
            self.ftp.login(self.username, self.password)
        else:
            self.telnet = telnetlib.Telnet(self.host)
            self.telnet.read_until(b"login: ")
            self.telnet.write(self.username.encode('ascii') + b"\n")
            self.telnet.read_until(b"Password: ")
            self.telnet.write(self.password.encode('ascii') + b"\n")
            self.ftp = ftplib.FTP(self.host)
            self.ftp.login(self.username, self.password)
    
    def deploy_monitor_script(self):
        script_content = self._generate_script_content()
        remote_path = self._get_startup_path()
        
        with open('monitor_script.tmp', 'w') as f:
            f.write(script_content)
        
        with open('monitor_script.tmp', 'rb') as f:
            self.ftp.storbinary(f'STOR {remote_path}/monitor_script', f)
        
        if self.os_type == 'linux':
            self.ssh.exec_command(f'chmod +x {remote_path}/monitor_script')
            self.ssh.exec_command(f'echo "@reboot {remote_path}/monitor_script" | crontab -')
        else:
            self.ftp.storbinary('STOR C:\\Users\\Public\\monitor_script.bat', open('monitor_script.tmp', 'rb'))
            self.telnet.write(b'reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v Monitor /t REG_SZ /d "C:\\Users\\Public\\monitor_script.bat"\n')
    
    def collect_data(self):
        try:
            if self.os_type == 'linux':
                stdin, stdout, stderr = self.ssh.exec_command('cat /tmp/monitor_log.txt')
                data = stdout.read().decode()
                self.ssh.exec_command('echo "" > /tmp/monitor_log.txt')
            else:
                self.telnet.write(b'type C:\\monitor_log.txt\n')
                time.sleep(1)
                data = self.telnet.read_very_eager().decode()
                self.telnet.write(b'echo. > C:\\monitor_log.txt\n')
            return data
        except Exception as e:
            return f"Erro na coleta: {str(e)}"
    
    def _generate_script_content(self):
        if self.os_type == 'linux':
            return """#!/bin/bash
mkdir -p /tmp
while true; do
    MEM=$(free -m | awk 'NR==2{printf "%.2f%%", $3*100/$2}')
    CPU=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1"%"}')
    DISK=$(df -h | awk '$NF=="/"{printf "%s", $5}')
    DATE=$(date '+%Y-%m-%d %H:%M:%S')
    echo "$DATE | CPU: $CPU | MEM: $MEM | DISK: $DISK" >> /tmp/monitor_log.txt
    sleep 30
done
"""
        else:
            return """@echo off
:loop
for /f "tokens=2 delims==" %%a in ('wmic cpu get loadpercentage /value') do set CPU=%%a%%
for /f "tokens=2 delims==" %%a in ('wmic OS get FreePhysicalMemory /value') do set FREEMEM=%%a
for /f "tokens=2 delims==" %%a in ('wmic OS get TotalVisibleMemorySize /value') do set TOTALMEM=%%a
set /a MEMUSAGE=100-(FREEMEM*100/TOTALMEM)
for /f "tokens=2 delims==" %%a in ('wmic logicaldisk where "DeviceID='C:'" get FreeSpace /value') do set FREESPACE=%%a
for /f "tokens=2 delims==" %%a in ('wmic logicaldisk where "DeviceID='C:'" get Size /value') do set TOTALSIZE=%%a
set /a DISKUSAGE=100-(FREESPACE*100/TOTALSIZE)
echo %DATE% %TIME% | CPU: %CPU%%% | MEM: %MEMUSAGE%%% | DISK: %DISKUSAGE%%% >> C:\\monitor_log.txt
timeout /t 30 /nobreak >nul
goto loop
"""

    def _get_startup_path(self):
        if self.os_type == 'linux':
            return '/etc/cron.d'
        else:
            return 'C:\\Users\\Public'

def main():
    machines = [
        MachineMonitor('192.168.1.101', 'linux', 'user1', 'senha1'),
        MachineMonitor('192.168.1.102', 'linux', 'user2', 'senha2'),
        MachineMonitor('192.168.1.103', 'windows', 'user3', 'senha3')
    ]
    
    for machine in machines:
        try:
            machine.connect()
            machine.deploy_monitor_script()
            print(f"Script implantado em {machine.host}")
        except Exception as e:
            print(f"Erro em {machine.host}: {str(e)}")
    
    def collector_thread():
        while True:
            for machine in machines:
                try:
                    data = machine.collect_data()
                    print(f"Dados de {machine.host}:\n{data}")
                except Exception as e:
                    print(f"Erro ao coletar de {machine.host}: {str(e)}")
            time.sleep(60)
    
    collector = threading.Thread(target=collector_thread, daemon=True)
    collector.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Encerrando monitoramento...")

if __name__ == "__main__":
    main()