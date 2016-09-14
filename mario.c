#include <stdio.h>
#include <cs50.h>

int main(void) 
{
    int n; 
    
    //Get Height from user and reject if not between 0-23
    do 
    {
        printf("Height: ");
        n = get_int();
    }
    while(n < 0 || n > 23);
    
    //Iteratively print spaces and hashes for the specified height of the pyramid
    for(int i = 0; i < n; i++)
    {
       //Print Spaces
        for(int j = 0; j < n-(i+1); j++)
        {
            printf(" ");
        
        }
        
        //Print Hashes
        for(int k = 0; k < 2 + i; k++)
        {
            printf("#");
        
        }
        
        //Move to next line
        printf("\n");
        
    }
}