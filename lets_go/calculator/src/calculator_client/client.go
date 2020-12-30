package main

import (
	"context"
	"fmt"
	"io"
	"log"

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
	doPrimeNumberDecomposition(c)
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
