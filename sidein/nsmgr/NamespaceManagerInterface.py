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


from typing import Dict
import abc
from sidein.ns.NamespaceInterface import NamespaceInterface


class NamespaceManagerInterface(metaclass=abc.ABCMeta):
    """
    Namespace manager objects are responsible for taking care of namespace objects.
    """

    # NOTE: The reason why this interface doesn't export a namespace_exists() method is that it would encourage its
    # thread-unsafe use. See the NOTE in the SimpleContainerInteface.py file for more details.

    __slots__ = ()

    @abc.abstractmethod
    def add_namespace_if_not_exists_and_get_it(self, name: str) -> NamespaceInterface:
        """
        Returns the namespace named 'name' from the namespace manager.
        If the namespace doesn't exist, it is automatically created prior to returning it.

        :param name: The requested namespace's name.
        :return: The namespace named 'name'.
        """

        raise NotImplementedError(NamespaceManagerInterface.add_namespace_if_not_exists_and_get_it.__qualname__)

    @abc.abstractmethod
    def get_namespace(self, name: str) -> NamespaceInterface:
        """
        Returns the namespace named 'name' from the namespace manager.

        :param name: The requested namespace's name.
        :return: The namespace named 'name'.
        :raises NamespaceNotFoundException: If a namespace named 'name' isn't present in the namespace manager.
        """

        raise NotImplementedError(NamespaceManagerInterface.get_namespace.__qualname__)

    @abc.abstractmethod
    def get_all_namespaces(self) -> Dict[str, NamespaceInterface]:
        """
        Returns all the namespaces stored in the namespace manager in a {name: namespace} dictionary.

        :return: All the namespaces stored in the namespace manager.
        """

        raise NotImplementedError(NamespaceManagerInterface.get_all_namespaces.__qualname__)

    @abc.abstractmethod
    def add_namespace(self, name: str) -> None:
        """
        Adds a new namespace named 'name' to the namespace manager.

        :param name: The added namespace's name.
        :raises NamespaceExistsException: If a namespace named 'name' already exists in the namespace manager.
        """

        raise NotImplementedError(NamespaceManagerInterface.add_namespace.__qualname__)

    @abc.abstractmethod
    def remove_namespace(self, name: str) -> None:
        """
        Removes the namespace named 'name' from the namespace manager.

        Note that all references to the removed namespace obtained prior to removing it stay valid.
        This behavior can have "unexpected" effects, e.g. when a namespace is removed and a new namespace with the same
         name is added to the namespace manager, all functions/methods that have been decorated with the old namespace's
         inject_dependencies() method (note that decorators are evaluated at import-time in most circumstances) will
         still have their dependencies injected from the old, "removed" namespace when they are called (this obviously
         applies to the decorate_with_dependency() method too).
        Therefore, THE USAGE OF THIS METHOD IS DISCOURAGED in the vast majority of circumstances.

        :param name: The removed namespace's name.
        :raises NamespaceNotFoundException: If a namespace named 'name' isn't present in the namespace manager.
        """

        raise NotImplementedError(NamespaceManagerInterface.remove_namespace.__qualname__)

    @abc.abstractmethod
    def remove_all_namespaces(self) -> None:
        """
        Removes all the namespaces stored in the namespace manager.

        As with the remove_namespace() method, THE USAGE OF THIS METHOD IS DISCOURAGED in the vast majority of
         circumstances. See its docstring for more details.
        """

        raise NotImplementedError(NamespaceManagerInterface.remove_all_namespaces.__qualname__)
