
#!/bin/sh
N=5134
if [ "$(./randall "$N" | wc -c)" = "$N" ]
then
   echo "basic length test passed"
else
   echo "basic length test failed" 
fi

if [ "$(./randall -i mrand48_r "$N" | wc -c)" = "$N" ]
then
   echo "mrand48_r length test passed"
else
   echo "mrand48_r length test failed"
fi

if [ "$(./randall -i rdrand "$N" | wc -c)" = "$N" ]
then
   echo "rdrand length test passed"
else
   echo "rdrand length test failed"
fi

if [ "$(./randall -i /dev/urandom "$N" | wc -c)" = "$N" ]
then
   echo "file length test passed"
else
    echo "file length test failed"
    echo "$(./randall -i /dev/urandom "$N" | wc -c)"
fi

if [ "$(./randall -o 5 "$N" | wc -c)" = "$N" ]
then
   echo "byte batch length test passed"
else
    echo "byte batch length test failed"
    echo "$(./randall -o 5 "$N" | wc -c)"
fi

if [ "$(./randall -o stdout "$N" | wc -c)" = "$N" ]
then
   echo "stdout length test passed"
else
    echo "stdout length test failed"
    echo "$(./randall -o stdout "$N" | wc -c)"
fi

if [ "$(./randall -i rdrand -o stdout "$N" | wc -c)" = "$N" ]
then
   echo "rdrand + stdout length test passed"
else
    echo "rdrand + stdout length test failed"
    echo "$(./randall -i rdrand -o stdout "$N" | wc -c)"
fi

if [ "$(./randall -i mrand48_r -o stdout "$N" | wc -c)" = "$N" ]
then
   echo "mrand48_r + stdout length test passed"
else
    echo "mrand48_r + stdout length test failed"
    echo "$(./randall -i mrand48_r -o stdout "$N" | wc -c)"
fi

if [ "$(./randall -i mrand48_r -o 1 "$N" | wc -c)" = "$N" ]
then
   echo "mrand48_r + N length test passed"
else
    echo "mrand48_r + N length test failed"
    echo "$(./randall -i mrand48_r -o 1 "$N" | wc -c)"
fi

if [ "$(./randall -i rdrand -o 1 "$N" | wc -c)" = "$N" ]
then
   echo "rdrand + N length test passed"
else
    echo "rdrand + N length test failed"
    echo "$(./randall -i rdrand -o 1 "$N" | wc -c)"
fi

if [ "$(./randall -i /dev/urandom -o 2 "$N" | wc -c)" = "$N" ]
then
   echo "rdrand + N length test passed"
else
    echo "rdrand + N length test failed"
    echo "$(./randall -i /dev/random -o 2 "$N" | wc -c)"
fi
