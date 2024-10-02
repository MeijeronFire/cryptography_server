#include <stdio.h>
#include <gmp.h>
#include <stdbool.h>
#include <time.h>

bool isDiv(mpz_t num, unsigned int div) {
	mpz_t temp_algebra;
	mpz_init(temp_algebra);
	mpz_tdiv_r_ui(temp_algebra, num, div);
	bool returnval = (temp_algebra == 0);
	//bool returnval = (num / div) * div == num;
	mpz_clear(temp_algebra);
	return returnval;
}

bool isOdd(mpz_t num) {
	return mpz_tdiv_r_ui(num, num, 2) == 1;
	//bool returnval = (num % 2 == 1);
	//return returnval;
}

void twoSD(mpz_t num, int *S_ptr, mpz_t *D_ptr, mpz_t *numM1_ptr) {
	mpz_sub_ui(*numM1_ptr, num, 1);
	*S_ptr = 0;
	mpz_tdiv_q_ui(*D_ptr, *numM1_ptr, 2);
	//*D_ptr = (num-1 / 2);
	while (!isOdd(*D_ptr)) {
		mpz_tdiv_q_ui(*D_ptr, *D_ptr, 2);
		//*D_ptr = *D_ptr / 2;
		*S_ptr++;
	}
}

bool sieveCheck(mpz_t num) {
	int i;
	int firstPrimes[] = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97};
	for (i = 0; i < 25; i++) {
		if (isDiv(num, firstPrimes[i])) {
			return false;
		}
	}
	return true;
}

bool isPrime(mpz_t num, int iterations) {
	mpz_t D; // (longun)
	mpz_t y; // (longun)
	mpz_t numM1;
	mpz_init(numM1);
	mpz_init(D);
	mpz_init(y);
	int S;
	int j;

	mpz_t a;		// sorting out random numbers
	mpz_init(a);		// this will be the one written to
	
	gmp_randstate_t state;	// so this is the state (?)
	gmp_randinit_default(state); // setting the state (normal generator)
	gmp_randseed_ui(state, (unsigned long)time(NULL)); // better numbers

	if (!sieveCheck(num))
		return false;
	for (int i=0; i<iterations; i++) {
		mpz_urandomb(a, state, 2048); // this loads the actual rand #
		twoSD(num, &S, &D, &numM1);
		mpz_powm(y, a, D, num);
		// mod exp (a, D, num)
		if (!mpz_cmp_si(y, 1) && !mpz_cmp(y, numM1)) {
			j = 1;
			while (j < S && !mpz_cmp(y, numM1)) {
				mpz_powm_ui(y, y, 2, num);
				// y = y^2 mod num
				if (mpz_cmp_si(y, 1)) {
					mpz_clear(D);
					mpz_clear(y);
					mpz_clear(a);
					mpz_clear(numM1);
					gmp_randclear(state);
					return false;
				}
				j++;
			}
			if (!mpz_cmp(y, numM1)) {
				mpz_clear(D);
				mpz_clear(y);
				mpz_clear(a);
				mpz_clear(numM1);
				gmp_randclear(state);
				return false;
			}
		}
	}
	mpz_clear(D);
	mpz_clear(y);
	mpz_clear(a);
	mpz_clear(numM1);
	gmp_randclear(state);
	return true;
}

void primeGen(int bits, int iterations) {
	bool found = false;
	mpz_t candidate;	// sorting out random numbers
	mpz_init(candidate);	// this will be the one written to
	
	gmp_randstate_t cand_state;	// so this is the state (?)
	gmp_randinit_default(cand_state); // setting the state (normal generator)
	gmp_randseed_ui(cand_state, (unsigned long)time(NULL)); // better numbers
	while (!found) {
		mpz_urandomb(candidate, cand_state, bits); // this loads the actual rand #
		//candidate = 5; // longun, random between 3 and 2^bits
		found = isPrime(candidate, iterations);
		puts("failure.\n");
	}
	gmp_printf("%Zd\n", candidate);
	mpz_clear(candidate);
	gmp_randclear(cand_state);
}

int main() {
	primeGen(128, 64);
	//bool x = isDiv(15, 5);
	//printf("%B\n", x);
	return 0;
}
