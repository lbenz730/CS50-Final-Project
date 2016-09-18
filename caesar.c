/**
 * caesar.c
 *
 * Scrambles a message using caesar cipher
 *
 * Usage: ./vigenere k
 *
 * where k is a positive integer
 */

#include <stdio.h>
#include <cs50.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    // Print error message and quit if user didn't enter the correct number fo command line arguments
    if(argc != 2)
    {
        printf("Error: User must enter exactly one command line argument\n");
        return 1;
    }
    
    // Get key and convert it to an integer
    string k = argv[1];
    int key = atoi(k);
     
    // Print error message and return 1 if command line argument isn' integer 
    if(key == 0 && strcmp(k, "0") != 0)
    {
        printf("Usage: ./caesar k\n");
        return 1;
    }
    
   
    printf("plaintext: ");
    string p = get_string();
    printf("ciphertext: ");
    
    // Loop over chartacters in plaintext
    for (int i = 0, n = strlen(p); i < n; i++)
    {
        // Check if character is alphabetical
        if(isalpha(p[i]))
        {
           // Determine the case of the letter and handle accordingly
            if(isupper(p[i]))
            {
                //Convert the character index from ASCII to alphbatized. Shift it by the key (w/wraparound) and print ASCII result
                printf("%c", (p[i] - 'A' + key) % 26 + 'A');
            }
            else
            {
                printf("%c", (p[i] - 'a' + key) % 26 + 'a');
            }
        }
        //If character isn't alphabetical, go ahead and print it out
        else
        {
            printf("%c", p[i]);
        }
    }
    
    printf("\n");
}