#include <iostream>
#include <string>
#include <vector>
#include <utility>
#include <cmath>
#include "svm.h"
#include "complex.h"

	SoftMargin_SVM::SoftMargin_SVM(const bool verbose){
		this->verbose = verbose;
	}

	double SoftMargin_SVM::dot(const std::vector<double> x1, const std::vector<double> x2){

		size_t i;

		if (x1.size() != x2.size()){
			std::cerr << "Error : Couldn't match the number of elements for inner product." << std::endl;
			std::exit(-1);
		}

	
		double answer = 0.0;
		for(i = 0; i<x1.size(); i++){
			answer += x1[i] * x2[i];
		}

		return answer;

	}

	void SoftMargin_SVM::log(const std::string str){
		if (this->verbose){
			std::cout << str << std::flush;
		}
		return;
	}

	void SoftMargin_SVM::train(const std::vector<std::vector<double>> class1_data, const std::vector<std::vector<double>> class2_data, const size_t D, const double C, const double lr, const double limit){

		constexpr double eps = 0.0001; //0.0000001;
		

		size_t i, j;
		size_t N, Ns, Ns_in;
		bool judge;
		double term1, term2, term3;
		double delta;
		double beta;
		double error;
		std::vector<std::vector<double>> x;
		std::vector<int> y;
		std::vector<double> alpha;

		//set class 1 data
		for(i=0; i<class1_data.size(); i++){
			x.push_back(class1_data[i]);
			y.push_back(1);
		}

		//set class 2 data
		for(i=0; i<class2_data.size(); i++){
			x.push_back(class2_data[i]);
			y.push_back(-1);
		}

		//lagrange multipliers conditions
		N = x.size();
		alpha = std::vector<double>(N, 0.0);
		beta = 1.0;

		this -> log("\n");
		this -> log("//////////////////////////////Training//////////////////////////////\n");
		
		do {

			judge = false;
			error = 0.0;

			for (i = 0; i<N; i++){

				term1 = 0.0;
				for (j=0; j<N; j++){
					term1 += alpha[j] * (double)y[i] * (double) y[j] * this->dot(x[i], x[j]);
				}

				term2 = 0.0;
				for (j=0; j<N; j++){
					term2 += alpha[j] * (double)y[i] * (double) y[j];
				}

				delta = 1 - term1 - beta*term2;

				alpha[i] = alpha[i] + lr*delta;

				if (alpha[i]<0.0){
					alpha[i] = 0.0;
				}
				else if (alpha[i]>C){
					alpha[i] = C;
				}
				else if (std::abs(delta) > limit){
					judge = true;
					error = error + std::abs(delta) - limit;
				}
			

			}

			term3 = 0.0;
			for (i=0; i<N; i++){
				term3 += alpha[i] *(double) y[i];
			}
			beta += 0.5 * term3 * term3;

			// Output Residual Error
			this->log("\rerror: " + std::to_string(error));

		} while (judge);
		this->log("\n");
		this->log("////////////////////////////////////////////////////////\n");


		Ns = 0;
		Ns_in = 0;
		this -> ys = std::vector<int>();
		this -> xs = std::vector<std::vector<double>>();
		this -> alpha_s = std::vector<double>();
		this -> ys_in = std::vector<int>();
		this -> xs_in = std::vector<std::vector<double>>();
		this -> alpha_s_in = std::vector<double>();


		for(i = 0; i<N; i++){
			if((eps < alpha[i]) && (alpha[i] < C - eps)) {
				this -> ys.push_back(y[i]);
				this -> xs.push_back(x[i]);
				this->alpha_s.push_back(alpha[i]);
				Ns++;
			}
			else if(alpha[i] >= C - eps) {
				this -> ys_in.push_back(y[i]);
				this -> xs_in.push_back(x[i]);
				this->alpha_s_in.push_back(alpha[i]);
				Ns_in++;	
			}
		}

		this->log("Ns (number of support vectors on margin) = " + std::to_string(Ns) + "\n");
		this->log("Ns_in (number of support vectors inside margin) = " + std::to_string(Ns_in) + "\n");

		// Description for weights
		this->log("weight = [ ");
		this->w = std::vector<double>(D, 0.0);

		for (size_t z=0; z < D; z++){
		

			for (i = 0; i < Ns; i++){
				this->w[z] += alpha_s[i] * (double)ys[i] * xs[i][z];
			}

			for (i = 0; i < Ns_in; i++){
				this->w[z] += alpha_s_in[i] * (double)ys_in[i] * xs_in[i][z];
			}
			this->log(std::to_string(this->w[z]) + " ");
		}

		this->log("]\n");

		// Description for b
		this->b = 0.0;
		for (i = 0; i < Ns; i++){
			this->b += (double)this->ys[i] - this->dot(this->w, this->xs[i]);
	    	}
		this->b /= (double)Ns;
		this->log("bias = " + std::to_string(this->b) + "\n");
		this->log("////////////////////////////////////////////////////////\n\n");

		return;
		
	}

	void SoftMargin_SVM::test(const std::vector<std::vector<double>> class1_data, const std::vector<std::vector<double>> class2_data){

		size_t i;

		this -> correct_c1 = 0;
		for (i=0; i<class1_data.size(); i++){
			if (this->g(class1_data[i]) == 1){
				this -> correct_c1++ ;
			}
		}
		
		this -> correct_c2 = 0;
		for (i=0; i<class2_data.size(); i++){
			if (this->g(class2_data[i]) == -1){
				this->correct_c2++ ;
			}
		}

	
		this->accuracy = (double)(this->correct_c1 + this->correct_c2) / (double)(class1_data.size() + class2_data.size());
		this->accuracy_c1 = (double)this->correct_c1 / (double)class1_data.size();
		this->accuracy_c2 = (double)this->correct_c2 / (double)class2_data.size();

		return;

	}

	double SoftMargin_SVM::f(const std::vector<double> x){
		return this->dot(this->w, x) + this->b; 
	}

	double SoftMargin_SVM::g(const std::vector<double> x){
		double F;
		int G;

		F = this->f(x);
		if (F > 0.0){
			G = 1;
		}
		else {
			G = -1;
		}
		return G;
	}

	//complex versions of dot, train, and test
	double SoftMargin_SVM::dot(const std::vector<double> x1, const std::vector<Complex> x2){

		size_t i;

		if (x1.size() != x2.size()){
			std::cerr << "Error : Couldn't match the number of elements for inner product." << std::endl;
			std::exit(-1);
		}

	
		double answer = 0.0;
		for(i = 0; i<x1.size(); i++){
			answer += x1[i] * (re(x2[i]) + im(x2[i]));
		}

		return answer;

	}

	Complex SoftMargin_SVM::dot(std::vector<Complex> x1, std::vector<Complex> x2){

		size_t i;

		if (x1.size() != x2.size()){
			std::cerr << "Error : Couldn't match the number of elements for inner product." << std::endl;
			std::exit(-1);
		}

	
		Complex answer = Complex(0);
		for(i = 0; i<x1.size(); i++){
			answer += x1[i] * x2[i];
		}

		return answer;

	}

	void SoftMargin_SVM::train(const std::vector<std::vector<Complex>> class1_data, const std::vector<std::vector<Complex>> class2_data, const size_t D, const double C, const double lr, const double limit){

		constexpr double eps = 0.0001; //0.0000001;
		

		size_t i, j;
		size_t N, Ns, Ns_in;
		bool judge;
		double term1, term2, term3;
		double delta;
		double beta;
		double error;
		std::vector<std::vector<Complex>> x_complex;
		std::vector<int> y;
		std::vector<double> alpha;

		Complex temp;

		//set class 1 data
		for(i=0; i<class1_data.size(); i++){
			x_complex.push_back(class1_data[i]);
			y.push_back(1);
		}

		//set class 2 data
		for(i=0; i<class2_data.size(); i++){
			x_complex.push_back(class2_data[i]);
			y.push_back(-1);
		}

		//lagrange multipliers conditions
		N = x_complex.size();
		alpha = std::vector<double>(N, 0.0);
		beta = 1.0;

		this -> log("\n");
		this -> log("//////////////////////////////Training//////////////////////////////\n");
		
		do {

			judge = false;
			error = 0.0;

			for (i = 0; i<N; i++){

				term1 = 0.0;
				for (j=0; j<N; j++){
					temp = this->dot(x_complex[i], x_complex[j]);
					term1 += alpha[j] * (double)y[i] * (double) y[j] * (re(temp)  + im(temp));
				}

				term2 = 0.0;
				for (j=0; j<N; j++){
					term2 += alpha[j] * (double)y[i] * (double) y[j];
				}

				delta = 1 - term1 - beta*term2;

				alpha[i] = alpha[i] + lr*delta;

				if (alpha[i]<0.0){
					alpha[i] = 0.0;
				}
				else if (alpha[i]>C){
					alpha[i] = C;
				}
				else if (std::abs(delta) > limit){
					judge = true;
					error = error + std::abs(delta) - limit;
				}
			

			}

			term3 = 0.0;
			for (i=0; i<N; i++){
				term3 += alpha[i] *(double) y[i];
			}
			beta += 0.5 * term3 * term3;

			// Output Residual Error
			this->log("\rerror: " + std::to_string(error));

		} while (judge);
		this->log("\n");
		this->log("////////////////////////////////////////////////////////\n");


		Ns = 0;
		Ns_in = 0;
		this -> ys = std::vector<int>();
		this -> xs_complex = std::vector<std::vector<Complex>>();
		this -> alpha_s = std::vector<double>();
		this -> ys_in = std::vector<int>();
		this -> xs_in_complex = std::vector<std::vector<Complex>>();
		this -> alpha_s_in = std::vector<double>();


		for(i = 0; i<N; i++){
			if((eps < alpha[i]) && (alpha[i] < C - eps)) {
				this -> ys.push_back(y[i]);

				//xs now stores a complex number

				this -> xs_complex.push_back(x_complex[i]);
				this->alpha_s.push_back(alpha[i]);
				Ns++;
			}
			else if(alpha[i] >= C - eps) {
				this -> ys_in.push_back(y[i]);

				//xs_in now stores a complex number

				this -> xs_in_complex.push_back(x_complex[i]);
				this->alpha_s_in.push_back(alpha[i]);
				Ns_in++;	
			}
		}

		this->log("Ns (number of support vectors on margin) = " + std::to_string(Ns) + "\n");
		this->log("Ns_in (number of support vectors inside margin) = " + std::to_string(Ns_in) + "\n");

		// Description for weights
		this->log("weight = [ ");
		this->w = std::vector<double>(D, 0.0);

		for (size_t z=0; z < D; z++){
		
			//we add the magnitudes of the imaginary and real parts of each entry in the vector 

			for (i = 0; i < Ns; i++){
				this->w[z] += alpha_s[i] * (double)ys[i] * (re(xs_complex[i][z]) + im(xs_complex[i][z]));
			}

			for (i = 0; i < Ns_in; i++){
				this->w[z] += alpha_s_in[i] * (double)ys_in[i] * (re(xs_in_complex[i][z]) + im(xs_in_complex[i][z]));
			}
			this->log(std::to_string(this->w[z]) + " ");
		}

		this->log("]\n");

		// Description for b
		this->b = 0.0;
		for (i = 0; i < Ns; i++){
			this->b += (double)this->ys[i] - this->dot(this->w, this->xs[i]);
	    	}
		this->b /= (double)Ns;
		this->log("bias = " + std::to_string(this->b) + "\n");
		this->log("////////////////////////////////////////////////////////\n\n");

		return;
		
	}

	double SoftMargin_SVM::f(const std::vector<Complex> x){
		return this->dot(this->w, x) + this->b; 
	}

	double SoftMargin_SVM::g(const std::vector<Complex> x){
		double F;
		int G;

		F = this->f(x);
		if (F > 0.0){
			G = 1;
		}
		else {
			G = -1;
		}
		return G;
	}
	void SoftMargin_SVM::test(const std::vector<std::vector<Complex>> class1_data, const std::vector<std::vector<Complex>> class2_data){

		size_t i;

		this -> correct_c1 = 0;
		for (i=0; i<class1_data.size(); i++){
			if (this->g(class1_data[i]) == 1){
				this -> correct_c1++ ;
			}
		}
		
		this -> correct_c2 = 0;
		for (i=0; i<class2_data.size(); i++){
			if (this->g(class2_data[i]) == -1){
				this->correct_c2++ ;
			}
		}

	
		this->accuracy = (double)(this->correct_c1 + this->correct_c2) / (double)(class1_data.size() + class2_data.size());
		this->accuracy_c1 = (double)this->correct_c1 / (double)class1_data.size();
		this->accuracy_c2 = (double)this->correct_c2 / (double)class2_data.size();

		return;

	}

