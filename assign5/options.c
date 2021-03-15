#include <cpuid.h>
#include <errno.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <getopt.h>
#include <string.h>
#include "options.h"

/* function to take in input */
void read_options(int argc, char *argv[], struct opts* opts) {
    opts->r_src = "/dev/random"; 
    opts->valid = false;
    int a;
    while ((a = getopt(argc, argv, ":i:o:")) != -1)
    {
        switch (a) {
            case 'i':
                if (strcmp("rdrand", optarg) == 0)
                    opts->input = RDRAND;
                else if (strcmp("mrand48_r", optarg) == 0)
                    opts->input = MRAND48_R;
                else if ('/' == optarg[0]) {
                    opts->input = SLASH_F;
                    opts->r_src = optarg; 
                }
                else
                    break; 
                opts->valid = true;
                break;
            case 'o':
                if (strcmp("stdout", optarg) == 0)
                    opts->output = STDOUT;
                else {
                    opts->output = N;
                    opts->block_size = atoi(optarg);
                }
                opts->valid = true;
                break;
            case ':':
                break; 
            case '?':
                fprintf (stderr, "error: check arguments\n");
                exit(1);
            default:
                fprintf (stderr, "error: check arguments\n");
                exit(1);
        }
    }
    if (optind >= argc) {
        fprintf (stderr, "error: check arguments\n");
        exit(1);
    }
    
    opts->nbytes = atol(argv[optind]);
    if (opts->nbytes >= 0)
        opts->valid = true;
}


