#ifndef SVM_H
#define SVM_H


#include <string>
#include <vector>

class SoftMargin_SVM{

	private:
		bool verbose;
		std::vector<double> w;
		double b;
		std::vector<std::vector<double>> xs;
		std::vector<int> ys;
		std::vector<double> alphas_s;
		std::vector<std::vector<double>> xs_in;
		std::vector<int> ys_in;
		std::vector<double> alpha_s_in;

		double dot(const std::vector<double> x1, const std::vector<double> x2);
		void log(const std::string str);

	public:


		double accuracy;
		double accuracy_a;
		double accuracy_b;
		double auroc;
		size_t correct_a;
		size_t correct_b;


		SoftMargin_SVM() = delete;
		// not sure about _=
		SoftMargin_SVM(const bool verbose_=true)

		void train(const std::vector<std::vector<double>> class1_data, const std::vector<std::vector<double>> class2_data, const size_t D, const double C, const double lr, const double limit=0.0001);

		void test(const std::vector<std::vector<double>> class1_data, const std::vector<std::vector<double>> class2_data);
		double f(const std::vector<double> x);
		double g(const std::vector<double> x);
		
};




#endif
