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
from sidein.ns.NamespaceInterface import NamespaceInterface
from sidein.nsmgr.NamespaceManagerInterface import NamespaceManagerInterface


class SideinInterface(metaclass=abc.ABCMeta):
    """
    Sidein - Simple Dependency Injector

    The "gateway" to this library's functionality.
    """

    @classmethod
    @abc.abstractmethod
    def ns(cls, name: str) -> NamespaceInterface:
        """
        Returns the namespace named 'name' from the dependency injector's namespace manager.
        If the namespace doesn't exist, it is automatically created prior to returning it.

        This is just a convenience method to SideinInterface.get_namespace_manager().add_namespace_if_not_exists_and_get_it(name)

        :param name: The requested namespace's name.
        :return: The namespace named 'name'.
        """

        raise NotImplementedError(SideinInterface.ns.__qualname__)

    @classmethod
    @abc.abstractmethod
    def get_namespace_manager(cls) -> NamespaceManagerInterface:
        """
        Returns the dependency injector's namespace manager.

        :return: The dependency injector's namespace manager.
        """

        raise NotImplementedError(SideinInterface.ns.__qualname__)
