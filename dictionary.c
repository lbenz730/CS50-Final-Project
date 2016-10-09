/**
 * Luke Benz
 * 
 * CS50 pset 5
 * 
 * Implements a dictionary's functionality.
 */

#include <stdbool.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

#include "dictionary.h"

#define SIZE 143093
int wordcount = 0;

// declare hash function (given to me by my TA)
unsigned int hash(const char *s)
{
    unsigned int hash = 5381;
    int c;
    while ((c = (tolower(*s++))))
        hash = ((hash << 5) + hash) + c; /* hash * 33 + c */

    return hash % SIZE;
}

// create node struct
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// create hastable and initialize pointers to NULL
node *hashtable[SIZE] = {};

/**
 * Returns true if word is in dictionary else false.
 */
bool check(const char *word)
{
    // convert word to lowercase for correct lookup
    char lookup[LENGTH + 1];
    for(int i = 0; i <= strlen(word); i++)
    {
         lookup[i] = tolower(word[i]);
    }
    // iterate over words in correct bucket of hashtable
    for(node *cursor = hashtable[hash(word)]; cursor != NULL; cursor = cursor->next)
    {
        // if word in dictionary, return true
        if(strcmp(lookup, cursor->word) == 0)
        {
            return true;
        }
    }
    // else return false
    return false;
}

/**
 * Loads dictionary into memory. Returns true if successful else false.
 */
bool load(const char *dictionary)
{
    // open dictionary 
    FILE *dict = fopen(dictionary, "r");
    char word[LENGTH + 1];
      
    // scan words from file until end of file
    while(fscanf(dict, "%s", word) != EOF)
    {
        // malloc new node
        node *new_node = malloc(sizeof(node));
        
        // make sure there's enough space
        if(new_node == NULL)
        {
            unload();
            return false;
        }
        
        // copy word into new_node
        strcpy(new_node->word, word);
        
        // hash word to an index 
        int hashIndex = hash(word);
    
        // insert node at begining of its correct bucket
        if(hashtable[hashIndex] != NULL)
        {
            new_node->next = hashtable[hashIndex];
        }
        hashtable[hashIndex] = new_node;
        
        // increment wordcount
        wordcount++;
    }
    fclose(dict);
    return true;
}

/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void)
{
    return wordcount;
}

/**
 * Unloads dictionary from memory. Returns true if successful.
 */
bool unload(void)
{
    // iterate over buckets in hashtable
    for(long i = 0; i < SIZE; i++)
    {
        // create cursor to move through each linked list
        node *cursor = hashtable[i];
    
        // iterate over nodes in linked list and free then
        while(cursor != NULL)
        {
            node *tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }
    }
    return true;
}
