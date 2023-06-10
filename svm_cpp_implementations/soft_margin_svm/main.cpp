#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>
#include <algorithm>
#include <filesystem>
#include "svm.h"

namespace fs = std::__fs::filesystem;

void collect_paths(const std::string root, const std::string stub, std::vector<std::string> &paths);

std::vector<std::string> getPaths(const std::string root);

std::vector<std::vector<double>> getData(const std::vector<std::string> paths, const size_t D);




int main(){


	size_t nd = 2;		// number of dimensions
	double C = 1.0;	// constant for svm margin
	double lr = 0.0001;	// learning rate

	//get class1 training data
	std::string training_class1_directory = "datasets/toy/train/class1";
	std::vector<std::string> training_class1_paths = getPaths(training_class1_directory);
	std::vector<std::vector<double>> training_class1_data = getData(training_class1_paths, nd);

	//get class2 training data
	std::string training_class2_directory = "datasets/toy/train/class2";
	std::vector<std::string> training_class2_paths = getPaths(training_class2_directory);
	std::vector<std::vector<double>> training_class2_data = getData(training_class2_paths, nd);

	// Training for SVM
	SoftMargin_SVM svm(true);
	svm.train(training_class1_data, training_class2_data, nd, C, lr);


	//get class1 testing data
	std::string testing_class1_directory = "datasets/toy/test/class1";
	std::vector<std::string> testing_class1_paths = getPaths(testing_class1_directory);
	std::vector<std::vector<double>> testing_class1_data = getData(testing_class1_paths, nd);

	//get class2 testing data
	std::string testing_class2_directory = "datasets/toy/test/class2";
	std::vector<std::string> testing_class2_paths = getPaths(testing_class2_directory);
	std::vector<std::vector<double>> testing_class2_data = getData(testing_class2_paths, nd);

	// testing	
	svm.test(testing_class1_data, testing_class2_data);
	std::cout << "///////////////////////// Test /////////////////////////" << std::endl;
	std::cout << "accuracy-all: " << svm.accuracy << " (" << svm.correct_c1 + svm.correct_c2 << "/" << testing_class1_data.size() + testing_class2_data.size() << ")" << std::endl;
	std::cout << "accuracy-class1: " << svm.accuracy_c1 << " (" << svm.correct_c1 << "/" << testing_class1_data.size() << ")" << std::endl;
	std::cout << "accuracy-class2: " << svm.accuracy_c2 << " (" << svm.correct_c2 << "/" << testing_class2_data.size() << ")" << std::endl;
	std::cout << "////////////////////////////////////////////////////////" << std::endl;	
	

	return 0;
}


void collect_paths(const std::string root, const std::string sub, std::vector<std::string> &paths){

	fs::path ROOT(root);

	for (auto &p: fs::directory_iterator(ROOT)){
		if(!is_directory(p)){
			std::stringstream rpath;
			rpath << p.path().string();
			paths.push_back(rpath.str());
		}
		else{
			std::stringstream subsub;
			subsub << p.path().filename().string();
			collect_paths(root + '/' + subsub.str(), sub + subsub.str() + '/', paths);
		}
	}

}


std::vector<std::string> getPaths(const std::string root){

	std::vector<std::string> paths;
	collect_paths(root, "", paths);
	std::sort(paths.begin(), paths.end());
	return paths;

}

std::vector<std::vector<double> > getData(const std::vector<std::string> paths, const size_t D){

	size_t i;
	double vector_element;
	std::ifstream file;
	std::vector<double> temp_vector;
	std::vector<std::vector<double>> data;

	for (std::string path : paths){

		file.open(path);
		temp_vector = std::vector<double>(D);

		for(i=0; i<D; i++){
			file >> vector_element;
			temp_vector[i] = vector_element;
		}
		data.push_back(temp_vector);
		file.close();
	}

	return data;
}






