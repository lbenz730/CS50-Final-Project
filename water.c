#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int n;
    //Get user input and reject if negative
    do
    {
    printf("Minutes: ");
    n = get_int();
    }
    while(n < 0);
    
    //Caculate Bottles used and print result
    printf("Bottles: %i\n", 12*n);
    
}
