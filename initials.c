/**
 * initials.c
 *
 * Prints initials of entered name
 */
 
#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

int main(void)
{
    string name = get_string();
    
    // Loop over characters in name 
    for(int i = 0, n = strlen(name); i < n; i++)
    {
    // If character is a space, print next character in uppercase
        if(name[i] == ' ')
        { 
            printf("%c", toupper(name[i+1]));
        }
        // Cover cases where first char is initial 
        else if(name[i] != ' ' && i == 0)
        {
            printf("%c", toupper(name[i]));
        }
    }
    
    printf("\n");
}
