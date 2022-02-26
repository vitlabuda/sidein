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


from typing import final, Dict
from sidein.ns.NamespaceInterface import NamespaceInterface
from sidein.ns._Namespace import _Namespace
from sidein.nsmgr.NamespaceManagerInterface import NamespaceManagerInterface
from sidein.nsmgr.exc.NamespaceNotFoundException import NamespaceNotFoundException
from sidein.nsmgr.exc.NamespaceExistsException import NamespaceExistsException


@final
class _ThreadSafeNamespaceManager(NamespaceManagerInterface):
    """
    The implementation of namespace manager.
    For it to work properly in multi-threaded programs, it needs to be behind a thread-safety locking proxy.
    """

    __slots__ = "_namespaces",

    def __init__(self):
        self._namespaces: Dict[str, NamespaceInterface] = {}

    def add_namespace_if_not_exists_and_get_it(self, name: str) -> NamespaceInterface:
        if not self._namespace_exists(name):
            self._add_namespace_checkless(name)

        return self._get_namespace_checkless(name)

    def get_namespace(self, name: str) -> NamespaceInterface:
        if not self._namespace_exists(name):
            raise NamespaceNotFoundException(name)

        return self._get_namespace_checkless(name)

    def _get_namespace_checkless(self, name: str) -> NamespaceInterface:
        return self._namespaces[name]

    def get_all_namespaces(self) -> Dict[str, NamespaceInterface]:
        # Shallow-copy the dict to prevent (accidental) modification of this this class's internal members
        return self._namespaces.copy()

    def add_namespace(self, name: str) -> None:
        if self._namespace_exists(name):
            raise NamespaceExistsException(name)

        self._add_namespace_checkless(name)

    def _add_namespace_checkless(self, name: str) -> None:
        self._namespaces[name] = self._create_new_namespace()

    def remove_namespace(self, name: str) -> None:
        if not self._namespace_exists(name):
            raise NamespaceNotFoundException(name)

        self._remove_namespace_checkless(name)

    def _remove_namespace_checkless(self, name: str) -> None:
        del self._namespaces[name]

    def remove_all_namespaces(self) -> None:
        self._namespaces.clear()

    def _create_new_namespace(self) -> NamespaceInterface:
        return _Namespace()

    def _namespace_exists(self, name: str) -> bool:
        return name in self._namespaces
