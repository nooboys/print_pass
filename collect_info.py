# File: collect_info.py

import platform
import psutil
import paramiko
import sys
import json
import yaml
import os

class SecureConfig:
    def __init__(self, config_data):
        self._config = config_data

    def get(self, key):
        return self._config.get(key)

    def __getitem__(self, key):
        return self._config[key]

    def __str__(self):
        return "<SecureConfig: printing not allowed>"

    def __repr__(self):
        return "<SecureConfig: printing not allowed>"

def load_config(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    with open(file_path, "r") as f:
        if ext == ".json":
            return SecureConfig(json.load(f))
        elif ext in [".yaml", ".yml"]:
            return SecureConfig(yaml.safe_load(f))
        elif ext == ".txt":
            return SecureConfig(parse_txt_config(f))
        else:
            raise ValueError("Unsupported config format")

def parse_txt_config(f):
    data = {}
    for line in f:
        if "=" in line:
            k, v = line.strip().split("=", 1)
            data[k] = v
    return data

def print_local_info():
    print("\n[Agent Linux Machine Info]")
    print(f"CPU Cores       : {psutil.cpu_count(logical=True)}")
    print(f"Memory (GB)     : {round(psutil.virtual_memory().total / (1024**3), 2)}")
    print(f"OS Version      : {platform.platform()}")

def print_remote_info(ip, user, password):
    print("\n[Cloud Linux Machine Info via SSH]")
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip, username=user, password=password, timeout=10)

        cmds = {
            "CPU Cores"   : "nproc",
            "Memory (MB)" : "free -m | awk '/Mem:/ { print $2 }'",
            "OS Version": "cat /etc/os-release | grep PRETTY_NAME | cut -d '\"' -f2"
        }

        for label, cmd in cmds.items():
            try:
                stdin, stdout, stderr = ssh.exec_command(cmd)
                output = stdout.read().decode().strip()
                print(f"{label:15}: {output}")
            except Exception as inner_err:
                print(f"[WARNING] Failed to run '{label}' command: {inner_err}")

        ssh.close()
    except Exception as e:
        print(f"[WARNING] Skipped remote machine due to error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python collect_info.py <config_file>")
        sys.exit(1)

    config = load_config(sys.argv[1])
    print_local_info()
    print_remote_info(
        config.get("ip"),
        config.get("username"),
        config.get("password")
    )
