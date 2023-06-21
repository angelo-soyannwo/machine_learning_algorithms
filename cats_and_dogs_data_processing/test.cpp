
#include <fstream>
#include <iostream>
#include <string>
#include <sstream>
#include <vector>

int main() {
	std::ifstream my_file; 
	my_file.open("test.txt");
	if (!my_file) {
		std::cout << "No such file";
	}
	else {
		double real, imag;
		std::string line;

		while (getline(my_file, line) ) {

			//put line into a string stream
			std::istringstream iss(line);

			//Use a vector to store substrings
			std::string substring;
			std::vector<std::string> substrings;


			// Now, in a loop, get the substrings from the std::istringstream
        		while (std::getline(iss, substring, ',')) {

			        // Add the substring to the std::vector
        	    		substrings.push_back(substring);

        		}

			real = std::stod(substrings[0]);
			imag = std::stod(substrings[1]);
			std::cout << "r: " << real << ", i:" << imag << std::endl;
		}

	}
	my_file.close();
	return 0;

}
