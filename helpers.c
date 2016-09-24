/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */
       
#include <cs50.h>
#include <stdio.h>
#include <math.h>
#include "helpers.h"

/**
 * Returns true if value is in array of n values, else false.
 */
bool search(int value, int values[], int n)
{
    // reject if n is non-positive
    if(n <= 0)
    {
        return false;
    }
    // create bounds for binary search
    int left = 0;
    int right = n - 1;
    int middle = trunc((right + left)/ 2);
    
    // search for value
    while((right - left) >= 0)
    {
        if(values[middle] == value)
        {
            return true;
        }
        else if(values[middle] > value)
        {
            right = middle - 1;
            middle = trunc((right + left) / 2);
        }
        else if(values[middle] < value)
        {
            left = middle + 1;
            middle = trunc((right + left) / 2);
        }
    }
    // return false if needle not in haystack
    return false; 
}

/**
 * Sorts array of n values.
 */
void sort(int values[], int n)
{
    for(int i = 0; i < n - 1; i++)
    {
        // create moving bounds for bubble sort
        int left = 0;
        int right = 1;
        int sorted = (n - 1 - i);
        int tmp;
        int swaps = 0;
        
        // sort array
        while(right < sorted)
        {
            // swap larger values to right
            if(values[right] < values[left])
            {
                tmp = values[right];
                values[right] = values[left];
                values[left] = tmp;
                swaps++;
            }
            left++;
            right++;
        }
        // exit if no swaps made
        if(swaps == 0)
        {
            return;
        }
    }
    return;
}
