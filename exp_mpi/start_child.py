
from ctypes.util import find_library
import ctypes
import os

libmpi = find_library("mpi")
mode = ctypes.RTLD_GLOBAL
if hasattr(ctypes, "RTLD_NOW"):
    mode |= ctypes.RTLD_NOW
if hasattr(ctypes, "RTLD_NOLOAD"):
    mode |= ctypes.RTLD_NOLOAD
MPI = ctypes.CDLL(libmpi, mode=mode)
MPI.MPI_Init(0, None)
MPI.MPI_LOCK_EXCLUSIVE = 1


if __name__ == "__main__":

    INTP = ctypes.POINTER(ctypes.c_int)
    num = ctypes.c_int(-1)
    ptr = ctypes.cast(ctypes.addressof(num), INTP)

    CHAR_P = ctypes.POINTER(ctypes.c_char)
    buf = ctypes.c_char(0)
    char_ptr = ctypes.cast(ctypes.addressof(buf), CHAR_P)

    MPI.MPI_Comm_size(MPI.ompi_mpi_comm_world, ptr)
    size = ptr[0]
    MPI.MPI_Comm_rank(MPI.ompi_mpi_comm_world, ptr)
    rank = ptr[0]
    MPI.MPI_Get_processor_name(char_ptr, ptr)
    name = char_ptr[:ptr[0]].decode()
    print("MPI hello from {}/{} on {}".format(rank, size, name))
    print(os.getpid())

    win = ctypes.c_int()
    win_p = ctypes.cast(ctypes.addressof(win), INTP)
    t_sem = ctypes.c_int * 1
    sem = t_sem(ctypes.c_int(0))
    res = MPI.MPI_Win_allocate(8, 8, MPI.ompi_mpi_info_null,
                               MPI.ompi_mpi_comm_world, sem, win_p)
    print("result", res)

    MPI.MPI_Win_lock(MPI.MPI_LOCK_EXCLUSIVE, rank, 0, win_p)
    MPI.MPI_Win_unlock(1, win_p)

    MPI.MPI_Win_free(win_p)

    MPI.MPI_Finalize()
