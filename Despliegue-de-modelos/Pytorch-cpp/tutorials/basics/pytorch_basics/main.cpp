#include <torch/torch.h>
#include <torch/script.h>
#include <iostream>
#include <iomanip>

void print_tensor_size(const torch::Tensor&);
void print_script_module(const torch::jit::script::Module& module, size_t spaces = 0);

using namespace std;

int main() {
    std::cout << "\nIntroduccion a PyTorch\n\n";

    // Establecer la precisión de salida de coma flotante
    std::cout << std::fixed << std::setprecision(4);

    // ================================================================ //
    //                     EJEMPLO BÁSICO DE AUTOGRAD 1                 //
    // ================================================================ //

    std::cout << "---- EJEMPLO BASICO 1 DE AUTOGRAD ----\n";

    // Creación de los tensores
    torch::Tensor x = torch::tensor(1.0, torch::requires_grad());
    torch::Tensor w = torch::tensor(2.0, torch::requires_grad());
    torch::Tensor b = torch::tensor(3.0, torch::requires_grad());

    // Construimos un grafo computacional
    auto y = w * x + b;  // y = 2 * x + 3

    // Computamos las gradientes
    y.backward();

    // Imprimimos las gradientes
    std::cout << x.grad() << '\n';  // x.grad() = 2
    std::cout << w.grad() << '\n';  // w.grad() = 1
    std::cout << b.grad() << "\n\n";  // b.grad() = 1

    // ================================================================ //
    //                     EJEMPLO BASICO 2 DE AUTOGRAD                     //
    // ================================================================ //

    std::cout << "---- EJEMPLO BASICO 2 DE AUTOGRAD ----\n";

    // Creamos los tensores
    x = torch::randn({10, 3});
    y = torch::randn({10, 2});

    // Constuimos un capa Fully connected
    torch::nn::Linear linear(3, 2);
    std::cout << "w:\n" << linear->weight << '\n';
    std::cout << "b:\n" << linear->bias << '\n\n';

    // Creamos la función de pérdida y el optimizador
    torch::nn::MSELoss criterion;
    torch::optim::SGD optimizer(linear->parameters(), torch::optim::SGDOptions(0.01));

    // Forward pass
    auto pred = linear->forward(x);

    // Calculamos la pérdida
    auto loss = criterion(pred, y);
    std::cout << "Loss: " << loss.item<double>() << '\n\n';

    // Backward pass
    loss.backward();

    // Imprimimos las gradientes
    std::cout << "dL/dw:\n" << linear->weight.grad() << '\n\n';
    std::cout << "dL/db:\n" << linear->bias.grad() << '\n';

    // 1 paso del gradiente descendente
    optimizer.step();

    // Imprimimos la pérdida después del 1er paso del descenso de gradiente
    pred = linear->forward(x);
    loss = criterion(pred, y);
    std::cout << "Loss despues del 1er paso de optimizacion: " << loss.item<double>() << "\n\n";

    // =============================================================== //
    //               CREANDO TENSORES A PARTIR DE DATOS EXISTENTES     //
    // =============================================================== //

    std::cout << "---- CREANDO TENSORES A PARTIR DE DATOS EXISTENTES ----\n";

    // ADVERTENCIA: Tensores creados con torch::from_blob(ptr_to_data, ...) 
    // no es dueño de la memoria apuntada por ptr_to_data!
    // (ver https://pytorch.org/cppdocs/notes/tensor_basics.html#using-externally-created-data)
    //
    // Si desea un tensor que tenga su propia copia de los datos, puede llamar a clone() en el
    // tensor devuelto por torch::from_blob(), e.g.:
    // torch::Tensor t = torch::from_blob(ptr_to_data, ...).clone();
    // (ver https://github.com/pytorch/pytorch/issues/12506#issuecomment-429573396)

    // Tensor a partir de un array al estilo C
    float data_array[] = {1, 2, 3, 4};
    torch::Tensor t1 = torch::from_blob(data_array, {2, 2});
    std::cout << "Tensor desde array:\n" << t1 << '\n';

    TORCH_CHECK(data_array == t1.data_ptr<float>());

    // Tensor desde vector:
    std::vector<float> data_vector = {1, 2, 3, 4};
    torch::Tensor t2 = torch::from_blob(data_vector.data(), {2, 2});
    std::cout << "Tensor desde vector:\n" << t2 << "\n\n";

    TORCH_CHECK(data_vector.data() == t2.data_ptr<float>());

    // =============================================================== //
    //             CORTAR Y EXTRAER PARTES DE TENSORES                 //
    // =============================================================== //

    std::cout << "---- CORTAR Y EXTRAER PARTES DE TENSORES ----\n";

    std::vector<int64_t> test_data = {1, 2, 3, 4, 5, 6, 7, 8, 9};
    torch::Tensor s = torch::from_blob(test_data.data(), {3, 3}, torch::kInt64);
    std::cout << "s:\n" << s << '\n';
    // Output:
    // 1 2 3
    // 4 5 6
    // 7 8 9

    using torch::indexing::Slice;
    using torch::indexing::None;
    using torch::indexing::Ellipsis;

    // La indexación y el corte de tensores se realiza de manera muy similar a cómo
    // se hace en Python.
    //
    // Para obtener una traducción completa en paralelo de todos los tipos de indexación
    // consulte:
    // https://pytorch.org/cppdocs/notes/tensor_indexing.html

    // Extraer un solo elemento tensor:
    std::cout << "\"s[0,2]\" como tensor:\n" << s.index({0, 2}) << '\n';
    std::cout << "\"s[0,2]\" como value:\n" << s.index({0, 2}).item<int64_t>() << '\n';
    // Output:
    // 3

    // Corta un tensor a lo largo de una dimensión en un índice dado.
    std::cout << "\"s[:,2]\":\n" << s.index({Slice(), 2}) << '\n';
    // Output:
    // 3
    // 6
    // 9

    // Cortar un tensor a lo largo de una dimensión en índices dados de
    // un índice de inicio hasta, pero sin incluir, un índice de finalización 
    // con un tamaño de paso determinado.
    std::cout << "\"s[:2,:]\":\n" << s.index({Slice(None, 2), Slice()}) << '\n';
    // Output:
    // 1 2 3
    // 4 5 6
    std::cout << "\"s[:,1:]\":\n" << s.index({Slice(), Slice(1, None)}) << '\n';
    // Output:
    // 2 3
    // 5 6
    // 8 9
    std::cout << "\"s[:,::2]\":\n" << s.index({Slice(), Slice(None, None, 2)}) << '\n';
    // Output:
    // 1 3
    // 4 6
    // 7 9

    // Combinación.
    std::cout << "\"s[:2,1]\":\n" << s.index({Slice(None, 2), 1}) << '\n';
    // Output:
    // 2
    // 5

    // Elipsis (...).
    std::cout << "\"s[..., :2]\":\n" << s.index({Ellipsis, Slice(None, 2)}) << "\n\n";
    // Output:
    // 1 2
    // 4 5
    // 7 8

    // =============================================================== //
    //                         INPUT PIPELINE                          //
    // =============================================================== //

    std::cout << "---- INPUT PIPELINE ----\n";

    // Construcción del dataset MNIST
    const std::string MNIST_data_path = "../../../../data/mnist/";

    auto dataset = torch::data::datasets::MNIST(MNIST_data_path)
        .map(torch::data::transforms::Normalize<>(0.1307, 0.3081))
        .map(torch::data::transforms::Stack<>());

    // Obtenemos un par de datos
    auto example = dataset.get_batch(0);
    std::cout << "Tamano del ejemplo: ";
    std::cout << example.data.sizes() << "\n";
    std::cout << "Target del ejemplo: " << example.target.item<int>() << "\n";

    // Construcción de un data loader
    auto dataloader = torch::data::make_data_loader<torch::data::samplers::RandomSampler>(
        dataset, 64);

    // Obtención de un mini-batch
    auto example_batch = *dataloader->begin();
    std::cout << "Lote de muestra - tamano de los datos: ";
    std::cout << example_batch.data.sizes() << "\n";
    std::cout << "Lote de muestra - tamano del target: ";
    std::cout << example_batch.target.sizes() << "\n\n";

    // Uso real del cargador de datos:
    // for (auto& batch : *dataloader) {
        // Código de entrenamiento aquí
    // }

    // =============================================================== //
    //                       MODELOS PREENTRENADOS                     //
    // =============================================================== //

    std::cout << "---- MODELOS PREENTRENADOS  ----\n";
    // Se realiza la carga de un modelo previamente entrenado usando la API de C ++
     // de la siguiente manera:
     // En Python:
     // (1) Cree el modelo de pytorch (previamente entrenado).
     // (2) Convierta el modelo de pytorch en un torch.jit.ScriptModule (mediante TRACING o mediante anotaciones)
     // (3) Serializar el script en un archivo.
     // En C ++:
     // (4) Cargue el archivo serializado usando torch::jit::load ()
     // Consulte https://pytorch.org/tutorials/advanced/cpp_export.html para obtener más información.

    const std::string pretrained_model_path = "../../../../tutorials/basics/pytorch_basics/model/"
        "resnet18_scriptmodule.pt";

    torch::jit::script::Module resnet;

    try {
        resnet = torch::jit::load(pretrained_model_path);
    }
    catch (const torch::Error& error) {
        std::cerr << "No se pudo cargar el archivo serizalizado " << pretrained_model_path << ".\n"
            << "Puede crear este archivo utilizando el script 'create_resnet18_scriptmodule.py' "
            "en tutorials/basics/pytorch-basics/model/.\n";
        return -1;
    }

    std::cout << "Modelo Resnet18:\n";

    print_script_module(resnet, 2);

    std::cout << "\n";

    const auto fc_weight = resnet.attr("fc").toModule().attr("weight").toTensor();

    auto in_features = fc_weight.size(1);
    auto out_features = fc_weight.size(0);

    std::cout << "Capa Fully-connected: in_features=" << in_features << ", out_features=" << out_features << "\n";

    // Ejemplo de entrada
    auto sample_input = torch::randn({1, 3, 224, 224});
    std::vector<torch::jit::IValue> inputs{sample_input};

    // Forward pass
    std::cout << "Tamano de entrada: ";
    std::cout << sample_input.sizes() << "\n";
    auto output = resnet.forward(inputs).toTensor();
    std::cout << "Tamano de salida: ";
    std::cout << output.sizes() << "\n\n";

    // =============================================================== //
    //                      GUARDAR Y CARGAR UN MODELO                 //
    // =============================================================== //

    std::cout << "---- GUARDAR Y CARGAR UN MODELO ----\n";

    // Modelo de ejemplo simple
    torch::nn::Sequential model{
        torch::nn::Conv2d(torch::nn::Conv2dOptions(1, 16, 3).stride(2).padding(1)),
        torch::nn::ReLU()
    };

    // Ruta al archivo de salida del modelo (¡todas las carpetas deben existir!).
    const std::string model_save_path = "output/model.pt";

    // Guardamos el modelo
    torch::save(model, model_save_path);

    std::cout << "Modelo guardado:\n" << model << "\n";

    // Cargamos el modelo
    torch::load(model, model_save_path);

    std::cout << "Modelo cargado:\n" << model;
}

void print_script_module(const torch::jit::script::Module& module, size_t spaces) {
    for (const auto& sub_module : module.named_children()) {
        if (!sub_module.name.empty()) {
            std::cout << std::string(spaces, ' ') << sub_module.value.type()->name().value().name()
                << " " << sub_module.name << "\n";
        }

        print_script_module(sub_module.value, spaces + 2);
    }
}

