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
import functools
from sidein.Sidein import Sidein
from sidein.providers.simplecontainer.GlobalSimpleContainer import GlobalSimpleContainer


# If you have a decorator stored as a dependency, you can decorate a function with it using a namespace's
#  decorate_with_dependency() method. Keep in mind that the decorator is acquired and called EACH TIME a decorated
#  method is called! Both regular functions and coroutines can be decorated in this way.


def non_parametrized_decorator(func):
    @functools.wraps(func)
    def _wrapper(*args, **kwargs):
        print("Function decorated by the non-parametrized decorator has been called.")
        return func(*args, **kwargs)

    return _wrapper


def parametrized_decorator(text):
    def _decorator(func):
        def _wrapper(*args, **kwargs):
            print("Function decorated by the parametrized decorator has been called:", text)
            return func(*args, **kwargs)

        return _wrapper
    return _decorator


NAMESPACE_NAME = "cz.vitlabuda.sidein.example_004.example_namespace"
dependency_provider: GlobalSimpleContainer = Sidein.ns(NAMESPACE_NAME).get_dependency_provider()
dependency_provider.add_dependency("non_parametrized_decorator", non_parametrized_decorator)
dependency_provider.add_dependency("parametrized_decorator", parametrized_decorator)


# --- 1. Decorating a function with a non-parametrized decorator ---
print("--- 1. Decorating a function with a non-parametrized decorator ---")


@Sidein.ns(NAMESPACE_NAME).decorate_with_dependency("non_parametrized_decorator")
def decorated_function_1():
    print(decorated_function_1.__name__, "called.")


decorated_function_1()


# --- 2. Decorating a function with a parametrized decorator ---
print("--- 2. Decorating a function with a parametrized decorator ---")


@Sidein.ns(NAMESPACE_NAME).decorate_with_dependency("parametrized_decorator", lambda dependency: dependency("The decorator's parameter"))
def decorated_function_2():
    print(decorated_function_2.__name__, "called.")


decorated_function_2()
