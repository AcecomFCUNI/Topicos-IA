// Copyright 2020-present pytorch-cpp Authors
#include <torch/torch.h>
#include <iostream>
#include <iomanip>

int main() {
    std::cout << "\nRegresion Lineal\n\n";
    std::cout << "Entrenando en CPU.\n";

    // Hiperparametros
    const int64_t input_size = 1;
    const int64_t output_size = 1;
    const size_t num_epochs = 60;
    const double learning_rate = 0.001;

    // Dataset de ejemplo
    auto x_train = torch::randint(0, 10, {15, 1});
    auto y_train = torch::randint(0, 10, {15, 1});

    // Modelo de regresión lineal
    torch::nn::Linear model(input_size, output_size);

    // Optimizador
    torch::optim::SGD optimizer(model->parameters(), torch::optim::SGDOptions(learning_rate));

    // Establecemos la precisión de salida de coma flotante
    std::cout << std::fixed << std::setprecision(4);

    std::cout << "Entrenando...\n";

    // Entrenamos el modelo
    for (size_t epoch = 0; epoch != num_epochs; ++epoch) {
        // Forward pass
        auto output = model(x_train);
        auto loss = torch::nn::functional::mse_loss(output, y_train);

        // Backward pass y optimizamos
        optimizer.zero_grad();
        loss.backward();
        optimizer.step();

        if ((epoch + 1) % 5 == 0) {
            std::cout << "Epoch [" << (epoch + 1) << "/" << num_epochs <<
                "], Loss: " << loss.item<double>() << "\n";
        }
    }

    std::cout << "Entrenamiento finalizado!\n";
}
