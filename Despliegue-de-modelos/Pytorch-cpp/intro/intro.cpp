#include <torch/torch.h>
#include <math.h>
#include <iostream>
using namespace std;

int main() {

  /*
  En la carpeta 'build' ejecute 
  $ cmake ..
  $ cmake --build . --config Release
  */

  torch::Device device(torch::cuda::is_available() ? torch::kCUDA : torch::kCPU);
  auto x = torch::tensor({4.0}, torch::requires_grad());
  cout<<"imprimiendo x..\n"<<x<<endl;
  auto y = x*x;
  cout<<"imprimiento y..\n"<<y<<endl;
  y.backward();


  cout << "Imprimiendo dy/dx..\n";
  cout << x.grad() <<endl;
	
}

