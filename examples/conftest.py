import atexit
import os
import shutil
import tempfile
import uuid

import pytest

if os.name != "nt":
    nbval_kernel = pytest.importorskip("nbval.kernel")
    from jupyter_client.manager import KernelManager

    # Over TCP each kernel picks five free ports, closes them and binds them
    # again in the kernel process. With several xdist workers starting kernels
    # at once another process can take a port in between, and the kernel dies
    # with "Address already in use" (jupyter/jupyter_client#487). IPC sockets
    # have unique paths, so they cannot collide.
    _IPC_DIR = tempfile.mkdtemp(prefix="pmui-nbval-")
    atexit.register(shutil.rmtree, _IPC_DIR, ignore_errors=True)

    class IPCKernelManager(KernelManager):

        def __init__(self, **kwargs):
            kwargs.setdefault("transport", "ipc")
            kwargs.setdefault("ip", os.path.join(_IPC_DIR, uuid.uuid4().hex[:12]))
            super().__init__(**kwargs)

    nbval_kernel.KernelManager = IPCKernelManager
