import os
import subprocess
import signal

class UpgradedWirelessAuditor:
    def __init__(self, interface: str = "wlan0mon"):
        self.interface = interface
        self.active_processes = []

    def enable_monitor_mode(self, raw_interface: str):
        try:
            subprocess.run(["sudo", "airmon-ng", "check", "kill"], check=True)
            subprocess.run(["sudo", "airmon-ng", "start", raw_interface], check=True)
            self.interface = f"{raw_interface}mon"
            return {"status": "SUCCESS", "active_interface": self.interface}
        except Exception as e:
            return {"status": "FAILED", "error": str(e)}

    def capture_handshake(self, bssid: str, channel: str, output_prefix: str):
        cmd = ["sudo", "airodump-ng", "--bssid", bssid, "-c", channel, "-w", f"static/network_logs/{output_prefix}", self.interface]
        proc = subprocess.Popen(cmd, preexec_fn=os.setsid)
        self.active_processes.append(proc)
        return {"status": "CAPTURING_STARTED", "process_id": proc.pid}

    def stop_all_audits(self):
        for proc in self.active_processes:
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
            except:
                pass
        self.active_processes = []
        return {"status": "CLEANED_UP"}
