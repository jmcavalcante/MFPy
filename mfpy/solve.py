from .equations import Pacejka
from .preprocess import PreProcessing
from collections import namedtuple

def solve(input_values,header,check_limits=False,no_warnings=False):

    PreProcessing.check_speed_Fz(input_values) #Check for negative or null speed and FZ

    header_checked = PreProcessing.check_coeff(header,no_warnings) #Check the necessary parameters in the tir file

    PreProcessing.check_input_size(input_values) #Check input len

    output = namedtuple('MFOutput',["alpha","kappa",'gamma','VX',"FX","FY",'muX','muY','FZ','MX','MY','MZ','t','s','FX0','FY0','MZ0','MZr0','t0','Re','rho','omega'])
    
    if check_limits == True:
        input_final = PreProcessing.check_limits(header_checked,input_values,no_warnings) #Limitating the input using the tir file parameter
    else:
        input_final = input_values
    alpha_input,kappa_input,gamma_input,Fz_input,Vx_input = input_values #Initial values (input user)
    alpha,kappa,gamma,Fz,Vx = input_final #Creating solve variables for calculating corrected by lim check

    nominal,Radius_coef,Fx_pure_coef,Fy_pure_coef,Mz_pure_coef,Fx_combined_coef,Fy_combined_coef,Mz_combined_coef,My_coef,Mx_coef = PreProcessing.creating_coefs(header_checked) #The necessary coefs for pacejka function

    Fx_pure_output = Pacejka.Fx_pure((alpha,kappa,gamma,Fz,Vx),*Fx_pure_coef,nominal['FZ0']) #Fx0 pure slip

    Fy_pure_output = Pacejka.Fy_pure((alpha,kappa,gamma,Fz,Vx),*Fy_pure_coef,nominal['FZ0']) #Fy0 pure cornering

    Mz_pure_output = Pacejka.Mz_pure(((alpha,kappa,gamma,Fz,Vx)),*Mz_pure_coef,nominal['FZ0'],nominal['R0'],Fy_pure_output) #Mz0 pure cornering

    Fx_combined_output = Pacejka.Fx_combined((alpha,kappa,gamma,Fz,Vx),*Fx_combined_coef,nominal['FZ0'],Fx_pure_output) #Fx combined

    Fy_combined_output = Pacejka.Fy_combined((alpha,kappa,gamma,Fz,Vx),*Fy_combined_coef,nominal['FZ0'],Fy_pure_output) #Fy combined

    Mz_combined_output = Pacejka.Mz_combined((alpha,kappa,gamma,Fz,Vx),*Mz_combined_coef,nominal['FZ0'],nominal['R0'],Fx_combined_output,Fy_combined_output,Mz_pure_output,
                                                Fx_pure_output,Fy_pure_output,) #Mz combined

    My_output = Pacejka.My_RR((Fz,Vx),nominal['FZ0'],nominal['R0'],nominal['V0'],Fx_combined_output,*My_coef) #Rolling resistance torque

    Mx_output = Pacejka.Mx_overturning((gamma,Fz,Vx),nominal['FZ0'],nominal['R0'],Fy_combined_output,*Mx_coef) #Overturning torque

    Radius_output = Pacejka.Radius((Fz,Vx),*Radius_coef,nominal['FZ0'],nominal['R0'])

    result = output(muX=Fx_pure_output[1],FX0=Fx_pure_output[0],
                    muY=Fy_pure_output[1],FY0=Fy_pure_output[0],
                    MZ0=Mz_pure_output[0],MZr0=Mz_pure_output[1],t0=Mz_pure_output[2],
                    FX=Fx_combined_output[0],FY=Fy_combined_output[0],
                    MZ=Mz_combined_output[0],s=Mz_combined_output[2],t=Mz_combined_output[1],
                    MY=My_output[0],MX=Mx_output[0],
                    alpha=alpha_input,gamma=gamma_input,FZ=Fz_input,
                    kappa=kappa_input,VX=Vx_input,
                    Re=Radius_output[0],rho=Radius_output[1],omega=Radius_output[2])

    return result


        
        


    
  
