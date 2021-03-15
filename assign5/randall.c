/* Generate N bytes of random output.  */

/* When generating output this program uses the x86-64 RDRAND
   instruction if available to generate random numbers, falling back
   on /dev/random and stdio otherwise.

   This program is not portable.  Compile it with gcc -mrdrnd for a
   x86-64 machine.

   Copyright 2015, 2017, 2020 Paul Eggert

   This program is free software: you can redistribute it and/or
   modify it under the terms of the GNU General Public License as
   published by the Free Software Foundation, either version 3 of the
   License, or (at your option) any later version.

   This program is distributed in the hope that it will be useful, but
   WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
   General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

#include <cpuid.h>
#include <errno.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "./output.h"
#include "./options.h"
#include "./rand64-hw.h"
#include "./rand64-sw.h"

struct cpuid { unsigned eax, ebx, ecx, edx; };

/* Return information about the CPU.  See <http://wiki.osdev.org/CPUID>. */
struct cpuid
cpuid (unsigned int leaf, unsigned int subleaf)
{
  struct cpuid result;
  asm ("cpuid"
       : "=a" (result.eax), "=b" (result.ebx),
     "=c" (result.ecx), "=d" (result.edx)
       : "a" (leaf), "c" (subleaf));
  return result;
}

/* Return true if the CPU supports the RDRAND instruction. */
_Bool
rdrand_supported (void)
{
  struct cpuid extended = cpuid (1, 0);
  return (extended.ecx & bit_RDRND) != 0;
}

char* r_src; //file name if needed

/* Main program, which outputs N bytes of random data.  */
int
main (int argc, char **argv)
{
    struct opts opts;
    opts.valid = false;
    read_options(argc, argv, &opts);
    if (opts.valid == false)
    {
        fprintf (stderr, "%s: usage: %s NBYTES\n", argv[0], argv[0]);
        return 1;
    }
    /* If there's no work to do, don't worry about which library to use. */
    if (opts.nbytes == 0)
      return 0;
  
  /* Now that we know we have work to do, arrange to use the
     appropriate library.  */
  void (*initialize) (void);
  unsigned long long (*rand64) (void);
  void (*finalize) (void);
    
   
  if (rdrand_supported () && opts.input != SLASH_F )
    {
      initialize = hardware_rand64_init;
      if (opts.input == MRAND48_R) /*if mrand48 needs to be used*/
          rand64 = hardware_mrand48;
      else                         /*if rdrand needs to be used, the default*/
          rand64 = hardware_rand64;
      finalize = hardware_rand64_fini;
    }
  else /*for slash_f, custom file*/
    {
        if(opts.input == RDRAND) {
            fprintf (stderr, "error: rdrand is not supported");
            exit(1);
        }
        r_src = opts.r_src; 
      initialize = software_rand64_init;
      rand64 = software_rand64;
      finalize = software_rand64_fini;
    }

  initialize ();
  int wordsize = sizeof rand64 ();
  int output_errno = 0;

    char* buf; /* buffer for outputing bursts of bytes*/

  do
    {
      unsigned long long x = rand64 ();
      int outbytes;
      
      if(opts.output == N) {
          int buf_size = opts.block_size * 1000;
          outbytes = opts.nbytes < buf_size ? opts.nbytes : buf_size;
          buf = (char*) malloc(outbytes);
          /*copy to x 8 bytes at a time*/
          for(int k = 0; k < outbytes/8; k++)
          {
              x = rand64 ();
              memcpy(buf + 8*k, &x, 8);
          }
          writebyteblocks (outbytes, buf);
      }
      else {
          outbytes = opts.nbytes < wordsize ? opts.nbytes : wordsize;
          if (!writebytes (x, outbytes))
          {
              output_errno = errno;
              break;
          }
      }
        opts.nbytes -= outbytes;
    }
  while (0 < opts.nbytes);
    
    free(buf);

  if (fclose (stdout) != 0)
    output_errno = errno;

  if (output_errno)
    {
      errno = output_errno;
      perror ("output");
    }

  finalize ();
  return !!output_errno;
}
