from .equations import Pacejka
import glob
import os
import pandas as pd
import statistics
import numpy as np
import scipy

class Fit:

    @staticmethod
    def Fx_pure(folder,initial_guess=None,Fz_nom = None,full_output = 0):
        #Reading folder with .csv for Fx
        """
        The folder must contains .csv files with columns LSR and Fx. Each file shoud have the follow name structure:
        FZXXXX.csv
        Where XXXX is the value for the vertical force used in this test
        The user can follow the examples in the sample/fit  
        """
        Fz_list = []
        Fx_list = []
        kappa_list = []

        for csv_file in glob.glob(os.path.join(folder, '*.csv')):
            name_file = os.path.basename(csv_file)
            data = pd.read_csv(csv_file,sep=';').sort_values(by='LSR')
            Fz_list.append(float(name_file[2:-4]))
            Fx_list.append(data['FX'])
            kappa_list.append(data['LSR'])
            
        #Function used in the LS method
        if Fz_nom == None:
            Fz_nom = statistics.median(Fz_list)

        def residuals_Fx(params,x,y):
            return y - Pacejka.Fx_pure(x,*params,Fz_nom)[0].ravel()  
        
        #Checking sizes for all csv (they should have the same lenght)
        size = min(len(lis) for lis in Fx_list)
        Fx_list = [i[:size] for i in Fx_list]
        Fx_data = np.array(Fx_list).ravel()
        kappa_list = [i[:size].to_numpy() for i in kappa_list]
        Fz_data = np.array([np.ones(size)*i for i in Fz_list])
        kappa_data = np.array(kappa_list)

        if initial_guess==None:
            initial_guess = [1,1,0,0.1,0.5,0,0,5,1,0,0,0,0,0] #Default initial guess

        lower_bounds = [0, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf]
        upper_bounds = [ np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf]

    #For the interface (app)
        if full_output=='data_only':
            Fx_initial = Pacejka.Fx_pure((kappa_data,Fz_data),*initial_guess,Fz_nom)[0].ravel()
            Fz_data_output = [i[0] for i in Fz_data]
            Fx_data_output = [Fx_data[i:i+size] for i in range(0,len(Fx_data),size)]
            Fx_initial_output = [Fx_initial[i:i+size] for i in range(0,len(Fx_initial),size)]
            return Fz_data_output,Fx_data_output,kappa_data,Fx_initial_output
        
        result= scipy.optimize.least_squares(residuals_Fx, initial_guess, args=((kappa_data,Fz_data),Fx_data), max_nfev=100000,bounds=(lower_bounds,upper_bounds))

        p_fit = result.x

        if full_output == 2:
            Fx_initial = Pacejka.Fx_pure((kappa_data,Fz_data),*initial_guess,Fz_nom)[0].ravel()
            Fx_fit = Pacejka.Fx_pure((kappa_data,Fz_data),*p_fit,Fz_nom)[0].ravel()
            Fz_data_output = [i[0] for i in Fz_data]
            Fx_data_output = [Fx_data[i:i+size] for i in range(0,len(Fx_data),size)]
            Fx_fit_output = [Fx_fit[i:i+size] for i in range(0,len(Fx_fit),size)]
            Fx_initial_output = [Fx_initial[i:i+size] for i in range(0,len(Fx_initial),size)]
            return p_fit,initial_guess,Fz_nom,Fz_data_output,Fx_data_output,kappa_data,Fx_initial_output,Fx_fit_output
        
        elif full_output == 1:
            return p_fit,initial_guess,Fz_nom
        else:
            return p_fit,Fz_nom
    @staticmethod    
    def Fy_pure(folder,initial_guess=None,Fz_nom = None,full_output = 0):
        #Reading folder with .csv for Fy
        """
        The folder must contains .csv files with columns SA and Fy. Each file shoud have the follow name structure:
        FZXXXX_gammaYYYY.csv
        Where XXXX is the value for the vertical force used in this test
        YYYY is the value in rad for the inclination angle
        The user can follow the examples in the sample/fit  
        """
        Fz_list = []
        Fy_list = []
        alpha_list = []
        gamma_list = []

        for csv_file in glob.glob(os.path.join(folder, '*.csv')):
            name_file = os.path.basename(csv_file)
            data = pd.read_csv(csv_file,sep=';').sort_values(by='SA')
            index = name_file.find('_gamma')
            Fz_list.append(float(name_file[2:index]))
            gamma_list.append(float(name_file[index + len('_gamma'):-4]))
            alpha_list.append(data['SA'])
            Fy_list.append(data['FY'])

        #Function used in the LS method
        if Fz_nom == None:
            Fz_nom = statistics.median(Fz_list)

        def residuals_Fy(params,x,y):
            return y - Pacejka.Fy_pure(x,*params,Fz_nom)[0].ravel()  
        
        #Checking sizes for all csv (they should have the same lenght)
        size = min(len(lis) for lis in Fy_list)
        Fy_list = [i[:size] for i in Fy_list]
        Fy_data = np.array(Fy_list).ravel()
        alpha_list = [i[:size].to_numpy() for i in alpha_list]
        Fz_data = np.array([np.ones(size)*i for i in Fz_list])
        gamma_data = np.array([np.ones(size)*i for i in gamma_list])
        alpha_data = np.array(alpha_list)

        if initial_guess==None:
            initial_guess =  [1,1,0,0,0,0,0,1,0,1,1,0,1,0,0,0,0,0,0,0,0,0] #Default initial guess

        lower_bounds = [0, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf,
                 -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf]
        upper_bounds = [ np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf,
                 np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf]

        #For the interface (app)
        if full_output=='data_only':
            Fy_initial = Pacejka.Fy_pure((alpha_data,gamma_data,Fz_data),*initial_guess,Fz_nom)[0].ravel()
            Fz_data_output = [i[0] for i in Fz_data]
            Fy_data_output = [Fy_data[i:i+size] for i in range(0,len(Fy_data),size)]
            Fy_initial_output = [Fy_initial[i:i+size] for i in range(0,len(Fy_initial),size)]
            return Fz_data_output,Fy_data_output,alpha_data,gamma_data,Fy_initial_output
        result= scipy.optimize.least_squares(residuals_Fy, initial_guess, args=((alpha_data,gamma_data,Fz_data),Fy_data), max_nfev=100000,bounds=(lower_bounds,upper_bounds))
        p_fit = result.x

        if full_output == 2:
            Fy_initial = Pacejka.Fy_pure((alpha_data,gamma_data,Fz_data),*initial_guess,Fz_nom)[0].ravel()
            Fz_data_output = [i[0] for i in Fz_data]
            Fy_data_output = [Fy_data[i:i+size] for i in range(0,len(Fy_data),size)]
            Fy_initial_output = [Fy_initial[i:i+size] for i in range(0,len(Fy_initial),size)]
            Fy_fit = Pacejka.Fy_pure((alpha_data,gamma_data,Fz_data),*p_fit,Fz_nom)[0].ravel()
            Fy_fit_output = [Fy_fit[i:i+size] for i in range(0,len(Fy_fit),size)]
            return p_fit,initial_guess,Fz_nom,Fz_data_output,Fy_data_output,alpha_data,gamma_data,Fy_initial_output,Fy_fit_output
        
        elif full_output == 1:
            return p_fit,initial_guess,Fz_nom
        else:
            return p_fit,Fz_nom
        
    @staticmethod    
    def Mz_pure(folder,R0,p_Fy_pure,initial_guess=None,Fz_nom = None,full_output = 0):
        #Reading folder with .csv for Fy
        """
        The folder must contains .csv files with columns SA and Mz. Each file shoud have the follow name structure:
        FzXXXX_gammaYYYY.csv
        Where XXXX is the value for the vertical force used in this test
        YYYY is the value in rad for the inclination angle
        The user can follow the examples in the sample/fit  
        """
        Fz_list = []
        Mz_list = []
        alpha_list = []
        gamma_list = []

        for csv_file in glob.glob(os.path.join(folder, '*.csv')):
            name_file = os.path.basename(csv_file)
            data = pd.read_csv(csv_file,sep=';').sort_values(by='SA')
            index = name_file.find('_gamma')
            Fz_list.append(float(name_file[2:index]))
            gamma_list.append(float(name_file[index + len('_gamma'):-4]))
            alpha_list.append(data['SA'])
            Mz_list.append(data['MZ'])

        #Function used in the LS method
        if Fz_nom == None:
            Fz_nom = statistics.median(Fz_list)

        def residuals_Mz(params,x,y):
            Fy0_output = Pacejka.Fy_pure(x,*p_Fy_pure,Fz_nom)
            return y - Pacejka.Mz_pure(x,*params,Fz_nom,R0,Fy0_output)[0].ravel()

        
        #Checking sizes for all csv (they should have the same lenght)
        size = min(len(lis) for lis in Mz_list)
        Mz_list = [i[:size] for i in Mz_list]
        Mz_data = np.array(Mz_list).ravel()
        alpha_list = [i[:size].to_numpy() for i in alpha_list]
        Fz_data = np.array([np.ones(size)*i for i in Fz_list])
        gamma_data = np.array([np.ones(size)*i for i in gamma_list])
        alpha_data = np.array(alpha_list)

        if initial_guess == None:
            initial_guess = [20,-1,0,0,0,0,0,1,0.0,-0.00,1,0,0.00,-0.00,-0.1,0.00,0,0,-1,1,0,0,0,0,0,0,0] #Default initial guess

        lower_bounds = [0, -np.inf, -np.inf, -np.inf, -np.inf, -0.1, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf,
                 -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf]
        upper_bounds = [ np.inf, np.inf, np.inf, np.inf, np.inf, 0.1, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf,
                 np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf]

        result= scipy.optimize.least_squares(residuals_Mz, initial_guess, args=((alpha_data,gamma_data,Fz_data),Mz_data), max_nfev=100000,bounds=(lower_bounds,upper_bounds))
        p_fit = result.x

        if full_output == 2:
            Mz_initial = Pacejka.Fx_pure((alpha_data,gamma_data,Fz_data),*initial_guess,Fz_nom)[0].ravel()
            Mz_fit = Pacejka.Fx_pure((alpha_data,gamma_data,Fz_data),*p_fit,Fz_nom)[0].ravel()

            return p_fit,initial_guess,Fz_nom,Fz_data,Mz_data,alpha_data,gamma_data,Mz_initial,Mz_fit
        
        elif full_output == 1:
            return p_fit,initial_guess,Fz_nom
        else:
            return p_fit,Fz_nom