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


from typing import final, Any, Dict
import threading
from sidein.providers.simplecontainer.SimpleContainerInterface import SimpleContainerInterface
from sidein.providers.simplecontainer._ThreadSafeGlobalSimpleContainer import _ThreadSafeGlobalSimpleContainer


@final
class GlobalSimpleContainer(SimpleContainerInterface):
    """
    A thread-safety locking proxy to the "true" simple container implementation.
    """

    # DP: Proxy

    __slots__ = "_sc_lock", "_thread_safe_sc"

    def __init__(self):
        self._sc_lock: threading.Lock = threading.Lock()
        self._thread_safe_sc: SimpleContainerInterface = _ThreadSafeGlobalSimpleContainer()

    def get_dependency(self, name: str) -> Any:
        with self._sc_lock:
            return self._thread_safe_sc.get_dependency(name)

    def get_all_dependencies(self) -> Dict[str, Any]:
        with self._sc_lock:
            return self._thread_safe_sc.get_all_dependencies()

    def add_dependency(self, name: str, dependency: Any) -> None:
        with self._sc_lock:
            return self._thread_safe_sc.add_dependency(name, dependency)

    def replace_dependency(self, name: str, dependency: Any) -> None:
        with self._sc_lock:
            return self._thread_safe_sc.replace_dependency(name, dependency)

    def add_or_replace_dependency(self, name: str, dependency: Any) -> bool:
        with self._sc_lock:
            return self._thread_safe_sc.add_or_replace_dependency(name, dependency)

    def remove_dependency(self, name: str) -> None:
        with self._sc_lock:
            return self._thread_safe_sc.remove_dependency(name)

    def remove_all_dependencies(self) -> None:
        with self._sc_lock:
            return self._thread_safe_sc.remove_all_dependencies()
