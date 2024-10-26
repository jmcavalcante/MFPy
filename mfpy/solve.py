from .equations import pacejka
from collections import namedtuple
import numpy as np

def solve(alpha_kappa_gamma_FZ_VX,tir_data,check_limits=False,star_correction=False):

    #Checking the size of the inputs:
    sizes = [len(i) for i in alpha_kappa_gamma_FZ_VX]
    if all(size == sizes[0] for size in sizes) == False:
        raise TypeError('Inputs with differents sizes.')
    
    #Initial values (input user)
    alpha_input,kappa_input,gamma_input,FZ_input,VX = alpha_kappa_gamma_FZ_VX 

    #Checking for negative or null speed and FZ
    if any(fz <= 0 for fz in FZ_input) == True or any(v <= tir_data.MODEL.VXLOW for v in VX) == True:
        raise ValueError('No compability with negative or null  FZ and VX lower than VXLOW')
     
    #Checking limits from the .tir data info
    if check_limits == True:
        #alpha:
        if np.all((alpha_input >= tir_data.SLIP_ANGLE_RANGE.ALPMIN) & (alpha_input <= tir_data.SLIP_ANGLE_RANGE.ALPMAX)) == False:
            alpha = np.clip(alpha_input, tir_data.SLIP_ANGLE_RANGE.ALPMIN, tir_data.SLIP_ANGLE_RANGE.ALPMAX)
            print('Slip angle input is outside the range value. The result will be saturated')
        else:
            alpha = alpha_input
        #FZ
        if np.all((FZ_input >= tir_data.VERTICAL_FORCE_RANGE.FZMIN) & (alpha_input <= tir_data.VERTICAL_FORCE_RANGE.FZMAX)) == False:
            FZ = np.clip(FZ_input, tir_data.VERTICAL_FORCE_RANGE.FZMIN, tir_data.VERTICAL_FORCE_RANGE.FZMAX)
            print('FZ input is outside the range value. The result will be saturated')
        else:
            FZ = FZ_input
        #kappa:
        if np.all((kappa_input >= tir_data.LONG_SLIP_RANGE.KPUMIN) & (kappa_input <= tir_data.LONG_SLIP_RANGE.KPUMAX)) == False:
            kappa = np.clip(kappa_input, tir_data.LONG_SLIP_RANGE.KPUMIN, tir_data.LONG_SLIP_RANGE.KPUMAX)
            print('Slip ratio input is outside the range value. The result will be saturated')
        else:
            kappa = kappa_input
        #gamma
        if np.all((gamma_input >= tir_data.INCLINATION_ANGLE_RANGE.CAMMIN) & (gamma_input <= tir_data.INCLINATION_ANGLE_RANGE.CAMMAX)) == False:
            gamma = np.clip(gamma_input, tir_data.INCLINATION_ANGLE_RANGE.CAMMIN, tir_data.INCLINATION_ANGLE_RANGE.CAMMAX)
            print('Inclination angle input is outside the range value. The result will be saturated')
        else:
            gamma = gamma_input
    else:
        alpha,kappa,gamma,FZ,VX = alpha_input,kappa_input,gamma_input,FZ_input,VX

    
    #Output namedTuple
    output = namedtuple('MFOutput',["alpha","kappa",'gamma','VX',"FX","FY",'muX','muY','FZ','MX','MY','MZ','t','s','FX0','FY0','MZ0','MZr0','t0','Re','rho','omega'])
    
    #nominal,Radius_coef,FX_pure_coef,FY_pure_coef,MZ_pure_coef,FX_combined_coef,FY_combined_coef,MZ_combined_coef,My_coef,Mx_coef = preprocessing.creating_coefs(tir_data_checked) #The necessary coefs for pacejka function
    
    #FX pure slip calculation
    FX_pure_output = pacejka.FX_pure((alpha,kappa,gamma,FZ,VX),*[tir_data.LONGITUDINAL_COEFFICIENTS.PCX1,
                                                                 tir_data.LONGITUDINAL_COEFFICIENTS.PDX1,
                                                                 tir_data.LONGITUDINAL_COEFFICIENTS.PDX2,
                                                                 tir_data.LONGITUDINAL_COEFFICIENTS.PDX3,
                                                                 tir_data.LONGITUDINAL_COEFFICIENTS.PEX1,
                                                                 tir_data.LONGITUDINAL_COEFFICIENTS.PEX2,
                                                                 tir_data.LONGITUDINAL_COEFFICIENTS.PEX3,
                                                                 tir_data.LONGITUDINAL_COEFFICIENTS.PEX4,
                                                                 tir_data.LONGITUDINAL_COEFFICIENTS.PKX1,
                                                                 tir_data.LONGITUDINAL_COEFFICIENTS.PKX2,
                                                                 tir_data.LONGITUDINAL_COEFFICIENTS.PKX3,
                                                                 tir_data.LONGITUDINAL_COEFFICIENTS.PHX1,
                                                                 tir_data.LONGITUDINAL_COEFFICIENTS.PHX2,
                                                                 tir_data.LONGITUDINAL_COEFFICIENTS.PVX1,
                                                                 tir_data.LONGITUDINAL_COEFFICIENTS.PVX2],
                                                                 tir_data.VERTICAL.FNOMIN,scaling_coefficients=tir_data.SCALING_COEFFICIENTS)
    
    #FX pure cornering calculation
    FY_pure_output = pacejka.FY_pure((alpha,kappa,gamma,FZ,VX),*[tir_data.LATERAL_COEFFICIENTS.PCY1,
                                                                 tir_data.LATERAL_COEFFICIENTS.PDY1,
                                                                 tir_data.LATERAL_COEFFICIENTS.PDY2,
                                                                 tir_data.LATERAL_COEFFICIENTS.PDY3,
                                                                 tir_data.LATERAL_COEFFICIENTS.PEY1,
                                                                 tir_data.LATERAL_COEFFICIENTS.PEY2,
                                                                 tir_data.LATERAL_COEFFICIENTS.PEY3,
                                                                 tir_data.LATERAL_COEFFICIENTS.PEY4,
                                                                 tir_data.LATERAL_COEFFICIENTS.PKY1,
                                                                 tir_data.LATERAL_COEFFICIENTS.PKY2,
                                                                 tir_data.LATERAL_COEFFICIENTS.PKY3,
                                                                 tir_data.LATERAL_COEFFICIENTS.PHY1,
                                                                 tir_data.LATERAL_COEFFICIENTS.PHY2,
                                                                 tir_data.LATERAL_COEFFICIENTS.PHY3,
                                                                 tir_data.LATERAL_COEFFICIENTS.PVY1,
                                                                 tir_data.LATERAL_COEFFICIENTS.PVY2,
                                                                 tir_data.LATERAL_COEFFICIENTS.PVY3,
                                                                 tir_data.LATERAL_COEFFICIENTS.PVY4,],tir_data.VERTICAL.FNOMIN,scaling_coefficients=tir_data.SCALING_COEFFICIENTS,star_correction=star_correction)

    #FX pure cornering calculation with zero camber
    FY_pure_gamma0_output = pacejka.FY_pure((alpha,kappa,np.zeros(len(alpha)),FZ,VX),*[tir_data.LATERAL_COEFFICIENTS.PCY1,
                                                                 tir_data.LATERAL_COEFFICIENTS.PDY1,
                                                                 tir_data.LATERAL_COEFFICIENTS.PDY2,
                                                                 tir_data.LATERAL_COEFFICIENTS.PDY3,
                                                                 tir_data.LATERAL_COEFFICIENTS.PEY1,
                                                                 tir_data.LATERAL_COEFFICIENTS.PEY2,
                                                                 tir_data.LATERAL_COEFFICIENTS.PEY3,
                                                                 tir_data.LATERAL_COEFFICIENTS.PEY4,
                                                                 tir_data.LATERAL_COEFFICIENTS.PKY1,
                                                                 tir_data.LATERAL_COEFFICIENTS.PKY2,
                                                                 tir_data.LATERAL_COEFFICIENTS.PKY3,
                                                                 tir_data.LATERAL_COEFFICIENTS.PHY1,
                                                                 tir_data.LATERAL_COEFFICIENTS.PHY2,
                                                                 tir_data.LATERAL_COEFFICIENTS.PHY3,
                                                                 tir_data.LATERAL_COEFFICIENTS.PVY1,
                                                                 tir_data.LATERAL_COEFFICIENTS.PVY2,
                                                                 tir_data.LATERAL_COEFFICIENTS.PVY3,
                                                                 tir_data.LATERAL_COEFFICIENTS.PVY4,],tir_data.VERTICAL.FNOMIN,scaling_coefficients=tir_data.SCALING_COEFFICIENTS,star_correction=star_correction)
    #MZ0 pure cornering
    MZ_pure_output = pacejka.MZ_pure(((alpha,kappa,gamma,FZ,VX)),*[tir_data.ALIGNING_COEFFICIENTS.QBZ1,
                                                                 tir_data.ALIGNING_COEFFICIENTS.QBZ2,
                                                                 tir_data.ALIGNING_COEFFICIENTS.QBZ3,
                                                                 tir_data.ALIGNING_COEFFICIENTS.QBZ4,
                                                                 tir_data.ALIGNING_COEFFICIENTS.QBZ5,
                                                                 tir_data.ALIGNING_COEFFICIENTS.QBZ9,
                                                                 tir_data.ALIGNING_COEFFICIENTS.QBZ10,
                                                                 tir_data.ALIGNING_COEFFICIENTS.QCZ1,
                                                                 tir_data.ALIGNING_COEFFICIENTS.QDZ1,
                                                                 tir_data.ALIGNING_COEFFICIENTS.QDZ2,
                                                                 tir_data.ALIGNING_COEFFICIENTS.QDZ3,
                                                                 tir_data.ALIGNING_COEFFICIENTS.QDZ4,
                                                                 tir_data.ALIGNING_COEFFICIENTS.QDZ6,
                                                                 tir_data.ALIGNING_COEFFICIENTS.QDZ7,
                                                                 tir_data.ALIGNING_COEFFICIENTS.QDZ8,
                                                                 tir_data.ALIGNING_COEFFICIENTS.QDZ9,
                                                                 tir_data.ALIGNING_COEFFICIENTS.QEZ1,
                                                                 tir_data.ALIGNING_COEFFICIENTS.QEZ2,
                                                                 tir_data.ALIGNING_COEFFICIENTS.QEZ3,
                                                                 tir_data.ALIGNING_COEFFICIENTS.QEZ4,
                                                                 tir_data.ALIGNING_COEFFICIENTS.QEZ5,
                                                                 tir_data.ALIGNING_COEFFICIENTS.QHZ1,
                                                                 tir_data.ALIGNING_COEFFICIENTS.QHZ2,
                                                                 tir_data.ALIGNING_COEFFICIENTS.QHZ3,
                                                                 tir_data.ALIGNING_COEFFICIENTS.QHZ4],
                                                                 tir_data.VERTICAL.FNOMIN,tir_data.DIMENSION.UNLOADED_RADIUS,FY_pure_gamma0_output,scaling_coefficients=tir_data.SCALING_COEFFICIENTS,star_correction=star_correction) 
    #FX combined
    FX_combined_output = pacejka.FX_combined((alpha,kappa,gamma,FZ,VX),*[tir_data.LONGITUDINAL_COEFFICIENTS.RBX1,
                                                                 tir_data.LONGITUDINAL_COEFFICIENTS.RBX2,
                                                                 tir_data.LONGITUDINAL_COEFFICIENTS.RCX1,
                                                                 tir_data.LONGITUDINAL_COEFFICIENTS.REX1,
                                                                 tir_data.LONGITUDINAL_COEFFICIENTS.REX2,
                                                                 tir_data.LONGITUDINAL_COEFFICIENTS.RHX1]
                                                                 ,tir_data.VERTICAL.FNOMIN,FX_pure_output,scaling_coefficients=tir_data.SCALING_COEFFICIENTS,star_correction=star_correction) 
    #FY combined
    FY_combined_output = pacejka.FY_combined((alpha,kappa,gamma,FZ,VX),*[tir_data.LATERAL_COEFFICIENTS.RBY1,
                                                                tir_data.LATERAL_COEFFICIENTS.RBY2,
                                                                tir_data.LATERAL_COEFFICIENTS.RBY3,
                                                                tir_data.LATERAL_COEFFICIENTS.RCY1,
                                                                tir_data.LATERAL_COEFFICIENTS.REY1,
                                                                tir_data.LATERAL_COEFFICIENTS.REY2,
                                                                tir_data.LATERAL_COEFFICIENTS.RHY1,
                                                                tir_data.LATERAL_COEFFICIENTS.RHY2,
                                                                tir_data.LATERAL_COEFFICIENTS.RVY1,
                                                                tir_data.LATERAL_COEFFICIENTS.RVY2,
                                                                tir_data.LATERAL_COEFFICIENTS.RVY3,
                                                                tir_data.LATERAL_COEFFICIENTS.RVY4,
                                                                tir_data.LATERAL_COEFFICIENTS.RVY5,
                                                                tir_data.LATERAL_COEFFICIENTS.RVY6],
                                                                tir_data.VERTICAL.FNOMIN,FY_pure_output,scaling_coefficients=tir_data.SCALING_COEFFICIENTS,star_correction=star_correction) 
    #FY combined with zero camber
    FY_gamma0_combined_output = pacejka.FY_combined((alpha,kappa,np.zeros(len(alpha)),FZ,VX),*[tir_data.LATERAL_COEFFICIENTS.RBY1,
                                                                tir_data.LATERAL_COEFFICIENTS.RBY2,
                                                                tir_data.LATERAL_COEFFICIENTS.RBY3,
                                                                tir_data.LATERAL_COEFFICIENTS.RCY1,
                                                                tir_data.LATERAL_COEFFICIENTS.REY1,
                                                                tir_data.LATERAL_COEFFICIENTS.REY2,
                                                                tir_data.LATERAL_COEFFICIENTS.RHY1,
                                                                tir_data.LATERAL_COEFFICIENTS.RHY2,
                                                                tir_data.LATERAL_COEFFICIENTS.RVY1,
                                                                tir_data.LATERAL_COEFFICIENTS.RVY2,
                                                                tir_data.LATERAL_COEFFICIENTS.RVY3,
                                                                tir_data.LATERAL_COEFFICIENTS.RVY4,
                                                                tir_data.LATERAL_COEFFICIENTS.RVY5,
                                                                tir_data.LATERAL_COEFFICIENTS.RVY6],
                                                                tir_data.VERTICAL.FNOMIN,FY_pure_output,scaling_coefficients=tir_data.SCALING_COEFFICIENTS,star_correction=star_correction) 
    #MZ combined
    MZ_combined_output = pacejka.MZ_combined((alpha,kappa,gamma,FZ,VX),*[tir_data.ALIGNING_COEFFICIENTS.SSZ1,
                                                                 tir_data.ALIGNING_COEFFICIENTS.SSZ2,
                                                                 tir_data.ALIGNING_COEFFICIENTS.SSZ3,
                                                                 tir_data.ALIGNING_COEFFICIENTS.SSZ4],
                                             tir_data.VERTICAL.FNOMIN,tir_data.DIMENSION.UNLOADED_RADIUS,FX_combined_output,FY_gamma0_combined_output,MZ_pure_output,
                                                FX_pure_output,FY_pure_gamma0_output,scaling_coefficients=tir_data.SCALING_COEFFICIENTS,star_correction=star_correction) 
    #MX torque (overturning)
    MX_output = pacejka.MX_overturning((gamma,FZ,VX),*[tir_data.OVERTURNING_COEFFICIENTS.QSX1,
                                                       tir_data.OVERTURNING_COEFFICIENTS.QSX2,
                                                       tir_data.OVERTURNING_COEFFICIENTS.QSX3],
                                       tir_data.VERTICAL.FNOMIN,tir_data.DIMENSION.UNLOADED_RADIUS,FY_combined_output,scaling_coefficients=tir_data.SCALING_COEFFICIENTS) 
    #MY torque (rolling resistance)
    MY_output = pacejka.MY_RR((FZ,VX),*[tir_data.ROLLING_COEFFICIENTS.QSY1,
                                                       tir_data.ROLLING_COEFFICIENTS.QSY2,
                                                       tir_data.ROLLING_COEFFICIENTS.QSY3,
                                                       tir_data.ROLLING_COEFFICIENTS.QSY4]
                              ,tir_data.VERTICAL.FNOMIN,tir_data.DIMENSION.UNLOADED_RADIUS,tir_data.MODEL.LONGVL,FX_combined_output,scaling_coefficients=tir_data.SCALING_COEFFICIENTS) 
    #Radius
    Radius_output = pacejka.Radius((FZ,VX),*[tir_data.VERTICAL.VERTICAL_STIFFNESS,
                                             tir_data.VERTICAL.BREFF,
                                             tir_data.VERTICAL.DREFF,
                                             tir_data.VERTICAL.FREFF],
                                             tir_data.VERTICAL.FNOMIN,tir_data.DIMENSION.UNLOADED_RADIUS)


    result = output(muX=FX_pure_output[1],FX0=FX_pure_output[0],
                    muY=FY_pure_output[1],FY0=FY_pure_output[0],
                    MZ0=MZ_pure_output[0],MZr0=MZ_pure_output[1],t0=MZ_pure_output[2],
                    FX=FX_combined_output[0],FY=FY_combined_output[0],
                    MZ=MZ_combined_output[0],s=MZ_combined_output[2],t=MZ_combined_output[1],
                    MY=MY_output[0],MX=MX_output[0],
                    alpha=alpha_input,gamma=gamma_input,FZ=FZ_input,
                    kappa=kappa_input,VX=VX,
                    Re=Radius_output[0],rho=Radius_output[1],omega=Radius_output[2])

    return result


        
        


    
  
