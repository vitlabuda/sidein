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


from typing import final, Optional
from sidein.SideinInterface import SideinInterface
from sidein.ns.NamespaceInterface import NamespaceInterface
from sidein.nsmgr.NamespaceManagerInterface import NamespaceManagerInterface
from sidein.nsmgr._NamespaceManager import _NamespaceManager


@final
class _ThreadSafeSidein(SideinInterface):
    """
    The implementation of this library's "gateway class".
    For it to work properly in multi-threaded programs, it needs to be behind a thread-safety locking proxy.
    """

    _namespace_manager: Optional[NamespaceManagerInterface] = None  # Lazy initialization

    @classmethod
    def ns(cls, name: str) -> NamespaceInterface:
        return cls.get_namespace_manager().add_namespace_if_not_exists_and_get_it(name)

    @classmethod
    def get_namespace_manager(cls) -> NamespaceManagerInterface:
        if cls._namespace_manager is None:
            cls._namespace_manager = cls._create_new_namespace_manager()

        return cls._namespace_manager

    @classmethod
    def _create_new_namespace_manager(cls) -> NamespaceManagerInterface:
        return _NamespaceManager()

    def __init__(self):
        raise NotImplementedError("{} is not supposed to be instantiated!".format(_ThreadSafeSidein.__qualname__))
