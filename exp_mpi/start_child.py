
from ctypes.util import find_library
import ctypes

libmpi = find_library("mpi")
mode = ctypes.RTLD_GLOBAL
if hasattr(ctypes, "RTLD_NOW"):
    mode |= ctypes.RTLD_NOW
if hasattr(ctypes, "RTLD_NOLOAD"):
    mode |= ctypes.RTLD_NOLOAD
MPI = ctypes.CDLL(libmpi, mode=mode)
MPI.MPI_Init()

INTP = ctypes.POINTER(ctypes.c_int)
num = ctypes.c_int(-1)
ptr = ctypes.cast(ctypes.addressof(num), INTP)

MPI.MPI_Comm_size(MPI.ompi_mpi_comm_world, ptr)
size = ptr[0]
MPI.MPI_Comm_rank(MPI.ompi_mpi_comm_world, ptr)
rank = ptr[0]
print("MPI hello from {}/{}".format(rank, size))

MPI.MPI_Finalize()
