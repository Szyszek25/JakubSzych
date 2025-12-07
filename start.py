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
        errors.append(f"❌ Port 8002 jest zajęty! Zatrzymaj inne aplikacje używające tego portu.")
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
    
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    
    try:
        backend_process = subprocess.Popen(
            [str(venv_python), str(api_file)],
            cwd=str(BACKEND_DIR),
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        # Czekaj na start backendu (sprawdź czy odpowiada)
        print(f"  ⏳ Czekam na start backendu...")
        time.sleep(3)
        
        # Sprawdź czy proces działa
        if backend_process.poll() is None:
            print(f"  {Colors.GREEN}✅ Backend API uruchomiony{Colors.RESET}")
            print(f"  📡 API: {Colors.CYAN}http://localhost:8002{Colors.RESET}")
            print(f"  📚 Docs: {Colors.CYAN}http://localhost:8002/docs{Colors.RESET}\n")
            return True
        else:
            print(f"  {Colors.RED}❌ Backend nie uruchomił się poprawnie{Colors.RESET}")
            return False
            
    except Exception as e:
        print(f"  {Colors.RED}❌ Błąd uruchamiania backendu: {e}{Colors.RESET}")
        return False

def start_frontend():
    """Uruchom frontend"""
    global frontend_process
    
    print(f"{Colors.CYAN}🚀 Uruchamianie Frontend (Vite)...{Colors.RESET}")
    
    npm_cmd = "npm.cmd" if platform.system() == 'Windows' else "npm"
    
    try:
        frontend_process = subprocess.Popen(
            [npm_cmd, "run", "dev"],
            cwd=str(FRONTEND_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        # Czekaj na start frontendu
        print(f"  ⏳ Czekam na start frontendu...")
        time.sleep(5)
        
        # Sprawdź czy proces działa
        if frontend_process.poll() is None:
            print(f"  {Colors.GREEN}✅ Frontend uruchomiony{Colors.RESET}")
            print(f"  🌐 Frontend: {Colors.CYAN}http://localhost:5173{Colors.RESET} (lub następny dostępny port)\n")
            return True
        else:
            print(f"  {Colors.RED}❌ Frontend nie uruchomił się poprawnie{Colors.RESET}")
            return False
            
    except Exception as e:
        print(f"  {Colors.RED}❌ Błąd uruchamiania frontendu: {e}{Colors.RESET}")
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
    
    # Monitoruj procesy
    try:
        while True:
            time.sleep(1)
            
            # Sprawdź czy backend działa
            if backend_process and backend_process.poll() is not None:
                print(f"\n{Colors.RED}❌ Backend zatrzymał się nieoczekiwanie!{Colors.RESET}")
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

