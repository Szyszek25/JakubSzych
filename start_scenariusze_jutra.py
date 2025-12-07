#!/usr/bin/env python3
"""
🚀 Scenariusze Jutra - Główny plik uruchomieniowy
Uruchamia backend API i frontend w jednym pipeline
"""

import os
import sys
import subprocess
import time
import signal
import platform
from pathlib import Path

# Kolory dla terminala
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

# Windows nie obsługuje ANSI colors domyślnie
if platform.system() == 'Windows':
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except:
        # Fallback - wyłącz kolory
        for attr in dir(Colors):
            if not attr.startswith('_'):
                setattr(Colors, attr, '')

# Ścieżki
BASE_DIR = Path(__file__).parent.absolute()
BACKEND_DIR = BASE_DIR / "SCENARIUSZE_JUTRA"
FRONTEND_DIR = BASE_DIR / "dashboard-frontend"

# Procesy
backend_process = None
frontend_process = None

def print_header():
    """Wyświetl nagłówek"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*70}")
    print("🌍 SCENARIUSZE JUTRA - SYSTEM ANALIZY FORESIGHTOWEJ")
    print("="*70)
    print(f"{Colors.RESET}")
    print(f"{Colors.BLUE}Uruchamianie całego systemu (Backend + Frontend){Colors.RESET}\n")

def check_requirements():
    """Sprawdź wymagania systemowe"""
    print(f"{Colors.YELLOW}🔍 Sprawdzanie wymagań...{Colors.RESET}")
    
    errors = []
    
    # Sprawdź Python
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 9):
        errors.append(f"❌ Python 3.9+ wymagany (obecny: {python_version.major}.{python_version.minor})")
    else:
        print(f"  ✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Sprawdź backend venv
    venv_python = BACKEND_DIR / "venv" / "Scripts" / "python.exe" if platform.system() == 'Windows' else BACKEND_DIR / "venv" / "bin" / "python"
    if not venv_python.exists():
        errors.append(f"❌ Backend venv nie istnieje! Uruchom: cd {BACKEND_DIR} && python -m venv venv")
    else:
        print(f"  ✅ Backend venv istnieje")
    
    # Sprawdź frontend node_modules
    node_modules = FRONTEND_DIR / "node_modules"
    if not node_modules.exists():
        errors.append(f"❌ Frontend node_modules nie istnieje! Uruchom: cd {FRONTEND_DIR} && npm install")
    else:
        print(f"  ✅ Frontend node_modules istnieje")
    
    # Sprawdź czy porty są wolne
    import socket
    def is_port_free(port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind(('localhost', port))
            sock.close()
            return True
        except:
            return False
    
    if not is_port_free(8002):
        print(f"  ⚠️  Port 8002 jest zajęty - próbuję znaleźć i zatrzymać proces...")
        # Spróbuj znaleźć i zabić proces używający portu 8002
        if platform.system() == 'Windows':
            try:
                import subprocess
                # Znajdź PID procesu używającego portu 8002
                result = subprocess.run(
                    ['netstat', '-ano'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                for line in result.stdout.split('\n'):
                    if ':8002' in line and 'LISTENING' in line:
                        parts = line.split()
                        if len(parts) > 4:
                            pid = parts[-1]
                            print(f"  🔍 Znaleziono proces PID: {pid}")
                            # Zabij proces
                            try:
                                subprocess.run(['taskkill', '/F', '/PID', pid], 
                                             capture_output=True, timeout=5)
                                print(f"  ✅ Proces {pid} zatrzymany")
                                time.sleep(2)  # Czekaj na zwolnienie portu
                                if is_port_free(8002):
                                    print(f"  ✅ Port 8002 jest teraz wolny")
                                    break
                            except:
                                print(f"  ⚠️  Nie udało się zatrzymać procesu {pid}")
                                errors.append(f"❌ Port 8002 jest zajęty przez proces PID: {pid}. Zatrzymaj go ręcznie: taskkill /F /PID {pid}")
                if not is_port_free(8002):
                    errors.append(f"❌ Port 8002 jest nadal zajęty. Zatrzymaj proces ręcznie lub użyj innego portu.")
            except Exception as e:
                errors.append(f"❌ Port 8002 jest zajęty. Zatrzymaj proces ręcznie: taskkill /F /PID <PID>")
        else:
            # Linux/Mac
            try:
                import subprocess
                result = subprocess.run(
                    ['lsof', '-ti:8002'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    pid = result.stdout.strip()
                    print(f"  🔍 Znaleziono proces PID: {pid}")
                    subprocess.run(['kill', '-9', pid], timeout=5)
                    print(f"  ✅ Proces {pid} zatrzymany")
                    time.sleep(2)
            except:
                pass
            if not is_port_free(8002):
                errors.append(f"❌ Port 8002 jest zajęty. Zatrzymaj proces ręcznie: kill -9 $(lsof -ti:8002)")
    else:
        print(f"  ✅ Port 8002 jest wolny")
    
    if not is_port_free(5173):
        print(f"  ⚠️  Port 5173 jest zajęty (Vite użyje następnego dostępnego)")
    
    if errors:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ BŁĘDY:{Colors.RESET}")
        for error in errors:
            print(f"  {error}")
        print(f"\n{Colors.YELLOW}Napraw błędy i uruchom ponownie.{Colors.RESET}\n")
        return False
    
    print(f"{Colors.GREEN}✅ Wszystkie wymagania spełnione!{Colors.RESET}\n")
    return True

def start_backend():
    """Uruchom backend API"""
    global backend_process
    
    print(f"{Colors.CYAN}🚀 Uruchamianie Backend API (port 8002)...{Colors.RESET}")
    
    venv_python = BACKEND_DIR / "venv" / "Scripts" / "python.exe" if platform.system() == 'Windows' else BACKEND_DIR / "venv" / "bin" / "python"
    api_file = BACKEND_DIR / "api_scenarios.py"
    
    if not venv_python.exists():
        print(f"  {Colors.RED}❌ Backend venv nie istnieje: {venv_python}{Colors.RESET}")
        return False
    
    if not api_file.exists():
        print(f"  {Colors.RED}❌ Plik API nie istnieje: {api_file}{Colors.RESET}")
        return False
    
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    
    try:
        # Uruchom backend - użyj None dla stdout żeby widzieć output na żywo
        # Ale najpierw sprawdźmy czy backend się uruchomi poprawnie
        print(f"  🔧 Uruchamianie: {venv_python} {api_file}")
        
        backend_process = subprocess.Popen(
            [str(venv_python), str(api_file)],
            cwd=str(BACKEND_DIR),
            env=env,
            stdout=None,  # Wyświetlaj output na żywo
            stderr=subprocess.STDOUT,
            text=True
        )
        
        # Czekaj na start backendu i sprawdź czy odpowiada na HTTP
        print(f"  ⏳ Czekam na start backendu (max 20 sekund)...")
        
        import socket
        import urllib.request
        import urllib.error
        
        max_attempts = 20
        for attempt in range(max_attempts):
            time.sleep(1)
            
            # Sprawdź czy proces jeszcze działa
            if backend_process.poll() is not None:
                # Proces zakończył się - sprawdź kod wyjścia
                exit_code = backend_process.returncode
                print(f"  {Colors.RED}❌ Backend zakończył się z kodem: {exit_code}{Colors.RESET}")
                print(f"  {Colors.YELLOW}Sprawdź output powyżej dla szczegółów błędu{Colors.RESET}")
                print(f"  {Colors.YELLOW}Możesz też uruchomić ręcznie: cd {BACKEND_DIR} && {venv_python} {api_file}{Colors.RESET}")
                return False
            
            # Sprawdź czy backend odpowiada na HTTP
            try:
                response = urllib.request.urlopen('http://localhost:8002/', timeout=2)
                if response.getcode() == 200:
                    print(f"  {Colors.GREEN}✅ Backend API uruchomiony{Colors.RESET}")
                    print(f"  📡 API: {Colors.CYAN}http://localhost:8002{Colors.RESET}")
                    print(f"  📚 Docs: {Colors.CYAN}http://localhost:8002/docs{Colors.RESET}\n")
                    return True
            except (urllib.error.URLError, socket.timeout, ConnectionRefusedError):
                # Backend jeszcze nie odpowiada, kontynuuj czekanie
                if attempt % 3 == 0 and attempt < max_attempts - 1:
                    print(f"  ⏳ Czekam... ({attempt + 1}/{max_attempts})")
                continue
        
        # Backend nie odpowiedział w czasie, ale proces może jeszcze działać
        if backend_process.poll() is None:
            print(f"  {Colors.YELLOW}⚠️  Backend nie odpowiedział w ciągu {max_attempts} sekund, ale proces działa{Colors.RESET}")
            print(f"  {Colors.YELLOW}Sprawdź czy backend uruchomił się poprawnie w output powyżej{Colors.RESET}")
            # Spróbuj jeszcze raz sprawdzić po dodatkowej sekundzie
            time.sleep(2)
            try:
                response = urllib.request.urlopen('http://localhost:8002/', timeout=2)
                if response.getcode() == 200:
                    print(f"  {Colors.GREEN}✅ Backend API uruchomiony (po dłuższym czasie){Colors.RESET}")
                    return True
            except:
                pass
        
        print(f"  {Colors.RED}❌ Backend nie odpowiedział na http://localhost:8002/{Colors.RESET}")
        return False
            
    except Exception as e:
        print(f"  {Colors.RED}❌ Błąd uruchamiania backendu: {e}{Colors.RESET}")
        import traceback
        print(f"  {Colors.YELLOW}{traceback.format_exc()}{Colors.RESET}")
        return False

def start_frontend():
    """Uruchom frontend"""
    global frontend_process
    
    print(f"{Colors.CYAN}🚀 Uruchamianie Frontend (Vite)...{Colors.RESET}")
    
    npm_cmd = "npm.cmd" if platform.system() == 'Windows' else "npm"
    
    try:
        # Uruchom frontend z wyświetlaniem outputu na żywo
        frontend_process = subprocess.Popen(
            [npm_cmd, "run", "dev"],
            cwd=str(FRONTEND_DIR),
            stdout=None,  # Wyświetlaj output na żywo
            stderr=subprocess.STDOUT,
            text=True
        )
        
        # Czekaj na start frontendu
        print(f"  ⏳ Czekam na start frontendu (max 15 sekund)...")
        time.sleep(5)
        
        # Sprawdź czy proces działa
        if frontend_process.poll() is None:
            print(f"  {Colors.GREEN}✅ Frontend uruchomiony{Colors.RESET}")
            print(f"  🌐 Frontend: {Colors.CYAN}http://localhost:5173{Colors.RESET} (lub następny dostępny port)")
            print(f"  {Colors.YELLOW}Sprawdź output powyżej dla dokładnego adresu URL{Colors.RESET}\n")
            return True
        else:
            exit_code = frontend_process.returncode
            print(f"  {Colors.RED}❌ Frontend nie uruchomił się poprawnie (kod: {exit_code}){Colors.RESET}")
            print(f"  {Colors.YELLOW}Sprawdź output powyżej dla szczegółów błędu{Colors.RESET}")
            return False
            
    except Exception as e:
        print(f"  {Colors.RED}❌ Błąd uruchamiania frontendu: {e}{Colors.RESET}")
        import traceback
        print(f"  {Colors.YELLOW}{traceback.format_exc()}{Colors.RESET}")
        return False

def cleanup():
    """Zatrzymaj wszystkie procesy"""
    global backend_process, frontend_process
    
    print(f"\n{Colors.YELLOW}🛑 Zatrzymywanie procesów...{Colors.RESET}")
    
    if backend_process:
        try:
            backend_process.terminate()
            backend_process.wait(timeout=5)
            print(f"  ✅ Backend zatrzymany")
        except:
            backend_process.kill()
            print(f"  ⚠️  Backend wymuszony do zatrzymania")
    
    if frontend_process:
        try:
            frontend_process.terminate()
            frontend_process.wait(timeout=5)
            print(f"  ✅ Frontend zatrzymany")
        except:
            frontend_process.kill()
            print(f"  ⚠️  Frontend wymuszony do zatrzymania")
    
    print(f"{Colors.GREEN}✅ Wszystkie procesy zatrzymane{Colors.RESET}\n")

def signal_handler(sig, frame):
    """Obsługa sygnałów (Ctrl+C)"""
    cleanup()
    sys.exit(0)

def main():
    """Główna funkcja"""
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print_header()
    
    # Sprawdź wymagania
    if not check_requirements():
        sys.exit(1)
    
    # Uruchom backend
    if not start_backend():
        cleanup()
        sys.exit(1)
    
    # Uruchom frontend
    if not start_frontend():
        cleanup()
        sys.exit(1)
    
    # Wyświetl informacje
    print(f"{Colors.GREEN}{Colors.BOLD}{'='*70}")
    print("✅ SYSTEM URUCHOMIONY POMYŚLNIE!")
    print("="*70)
    print(f"{Colors.RESET}")
    print(f"{Colors.CYAN}📡 Backend API:{Colors.RESET} http://localhost:8002")
    print(f"{Colors.CYAN}📚 Dokumentacja API:{Colors.RESET} http://localhost:8002/docs")
    print(f"{Colors.CYAN}🌐 Frontend:{Colors.RESET} http://localhost:5173 (lub następny dostępny port)")
    print(f"\n{Colors.YELLOW}Naciśnij Ctrl+C aby zatrzymać wszystkie serwisy{Colors.RESET}\n")
    
    # Monitoruj procesy (output jest już wyświetlany na żywo bo stdout=None)
    try:
        while True:
            time.sleep(1)
            
            # Sprawdź czy backend działa
            if backend_process and backend_process.poll() is not None:
                print(f"\n{Colors.RED}❌ Backend zatrzymał się nieoczekiwanie!{Colors.RESET}")
                print(f"  {Colors.YELLOW}Kod wyjścia: {backend_process.returncode}{Colors.RESET}")
                cleanup()
                sys.exit(1)
            
            # Sprawdź czy frontend działa
            if frontend_process and frontend_process.poll() is not None:
                print(f"\n{Colors.RED}❌ Frontend zatrzymał się nieoczekiwanie!{Colors.RESET}")
                cleanup()
                sys.exit(1)
                
    except KeyboardInterrupt:
        pass
    finally:
        cleanup()

if __name__ == "__main__":
    main()

