#include <stdio.h>
#include <stdlib.h> 
#include <unistd.h> 

int main() {
    int i;
    system("clear");
    for (i = 1; i <= 120; i++) {
        printf("\033[41;37mI LOVE YOU <3\033[0m  ");
        fflush(stdout);
        usleep(100000); 
    }

    return 0;
}
