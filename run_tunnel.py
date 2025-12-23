import os
import sys
import time
from pyngrok import ngrok, conf
from dotenv import load_dotenv

# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True)

# Load environment variables
load_dotenv()

def start_tunnel():
    print("Iniciando script...", flush=True)
    # Check for authtoken
    token = os.environ.get("NGROK_AUTHTOKEN")
    
    try:
        if token:
            print("Configurando Authtoken...", flush=True)
            ngrok.set_auth_token(token)
            
        # Start tunnel
        print("Conectando ao Ngrok...", flush=True)
        # conf.get_default().monitor_thread = False # Prevent blocking monitor thread issues if any
        tunnel = ngrok.connect(8000)
        public_url = tunnel.public_url
        
        print("\n" + "="*60, flush=True)
        print(f" SUCESSO! O Ngrok está rodando.", flush=True)
        print(f" Copie a URL abaixo para o GitHub Secret (GENURL) e para seu .env:", flush=True)
        print(f"\n {public_url} \n", flush=True)
        print("="*60 + "\n", flush=True)
        print("Pressione Ctrl+C para encerrar o túnel.", flush=True)
        
        # Keep process alive
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nEncerrando túnel...", flush=True)
        ngrok.kill()
        sys.exit(0)
    except Exception as e:
        print(f"Erro ao iniciar ngrok: {e}", flush=True)
        # Print more details if available
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    start_tunnel()
