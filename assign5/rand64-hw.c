#include <stdio.h>
#include <stdlib.h>
#include <immintrin.h>
#include <time.h>
#include "rand64-hw.h"

struct drand48_data buffer;

void
hardware_rand64_init (void)
{
    srand48_r(time(NULL), &buffer);
}

/* Return a random value, using hardware operations.  */
unsigned long long
hardware_rand64 (void)
{
  unsigned long long int x;
  while (! _rdrand64_step (&x))
    continue;
  return x;
}

unsigned long long hardware_mrand48 (void)
{
    long int x;
    long int y;
    mrand48_r (&buffer, &x);
    mrand48_r (&buffer, &y);
    return (((unsigned long long) x) << 32) | ((unsigned long long) y & 0x00000000FFFFFFFF);
}

/* Finalize the hardware rand64 implementation.  */
void
hardware_rand64_fini (void)
{
    
}

