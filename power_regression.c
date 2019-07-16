#include <stdio.h>
#include <math.h>
double find_beta(double arr_x[], double arr_y[], int n);
double find_gamma(double arr_x[], double arr_y[], int n, double beta);
int main()
{
	double arr_x[] = {3,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75};
	double arr_y[] = {9.5,8.4,7.7,7.3,7,6.8,6.6,6.3,6,5.7,5.5,5.35,5.2,5.1,5.05,5};
	int n = sizeof(arr_x)/sizeof(double);
	int m = sizeof(arr_y)/sizeof(double);
	printf(" %d, %d \n",n,m);
	double beta = find_beta(arr_x, arr_y, n);
	double gamma = find_gamma(arr_x, arr_y, n, beta);
	printf("%lf\n", gamma);
	printf("y = %lf * x ^ %lf\n", pow(10, gamma), beta);
	printf("f(x) = %lf\n", pow(10, gamma) * pow(75, beta));
	return 0;
}

double find_beta(double arr_x[], double arr_y[], int n)
{
	double sum_0 =0, sum_1 = 0, sum_2 = 0, sum_3 = 0, temp_x, temp_y;
	int	i;
	for(i = 0; i < n; i++)
	{
		temp_x = log10(arr_x[i]);
		temp_y = log10(arr_y[i]);
		sum_0 += temp_x * temp_y;
		sum_1 += temp_x;
		sum_2 += temp_y;
		sum_3 += pow(temp_x,2);
	}
	return ((n*sum_0) - (sum_1 * sum_2)) / ((n * sum_3) - (pow(sum_1,2)));
}

double find_gamma(double arr_x[], double arr_y[], int n, double beta)
{
	double sum_0 = 0, sum_1 = 0;
	int	i;
	for(i = 0; i < n; i++)
	{
		sum_0 += log10(arr_y[i]);
		sum_1 += log10(arr_x[i]);
	}
	return (sum_0 - (beta * sum_1)) / n;
}
