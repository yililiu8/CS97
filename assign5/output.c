#include <limits.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include "output.h"

bool
writebytes (unsigned long long x, int nbytes)
{
  do
    {
      if (putchar (x) < 0)
          return false;
      x >>= CHAR_BIT;
      nbytes--;
    }
  while (0 < nbytes);

  return true;
}

bool writebyteblocks (int nbytes, char* buf) {
    if (write(1, buf, nbytes) < 0) {
        fprintf (stderr, "error in writing byte blocks\n");
        exit(1);
        return false;
    }
    return true;
}

