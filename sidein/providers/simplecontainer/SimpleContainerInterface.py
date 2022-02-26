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


import abc
from typing import Any, Dict
from sidein.providers.DependencyProviderInterface import DependencyProviderInterface


class SimpleContainerInterface(DependencyProviderInterface, metaclass=abc.ABCMeta):
    """
    A dependency provider implementation which stores dependencies in an internal dictionary.
    """

    # NOTE: As you might've noticed, there is no dependency_exists() method in this interface. The reason for that is
    # that it would encourage its thread-unsafe use. Consider the following code:
    #
    # if container.dependency_exists(name):
    #     container.remove_dependency(name)
    #
    # If two threads executed this piece of code at the same time, a race condition could occur (while the methods
    # exported by this interface are guaranteed to be thread-safe, this doesn't mean they cannot be used wrongly).
    # For this reason, it's reasonable to think of a better, thread-safe method of achieving your goal - a method which
    # doesn't check the presence of a dependency at all; for example, instead of the above code snippet, you could
    # write this:
    #
    # try:
    #     container.remove_dependency(name)  # This method *itself* is guaranteed to be thread-safe
    # except DependencyProviderException:
    #     pass

    __slots__ = ()

    @abc.abstractmethod
    def get_dependency(self, name: str) -> Any:
        """
        Returns the dependency named 'name' from the dependency container.

        :param name: The requested dependency's name.
        :return: The dependency named 'name'.
        :raises DependencyInSCNotFoundException: If the requested dependency isn't present in the dependency container. (DependencyInSCNotFoundException is a subclass of DependencyProviderException!)
        """

        raise NotImplementedError(SimpleContainerInterface.get_dependency.__qualname__)

    @abc.abstractmethod
    def get_all_dependencies(self) -> Dict[str, Any]:
        """
        Returns all the dependencies stored in the dependency container in a {name: dependency} dictionary.

        :return: All the dependencies stored in the dependency container.
        """

        raise NotImplementedError(SimpleContainerInterface.get_all_dependencies.__qualname__)

    @abc.abstractmethod
    def add_dependency(self, name: str, dependency: Any) -> None:
        """
        Adds the dependency 'dependency' to the dependency container under the name 'name'.

        :param name: The added dependency's name.
        :param dependency: The added dependency.
        :raises DependencyInSCExistsException: If the added dependency is already present in the dependency container.
        """

        raise NotImplementedError(SimpleContainerInterface.add_dependency.__qualname__)

    @abc.abstractmethod
    def replace_dependency(self, name: str, dependency: Any) -> None:
        """
        Replaces the already existing dependency named 'name' with the new dependency 'dependency' in the dependency container.

        :param name: The replaced dependency's name.
        :param dependency: The new dependency to replace the old dependency with.
        :raises DependencyInSCNotFoundException: If the replaced dependency isn't present in the dependency container.
        """

        raise NotImplementedError(SimpleContainerInterface.replace_dependency.__qualname__)

    @abc.abstractmethod
    def add_or_replace_dependency(self, name: str, dependency: Any) -> bool:
        """
        Adds the dependency 'dependency' to the dependency container under the name 'name', if it isn't present there.
        Otherwise, the old dependency is replaced with the new one.

        :param name: The added or replaced dependency's name.
        :param dependency: The new dependency to add or to replace the old dependency with.
        :return: True if the dependency is replaced, False if it is added.
        """

        raise NotImplementedError(SimpleContainerInterface.add_or_replace_dependency.__qualname__)

    @abc.abstractmethod
    def remove_dependency(self, name: str) -> None:
        """
        Removes the dependency named 'name' from the dependency container.

        :param name: The removed dependency's name.
        :raises DependencyInSCNotFoundException: If the removed dependency isn't present in the dependency container.
        """

        raise NotImplementedError(SimpleContainerInterface.remove_dependency.__qualname__)

    @abc.abstractmethod
    def remove_all_dependencies(self) -> None:
        """
        Removes all the dependencies stored in the dependency container.
        """

        raise NotImplementedError(SimpleContainerInterface.remove_all_dependencies.__qualname__)
