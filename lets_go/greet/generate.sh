#!/bin/bash

export GOROOT=/usr/local/go
export GOPATH=$HOME/go
export GOBIN=$GOPATH/bin
export PATH=$PATH:$GOROOT:$GOPATH:$GOBIN
export GOPATH=$HOME/go:$(pwd)
PATH=$PATH:$GOPATH/bin

echo $HOME
echo $PATH

protoc greetpb/greet.proto --go_out=plugins=grpc:.
protoc greetpb/greet.proto --go-grpc_out=.