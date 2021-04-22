
#ifndef RANDOMNUMBERGENERATOR_HH
#define RANDOMNUMBERGENERATOR_HH
#include <cmath>
#include <vector>
#include "algorithms.hpp"
class RandomNumberGenerator
{
private:

	long seed;

public:
	RandomNumberGenerator(long seedValue) :
		seed(seedValue)
	{}
	int nextInt(int low, int high) {
		long k;
		double value_0_1;
		long m = 2147483647l, a = 16807l, b = 127773l, c = 2836l;

		k = seed / b;
		seed = a * (seed % b) - k * c;
		if (seed < 0)
			seed = seed + m;
		value_0_1 = seed;
		value_0_1 /= m;
		return low + (int)floor(value_0_1 * (high - low + 1));
	}
	float nextFloat(int low, int high) {
		low *= 100000;
		high *= 100000;
		float val = nextInt(low, high) / 100000.0;
		return val;
	}
};

std::vector<Task*> generateOperations(const int &n, const int &m, const int &seed) {
    RandomNumberGenerator random(seed);
    std::vector<Task*> J;

    for(int j = 1; j <= n; ++j) {
        Task* tmp = new Task();
        for(int i = 1; i <= m; ++i) {
            tmp->addOperation(Operation(j, random.nextInt(1, 29)));
        }
        J.push_back(tmp);
    }
    return J;
}
#endif