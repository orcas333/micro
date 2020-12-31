package main

import (
	"calculatorpb"
	"context"
	"fmt"
	"io"
	"log"
	"net"
	"time"

	"google.golang.org/grpc"
)

type server struct{}

func (*server) Calculate(ctx context.Context, req *calculatorpb.CalculatorRequest) (*calculatorpb.CalculatorResponse, error) {
	fmt.Printf("Calculate function was invoked with %v\n", req)
	result := req.GetSumInput().GetInteger_1() + req.GetSumInput().GetInteger_2()
	res := &calculatorpb.CalculatorResponse{
		Result: result,
	}
	return res, nil
}

func (*server) PrimeNumberDecomposition(req *calculatorpb.PrimeNumberDecompositionRequest, stream calculatorpb.CalculatorService_PrimeNumberDecompositionServer) error {
	fmt.Printf("PrimeNumberDecomposition function was invoked with %v\n", req)
	Input := req.GetInput()
	var prime_number int32
	// Prime Number Decomposition Algorithm
	var k int32 = 2
	N := Input
	for N > 1 {
		if N%k == 0 {
			prime_number = k
			res := &calculatorpb.PrimeNumberDecompositionResponse{
				PrimeNum: prime_number,
			}
			stream.Send(res)
			time.Sleep(100 * time.Millisecond)
			N = N / k
		} else {
			k = k + 1
		}
	}
	return nil
}

func (*server) ComputeAverage(stream calculatorpb.CalculatorService_ComputeAverageServer) error {
	fmt.Printf("ComputeAverage function was invoked with a streaming request...\n")
	var sum float64 = 0
	var count float64 = 0

	for {
		req, err := stream.Recv()
		if err == io.EOF {
			// we have finished reading the client stream
			return stream.SendAndClose(&calculatorpb.ComputeAverageResponse{
				Result: sum / count,
			})
		}
		if err != nil {
			log.Fatalf("Error while reading client stream: %v", err)
		}
		// input_num := req.GetInput()
		sum += float64(req.GetInput())
		count += 1.0
	}
}

func main() {
	fmt.Println("The server says hello world!...")

	lis, err := net.Listen("tcp", "0.0.0:50051")
	if err != nil {
		log.Fatalf("Failed to listen: %v", err)
	}

	s := grpc.NewServer()
	calculatorpb.RegisterCalculatorServiceServer(s, &server{})

	if err := s.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}
