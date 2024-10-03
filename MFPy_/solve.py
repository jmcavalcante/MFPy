from .equations import Pacejka
from .preprocess import PreProcessing

def solve(input_values,header,check_limits=False):

    header_checked = PreProcessing.check_coeff(header) #Check the necessary parameters in the tir file

    PreProcessing.check_input_size(input_values) #Check input len

    result = PreProcessing.output_structure()
    result['alpha'],result['kappa'],result['gamma'],result['Fz'],result['Vx'] = input_values[0],input_values[1],input_values[2],input_values[3],input_values[4]

    if check_limits == True:
        input_final = PreProcessing.check_limits(header_checked,input_values) #Limitating the input using the tir file parameter
    else:
        input_final = input_values

    alpha,kappa,gamma,Fz,Vx = input_final #Creating input variables

    nominal,Fx_pure_coef,Fy_pure_coef,Mz_pure_coef,Fx_combined_coef,Fy_combined_coef,Mz_combined_coef,My_coef,Mx_coef = PreProcessing.creating_coefs(header_checked) #The necessary coefs for pacejka function

    Fx_pure_output = Pacejka.Fx_pure((kappa,Fz),*Fx_pure_coef,nominal['FZ0']) #Fx0 pure slip
    result['muX'] = Fx_pure_output[1]
    result['FX0'] = Fx_pure_output[0]

    Fy_pure_output = Pacejka.Fy_pure((alpha,gamma,Fz),*Fy_pure_coef,nominal['FZ0']) #Fy0 pure cornering
    result['muY'] = Fy_pure_output[1]
    result['FY0'] = Fy_pure_output[0]

    Mz_pure_output = Pacejka.Mz_pure(((alpha,gamma,Fz)),*Mz_pure_coef,nominal['FZ0'],nominal['R0'],Fy_pure_output) #Mz0 pure cornering
    result['MZ0'] = Mz_pure_output[0]
    result['MZr0'] = Mz_pure_output[1]
    result['t0'] = Mz_pure_output[2]

    Fx_combined_output = Pacejka.Fx_combined((alpha,kappa,gamma,Fz),*Fx_combined_coef,nominal['FZ0'],Fx_pure_output) #Fx combined
    result['FX'] = Fx_combined_output[0]

    Fy_combined_output = Pacejka.Fy_combined((alpha,kappa,gamma,Fz),*Fy_combined_coef,nominal['FZ0'],Fy_pure_output) #Fy combined
    result['FY'] = Fy_combined_output[0]

    Mz_combined_output = Pacejka.Mz_combined((alpha,kappa,gamma,Fz),*Mz_combined_coef,nominal['FZ0'],nominal['R0'],Fx_combined_output,Fy_combined_output,Mz_pure_output,
                                                Fx_pure_output,Fy_pure_output,) #Mz combined
    result['MZ'] = Mz_combined_output[0]
    result['t'] = Mz_combined_output[1]
    result['s'] = Mz_combined_output[2]

    My_output = Pacejka.My_RR((Fz,Vx),nominal['FZ0'],nominal['R0'],nominal['V0'],Fx_combined_output,*My_coef) #Rolling resistance torque
    result['MY'] = My_output[0]

    Mx_output = Pacejka.Mx_overturning((gamma,Fz,Vx),nominal['FZ0'],nominal['R0'],Fy_combined_output,*Mx_coef) #Overturning torque
    result['MX'] = Mx_output[0]

    return result


        
        


    
  