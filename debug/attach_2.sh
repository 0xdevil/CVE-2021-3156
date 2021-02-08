#!/bin/sh

gdb-pwndbg --pid=`pidof test` -x ./gdb_cmds
