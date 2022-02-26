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
import threading
from sidein.ns.NamespaceInterface import NamespaceInterface
from sidein.nsmgr.NamespaceManagerInterface import NamespaceManagerInterface
from sidein.nsmgr._ThreadSafeNamespaceManager import _ThreadSafeNamespaceManager


@final
class _NamespaceManager(NamespaceManagerInterface):
    """
    A thread-safety locking proxy to the "true" namespace manager implementation.
    """

    # DP: Proxy

    __slots__ = "_nsmgr_lock", "_thread_safe_nsmgr"

    def __init__(self):
        self._nsmgr_lock: threading.Lock = threading.Lock()
        self._thread_safe_nsmgr: NamespaceManagerInterface = _ThreadSafeNamespaceManager()

    def add_namespace_if_not_exists_and_get_it(self, name: str) -> NamespaceInterface:
        with self._nsmgr_lock:
            return self._thread_safe_nsmgr.add_namespace_if_not_exists_and_get_it(name)

    def get_namespace(self, name: str) -> NamespaceInterface:
        with self._nsmgr_lock:
            return self._thread_safe_nsmgr.get_namespace(name)

    def get_all_namespaces(self) -> Dict[str, NamespaceInterface]:
        with self._nsmgr_lock:
            return self._thread_safe_nsmgr.get_all_namespaces()

    def add_namespace(self, name: str) -> None:
        with self._nsmgr_lock:
            return self._thread_safe_nsmgr.add_namespace(name)

    def remove_namespace(self, name: str) -> None:
        with self._nsmgr_lock:
            return self._thread_safe_nsmgr.remove_namespace(name)

    def remove_all_namespaces(self) -> None:
        with self._nsmgr_lock:
            return self._thread_safe_nsmgr.remove_all_namespaces()
