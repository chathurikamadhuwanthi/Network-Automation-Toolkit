import psutil
import subprocess
import time

def get_system_stats():
      cpu =  psutil.cpu_percent(interval=1)
      ram = psutil.virtual_memory().percent
      disk = psutil.disk_usage('/').percent
      return cpu, ram, disk

def check_service(service_name):
     result = subprocess.run(
            ["systemctl", "is-active", service_name],
             capture_output=True, text=True
     )
     return result.stdout.strip()

def restart_service(service_name):
    print(f"  {service_name.upper()} DOWN detected! Restarting...")
    subprocess.run(["sudo", "systemctl", "restart", service_name])
     
def monitor():
     print("starting system monitor ...(ctrl+c to stop)")
     while True:
           cpu, ram, disk = get_system_stats()
           ssh_status = check_service("ssh")

           if ssh_status != "active":
              restart_service("ssh")
              ssh_status = check_service("ssh")

           status_label = "ACTIVE " if ssh_status == "active"  else "INACTIVE "
           print(f"CPU: {cpu}% | RAM: {ram}% | Disk: {disk}% | SSH Service: {status_label}")
           time.sleep(5)

if __name__ == "__main__":
    monitor() 
