const { Histogram, register } = require('prom-client');    
const express = require('express');    
const app = express();    
const port = 8081;    
const host = '0.0.0.0';    
    
app.use(express.json());     
  
// Create a histogram metric  
const responseTimes = new Histogram({  
  name: 'http_response_time_seconds',  
  help: 'Histogram of http response durations',  
  labelNames: ['method', 'status_code'],  
  buckets: [100, 200, 300, 400, 500, 600, 700, 800] // Buckets for response time from 0.1s to 5s  
});

const fibonacci = (num) => {    
    if (num <= 1) return 1;    
    return fibonacci(num - 1) + fibonacci(num - 2);    
}    
    
app.post('/fibonacci', (req, res) => {  
    const start = Date.now(); // Start the timer  
  
    const fibonacciNumber = fibonacci(req.body.number);    
  
    const responseTime = Date.now() - start; // Calculate the response time  
    console.log("Response time: ", responseTime, "ms");
    responseTimes.observe({ method: 'POST', status_code: res.statusCode}, responseTime); // Record to histogram, convert ms to seconds  
    
    res.send(`Fibonacci number is ${fibonacciNumber}!\n`);    
});    
    
app.get('/metrics', async (req, res) => {    
    res.set('Content-Type', register.contentType);    
    res.end(await register.metrics());    
});    
    
app.listen(port, host, () => {    
    console.log(`Server listening at http://${host}:${port}`);    
});  