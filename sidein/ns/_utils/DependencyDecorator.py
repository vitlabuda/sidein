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


from typing import final, Callable, Optional, Any
import inspect
import functools
from sidein.ns.NamespaceInterface import NamespaceInterface
from sidein.ns.exc.NotAFunctionError import NotAFunctionError
from sidein.ns.exc.decoration.InvalidReplacementFunctionError import InvalidReplacementFunctionError
from sidein.ns.exc.decoration.InvalidDecoratorExtractorError import InvalidDecoratorExtractorError
from sidein.ns.exc.decoration.DecoratorExtractorRaisedAnExceptionError import DecoratorExtractorRaisedAnExceptionError
from sidein.ns.exc.decoration.InvalidDecoratorError import InvalidDecoratorError
from sidein.ns.exc.decoration.DecoratorRaisedAnExceptionError import DecoratorRaisedAnExceptionError


@final
class DependencyDecorator:
    """
    Helper class that handles this library's "decorate with dependency" feature.
    Used by _Namespace.decorate_with_dependency().
    """

    __slots__ = "_namespace",

    def __init__(self, namespace: NamespaceInterface):
        self._namespace: NamespaceInterface = namespace

    def generate_dependency_decorator_for_function(self, func: Callable, name: str, decorator_extractor: Optional[Callable[[Any], Callable]]) -> Callable:
        if decorator_extractor is None:
            decorator_extractor = self._generate_default_decorator_extractor()

        if inspect.iscoroutinefunction(func):
            return self._generate_dependency_decorator_for_async_function(func, name, decorator_extractor)

        if inspect.isroutine(func):
            return self._generate_dependency_decorator_for_regular_function(func, name, decorator_extractor)

        raise NotAFunctionError("Only functions and methods can be decorated with a dependency, not {}!".format(func))

    def _generate_default_decorator_extractor(self) -> Callable[[Any], Callable]:
        def _default_decorator_extractor(dependency: Any):
            return dependency

        return _default_decorator_extractor

    def _generate_dependency_decorator_for_regular_function(self, func: Callable, name: str, decorator_extractor: Callable[[Any], Callable]) -> Callable:
        @functools.wraps(func)
        def _regular_function_dependency_decorator(*args, **kwargs):
            replacement_function = self._get_replacement_function(func, name, decorator_extractor)

            if not inspect.isroutine(replacement_function) or inspect.iscoroutinefunction(replacement_function):
                raise InvalidReplacementFunctionError("A regular function can only be decorated with a regular replacement function, not with {}!".format(replacement_function))

            return replacement_function(*args, **kwargs)

        return _regular_function_dependency_decorator

    def _generate_dependency_decorator_for_async_function(self, async_func: Callable, name: str, decorator_extractor: Callable[[Any], Callable]) -> Callable:
        @functools.wraps(async_func)
        async def _async_function_dependency_decorator(*args, **kwargs):
            replacement_function = self._get_replacement_function(async_func, name, decorator_extractor)

            if not inspect.isroutine(replacement_function) or not inspect.iscoroutinefunction(replacement_function):
                raise InvalidReplacementFunctionError("An async function can only be decorated with an async replacement function, not with {}!".format(replacement_function))

            return await replacement_function(*args, **kwargs)

        return _async_function_dependency_decorator

    def _get_replacement_function(self, func: Callable, name: str, decorator_extractor: Callable[[Any], Callable]) -> Callable:
        # Acquire the requested dependency
        dependency = self._namespace.get_dependency(name, False)  # This method must be thread-safe!

        # Acquire the decorator
        if not inspect.isroutine(decorator_extractor) or inspect.iscoroutinefunction(decorator_extractor):
            raise InvalidDecoratorExtractorError("The decorator extractor must be a regular function, not {}!".format(decorator_extractor))

        try:
            decorator = decorator_extractor(dependency)
        except Exception as e:
            raise DecoratorExtractorRaisedAnExceptionError("The decorator extractor has raised an exception! ({})".format(str(e)), e)

        # Acquire the replacement function
        if not inspect.isroutine(decorator) or inspect.iscoroutinefunction(decorator):
            raise InvalidDecoratorError("The extracted decorator must be a regular function, not {}!".format(decorator))

        try:
            replacement_function = decorator(func)
        except Exception as e:
            raise DecoratorRaisedAnExceptionError("The extracted decorator has raised an exception! ({})".format(str(e)), e)

        # Return the replacement function
        return replacement_function
