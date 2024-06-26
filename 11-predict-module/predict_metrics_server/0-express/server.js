const { Gauge, register } = require('prom-client');    
const express = require('express');    
const app = express();    
const port = 8081;    
const host = '0.0.0.0';    
    
app.use(express.json());     

const futurePodCPUUsage = new Gauge({  
    name: 'future_pod_cpu_usage',  
    help: 'Predicted future CPU usage of the pod',  
    labelNames: ['pod']
});

app.post('/set_future_cpu_usage', (req, res) => {  
    futurePodCPUUsage.set({ pod: 'express-85466c68b9-9d8cx' }, req.body.number);  
    console.log("Future CPU Usage: ", req.body.number);
    res.send(`The future CPU usage is ${req.body.number}!\n`);    
});    

app.get('/metrics', async (req, res) => {    
    res.set('Content-Type', register.contentType);    
    res.end(await register.metrics());    
}); 
    
app.listen(port, host, () => {    
    console.log(`Server listening at http://${host}:${port}`);    
});  