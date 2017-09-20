package main

import (
	"flag"
	"fmt"
)

var inputName = flag.String("name", "CHENJIAN", "Input Your Name.")
var inputAge = flag.Int("age", 27, "Input Your Age")
var inputGender = flag.String("gender", "female", "Input Your Gender")
var inputFlagvar int

func Init() {
	flag.IntVar(&inputFlagvar, "flagname", 1234, "Help")
}
func main() {
	Init()
	flag.Parse()
	// func Args() []string
	// Args returns the non-flag command-line arguments.
	// func NArg() int
	// NArg is the number of arguments remaining after flags have been processed.
	fmt.Printf("args=%s, num=%d\n", flag.Args(), flag.NArg())
	for i := 0; i != flag.NArg(); i++ {
		fmt.Printf("arg[%d]=%s\n", i, flag.Arg(i))
	}
	fmt.Println("name=", *inputName)
	fmt.Println("age=", *inputAge)
	fmt.Println("gender=", *inputGender)
	fmt.Println("flagname=", inputFlagvar)
}