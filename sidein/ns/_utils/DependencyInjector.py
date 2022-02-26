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


from typing import final, Callable, Tuple, Any, Dict
import inspect
import functools
from sidein.ns.NamespaceInterface import NamespaceInterface
from sidein.ns.exc.NotAFunctionError import NotAFunctionError


@final
class DependencyInjector:
    """
    Helper class that handles this library's dependency injection capabilities.
    Used by _Namespace.inject_dependencies().
    """

    __slots__ = "_namespace",

    def __init__(self, namespace: NamespaceInterface):
        self._namespace: NamespaceInterface = namespace

    def generate_injector_for_function(self, func: Callable, names: Tuple[str, ...], in_obtainers: bool, as_kwargs: bool) -> Callable:
        if inspect.iscoroutinefunction(func):
            return self._generate_injector_for_async_function(func, names, in_obtainers, as_kwargs)

        if inspect.isroutine(func):
            return self._generate_injector_for_regular_function(func, names, in_obtainers, as_kwargs)

        raise NotAFunctionError("Dependencies can only be injected to functions and methods, not to {}!".format(func))

    def _generate_injector_for_regular_function(self, func: Callable, names: Tuple[str, ...], in_obtainers: bool, as_kwargs: bool) -> Callable:
        @functools.wraps(func)
        def _regular_function_injector(*args, **kwargs):
            # Each time the function is called (!), the required dependencies are injected into the callable's arguments
            #  from the namespace's current dependency provider (from the namespace provider that is set when the method
            #  is called)
            args, kwargs = self._perform_injection(args, kwargs, names, in_obtainers, as_kwargs)

            return func(*args, **kwargs)

        return _regular_function_injector

    def _generate_injector_for_async_function(self, async_func: Callable, names: Tuple[str, ...], in_obtainers: bool, as_kwargs: bool) -> Callable:
        @functools.wraps(async_func)
        async def _async_function_injector(*args, **kwargs):
            # Each time the function is called (!), the required dependencies are injected into the callable's arguments
            #  from the namespace's current dependency provider (from the namespace provider that is set when the method
            #  is called)
            args, kwargs = self._perform_injection(args, kwargs, names, in_obtainers, as_kwargs)

            return await async_func(*args, **kwargs)

        return _async_function_injector

    def _perform_injection(self, args: Tuple[Any, ...], kwargs: Dict[str, Any], names: Tuple[str, ...], in_obtainers: bool, as_kwargs: bool) -> Tuple[Tuple[Any, ...], Dict[str, Any]]:
        dependencies = self._namespace.get_dependencies(*names, in_obtainers=in_obtainers)  # This method must be thread-safe!

        if as_kwargs:
            kwargs.update(dependencies)
        else:
            # Just appending dependencies.values() is not possible, as dictionaries may not preserve their order
            args += tuple(dependencies[name] for name in names)

        # It is not necessary to return the kwargs, because the dictionary containing them is obviously mutable, but
        #  it's done nevertheless due to code consistency and possible future changes
        return args, kwargs
