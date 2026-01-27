#!/bin/bash

# Loop from X=1 to X=100
for x in {1..100}
do
    # Queue the simulation with n=1000 using task spooler
    tsp python3 sim.py $x 10000
done

echo "Queued 100 simulations (X=1 to 100) with n=1000 each."
