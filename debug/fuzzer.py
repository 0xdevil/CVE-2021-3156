from pwn import *
from colorama import init, Fore
from random import randint, choice
from concurrent.futures import ThreadPoolExecutor
import datetime, string

colorama = init()

SB = '\033[1m'
EB = '\033[0m'
R = Fore.RED
G = Fore.GREEN
C = Fore.CYAN
M = Fore.MAGENTA
Y = Fore.YELLOW
B = Fore.BLUE
W = Fore.WHITE

'''
Terminal #1:
    - python3 fuzzer.py SILENT

Terminal #2:
    - dmesg -w --ctime
'''

class Fuzzer:


    def __init__(self, path, options, threads, max_tries,
                        max_buff_size, max_lc_size, max_env_size, timer):

        self.path = path
        self.options = options
        self.threads = threads
        self.max_tries = max_tries
        self.max_buff_size = max_buff_size
        self.max_lc_size = max_lc_size
        self.max_env_size = max_env_size
        self.charset = string.ascii_lowercase + string.ascii_uppercase
        self.timer = timer


    def _rand_rep(self, str, min, max):
        return str * randint(min, max)


    def _rand_str(self, min, max):
        return ''.join(self.charset[randint(min, len(self.charset) - 1)]
                        for _ in range(max))


    def _mega_string(self):
        return self._rand_rep('M', 0x1000, 0x10000)


    def _rand_de_bruijn(self):
        return cyclic(alphabet=''.join(set(self._rand_str(0x8, 0x10))),
                        length=randint(1, self.max_buff_size))


    def _timestamp(self):
        return datetime.datetime.now().strftime("%H:%M:%S")


    def _dont_burn_my_pc_pls(self):
        sleep(self.timer)


    def _prepare_fuzzing(self):

        os.system('echo 9999 > /proc/sys/kernel/printk_ratelimit_burst')
        os.system('echo 0 > /proc/sys/kernel/randomize_va_space')


    def _fuzzer(self):

        for _ in range(self.max_tries):

            cmd = []
            env = {}

            env[self._rand_rep('A', 4, 8)] = self._rand_rep('A', 0x8, self.max_env_size)
            env['SUDO_ASKPASS'] = '/bin/false'
            env['LC_TIME'] = 'C.UTF-8@' + self._rand_rep('A', 0x10, self.max_lc_size)

            cmd.append(self.path)
            cmd.extend(self.options)
            cmd.append(self._rand_rep('C', 0x10, self.max_buff_size) + '\\')

            self._dont_burn_my_pc_pls()

            io = process(cmd, env=env)
            status = io.poll()
            io.close()

            if status == -11:
                print(f'[{SB}{B}{self._timestamp()}{W}{EB}]'
                      f'[{SB}{R}SIGSEV{W}{EB}]: '
                      f'CMD = {cmd}, env = {env}')


    def start(self):

        self._prepare_fuzzing()

        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            for _ in range(self.threads): executor.submit(self._fuzzer)



Fuzzer( path='/usr/bin/sudoedit',
        options=['-A', '-s'],
        threads=16,
        max_tries=10000000,
        max_buff_size=0x100,
        max_lc_size=0x100,
        max_env_size=0x1000,
        timer=0.5 ).start()
