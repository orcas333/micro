package main

import (
	"context"
	"fmt"
	"io"
	"log"
	"time"

	"calculatorpb"

	"google.golang.org/grpc"
)

func main() {
	fmt.Println("I am a client saying hello world...")
	cc, err := grpc.Dial("localhost:50051", grpc.WithInsecure())
	if err != nil {
		log.Fatalf("Could not connect: %v", err)
	}

	defer cc.Close()

	c := calculatorpb.NewCalculatorServiceClient(cc)

	// doSum(c)
	// doPrimeNumberDecomposition(c)
	doComputeAverage(c)
}

func doSum(c calculatorpb.CalculatorServiceClient) {
	//Unary
	fmt.Println("Starting to do a Unary RPC for the Calculator..")
	req := &calculatorpb.CalculatorRequest{
		SumInput: &calculatorpb.Sum{
			Integer_1: 20,
			Integer_2: 52,
		},
	}
	res, err := c.Calculate(context.Background(), req)
	if err != nil {
		log.Fatalf("erro while calling Calculate RPC: %v", err)
	}
	log.Printf("Response from Calculate: %v", res.Result)

}

func doPrimeNumberDecomposition(c calculatorpb.CalculatorServiceClient) {
	//Server Streaming
	fmt.Println("Starting to do Server Streaming for PrimeNumberDecomposition...")

	req := &calculatorpb.PrimeNumberDecompositionRequest{
		Input: 302940,
	}

	resStream, err := c.PrimeNumberDecomposition(context.Background(), req)
	if err != nil {
		log.Fatalf("error while calling PrimeNumberDecomposition...")
	}

	for {
		msg, err := resStream.Recv()
		if err == io.EOF {
			// we've the reached the end of the stream
			break
		}
		if err != nil {
			log.Fatalf("error while reading stream for PrimeNumberDecomposition: %v", err)
		}
		log.Printf("Response from PrimeNumberDecomposition: %v", msg.GetPrimeNum())
	}
}

func doComputeAverage(c calculatorpb.CalculatorServiceClient) {
	fmt.Println("Starting to do a Client Streaming RPC to Compute the Average...")

	requests := []*calculatorpb.ComputeAverageRequest{
		&calculatorpb.ComputeAverageRequest{
			Input: 1,
		},
		&calculatorpb.ComputeAverageRequest{
			Input: 2,
		},
		&calculatorpb.ComputeAverageRequest{
			Input: 3,
		},
		&calculatorpb.ComputeAverageRequest{
			Input: 4,
		},
		&calculatorpb.ComputeAverageRequest{
			Input: 5,
		},
		&calculatorpb.ComputeAverageRequest{
			Input: 6,
		},
		&calculatorpb.ComputeAverageRequest{
			Input: 20,
		},
	}
	stream, err := c.ComputeAverage(context.Background())
	if err != nil {
		log.Fatalf("error while calling ComputeAverage: %v", err)
	}

	// we iterate over our slice and send each message individually
	for _, req := range requests {
		fmt.Printf("Sending req: %v\n", req)
		stream.Send(req)
		time.Sleep(100 * time.Millisecond)
	}

	res, err := stream.CloseAndRecv()
	if err != nil {
		log.Fatalf("error while receiving responses from ComputeAverage: %v", err)
	}
	fmt.Printf("ComputeAverage Response: %v\n", res)
}
