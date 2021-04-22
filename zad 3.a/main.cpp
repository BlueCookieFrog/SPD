

#include "RandomNumberGenerator.h"
#include <iostream>


//public variablees
int seed ,n ,m;





void info( const std::vector<Task*> Pi) {
    int cmax_tmp = Cmax(Pi);
    printf("pi: [");

    for(int i = 0; i < Pi.size(); ++i) {
        cout<<Pi[i]->operation[0].number;
        if (i != Pi.size() - 1) 
            {
                printf(", ");
            }
    }



    printf("]\n");
    printf("c: [");
     for(int i = 0; i < Pi.size(); ++i) {
         printf("[");
         for (int j=0; j<m; ++j)
            {
            cout<<Pi[i]->operation[j].end;
            if(j != m - 1) printf(", ");
         }
         printf("]");
        if(i != Pi.size() - 1) printf(", ");
    }
    printf("]\n");
    printf("Cmax : %d \n", cmax_tmp);
    printf("\n\n");
}


int main() {
    

    printf("Podaj seed: ");
    std::cin>>seed;
      printf("\n");
    printf("Podaj liczbe zadan n: ");
    std::cin>>n;
      printf("\n");
    printf("Podaj liczbe maszyn: ");
    std::cin>>m;
      printf("\n");
    printf("Seed: %d, rozmiar: %dx%d\n", seed, n, m);

    std::vector<Task*> J = generateOperations(n, m, seed);
 
        
    printf("p: [");
     for(int i = 0; i < J.size(); ++i) {
         printf("[");
         for (int j=0; j<m; ++j)
            {
            printf("%d", J[i]->operation[j].time);
            if(j != m - 1) printf(", ");
         }
         printf("]");
        if(i != J.size() - 1) printf(", ");
    }
    printf("]\n\n");
    // PERMUTACJA NATURALNA
    printf("Permutacja Naturalna: \n");
    info(J);
    printf("\n");
    // ALGORYTM JOHNSONA
    printf("Johnson: \n");
    info(Jonson(J));
    printf("\n");
    // BRUTE FORCE
   // printf("BF: \n");
   // info( BruteForce(J));
    // printf("\n");



    return 0;
}

