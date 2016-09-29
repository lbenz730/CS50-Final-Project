/**
 * resize.c
 * 
 * Luke Benz
 * 
 * resizes a bmp image file by a factor of n, 
 * where n is a positive integer no greater than 100
 * 
 * Usage: ./resize n infile outfile
 */
       
#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    int n = atoi(argv[1]);
    if(argc != 4 || n == 0 || n > 100)
    {
        printf("Usage: ./resize n infile outfile\n");
        return 1;
    }

    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file 
    FILE *inptr = fopen(infile, "r");
    if(inptr == NULL)
    {
        printf("Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if(outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if(bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 || 
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    // store padding for scanlines of original image and original image dimensions
    int paddingOld =  (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    int biWidthOld = bi.biWidth;
    int biHeightOld = bi.biHeight;
    
    // update width, height of image, padding, size of image, and size of file
    bi.biWidth *=n;
    bi.biHeight *= n;
    int paddingNew =  (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    bi.biSizeImage = ((sizeof(RGBTRIPLE) * bi.biWidth) + paddingNew) * abs(bi.biHeight);
    bf.bfSize = bi.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);
    
    // write outfile's BITMAPFILEHEADER 
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);
    
    // write outfile's BITMAPINFOHEADER 
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);

    // iterate over infile's scanlines
    for(int i = 0, biHeight = abs(biHeightOld); i < biHeight; i++)
    {
        for(int w = 0; w < n; w++)
        {
            // iterate over pixels
            for(int j = 0; j < biWidthOld; j++)
            {
                // temporary storage
                RGBTRIPLE triple;
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);
               
                // write pixel to outfile n times
                for(int z = 0; z < n; z++)
                {
                    fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                }
            }
             // write padding for resized image
            for(int k = 0; k < paddingNew; k++)
            {
                fputc(0x00, outptr);
            }
            // send cursor back to begining of scanline
            if(w < n - 1)
            {
                fseek(inptr, -1 * biWidthOld * sizeof(RGBTRIPLE), SEEK_CUR);
            }
        }
        // skip over old padding, if any
        fseek(inptr, paddingOld, SEEK_CUR);
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
