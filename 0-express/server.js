const { Histogram, register } = require('prom-client');    
const express = require('express');    
const app = express();    
const port = 8081;    
const host = '0.0.0.0';    
const fs = require('fs');  
const os = require('os');  
const path = require('path');  
    
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


app.post('/fibonacci_v2', (req, res) => {  
    const start = Date.now(); // Start the timer  

    let fibSequence = [0, 1];  
  
    const n = req.body.number;
    if (n <= 1) {  
        return fibSequence[n];  
    }  
  
    for (let i = 2; i <= n; i++) {  
        fibSequence[i] = fibSequence[i-1] + fibSequence[i-2];  
    }  
  
    const fibonacciNumber = fibSequence[n];    
  
    const responseTime = Date.now() - start; // Calculate the response time  
    console.log("Response time: ", responseTime, "ms");
    responseTimes.observe({ method: 'POST', status_code: res.statusCode}, responseTime); // Record to histogram, convert ms to seconds  
    
    res.send(`Fibonacci number is ${fibonacciNumber}!\n`);    
}); 

app.post('/fibonacci_v3', (req, res) => {  
    const start = Date.now(); // Start the timer  
    
    
  
    // Write 1MB of data to a file  
    const filePath = path.join(os.tmpdir(), 'data.txt');  
    const data = Buffer.alloc(1 << 20).toString(); // 1MB of data  
    fs.writeFile(filePath, data, (err) => {  
        if (err) {  
            console.error(err);  
            res.status(500).send('Error writing file');  
            return;  
        }  

        let fibSequence = [0, 1];    
    
        const n = req.body.number;  
        if (n <= 1) {    
            return fibSequence[n];    
        }    
        
        for (let i = 2; i <= n; i++) {    
            fibSequence[i] = fibSequence[i-1] + fibSequence[i-2];    
        }    
        
        const fibonacciNumber = fibSequence[n];  
  
        const responseTime = Date.now() - start; // Calculate the response time    
        console.log("Response time: ", responseTime, "ms");  
        responseTimes.observe({ method: 'POST', status_code: res.statusCode}, responseTime); // Record to histogram, convert ms to seconds    
  
        // Send the response, then delete the file  
        res.send(`Fibonacci number is ${fibonacciNumber}!\n`);  
        fs.unlink(filePath, (err) => {  
            if (err) {  
                console.error(err);  
            }  
        });  
    });  
});
    
app.get('/metrics', async (req, res) => {    
    res.set('Content-Type', register.contentType);    
    res.end(await register.metrics());    
});    
    
app.listen(port, host, () => {    
    console.log(`Server listening at http://${host}:${port}`);    
});  