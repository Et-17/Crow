#include <stdio.h>

#include "eph_reader/eph_reader.h"

int main()
{
    printf("sizeof(struct block): %d\n\n", sizeof(struct block));

    struct block *first_block = first_block_in_file("ephemeris");

    printf("Start date: %f\n", first_block->start);
    printf("End date: %f\n", first_block->end);

    for (int comp = 0; comp < 3; comp++)
    {
        printf("Sun coeffs: [");
        for (int i = 0; i < 13; i++)
        {
            if (i != 0)
            {
                printf(", ");
            }

            printf("%e", (first_block->sun)[0][comp][i]);
        }
        printf("]\n");
    }

    return 0;
}
