#!/bin/sh

gdb-pwndbg --pid=`pidof sudoedit` -x ./gdb_cmds
