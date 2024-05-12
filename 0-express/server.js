const { Counter, Histogram, register } = require('prom-client');    
const express = require('express');    
const app = express();    
const port = 8081;    
const host = '0.0.0.0';    
    
app.use(express.json());    
    
const counter = new Counter({    
    name: 'http_requests_total',    
    help: 'Total number of http requests',    
    labelNames: ['method'],    
});  
  
// Create a histogram metric  
const responseTimes = new Histogram({  
  name: 'http_response_time_seconds',  
  help: 'Histogram of http response durations',  
  labelNames: ['method', 'status_code'],  
  buckets: [0.1, 0.2, 0.3, 0.4, 0.5, 1, 2, 5] // Buckets for response time from 0.1s to 5s  
});  
  
const fibonacci = (num) => {    
    if (num <= 1) return 1;    
    return fibonacci(num - 1) + fibonacci(num - 2);    
}    
    
app.post('/fibonacci', (req, res) => {  
    const start = Date.now(); // Start the timer  
  
    const fibonacciNumber = fibonacci(req.body.number);    
    counter.inc({ method: 'POST' });  
  
    const responseTime = Date.now() - start; // Calculate the response time  
    responseTimes.observe({ method: 'POST', status_code: res.statusCode }, responseTime / 1000); // Record to histogram, convert ms to seconds  
    
    res.send(`Fibonacci number is ${fibonacciNumber}!\n`);    
});    
    
app.get('/metrics', async (req, res) => {    
    res.set('Content-Type', register.contentType);    
    res.end(await register.metrics());    
});    
    
app.listen(port, host, () => {    
    console.log(`Server listening at http://${host}:${port}`);    
});  