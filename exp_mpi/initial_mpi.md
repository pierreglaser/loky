# Listing all the symbole in the lib

`nm -D /usr/lib/openmpi/libmpi.so.12`

# Loading the MPI library

```python
from ctypes.util import find_library
import ctypes
libmpi = find_library("mpi")
mode = ctypes.RTLD_GLOBAL
if hasattr(ctypes, "RTLD_NOW"):
    mode |= ctypes.RTLD_NOW
if hasattr(ctypes, "RTLD_NOLOAD"):
    mode |= ctypes.RTLD_NOLOAD
MPI = ctypes.CDLL(libmpi, mode=mode)

```
