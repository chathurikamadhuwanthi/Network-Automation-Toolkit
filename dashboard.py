from flask import Flask, render_template_string
import psutil
import subprocess

app = Flask(__name__)

def get_system_stats():
         cpu = psutil.cpu_percent(interval=1)
         ram = psutil.virtual_memory().percent
         disk = psutil.disk_usage('/').percent
         return cpu, ram, disk

def check_service(service_name):
         result = subprocess.run(
            ["systemctl", "is-active", service_name],
             capture_output=True, text=True

         )
         return result.stdout.strip()

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
   <title>Network Monitor Dashboard</title>
   <metaa http-equiv="refresh' content="5">
   <style>
       
       body{font-family: Arial; background:#1e1e2f; color: white; margin: 0; min-height: 100hv; display: flex; flex-direction: column; align-items:center; text-align:center; padding: 60px 20px 30px; }
       .card  {background: #2a2a40; display: inline-block; padding:30px 50px; border-radius: 12px; margin: 10px; }
       .status-activ]e { color:#4ade80; font-weight: bold; }
       .status-inactive { color: #f87171; font-weight: bold;}
       h1 { color:#60a5fa;}
  </style>
</head>  
<body>
  <h1>Network Automation Monitor</h1>
  <div class="card"><h2>CPU</h2><p>{{ cpu }}%</p></div>
  <div class="card"><h2>RAM</h2><p>{{ ram }}%</p></div>
  <div class="card"><h2>Disk</h2><p>{{ disk }}%</p></div>
  <div class="card"><h2>SSH Service</h2>
        <p class="{{ 'status-active' if ssh_status == 'active' else 'status-inactive' }}">
             {{' ACTIVE ' if ssh_status == 'active' else 'INACTIVE' }}
       </p>
  </div>
</body>
</html>
"""

@app.route('/')
def dashboard():
     cpu, ram, disk = get_system_stats()
     ssh_status = check_service("ssh")
     return render_template_string(HTML_PAGE, cpu=cpu, ram=ram, disk=disk, ssh_status=ssh_status)

if  __name__ == "__main__":
     app.run(host='0.0.0.0', port=5000)
   



