package main

import (
	"context"
	"fmt"
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

	doUnary(c)
}

func doUnary(c calculatorpb.CalculatorServiceClient) {
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
