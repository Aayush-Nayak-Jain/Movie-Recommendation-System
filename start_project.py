import os
import webbrowser
import subprocess
import time
from sys import exit

def run_django_server():
    if not os.path.exists('manage.py'):
        print("Error: manage.py not found in the current directory!")
        input("Press Enter to exit...")
        exit(1)
    
    print("Starting Django development server...")
    
    # Start the server without auto-reloader for cleaner exit
    server_process = subprocess.Popen(
        ['python', 'manage.py', 'runserver', '--noreload'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait 2 seconds to ensure server is ready before opening browser
    time.sleep(2)
    webbrowser.open_new_tab("http://127.0.0.1:8000")
    
    try:
        # Print server output in real-time
        while True:
            output = server_process.stdout.readline()
            if output == '' and server_process.poll() is not None:
                break
            if output:
                print(output.strip())
    except KeyboardInterrupt:
        print("\nStopping server...")
        server_process.terminate()
        exit(0)

if __name__ == "__main__":
    run_django_server()