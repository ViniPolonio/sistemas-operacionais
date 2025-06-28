import os
import threading
import paramiko
import telnetlib
import time
import hashlib
from datetime import datetime

class PDFCollector:
    def __init__(self):
        self.file_structures = {}
        self.running = False
        self.setup_vms()
        
    def setup_vms(self):
        self.vms = [
            {
                "host": "192.168.1.101",
                "os": "linux",
                "user": "user1",
                "pass": "senha1",
                "conn": None,
                "last_scan": None
            },
            {
                "host": "192.168.1.102",
                "os": "linux", 
                "user": "user2",
                "pass": "senha2",
                "conn": None,
                "last_scan": None
            },
            {
                "host": "192.168.1.103",
                "os": "windows",
                "user": "user3",
                "pass": "senha3",
                "conn": None,
                "last_scan": None
            }
        ]
        
    def connect(self, vm):
        try:
            if vm['os'] == 'linux':
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(vm['host'], 
                           username=vm['user'],
                           password=vm['pass'],
                           timeout=10)
                vm['conn'] = {'ssh': ssh}
                return True
            else:
                tn = telnetlib.Telnet(vm['host'], timeout=10)
                tn.read_until(b"login: ", timeout=5)
                tn.write(vm['user'].encode() + b"\n")
                tn.read_until(b"Password: ", timeout=5)
                tn.write(vm['pass'].encode() + b"\n")
                tn.write(b"echo %USERNAME%\n")
                if tn.read_until(b"%USERNAME%", timeout=3):
                    vm['conn'] = {'telnet': tn}
                    return True
        except Exception as e:
            print(f"Erro ao conectar em {vm['host']}: {str(e)}")
            return False
    
    def disconnect(self, vm):
        if vm['conn']:
            if 'ssh' in vm['conn']:
                vm['conn']['ssh'].close()
            elif 'telnet' in vm['conn']:
                vm['conn']['telnet'].close()
            vm['conn'] = None
    
    def list_files_manual(self, vm, path):
        files = []
        try:
            if vm['os'] == 'linux':
                if not vm['conn'] or 'ssh' not in vm['conn']:
                    if not self.connect(vm):
                        return []
                
                stdin, stdout, stderr = vm['conn']['ssh'].exec_command(
                    f'find "{path}" -type f -name "*.pdf" 2>/dev/null')
                files = stdout.read().decode().splitlines()
            else:
                if not vm['conn'] or 'telnet' not in vm['conn']:
                    if not self.connect(vm):
                        return []
                
                vm['conn']['telnet'].write(
                    f'dir /s /b "{path}\\*.pdf"\r\n'.encode())
                time.sleep(1)
                output = vm['conn']['telnet'].read_very_eager().decode()
                files = [line.strip() for line in output.splitlines() 
                        if line.strip() and line.lower().endswith('.pdf')]
        
        except Exception as e:
            print(f"Erro ao listar arquivos em {vm['host']}: {str(e)}")
        
        return files
    
    def get_file_metadata(self, vm, file_path):
        try:
            if vm['os'] == 'linux':
                cmd = f'stat -c "%s %Y" "{file_path}"'
                stdin, stdout, stderr = vm['conn']['ssh'].exec_command(cmd)
                size, mtime = stdout.read().decode().strip().split()
            else:
                vm['conn']['telnet'].write(
                    f'for %i in ("{file_path}") do echo %~zi %~ti\r\n'.encode())
                time.sleep(0.5)
                output = vm['conn']['telnet'].read_very_eager().decode()
                size, mtime = output.strip().split()[:2]
            
            return {
                'size': int(size),
                'modified': mtime,
                'hash': hashlib.md5(file_path.encode()).hexdigest()[:8]
            }
        except:
            return None
    
    def scan_vm(self, vm):
        print(f"\n[🔍] Iniciando varredura em {vm['host']}...")
        
        if not self.connect(vm):
            print(f"[❌] Falha ao conectar em {vm['host']}")
            return
        
        search_paths = ['/home', '/var'] if vm['os'] == 'linux' else ['C:\\Users']
        
        current_files = {}
        for path in search_paths:
            for file_path in self.list_files_manual(vm, path):
                metadata = self.get_file_metadata(vm, file_path)
                if metadata:
                    current_files[file_path] = metadata
        
        changes = self.detect_changes(vm['host'], current_files)
        self.file_structures[vm['host']] = {
            'files': current_files,
            'last_scan': datetime.now().isoformat()
        }
        
        for file_path in changes['new']:
            self.analyze_pdf(vm, file_path)
        
        self.disconnect(vm)
        print(f"[✅] Varredura em {vm['host']} concluída")
    
    def detect_changes(self, host, current_files):
        previous = self.file_structures.get(host, {}).get('files', {})
        
        changes = {
            'new': [],
            'modified': [],
            'deleted': [f for f in previous if f not in current_files]
        }
        
        for file_path, data in current_files.items():
            if file_path not in previous:
                changes['new'].append(file_path)
            elif data['size'] != previous[file_path]['size'] or \
                 data['modified'] != previous[file_path]['modified']:
                changes['modified'].append(file_path)
        
        return changes
    
    def analyze_pdf(self, vm, file_path):
        print(f"\n[📄] Analisando arquivo: {file_path}")
        
        try:
            from ollama import Client
            ollama = Client(host='http://localhost:11434')
            prompt = f"Resuma o conteúdo do arquivo {os.path.basename(file_path)}"
            response = ollama.generate(model='llama2', prompt=prompt)
            
            print(f"[🔍] Tema identificado (Ollama): {response['response']}")
            print(f"[🖥️] Origem: {vm['host']} ({vm['os']})")
            print(f"[⏱️] Última modificação: {self.file_structures[vm['host']]['files'][file_path]['modified']}")
        
        except Exception as e:
            print(f"[❌] Erro ao analisar PDF: {str(e)}")
    
    def continuous_scan(self, interval=300):
        self.running = True
        while self.running:
            start_time = time.time()
            
            threads = []
            for vm in self.vms:
                t = threading.Thread(target=self.scan_vm, args=(vm.copy(),))
                t.start()
                threads.append(t)
            
            for t in threads:
                t.join()
            
            elapsed = time.time() - start_time
            sleep_time = max(0, interval - elapsed)
            
            if self.running and sleep_time > 0:
                print(f"\n[⏳] Próxima varredura em {sleep_time:.1f} segundos...")
                time.sleep(sleep_time)
    
    def run(self):
        print("""
        ██████╗ ██████╗ ███████╗     ██████╗ █████╗ ██████╗ 
        ██╔══██╗██╔══██╗██╔════╝    ██╔════╝██╔══██╗██╔══██╗
        ██████╔╝██████╔╝█████╗      ██║     ███████║██║  ██║
        ██╔═══╝ ██╔══██╗██╔══╝      ██║     ██╔══██║██║  ██║
        ██║     ██║  ██║███████╗    ╚██████╗██║  ██║██████╔╝
        ╚═╝     ╚═╝  ╚═╝╚══════╝     ╚═════╝╚═╝  ╚═╝╚═════╝ 
        """)
        print("Sistema de Coleta e Análise de PDFs em VMs\n")
        
        try:
            print("[⚡] Realizando primeira varredura completa...")
            initial_threads = []
            for vm in self.vms:
                t = threading.Thread(target=self.scan_vm, args=(vm.copy(),))
                t.start()
                initial_threads.append(t)
            
            for t in initial_threads:
                t.join()
            
            print("\n[🔁] Iniciando monitoramento contínuo...")
            self.continuous_scan()
            
        except KeyboardInterrupt:
            print("\n[🛑] Recebido comando para parar...")
            self.running = False
            for vm in self.vms:
                self.disconnect(vm)
            print("[👋] Sistema encerrado com segurança")

if __name__ == "__main__":
    collector = PDFCollector()
    collector.run()