export GOROOT=/usr/local/go
export GOPATH=$HOME/go:$(pwd):$HOME/go/bin
export PATH=$PATH:$GOROOT:$GOPATH
# export GOBIN=$GOPATH/bin
# export PATH=$PATH:$GOROOT:$GOPATH:$GOBIN
# PATH=$PATH:$GOPATH/bin

# PATH=$GOPATH

protoc src/greetpb/greet.proto --go_out=plugins=grpc:.
# protoc greetpb/greet.proto --go-grpc_out=.