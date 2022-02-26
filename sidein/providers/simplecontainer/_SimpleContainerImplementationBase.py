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


from typing import Dict, Any
import abc
from sidein.providers.simplecontainer.SimpleContainerInterface import SimpleContainerInterface
from sidein.providers.simplecontainer.exc.DependencyInSCNotFoundException import DependencyInSCNotFoundException
from sidein.providers.simplecontainer.exc.DependencyInSCExistsException import DependencyInSCExistsException


class _SimpleContainerImplementationBase(SimpleContainerInterface, metaclass=abc.ABCMeta):
    """
    The base class for simple container implementations which store dependencies in a dictionary.
    """

    __slots__ = ()

    @abc.abstractmethod
    def _get_dependency_storage_dict(self) -> Dict[str, Any]:
        raise NotImplementedError(_SimpleContainerImplementationBase._get_dependency_storage_dict.__qualname__)

    def get_dependency(self, name: str) -> Any:
        if not self._dependency_exists(name):
            raise DependencyInSCNotFoundException(name)

        return self._get_dependency_checkless(name)

    def _get_dependency_checkless(self, name: str) -> Any:
        return self._get_dependency_storage_dict()[name]

    def get_all_dependencies(self) -> Dict[str, Any]:
        # Shallow-copy the dict to prevent (accidental) modification of this this class's internal members
        return self._get_dependency_storage_dict().copy()

    def add_dependency(self, name: str, dependency: Any) -> None:
        if self._dependency_exists(name):
            raise DependencyInSCExistsException(name)

        self._add_or_replace_dependency_checkless(name, dependency)

    def replace_dependency(self, name: str, dependency: Any) -> None:
        if not self._dependency_exists(name):
            raise DependencyInSCNotFoundException(name)

        self._add_or_replace_dependency_checkless(name, dependency)

    def add_or_replace_dependency(self, name: str, dependency: Any) -> bool:
        is_going_to_be_replaced = self._dependency_exists(name)

        self._add_or_replace_dependency_checkless(name, dependency)

        return is_going_to_be_replaced  # Returns True if the dependency is replaced, False if it is added.

    # There is nothing to check in this method, but it has "checkless" in its name nevertheless due to code consistency.
    def _add_or_replace_dependency_checkless(self, name: str, dependency: Any) -> None:
        self._get_dependency_storage_dict()[name] = dependency

    def remove_dependency(self, name: str) -> None:
        if not self._dependency_exists(name):
            raise DependencyInSCNotFoundException(name)

        self._remove_dependency_checkless(name)

    def _remove_dependency_checkless(self, name: str) -> None:
        del self._get_dependency_storage_dict()[name]

    def remove_all_dependencies(self) -> None:
        self._get_dependency_storage_dict().clear()

    def _dependency_exists(self, name: str) -> bool:
        return name in self._get_dependency_storage_dict()
