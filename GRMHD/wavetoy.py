# Step 1: Import needed core NRPy+ modules
from outputC import lhrh         # NRPy+: Core C code output module
import finite_difference as fin  # NRPy+: Finite difference C code generation module
import NRPy_param_funcs as par   # NRPy+: Parameter interface
import grid as gri               # NRPy+: Functions having to do with numerical grids
import loop as lp                # NRPy+: Generate C code loops
import indexedexp as ixp         # NRPy+: Symbolic indexed expression (e.g., tensors, vectors, etc.) support
import reference_metric as rfm   # NRPy+: Reference metric support
import os, sys                   # Standard Python modules for multiplatform OS-level functions
import time                      # Standard Python module; useful for benchmarking
import ScalarWave.ScalarWaveCurvilinear_RHSs as swrhs


def WaveToy_RHSs__generate_symbolic_expressions():
    ######################################
    # START: GENERATE SYMBOLIC EXPRESSIONS
    print("Generating symbolic expressions for WaveToy RHSs...")
    start = time.time()

    #par.set_parval_from_str("reference_metric::enable_rfm_precompute", "True")
    #par.set_parval_from_str("reference_metric::rfm_precompute_Ccode_outdir", os.path.join(outdir, "rfm_files/"))

    swrhs.ScalarWaveCurvilinear_RHSs()

    end = time.time()
    print("(BENCH) Finished WaveToy RHS symbolic expressions in " + str(end - start) + " seconds.")
    # END: GENERATE SYMBOLIC EXPRESSIONS
    ######################################

    # Step 2: Register uu_rhs and vv_rhs gridfunctions so
    # they can be written to by NRPy.

    uu_rhs, vv_rhs = gri.register_gridfunctions("AUX", ["uu_rhs", "vv_rhs"])

    WaveToy_RHSs_SymbExpressions = [ \
        lhrh(lhs=gri.gfaccess("out_gfs", "uu_rhs"), rhs=swrhs.uu_rhs), \
        lhrh(lhs=gri.gfaccess("out_gfs", "vv_rhs"), rhs=swrhs.vv_rhs)]

    return WaveToy_RHSs_SymbExpressions

def WaveToy_RHSs__generate_Ccode(all_RHSs_exprs_list):
   # print("Generating C code for WaveToy RHSs (FD_order=" + str(FD_order) + ") in " + par.parval_from_str(
   #     "reference_metric::CoordSystem") + " coordinates.")
    start = time.time()

    # Store original finite-differencing order:
    FD_order_orig = par.parval_from_str("finite_difference::FD_CENTDERIVS_ORDER")
    # Set new finite-differencing order:
   # par.set_parval_from_str("finite_difference::FD_CENTDERIVS_ORDER", FD_order)

    WaveToy_RHSs_string = fin.FD_outputC("returnstring", all_RHSs_exprs_list,
                                         params="outCverbose=False,enable_SIMD=True")

    #filename = "WaveToy_RHSs" + "_FD_order_" + str(FD_order) + ".h"

    result = lp.loop(["i2", "i1", "i0"], ["cctk_nghostzones[2]", "cctk_nghostzones[1]", "cctk_nghostzones[0]"],
                    ["cctk_lsh[2]-cctk_nghostzones[2]", "cctk_lsh[1]-cctk_nghostzones[1]",
                     "cctk_lsh[0]-cctk_nghostzones[0]"],
                    ["1", "1", "SIMD_width"],
                    ["#pragma omp parallel for",
                     "#include \"rfm_files/rfm_struct__SIMD_outer_read2.h\"",
                     r"""    #include "rfm_files/rfm_struct__SIMD_outer_read1.h"
#if (defined __INTEL_COMPILER && __INTEL_COMPILER_BUILD_DATE >= 20180804)
   #pragma ivdep         // Forces Intel compiler (if Intel compiler used) to ignore certain SIMD vector dependencies
   #pragma vector always // Forces Intel compiler (if Intel compiler used) to vectorize
#endif"""], "",
                    "#include \"rfm_files/rfm_struct__SIMD_inner_read0.h\"\n" + WaveToy_RHSs_string)

    # Restore original finite-differencing order:
    par.set_parval_from_str("finite_difference::FD_CENTDERIVS_ORDER", FD_order_orig)

    end = time.time()
    return result

    #print("(BENCH) Finished WaveToy_RHS C codegen (FD_order=" + str(FD_order) + ") in " + str(
    #    end - start) + " seconds.")

#print(WaveToy_RHSs__generate_symbolic_expressions())

print(WaveToy_RHSs__generate_Ccode(WaveToy_RHSs__generate_symbolic_expressions()))
