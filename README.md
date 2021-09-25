# Sidein
**Sidein** is a flexible, object-oriented Python dependency injector which hides the boring stuff away and leaves the important things up to you.



## Features and characteristics
* supports **Python 3.9 and above**
* dependency injection to both regular functions and coroutines
* the ability to decorate functions with dependencies
* support for multiple [namespaces](sidein/ns/NamespaceInterface.py)
* design centered around [dependency providers](sidein/providers/DependencyProviderInterface.py)
  * the ability to create your own dependency provider classes
* [dependency obtainer objects](sidein/obtainer/DependencyObtainerInterface.py)
* thread-safe
* data-type agnostic
* object-oriented



## Requirements
The library targets **Python 3.9 and above**.
It might work in older Python 3 versions, but nothing is guaranteed.  

No dependencies *(other than the Python standard library)* are required.



## Usage
The [examples](examples) will give you an overview of what this library can do.
See the classes' and their methods' docstrings for usage and implementation details.



## Licensing
This project is licensed under the **3-clause BSD license**. See the [LICENSE](LICENSE) file for details.

Written by **[Vít Labuda](https://vitlabuda.cz/)**.
