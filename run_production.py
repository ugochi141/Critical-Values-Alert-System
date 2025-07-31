"""
Production runner for Critical Values Alert System
Handles connection issues and provides automatic recovery
"""

import subprocess
import time
import sys
import os
import signal
import psutil

class StreamlitRunner:
    def __init__(self, app_path="app.py", port=8501):
        self.app_path = app_path
        self.port = port
        self.process = None
        self.restart_count = 0
        self.max_restarts = 5
        
    def kill_existing_processes(self):
        """Kill any existing Streamlit processes on the specified port"""
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                # Check if process is using our port
                if 'streamlit' in proc.info['name'].lower():
                    for conn in proc.connections('inet'):
                        if conn.laddr.port == self.port:
                            print(f"Killing existing Streamlit process (PID: {proc.info['pid']})")
                            proc.kill()
                            time.sleep(1)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
                
    def start_streamlit(self):
        """Start the Streamlit application"""
        self.kill_existing_processes()
        
        cmd = [
            sys.executable, "-m", "streamlit", "run",
            self.app_path,
            "--server.port", str(self.port),
            "--server.address", "0.0.0.0",
            "--server.headless", "true",
            "--browser.gatherUsageStats", "false",
            "--server.runOnSave", "true",
            "--server.allowRunOnSave", "true",
            "--server.fileWatcherType", "auto",
            "--server.enableCORS", "false",
            "--server.enableXsrfProtection", "false"
        ]
        
        print(f"Starting Streamlit app on port {self.port}...")
        self.process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            bufsize=1
        )
        
        # Wait for startup
        time.sleep(3)
        
        if self.process.poll() is None:
            print(f"✅ Streamlit app is running at http://localhost:{self.port}")
            return True
        else:
            print("❌ Failed to start Streamlit app")
            return False
            
    def monitor_and_restart(self):
        """Monitor the Streamlit process and restart if needed"""
        print("\nMonitoring Streamlit app... Press Ctrl+C to stop")
        
        try:
            while True:
                if self.process.poll() is not None:
                    # Process has terminated
                    print("\n⚠️  Streamlit process terminated unexpectedly")
                    
                    if self.restart_count < self.max_restarts:
                        self.restart_count += 1
                        print(f"Attempting restart {self.restart_count}/{self.max_restarts}...")
                        
                        time.sleep(2)  # Brief pause before restart
                        
                        if self.start_streamlit():
                            print("✅ Successfully restarted")
                        else:
                            print("❌ Restart failed")
                            break
                    else:
                        print("❌ Maximum restart attempts reached. Exiting.")
                        break
                        
                # Check every 5 seconds
                time.sleep(5)
                
                # Reset restart count after 5 minutes of stable operation
                if self.restart_count > 0:
                    self.restart_count = max(0, self.restart_count - 0.1)
                    
        except KeyboardInterrupt:
            print("\n\nShutting down Streamlit app...")
            self.shutdown()
            
    def shutdown(self):
        """Gracefully shutdown the Streamlit process"""
        if self.process and self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
            print("✅ Streamlit app stopped")
            
    def run(self):
        """Main entry point"""
        print("🚀 Critical Values Alert System - Production Runner")
        print("=" * 50)
        
        if self.start_streamlit():
            self.monitor_and_restart()
        else:
            print("❌ Failed to start application")
            sys.exit(1)

if __name__ == "__main__":
    # Check if app.py exists
    if not os.path.exists("app.py"):
        print("❌ Error: app.py not found in current directory")
        sys.exit(1)
        
    # Create and run the Streamlit runner
    runner = StreamlitRunner("app.py", port=8501)
    runner.run()