<!--
Copyright (c) 2022 Vít Labuda. All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
following conditions are met:
 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following
    disclaimer.
 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
    following disclaimer in the documentation and/or other materials provided with the distribution.
 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
    products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
-->


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
