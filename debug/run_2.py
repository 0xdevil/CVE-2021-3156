import subprocess, signal

cmd = ['./test']
env = {}

p = subprocess.Popen(cmd, env=env)
p.send_signal(signal.SIGSTOP)

input('[+] Attach GDB')
