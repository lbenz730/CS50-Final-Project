/**
 * vigenere.c
 *
 * Scrambles a message using vigenere cipher
 *
 * Usage: ./vigenere k
 *
 * where k is a single keyword of alphbetical characters
 */

#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    // Print error message and quit if user didn't enter the correct number fo command line arguments
    if(argc != 2)
    {
        printf("Usage: ./vigenere k\n");
        return 1;
    }
    
    string key = argv[1];
    
    // Loop over characters to make sure that they're alphabetical
    for(int i=0, n = strlen(key); i < n; i++)
    {
        if(!isalpha(key[i]))
        {
            printf("Usage: ./vigenere k\n");
            return 1;
        }
    }
 
    printf("plaintext:");
    string p = get_string();
    printf("ciphertext:");
    
    int shift;
    int keyLength = strlen(key);
    
    // Loop over chartacters in plaintext
    for (int i = 0, n = strlen(p), j = 0; i < n; i++)
    {
        // Get alphabetical index of the j'th character in the key
        if(isupper(key[j%keyLength]))
        {
            shift = key[j%keyLength] - 'A';
        }
        else
        {
            shift = key[j%keyLength] - 'a';    
        }
        
        // Check if i'th character in p is alphabetical
        if(isalpha(p[i]))
        {
           // Determine the case of the letter and handle accordingly
            if(isupper(p[i]))
            {
                // Convert the character index from ASCII to alphbatized. Shift it by the key and print the result 
                printf("%c", (p[i] - 'A' + shift) % 26 + 'A');
                j++;
                 
            }
            else
            {
                printf("%c", (p[i]- 'a' + shift) % 26 + 'a');
                j++;
                 
            }
        }
        // If character isn't alphabetical, go ahead and print it out as is
        else
        {
            printf("%c", p[i]);
        }
    }

    printf("\n");
}