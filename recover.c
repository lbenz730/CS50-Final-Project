/**
 * recover.c
 * 
 * Luke Benz
 * 
 * recovers JPEG image files from memory card
 * check50 2016.recover recover.c
 * Usage: ./recover image
 */
#include <stdio.h>
#include <cs50.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char *argv[])
{
    // ensure proper usage
    if(argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }
    
    // remeber filename
    char* infile = argv[1];

    // create buffer array for storage
    uint8_t buffer[512];
    
    // create counter for number of JPG's found
    int jpeg = 0;
    
    // create character arry to store file name
    char filename[8];
    
    // open input file 
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        printf("Could not open %s.\n", infile);
        return 2;
    }
 
    // create file pointer to write files
    FILE *img; 

    // read blocks of 512 bytes
    while(fread(&buffer, 1, 512, inptr) == 512)
    {
        // see if block is beginning of jpg
        if(buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // determine if we've already found .jpg
            if(jpeg == 0)
            {
                sprintf(filename, "%03i.jpg", jpeg);
                img = fopen(filename, "w");
                jpeg++;
            }
            else
            {
                fclose(img);
                sprintf(filename, "%03i.jpg", jpeg);
                img = fopen(filename, "w");
                jpeg++;
            }
            // write first block to jpg file
            fwrite(&buffer, 1, 512, img);
        }
        // write block to file if we've already found .jpg
        else if(jpeg > 0)
        { 
            fwrite(&buffer, 1, 512, img);
        }
    }
}
