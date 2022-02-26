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


from typing import final, Type
import threading
from sidein.SideinInterface import SideinInterface
from sidein._ThreadSafeSidein import _ThreadSafeSidein
from sidein.ns.NamespaceInterface import NamespaceInterface
from sidein.nsmgr.NamespaceManagerInterface import NamespaceManagerInterface


@final
class Sidein(SideinInterface):
    """
    Sidein - Simple Dependency Injector

    A thread-safety locking proxy to this library's "gateway class".
    """

    # DP: Proxy

    _SIDEIN_LOCK: threading.Lock = threading.Lock()
    _THREAD_SAFE_SIDEIN: Type[SideinInterface] = _ThreadSafeSidein

    @classmethod
    def ns(cls, name: str) -> NamespaceInterface:
        with cls._SIDEIN_LOCK:
            return cls._THREAD_SAFE_SIDEIN.ns(name)

    @classmethod
    def get_namespace_manager(cls) -> NamespaceManagerInterface:
        with cls._SIDEIN_LOCK:
            return cls._THREAD_SAFE_SIDEIN.get_namespace_manager()

    def __init__(self):
        raise NotImplementedError("{} is not supposed to be instantiated!".format(Sidein.__qualname__))
