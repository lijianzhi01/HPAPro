#!/bin/bash  
  
while true; do  
  # Generate a random number between 5 and 45  
  x=$(( RANDOM % 41 + 5 ))  
  
  echo "Sending $x requests..."  
  
  # Send x requests in parallel  
  for ((j=1; j<=x; j++)); do  
    curl -d '{"number": 10}' -H "Content-Type: application/json" -s "localhost:8081/fibonacci" > /dev/null &  
  done  
  
  # Wait for all background processes to finish (all curl requests)  
  wait  
  
  # Sleep 1 second before starting the next round of requests  
  sleep 1  
done  
