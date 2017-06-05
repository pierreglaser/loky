
from ctypes.util import find_library
import ctypes

libmpi = find_library("mpi")
mode = ctypes.RTLD_GLOBAL
if hasattr(ctypes, "RTLD_NOW"):
    mode |= ctypes.RTLD_NOW
if hasattr(ctypes, "RTLD_NOLOAD"):
    mode |= ctypes.RTLD_NOLOAD
MPI = ctypes.CDLL(libmpi, mode=mode)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser('Programme to launch experiemnt')
    parser.add_argument('-n', type=int, default=4,
                        help='Number of MPI process spawned')

    args = parser.parse_args()

    MPI.MPI_Init()

    INTP = ctypes.POINTER(ctypes.c_int)
    num = ctypes.c_int(-1)
    ptr = ctypes.cast(ctypes.addressof(num), INTP)

    max_proc = ctypes.c_int(args.n)
    root = ctypes.c_int(0)
    intercomm = MPI.ompi_mpi_comm_null_addr

    icomm = ctypes.c_int()
    icomm_p = ctypes.cast(ctypes.addressof(icomm), INTP)

    cmd = ctypes.c_char_p(b"python")
    t_argv = ctypes.c_char_p * 1
    argv = t_argv(ctypes.c_char_p(b"start_child.py"))
    t_err_code = ctypes.c_int * max_proc.value
    err_code = t_err_code()

    MPI.MPI_Comm_spawn(cmd, argv, max_proc, MPI.ompi_mpi_info_null, root,
                       MPI.ompi_mpi_comm_world, icomm_p, err_code)

    print("Lanched {} processes".format(args.n))

    MPI.MPI_Finalize()
