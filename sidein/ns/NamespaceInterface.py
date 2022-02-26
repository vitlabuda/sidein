#!/bin/false

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


from typing import Callable, Any, Dict, Optional
import abc
from sidein.providers.DependencyProviderInterface import DependencyProviderInterface


class NamespaceInterface(metaclass=abc.ABCMeta):
    """
    Namespace objects are responsible for providing dependencies to their users from dependency providers.
    """

    __slots__ = ()

    @abc.abstractmethod
    def get_dependency_provider(self) -> DependencyProviderInterface:
        """
        Returns the dependency provider used by this namespace to acquire dependencies.

        Upon namespace creation, a GlobalSimpleContainer instance is automatically set as the default dependency
         provider for the new namespace. The default dependency provider will always be GlobalSimpleContainer - you
         can rely on this fact in your programs.

        :return: The dependency provider used by this namespace.
        """

        raise NotImplementedError(NamespaceInterface.get_dependency_provider.__qualname__)

    @abc.abstractmethod
    def set_dependency_provider(self, dependency_provider: DependencyProviderInterface) -> None:
        """
        Sets a new dependency provider to be used by this namespace to acquire dependencies.
        Note that when the namespace is created, it already has a default dependency provider set
         (GlobalSimpleContainer to be exact).

        :param dependency_provider: The new dependency provider to be used by this namespace.
        """

        raise NotImplementedError(NamespaceInterface.set_dependency_provider.__qualname__)

    @abc.abstractmethod
    def get_dependency(self, name: str, in_obtainer: bool = False) -> Any:
        """
        Returns the dependency named 'name' from the namespace's dependency provider.
        If 'in_obtainer' is True, a dependency obtainer object bound to the namespace and the dependency's name is
         returned instead of the "raw" dependency. See DependencyObtainerInterface's docstring for details.

        :param name: The requested dependency's name.
        :param in_obtainer: Whether to return a dependency obtainer object instead of the "raw" dependency.
        :return: The requested dependency or, if required, a dependency obtainer object bound to the requested dependency.
        :raises DependencyProviderException: If anything goes wrong in the dependency provider (e.g. if the dependency couldn't be found).
        """

        raise NotImplementedError(NamespaceInterface.get_dependency.__qualname__)

    @abc.abstractmethod
    def get_dependencies(self, *names: str, in_obtainers: bool = False) -> Dict[str, Any]:
        """
        This method works the same way as the get_dependency() method of this class, but it enables one to specify a
         variable number of dependencies.

        :param names: The requested dependencies' names.
        :param in_obtainers: Whether to return dependency obtainer objects instead of the "raw" dependencies.
        :return: All the requested dependencies or, if required, dependency obtainer objects bound to the requested dependencies.
        :raises DependencyProviderException: If anything goes wrong in the dependency provider (e.g. if the dependency couldn't be found).
        """

        raise NotImplementedError(NamespaceInterface.get_dependencies.__qualname__)

    @abc.abstractmethod
    def inject_dependencies(self, *names: str, in_obtainers: bool = False, as_kwargs: bool = True) -> Callable:
        """
        Functions or methods decorated with this  decorator will have their dependencies, specified in this decorator's
         arguments, automatically injected upon their call. This decorator supports both regular functions and
         coroutines (functions declared using "async def").
        See the docstring of this class's get_dependency() method to find out what the 'in_obtainers' argument does.
        If 'as_kwargs' is True, the requested dependencies are injected into the decorated function's **kwargs, with the
         arguments' keys being the dependencies' names. Otherwise, the dependencies are going to be appended to *args.

        :param names: The requested dependencies' names.
        :param in_obtainers: Whether to inject dependency obtainer objects instead of the "raw" dependencies.
        :param as_kwargs: Whether to inject the dependencies to **kwargs instead of *args.

        Upon calling the decorated function:
            :raises DependencyProviderException: If anything goes wrong in the dependency provider (e.g. if the dependency couldn't be found).
        """

        raise NotImplementedError(NamespaceInterface.inject_dependencies.__qualname__)

    @abc.abstractmethod
    def decorate_with_dependency(self, name: str, decorator_extractor: Optional[Callable[[Any], Callable]] = None) -> Callable:
        """
        This decorator enables one to decorate functions or methods with a dependency which acts like a decorator.

        Each time (!) a function or method decorated with this decorator is called, the dependency specified in
         the 'name' argument is acquired from the dependency provider. The dependency must be a non-parametrized
         decorator (into which the original function will be passed each time it's called). As with a regular decorator,
         the function returned by the decorator will be called (the arguments passed to the decorated function and its
         return value will stay unchanged). This decorator supports both regular functions and coroutines.
        If the dependency is a parametrized decorator or, for example, a completely different object from which you need
         to extract the decorator, one can pass a function to the 'decorator_extractor' argument. Each time the
         decorated function is called, the acquired dependency is passed to the "decorator extractor" function. The
         return value of that call is going to be used as the non-parametrized decorator instead of the "raw"
         dependency.

        The purpose and usage of this method might be quite tricky to understand just from the above explanation -
         I strongly recommend you to take a look at the examples if you want to make use of this feature.

        :param name: The requested dependency's name. If the 'decorator_extractor' optional argument is left empty, the dependency must be a non-parametrized decorator.
        :param decorator_extractor: A function into which the acquired dependency is going to be passed and whose return value is going to be used as the (non-parametrized) decorator.

        Upon calling the decorated function:
            :raises DependencyProviderException: If anything goes wrong in the dependency provider (e.g. if the dependency couldn't be found).
        """

        raise NotImplementedError(NamespaceInterface.decorate_with_dependency.__qualname__)
