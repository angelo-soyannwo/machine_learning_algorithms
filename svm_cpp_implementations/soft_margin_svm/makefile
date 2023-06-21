CC=g++ -std=c++11 -g

default: svm

svm: svm.o complex.o main.cpp
	$(CC) -o svm complex.o svm.o main.cpp


svm.o: svm.h svm.cpp
	$(CC) -c svm.cpp -o svm.o

complex.o: complex.h complex.cpp
	$(CC) -c complex.cpp -o complex.o

clean:
	rm svm.o complex.o
