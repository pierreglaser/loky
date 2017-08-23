
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


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser('Programme to launch MPI experiment')
    parser.add_argument('-n', type=int, default=4,
                        help='Number of MPI process spawned')

    args = parser.parse_args()

    print("Starting MPI program")
    INTP = ctypes.POINTER(ctypes.c_int)
    num = ctypes.c_int(-1)
    ptr = ctypes.cast(ctypes.addressof(num), INTP)

    max_proc = ctypes.c_int(args.n)
    root = ctypes.c_int(0)
    intercomm = MPI.ompi_mpi_comm_null_addr

    i_comm = ctypes.c_int()
    i_comm_p = ctypes.cast(ctypes.addressof(i_comm), INTP)

    cmd = ctypes.c_char_p(b"python")
    t_argv = ctypes.c_char_p * 1
    argv = t_argv(ctypes.c_char_p(b"start_child.py"))
    t_err_code = ctypes.c_int * max_proc.value
    err_code = t_err_code()

    MPI.MPI_Comm_spawn(cmd, argv, max_proc, MPI.ompi_mpi_info_null, root,
                       MPI.ompi_mpi_comm_world, i_comm_p, err_code)

    print("Launched {} processes".format(args.n))
    print("Main:", os.getpid())
    print("COMM_WOLRD", MPI.ompi_mpi_comm_world)
    print("COMM_WOLRD", i_comm_p)

    win = ctypes.c_int()
    win_p = ctypes.cast(ctypes.addressof(win), INTP)
    t_sem = ctypes.c_int * 1
    sem = t_sem(ctypes.c_int(0))

    print("Not args")
    res = MPI.MPI_Win_allocate(8, 8, MPI.ompi_mpi_info_null,
                               MPI.ompi_mpi_comm_world, sem, win_p)
    print("Main result", res)
    MPI.MPI_Win_free(win_p)
    print("Final fails?")

    MPI.MPI_Finalize()
