#!/usr/bin/env python3

# Copyright (c) 2022 Vít Labuda. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#  1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following
#     disclaimer.
#  2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
#     following disclaimer in the documentation and/or other materials provided with the distribution.
#  3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
#     products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import os.path
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))
from typing import Any
from sidein.Sidein import Sidein
from sidein.providers.DependencyProviderInterface import DependencyProviderInterface
from sidein.providers.exc.DependencyProviderException import DependencyProviderException


# You can use custom dependency providers with Sidein; in fact, it's recommended when creating complex projects, as
#  the default GlobalSimpleContainer can get quite inconvenient when you manage a lot of dependencies with it.


class CustomDependencyProvider(DependencyProviderInterface):
    # As already mentioned, this method is called EACH TIME a dependency is requested (the library doesn't "cache"
    #  dependencies in any way).
    def get_dependency(self, name: str) -> Any:
        dependency = {
            "first_dependency": "First dependency from the custom dependency provider",
            "second_dependency": "Second dependency from the custom dependency provider",
        }.get(name)

        if dependency is None:
            # When an error occurs while getting a dependency (e.g. a dependency with such name doesn't exist),
            #  a DependencyProviderException (or its subclass) must be raised.
            raise DependencyProviderException("The dependency isn't present in the dependency provider.")

        return dependency


NAMESPACE_NAME = "cz.vitlabuda.sidein.example_005.example_namespace"

# You can set the namespace's dependency provider by using the set_dependency_provider() method
Sidein.ns(NAMESPACE_NAME).set_dependency_provider(CustomDependencyProvider())


@Sidein.ns(NAMESPACE_NAME).inject_dependencies("first_dependency", "second_dependency")
def function_requiring_dependencies(first_dependency, second_dependency):
    # The dependencies are acquired from the custom dependency provider now.
    print("The first dependency is:", first_dependency)
    print("The second dependency is:", second_dependency)


function_requiring_dependencies()
