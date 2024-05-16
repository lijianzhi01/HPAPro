#!/bin/sh  
while true; do    
  # Generate a random number between 5 and 45    
  x=$(( RANDOM % 21 + 5 ))    
    
  echo "Sending $x requests..."    
    
  # Send x requests in parallel    
  seq $x | xargs -n1 -P$x -I{} curl -d '{"number": 30}' -H "Content-Type: application/json" -s "http://express.demo:8081/fibonacci" > /dev/null  
    
  # Sleep 1 second before starting the next round of requests    
  sleep 1    
done
