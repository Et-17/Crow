#ifndef EPH_READER_GUARD
#define EPH_READER_GUARD

struct block
{
    float start;
    float end;
    float sun[2][3][13];
    float moon[8][3][13];
};

struct block *first_block_in_file(char *filepath);

#endif
