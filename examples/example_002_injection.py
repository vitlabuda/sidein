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
import asyncio
from sidein.Sidein import Sidein
from sidein.providers.simplecontainer.GlobalSimpleContainer import GlobalSimpleContainer


NAMESPACE_NAME = "cz.vitlabuda.sidein.example_002.example_namespace"
dependency_provider: GlobalSimpleContainer = Sidein.ns(NAMESPACE_NAME).get_dependency_provider()
dependency_provider.add_dependency("first_dependency", "Hello Sidein!")
dependency_provider.add_dependency("second_dependency", 1234)


# --- 1. Injecting dependencies to a function with other arguments ---
print("--- 1. Injecting dependencies to a function with other arguments ---")


@Sidein.ns(NAMESPACE_NAME).inject_dependencies("first_dependency", "second_dependency")
def function_requiring_dependencies_1(argument, first_dependency, second_dependency):
    print("The argument is:", argument)
    print("The first dependency is:", first_dependency)
    print("The second dependency is:", second_dependency)


function_requiring_dependencies_1(1)
function_requiring_dependencies_1(argument=2)


# --- 2. Injecting dependencies to positional arguments ---
print("--- 2. Injecting dependencies to positional arguments ---")


@Sidein.ns(NAMESPACE_NAME).inject_dependencies("first_dependency", "second_dependency", as_kwargs=False)
def function_requiring_dependencies_2(argument, dep1, dep2):
    # Note that dependencies are inserted to the last positional arguments in the order they were requested and that
    #  the argument names don't have to match the dependency names.
    print("The argument is:", argument)
    print("The first dependency is:", dep1)
    print("The second dependency is:", dep2)


function_requiring_dependencies_2(1)


# --- 3. Injecting dependencies to a coroutine ---
print("--- 3. Injecting dependencies to a coroutine ---")


@Sidein.ns(NAMESPACE_NAME).inject_dependencies("first_dependency", "second_dependency")
async def coroutine_requiring_dependencies(first_dependency, second_dependency):
    # You can inject dependencies to a coroutine in the same way as to a regular function.
    print("The first dependency is:", first_dependency)
    print("The second dependency is:", second_dependency)


asyncio.run(coroutine_requiring_dependencies())


# --- 4. Injecting dependencies to a class ---
print("--- 4. Injecting dependencies to a class ---")


class ClassRequiringDependencies:
    # Currently, it's not possible to decorate classes with the dependency injector directly; to inject dependencies to
    #  new class instances, decorate the __init__() method.
    @Sidein.ns(NAMESPACE_NAME).inject_dependencies("first_dependency", "second_dependency")
    def __init__(self, first_dependency, second_dependency):
        self._first_dependency = first_dependency
        self._second_dependency = second_dependency

    def print_instance_vars(self):
        print("The first dependency is:", self._first_dependency)
        print("The second dependency is:", self._second_dependency)

    # It's obviously also possible to inject dependencies into other methods.
    @Sidein.ns(NAMESPACE_NAME).inject_dependencies("first_dependency", "second_dependency")
    def method_requiring_dependencies(self, first_dependency, second_dependency):
        print("The first dependency is:", first_dependency)
        print("The second dependency is:", second_dependency)


class_requiring_dependencies = ClassRequiringDependencies()
class_requiring_dependencies.print_instance_vars()
class_requiring_dependencies.method_requiring_dependencies()
