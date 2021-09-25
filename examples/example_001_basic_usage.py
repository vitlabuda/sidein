#!/usr/bin/env python3

# SPDX-License-Identifier: BSD-3-Clause
#
# Copyright (c) 2021 Vít Labuda. All rights reserved.
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
from sidein.Sidein import Sidein
from sidein.providers.simplecontainer.GlobalSimpleContainer import GlobalSimpleContainer


NAMESPACE_NAME = "cz.vitlabuda.sidein.example_001.example_namespace"


# Sidein is a flexible, object-oriented dependency injector for Python 3.9 and above which hides the boring stuff away
#  and leaves the important things up to you.

# The main "building blocks" of the Sidein library are namespaces.
# Each namespace has a name which should be fully qualified (to prevent collisions e.g. with third party modules'
#  namespaces), for example "com.example.myprogram.namespace_main".
# Namespaces can return dependencies, inject them to functions and decorate functions with them. Each dependency must
#  have a unique name which is used to request it.
# The dependencies are fetched from the namespace's dependency provider which is a class implementing the
#  NamespaceManagerInterface interface. The interface's get_dependency() method is called EACH TIME a dependency is
#  requested (the library doesn't "cache" dependencies in any way). The default dependency provider implementation is
#  GlobalSimpleContainer - this will never change and you can rely on this fact in your programs.

# Keep in mind that the main purpose of these examples is to give you a overview of what this library can do. See the
#  classes' (interfaces') and their methods' docstrings for usage and implementation details.


# You can add dependencies to a GlobalSimpleContainer instance the following way:
dependency_provider: GlobalSimpleContainer = Sidein.ns(NAMESPACE_NAME).get_dependency_provider()
dependency_provider.add_dependency("first_dependency", "Hello Sidein!")
dependency_provider.add_dependency("second_dependency", 1234)


# --- 1. Manually requesting a dependency ---
print("--- 1. Manually requesting a dependency ---")

dependency = Sidein.ns(NAMESPACE_NAME).get_dependency("first_dependency")
print("The first dependency is:", dependency)


# --- 2. Manually requesting multiple dependencies ---
print("--- 2. Manually requesting multiple dependencies ---")

dependencies = Sidein.ns(NAMESPACE_NAME).get_dependencies("first_dependency", "second_dependency")
print("The first dependency is:", dependencies["first_dependency"])
print("The second dependency is:", dependencies["second_dependency"])


# --- 3. Basic dependency injection ---
print("--- 3. Basic dependency injection ---")


@Sidein.ns(NAMESPACE_NAME).inject_dependencies("first_dependency", "second_dependency")
def function_requiring_dependencies(first_dependency, second_dependency):
    # Note that dependencies are injected to keywords arguments with the dependency name being the argument key.
    print("The first dependency is:", first_dependency)
    print("The second dependency is:", second_dependency)


function_requiring_dependencies()
