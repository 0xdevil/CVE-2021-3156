all:

	gcc -o exploit exploit.c -s
	gcc -shared -o libnss_XXXXXXX/XXXXXX.so.2 -fPIC libnss_XXXXXXX/XXXXXX.c

clean:

	rm exploit
	rm libnss_XXXXXXX/XXXXXX.so.2
