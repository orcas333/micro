package main

import (
	"fmt"
	"log"

	"greetpb"

	"google.golang.org/grpc"
)

func main() {
	fmt.Println("Hello I'm a Client")
	cc, err := grpc.Dial("localhost:50051", grpc.WithInsecure())
	if err != nil {
		log.Fatalf("Could not connect: %v", err)
	}

	defer cc.Close()

	c := greetpb.NewGreetServiceClient(cc)
	fmt.Printf("Created client: %f", c)

	// c.Greet( )
}
