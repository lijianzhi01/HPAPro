package main  
  
import (  
	"bufio"  
	"bytes"
	"fmt"  
	"net/http"  
	"os"  
	"strconv"  
	"sync"  
	"time"  
)  
  
func sendRequest(port string, wg *sync.WaitGroup) {  
	defer wg.Done()  
	// startTime := time.Now()  
	jsonStr := []byte(`{"number":30}`)  
	http.Post("http://127.0.0.1:"+port+"/fibonacci", "application/json", bytes.NewBuffer(jsonStr))  
	// endTime := time.Now()  
	// responseTime := endTime.Sub(startTime)  
	// fmt.Println("Response time: ", responseTime.Seconds(), " seconds")  
}  
  
func startPlay(filename, port string) {  
	file, err := os.Open(filename)  
	if err != nil {  
		fmt.Println(err)  
		return  
	}  
	fmt.Println(file)
	defer file.Close()  
  
	scanner := bufio.NewScanner(file)  
	lineNumber := 0  
	for scanner.Scan() {  
		lineNumber++  
		floatVal, err := strconv.ParseFloat(scanner.Text(), 64)  
		if err != nil {  
			fmt.Println("Failed to parse float: ", err)  
			return  
		}  
		concurrentRequests := int(floatVal)  

		if concurrentRequests > 0 {  
			fmt.Println("Line number: ", lineNumber, " Value: ", concurrentRequests)
			var wg sync.WaitGroup  
			for i := 0; i < concurrentRequests; i++ {  
				wg.Add(1)  
				go sendRequest(port, &wg)  
			}  
			wg.Wait()  
		}  
		time.Sleep(1 * time.Second)  
	}  
}  
  
func main() {  
	if len(os.Args) != 3 {  
		fmt.Println("Usage: ", os.Args[0], " <filename> <port>")  
		os.Exit(1)  
	}  
	startPlay(os.Args[1], os.Args[2])  
}  
