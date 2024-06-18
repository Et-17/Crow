#include <stdio.h>
#include <stdlib.h>

struct block
{
    float start;
    float end;
    float sun[13][3][2];
    float moon[13][3][8];
};

struct block *
first_block_in_file(char *filepath)
{
    struct block *first_block;
    FILE *fptr = fopen(filepath, "rb");

    if (fptr == NULL)
    {
        printf("Error opening file\n");
        exit(1);
    }

    fread(first_block, sizeof(struct block), 1, fptr);

    fclose(fptr);

    return first_block;
}
