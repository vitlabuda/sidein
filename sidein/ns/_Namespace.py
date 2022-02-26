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


from typing import final, Any, Dict, Callable, Optional
import threading
from sidein.ns.NamespaceInterface import NamespaceInterface
from sidein.ns._utils.DependencyInjector import DependencyInjector
from sidein.ns._utils.DependencyDecorator import DependencyDecorator
from sidein.ns.exc.DependencyProviderRaisedAnExceptionError import DependencyProviderRaisedAnExceptionError
from sidein.ns.exc.DuplicateDependencyRequestedError import DuplicateDependencyRequestedError
from sidein.providers.DependencyProviderInterface import DependencyProviderInterface
from sidein.providers.simplecontainer.GlobalSimpleContainer import GlobalSimpleContainer
from sidein.providers.exc.DependencyProviderException import DependencyProviderException
from sidein.providers.exc.DependencyProviderError import DependencyProviderError
from sidein.obtainer._DependencyObtainer import _DependencyObtainer


@final
class _Namespace(NamespaceInterface):
    """
    The implementation of namespace.
    """

    # This class isn't just a thread-safety locking proxy, as it's common in this library, because this class exposes
    # decorators to the outside (inject_deps) which require special handling in relation to locking.
    # (It's not a huge problem though, as the methods of this class which require locking are very simple.)

    __slots__ = "_lock", "_dependency_provider", "_dependency_injector", "_dependency_decorator"

    def __init__(self):
        self._lock: threading.Lock = threading.Lock()
        self._dependency_provider: DependencyProviderInterface = self._create_default_dependency_provider()

        self._dependency_injector: DependencyInjector = DependencyInjector(self)
        self._dependency_decorator: DependencyDecorator = DependencyDecorator(self)

    def _create_default_dependency_provider(self) -> DependencyProviderInterface:
        return GlobalSimpleContainer()  # MUST NOT BE CHANGED!

    def get_dependency_provider(self) -> DependencyProviderInterface:
        with self._lock:
            return self._dependency_provider

    def set_dependency_provider(self, dependency_provider: DependencyProviderInterface) -> None:
        with self._lock:
            self._dependency_provider = dependency_provider

    def get_dependency(self, name: str, in_obtainer: bool = False) -> Any:
        with self._lock:
            return self._get_dependency_thread_safe(name, in_obtainer)

    def get_dependencies(self, *names: str, in_obtainers: bool = False) -> Dict[str, Any]:
        if len(names) != len(set(names)):
            # This check is necessary, as the returned dictionary could have "less items" than it was requested if a
            #  name was specified multiple times in the arguments
            raise DuplicateDependencyRequestedError("A dependency was requested multiple times!")

        # All the required dependencies must be obtained under a single continuous lock to prevent other threads
        #  from changing the dependency provider halfway through the process (otherwise, it would be possible for the
        #  dependencies from a single injection request to be extracted from more than one dependency provider -->
        #  race condition).
        with self._lock:
            return {name: self._get_dependency_thread_safe(name, in_obtainers) for name in names}

    # This method must be called in a thread-safe context!
    def _get_dependency_thread_safe(self, name: str, in_obtainer: bool) -> Any:
        if in_obtainer:
            return _DependencyObtainer(self, name)

        try:
            return self._dependency_provider.get_dependency(name)
        except (DependencyProviderException, DependencyProviderError) as e:
            raise e
        except Exception as e:
            raise DependencyProviderRaisedAnExceptionError("The dependency provider has raised an unexpected exception!", e)

    def inject_dependencies(self, *names: str, in_obtainers: bool = False, as_kwargs: bool = True) -> Callable:
        def _inject_dependencies_decorator(func):
            return self._dependency_injector.generate_injector_for_function(func, names, in_obtainers, as_kwargs)

        return _inject_dependencies_decorator

    def decorate_with_dependency(self, name: str, decorator_extractor: Optional[Callable[[Any], Callable]] = None) -> Callable:
        def _decorate_with_dependency_decorator(func):
            return self._dependency_decorator.generate_dependency_decorator_for_function(func, name, decorator_extractor)

        return _decorate_with_dependency_decorator
