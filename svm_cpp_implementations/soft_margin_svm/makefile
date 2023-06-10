CC=g++ -std=c++11 -g

default: svm

svm: svm.o main.cpp
	$(CC) -o svm svm.o main.cpp

svm.o: svm.h svm.cpp
	$(CC) -c svm.cpp -o svm.o

clean:
	rm svm.o
