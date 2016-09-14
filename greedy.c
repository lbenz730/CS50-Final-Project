#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void) 
{
    
    //Get amount of change to return
    float change;
    do
    {
        printf("How much change is owed?\n");
        change = get_float();
    }
    while (change < 0);
    
    //Converts change to cents
    int cents = round(change*100);

    
    int coins = 0;

    
    //Return quarters
    while(cents >= 25)
    {
        cents -= 25;
        coins++;
    }
    
    //Return dimes
     while(cents >= 10)
    {
        cents -= 10;
        coins++;
    }
    
    //Return nickles
    while(cents >= 5)
    {
        cents -= 5;
        coins++;
    }
    
    //Return pennies
     while(cents >= 1)
    {
        cents -= 1;
        coins++;
    }
 
 
    //Print result
    printf("%i\n", coins);
 
  
}