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
from sidein.Sidein import Sidein
from sidein.obtainer.DependencyObtainerInterface import DependencyObtainerInterface


NAMESPACE_NAME = "cz.vitlabuda.sidein.example_003.example_namespace"
Sidein.ns(NAMESPACE_NAME).get_dependency_provider().add_dependency("unstable_dependency", 1)


# Dependency obtainer objects are responsible for holding a dependency's name and the namespace from which the
#  dependency comes from.
# This enables dependants to acquire the dependency later and/or repeatedly which is useful e.g. when the dependant
#  needs to replace the dependency and needs to get an updated reference to the dependency after that.
# The get_dependency(), get_dependencies() and inject_dependencies() methods can return dependency obtainer objects
#  instead of "raw" dependencies using the 'in_obtainer' (get_dependency) or 'in_obtainers' (get_dependencies,
#  inject_dependencies) keyword argument.

# The concept is easier to understand when you compare the following 2 classes:


class ClassUsingObtainer:
    @Sidein.ns(NAMESPACE_NAME).inject_dependencies("unstable_dependency", in_obtainers=True)
    def __init__(self, unstable_dependency):
        self._unstable_dependency_obtainer: DependencyObtainerInterface = unstable_dependency

    def print_dependency(self):
        # When called after increment_dependency(), the updated dependency is used here, as it's always obtained from
        #  the dependency provider in this case.
        print("The unstable dependency is:", self._unstable_dependency_obtainer.obtain_dependency())

    def increment_dependency(self):
        new_value = self._unstable_dependency_obtainer.obtain_dependency() + 1
        Sidein.ns(NAMESPACE_NAME).get_dependency_provider().replace_dependency("unstable_dependency", new_value)


class ClassNotUsingObtainer:
    @Sidein.ns(NAMESPACE_NAME).inject_dependencies("unstable_dependency")
    def __init__(self, unstable_dependency):
        self._unstable_dependency = unstable_dependency

    def print_dependency(self):
        # When called after increment_dependency(), the old dependency is used here, as the dependency is only obtained
        #  when instantiating the class in this case.
        print("The unstable dependency is:", self._unstable_dependency)

    def increment_dependency(self):
        new_value = self._unstable_dependency + 1
        Sidein.ns(NAMESPACE_NAME).get_dependency_provider().replace_dependency("unstable_dependency", new_value)


for class_ in (ClassUsingObtainer, ClassNotUsingObtainer):
    print("---", class_.__name__, "---")
    instance = class_()
    instance.print_dependency()
    instance.increment_dependency()
    instance.print_dependency()
