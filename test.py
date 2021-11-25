from outputC import outputC, outCfunction

# Should I implement extern "C" ?

def make_loop(type, index, ref, inter):
    fin = "loop_" + type + index + "(cctkGH, [&](const PointDesc &" + ref + ") {" + inter + "});"

    return fin

# desc = ""
# name = "WaveToyCPU_RHS"
#
# prestring = """DECLARE_CCTK_ARGUMENTS_WaveToyCPU_RHS; \n
#                           DECLARE_CCTK_PARAMETERS; \n
#                           const CCTK_REAL t = cctk_time; \n
#                                                     \n
#                            const array<int, dim> indextype = {1, 1, 1}; \n
#   const GF3D2layout layout(cctkGH, indextype); \n
#   const GF3D2<const CCTK_REAL> gf_phi(layout, phi); \n
#   const GF3D2<const CCTK_REAL> gf_psi(layout, psi); \n
#                         const GF3D2<CCTK_REAL> gf_phirhs(layout, phirhs); \n
#                 const GF3D2<CCTK_REAL> gf_psirhs(layout, psirhs);"""
#
# inter = """CCTK_REAL ddx_phi = \n
#         (gf_phi(p.I - p.DI[0]) - 2 * gf_phi(p.I) + gf_phi(p.I + p.DI[0])) / \n
#         pow(p.dx, 2); \n
#     CCTK_REAL ddy_phi = \n
#         (gf_phi(p.I - p.DI[1]) - 2 * gf_phi(p.I) + gf_phi(p.I + p.DI[1])) / \n
#         pow(p.dy, 2); \n
#     CCTK_REAL ddz_phi = \n
#         (gf_phi(p.I - p.DI[2]) - 2 * gf_phi(p.I) + gf_phi(p.I + p.DI[2])) / \n
#         pow(p.dz, 2); \n
#     gf_psirhs(p.I) = ddx_phi + ddy_phi + ddz_phi - pow(mass, 2) * gf_phi(p.I) + \n
#                      4 * M_PI * central_potential(t, p.x, p.y, p.z); \n
#     gf_phirhs(p.I) = gf_psi(p.I);"""
#
# loop = make_loop("int", "<1 , 1, 1>", "p", inter)
#
# body = prestring + loop
#
# string = outCfunction(
#     outfile="returnstring", desc=desc, name=name,
#     params="CCTK_ARGUMENTS",
#     body=body,
#     enableCparameters=False)
#
# print(string)

def declare(var_name, args, const):
    if const:
        fin = "const GF3D2<const CCTK_REAL> " + var_name + "(" + args + ");"

    else:
        fin = "const GF3D2<CCTK_REAL> " + var_name + "(" + args + ");"

    return fin


code = declare("psi", "layout, phirhs", const=False)

print(code)