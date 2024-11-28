from .equations import pacejka
import glob
import os
import pandas as pd
import statistics
import numpy as np
import scipy

class fit:

    @staticmethod
    def FX_pure(folder,initial_guess,FZ_nom = None,full_output = 0,lower_bounds = None, upper_bounds = None):
        #Reading folder with .csv for FX
        """
        The folder must contains .csv files with columns LSR and FX. Each file shoud have the follow name structure:
        FZXXXX.csv
        Where XXXX is the value for the vertical force used in this test
        The user can follow the examples in the sample/fit  
        """
        FZ_list     =   []
        FX_list     =   []
        kappa_list  =   []
        gamma_list  =    []

        for csv_file in glob.glob(os.path.join(folder, '*.csv')):
            name_file = os.path.basename(csv_file)
            data = pd.read_csv(csv_file,sep=';').sort_values(by='LSR')
            index_FZ = name_file.find('FZ')
            index_gamma = name_file.find('_gamma')
            FZ_list.append(float(name_file[index_FZ+2:index_gamma]))
            gamma_list.append(float(name_file[index_gamma + len('_gamma'):-4]))
            kappa_list.append(data['LSR'])
            FX_list.append(data['FX'])
            
        #Function used in the LS method
        if FZ_nom == None:
            FZ_nom = statistics.median(FZ_list)

        def residuals_FX(params,x,y):
            return y - pacejka.FX_pure(x,*params,FZ_nom)[0].ravel()  
        
        #Checking sizes for all csv (they should have the same lenght)
        size    =    min(len(lis) for lis in FX_list)
        FX_list =    [i[:size] for i in FX_list]
        FX_data =    np.array(FX_list).ravel()
        kappa_list = [i[:size].to_numpy() for i in kappa_list]
        FZ_data = np.array([np.ones(size)*i for i in FZ_list])
        kappa_data = np.array(kappa_list)
        alpha_data= np.zeros(FZ_data.shape)
        gamma_data = np.array([np.ones(size)*i for i in gamma_list])
        VX_data = np.ones(FZ_data.shape)*10


        if lower_bounds == None:
            lower_bounds = [0, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf]
        if upper_bounds == None:
            upper_bounds = [ np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf]

    #For the interface (app)
        if full_output=='data_only':
            FX_initial = pacejka.FX_pure((alpha_data,kappa_data,gamma_data,FZ_data,VX_data),*initial_guess,FZ_nom)[0].ravel()
            FZ_data_output = [i[0] for i in FZ_data]
            FX_data_output = [FX_data[i:i+size] for i in range(0,len(FX_data),size)]
            FX_initial_output = [FX_initial[i:i+size] for i in range(0,len(FX_initial),size)]
            return FZ_data_output,FX_data_output,kappa_data,gamma_data,FX_initial_output
        
        result= scipy.optimize.least_squares(residuals_FX, initial_guess, args=((alpha_data,kappa_data,gamma_data,FZ_data,VX_data),FX_data), max_nfev=10000,bounds=(lower_bounds,upper_bounds))

        p_fit = result.x

        if full_output == 2:
            FX_initial = pacejka.FX_pure((alpha_data,kappa_data,gamma_data,FZ_data,VX_data),*initial_guess,FZ_nom)[0].ravel()
            FX_fit = pacejka.FX_pure((alpha_data,kappa_data,gamma_data,FZ_data,VX_data),*p_fit,FZ_nom)[0].ravel()
            FZ_data_output = [i[0] for i in FZ_data]
            FX_data_output = [FX_data[i:i+size] for i in range(0,len(FX_data),size)]
            FX_fit_output = [FX_fit[i:i+size] for i in range(0,len(FX_fit),size)]
            FX_initial_output = [FX_initial[i:i+size] for i in range(0,len(FX_initial),size)]
            return p_fit,initial_guess,FZ_nom,FZ_data_output,FX_data_output,kappa_data,gamma_data,FX_initial_output,FX_fit_output
        
        elif full_output == 1:
            return p_fit,initial_guess,FZ_nom
        else:
            return p_fit,FZ_nom
    @staticmethod    
    def FY_pure(folder,initial_guess,FZ_nom = None,full_output = 0,lower_bounds = None, upper_bounds = None):
        #Reading folder with .csv for FY
        """
        The folder must contains .csv files with columns SA and FY. Each file shoud have the follow name structure:
        FZXXXX_gammaYYYY.csv
        Where XXXX is the value for the vertical force used in this test
        YYYY is the value in rad for the inclination angle
        The user can follow the examples in the sample/fit  
        """
        FZ_list = []
        FY_list = []
        alpha_list = []
        gamma_list = []

        for csv_file in glob.glob(os.path.join(folder, '*.csv')):
            name_file = os.path.basename(csv_file)
            data = pd.read_csv(csv_file,sep=';').sort_values(by='SA')
            index_FZ = name_file.find('FZ')
            index_gamma = name_file.find('_gamma')
            FZ_list.append(float(name_file[index_FZ+2:index_gamma]))
            gamma_list.append(float(name_file[index_gamma + len('_gamma'):-4]))
            alpha_list.append(data['SA'])
            FY_list.append(data['FY'])

        #Function used in the LS method
        if FZ_nom == None:
            FZ_nom = statistics.median(FZ_list)

        def residuals_FY(params,x,y):
            return y - pacejka.FY_pure(x,*params,FZ_nom)[0].ravel()  
        
        #Checking sizes for all csv (they should have the same lenght)
        size = min(len(lis) for lis in FY_list)
        FY_list = [i[:size] for i in FY_list]
        FY_data = np.array(FY_list).ravel()
        alpha_list = [i[:size].to_numpy() for i in alpha_list]
        FZ_data = np.array([np.ones(size)*i for i in FZ_list])
        gamma_data = np.array([np.ones(size)*i for i in gamma_list])
        alpha_data = np.array(alpha_list)
        VX_data = np.ones(FZ_data.shape)*10
        kappa_data = np.zeros(FZ_data.shape)

        if lower_bounds == None:
            lower_bounds = [0, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf,
                 -np.inf, -np.inf, -np.inf, -np.inf, -np.inf]
        if upper_bounds == None:
            upper_bounds = [ np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf,
                 np.inf, np.inf, np.inf, np.inf]

        #For the interface (app)
        if full_output=='data_only':
            FY_initial = pacejka.FY_pure((alpha_data,kappa_data,gamma_data,FZ_data,VX_data),*initial_guess,FZ_nom)[0].ravel()
            FZ_data_output = [i[0] for i in FZ_data]
            FY_data_output = [FY_data[i:i+size] for i in range(0,len(FY_data),size)]
            FY_initial_output = [FY_initial[i:i+size] for i in range(0,len(FY_initial),size)]
            return FZ_data_output,FY_data_output,alpha_data,gamma_data,FY_initial_output
        
        result= scipy.optimize.least_squares(residuals_FY, initial_guess, args=((alpha_data,kappa_data,gamma_data,FZ_data,VX_data),FY_data), max_nfev=10000,bounds=(lower_bounds,upper_bounds))
        p_fit = result.x

        if full_output == 2:
            FY_initial = pacejka.FY_pure((alpha_data,kappa_data,gamma_data,FZ_data,VX_data),*initial_guess,FZ_nom)[0].ravel()
            FZ_data_output = [i[0] for i in FZ_data]
            FY_data_output = [FY_data[i:i+size] for i in range(0,len(FY_data),size)]
            FY_initial_output = [FY_initial[i:i+size] for i in range(0,len(FY_initial),size)]
            FY_fit = pacejka.FY_pure((alpha_data,kappa_data,gamma_data,FZ_data,VX_data),*p_fit,FZ_nom)[0].ravel()
            FY_fit_output = [FY_fit[i:i+size] for i in range(0,len(FY_fit),size)]
            return p_fit,initial_guess,FZ_nom,FZ_data_output,FY_data_output,alpha_data,gamma_data,FY_initial_output,FY_fit_output
        
        elif full_output == 1:
            return p_fit,initial_guess,FZ_nom
        else:
            return p_fit,FZ_nom
    @staticmethod    
    def MZ_pure(folder,R0,VX,p_FY_pure,initial_guess,FZ_nom = None,full_output = 0,lower_bounds = None, upper_bounds = None):
        #Reading folder with .csv for FY
        """
        The folder must contains .csv files with columns SA and MZ. Each file shoud have the follow name structure:
        FZXXXX_gammaYYYY.csv
        Where XXXX is the value for the vertical force used in this test
        YYYY is the value in rad for the inclination angle
        The user can follow the examples in the sample/fit  
        """
        FZ_list = []
        MZ_list = []
        alpha_list = []
        gamma_list = []

        for csv_file in glob.glob(os.path.join(folder, '*.csv')):
            name_file = os.path.basename(csv_file)
            data = pd.read_csv(csv_file,sep=';').sort_values(by='SA')
            index_FZ = name_file.find('FZ')
            index_gamma = name_file.find('_gamma')
            FZ_list.append(float(name_file[index_FZ+2:index_gamma]))
            gamma_list.append(float(name_file[index_gamma + len('_gamma'):-4]))
            alpha_list.append(data['SA'])
            MZ_list.append(data['MZ'])

        #Function used in the LS method
        if FZ_nom == None:
            FZ_nom = statistics.median(FZ_list)

        def residuals_MZ(params,x,y):
            alpha_data,kappa_data,gamma_data,FZ_data,VX_data = x
            FY0 = pacejka.FY_pure((alpha_data,kappa_data,np.zeros(FZ_data.shape),FZ_data,VX_data),*p_FY_pure,FZ_nom)
            return y - pacejka.MZ_pure(x,*params,FZ_nom,R0,FY0)[0].ravel()

        
        #Checking sizes for all csv (they should have the same lenght)
        size = min(len(lis) for lis in MZ_list)
        MZ_list = [i[:size] for i in MZ_list]
        MZ_data = np.array(MZ_list).ravel()
        alpha_list = [i[:size].to_numpy() for i in alpha_list]
        FZ_data = np.array([np.ones(size)*i for i in FZ_list])
        gamma_data = np.array([np.ones(size)*i for i in gamma_list])
        alpha_data = np.array(alpha_list)
        VX_data = np.ones(FZ_data.shape)*VX
        kappa_data = np.zeros(FZ_data.shape)

        if lower_bounds == None:
            lower_bounds = [0, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf,
                 -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf]
        if upper_bounds == None:
            upper_bounds = [ np.inf, np.inf, np.inf, np.inf, np.inf,np.inf , np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf,
                 np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf]
        
        #For the interface (app)
        if full_output=='data_only':
            FY0 = pacejka.FY_pure((alpha_data,kappa_data,np.zeros(FZ_data.shape),FZ_data,VX_data),*p_FY_pure,FZ_nom)
            MZ_initial = pacejka.MZ_pure((alpha_data,kappa_data,gamma_data,FZ_data,VX_data),*initial_guess,FZ_nom,R0,FY0)[0].ravel()
            FZ_data_output = [i[0] for i in FZ_data]
            MZ_data_output = [MZ_data[i:i+size] for i in range(0,len(MZ_data),size)]
            MZ_initial_output = [MZ_initial[i:i+size] for i in range(0,len(MZ_initial),size)]
            return FZ_data_output,MZ_data_output,alpha_data,gamma_data,MZ_initial_output

        result= scipy.optimize.least_squares(residuals_MZ, initial_guess, args=((alpha_data,kappa_data,gamma_data,FZ_data,VX_data),MZ_data), max_nfev=10000,bounds=(lower_bounds,upper_bounds))
        p_fit = result.x

        if full_output == 2:
            FY0 = pacejka.FY_pure((alpha_data,kappa_data,np.zeros(FZ_data.shape),FZ_data,VX_data),*p_FY_pure,FZ_nom)
            MZ_initial = pacejka.MZ_pure((alpha_data,kappa_data,gamma_data,FZ_data,VX_data),*initial_guess,FZ_nom,R0,FY0)[0].ravel()
            FZ_data_output = [i[0] for i in FZ_data]
            MZ_initial_output = [MZ_initial[i:i+size] for i in range(0,len(MZ_initial),size)]
            MZ_data_output = [MZ_data[i:i+size] for i in range(0,len(MZ_data),size)]
            MZ_initial_output = [MZ_initial[i:i+size] for i in range(0,len(MZ_initial),size)]
            MZ_fit = pacejka.MZ_pure((alpha_data,kappa_data,gamma_data,FZ_data,VX_data),*p_fit,FZ_nom,R0,FY0)[0].ravel()
            MZ_fit_output = [MZ_fit[i:i+size] for i in range(0,len(MZ_fit),size)]
            

            return p_fit,initial_guess,FZ_nom,FZ_data_output,MZ_data_output,alpha_data,gamma_data,MZ_initial_output,MZ_fit_output
        
        elif full_output == 1:
            return p_fit,initial_guess,FZ_nom
        else:
            return p_fit,FZ_nom
    @staticmethod 
    def FX_combined(folder,p_FX_pure,initial_guess,FZ_nom = None,full_output = 0,lower_bounds = None, upper_bounds = None):
        #Reading folder with .csv for FX
        """
        The folder must contains .csv files with columns LSR and FX. Each file shoud have the follow name structure:
        FZXXXX_alphaXXXXX_gamaXXXXX.csv
        Where XXXX is the value for the vertical force used in this test
        The user can follow the examples in the sample/fit  
        """
        FZ_list = []
        FX_list = []
        kappa_list = []
        alpha_list = []

        for csv_file in glob.glob(os.path.join(folder, '*.csv')):
            name_file = os.path.basename(csv_file)
            data = pd.read_csv(csv_file,sep=';').sort_values(by='LSR')
            index_FZ = name_file.find('FZ')
            index_alpha = name_file.find('_alpha')
            FZ_list.append(float(name_file[index_FZ+2:index_alpha]))
            alpha_list.append(float(name_file[index_alpha+ len('_alpha'):-4]))
            FX_list.append(data['FX'])
            kappa_list.append(data['LSR'])
            
        #Function used in the LS method
        if FZ_nom == None:
            FZ_nom = statistics.median(FZ_list)
        def residuals_FX(params,x,y):     
            FX0_output = pacejka.FX_pure(x,*p_FX_pure,FZ_nom)
            return y - pacejka.FX_combined(x,*params,FZ_nom,FX0_output)[0].ravel()  
        
        #Checking sizes for all csv (they should have the same lenght)
        size = min(len(lis) for lis in FX_list)
        FX_list = [i[:size] for i in FX_list]
        FX_data = np.array(FX_list).ravel()
        kappa_list = [i[:size].to_numpy() for i in kappa_list]
        FZ_data = np.array([np.ones(size)*i for i in FZ_list])
        alpha_data = np.array([np.ones(size)*i for i in alpha_list])
        gamma_data =  np.zeros(FZ_data.shape)
        kappa_data = np.array(kappa_list)
        VX_data = np.ones(FZ_data.shape)*10

        if lower_bounds == None:
            lower_bounds = [0, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf]
        if upper_bounds == None:
            upper_bounds = [ np.inf, np.inf, np.inf, np.inf, np.inf, np.inf]

    #For the interface (app)
        if full_output=='data_only':       
            FX0_output = pacejka.FX_pure((alpha_data,kappa_data,gamma_data,FZ_data,VX_data),*p_FX_pure,FZ_nom)
            FX_initial = pacejka.FX_combined((alpha_data,kappa_data,gamma_data,FZ_data,VX_data),*initial_guess,FZ_nom,FX0_output)[0].ravel()
            FZ_data_output = [i[0] for i in FZ_data]
            FX_data_output = [FX_data[i:i+size] for i in range(0,len(FX_data),size)]
            FX_initial_output = [FX_initial[i:i+size] for i in range(0,len(FX_initial),size)]
            return FZ_data_output,FX_data_output,kappa_data,alpha_data,FX_initial_output
        
        result= scipy.optimize.least_squares(residuals_FX, initial_guess, args=((alpha_data,kappa_data,gamma_data,FZ_data,VX_data),FX_data), max_nfev=10000,bounds=(lower_bounds,upper_bounds))

        p_fit = result.x

        if full_output == 2:
            FX0_output = pacejka.FX_pure((alpha_data,kappa_data,gamma_data,FZ_data,VX_data),*p_FX_pure,FZ_nom)
            FX_initial = pacejka.FX_combined((alpha_data,kappa_data,gamma_data,FZ_data,VX_data),*initial_guess,FZ_nom,FX0_output)[0].ravel()
            FZ_data_output = [i[0] for i in FZ_data]
            FX_data_output = [FX_data[i:i+size] for i in range(0,len(FX_data),size)]
            FX_initial_output = [FX_initial[i:i+size] for i in range(0,len(FX_initial),size)]
            FX_fit = pacejka.FX_combined((alpha_data,kappa_data,gamma_data,FZ_data,VX_data),*p_fit,FZ_nom,FX0_output)[0].ravel()
            FX_fit_output = [FX_fit[i:i+size] for i in range(0,len(FX_fit),size)]
            
            return p_fit,initial_guess,FZ_nom,FZ_data_output,FX_data_output,kappa_data,alpha_data,FX_initial_output,FX_fit_output
        
        elif full_output == 1:
            return p_fit,initial_guess,FZ_nom
        else:
            return p_fit,FZ_nom
    @staticmethod 
    def FY_combined(folder,p_FY_pure,initial_guess,FZ_nom = None,full_output = 0,lower_bounds = None, upper_bounds = None):
        #Reading folder with .csv for FX
        """
        The folder must contains .csv files with columns SA and FY. Each file shoud have the follow name structure:
        FZXXXX_kappaXXXXX_gamaXXXXX.csv
        Where XXXX is the value for the variable used in this test
        The user can follow the examples in the sample/fit  
        """
        FZ_list = []
        FY_list = []
        kappa_list = []
        alpha_list = []
        gamma_list = []

        for csv_file in glob.glob(os.path.join(folder, '*.csv')):
            name_file = os.path.basename(csv_file)
            data = pd.read_csv(csv_file,sep=';').sort_values(by='SA')
            index_FZ = name_file.find('FZ')
            index_kappa = name_file.find('_kappa')
            index_gamma = name_file.find('_gamma')
            FZ_list.append(float(name_file[index_FZ+2:index_kappa]))
            kappa_list.append(float(name_file[index_kappa+ len('_kappa'):index_gamma]))
            gamma_list.append(float(name_file[index_gamma + len('_gamma'):-4]))
            FY_list.append(data['FY'])
            alpha_list.append(data['SA'])
            
        #Function used in the LS method
        if FZ_nom == None:
            FZ_nom = statistics.median(FZ_list)

        def residuals_FY(params,x,y):
            FY0_output = pacejka.FY_pure(x,*p_FY_pure,FZ_nom)
            return y - pacejka.FY_combined(x,*params,FZ_nom,FY0_output)[0].ravel()  
        
        #Checking sizes for all csv (they should have the same lenght)
        size = min(len(lis) for lis in FY_list)
        FY_list = [i[:size] for i in FY_list]
        FY_data = np.array(FY_list).ravel()
        alpha_list = [i[:size].to_numpy() for i in alpha_list]
        FZ_data = np.array([np.ones(size)*i for i in FZ_list])
        kappa_data = np.array([np.ones(size)*i for i in kappa_list])
        gamma_data = np.array([np.ones(size)*i for i in gamma_list])
        alpha_data = np.array(alpha_list)
        VX_data = np.ones(FZ_data.shape)

        if lower_bounds == None:
            lower_bounds = [-np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf,-np.inf,-np.inf,-np.inf,-np.inf,-np.inf,-np.inf,-np.inf]
        if upper_bounds == None:   
            upper_bounds = [ np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf,np.inf,np.inf,np.inf,np.inf,np.inf,np.inf,np.inf]

    #For the interface (app)
        if full_output=='data_only':       
            FY0_output = pacejka.FY_pure((alpha_data,kappa_data,gamma_data,FZ_data,VX_data),*p_FY_pure,FZ_nom)
            FY_initial = pacejka.FY_combined((alpha_data,kappa_data,gamma_data,FZ_data,VX_data),*initial_guess,FZ_nom,FY0_output)[0].ravel()
            FZ_data_output = [i[0] for i in FZ_data]
            FY_data_output = [FY_data[i:i+size] for i in range(0,len(FY_data),size)]
            FY_initial_output = [FY_initial[i:i+size] for i in range(0,len(FY_initial),size)]
            return FZ_data_output,FY_data_output,kappa_data,alpha_data,gamma_data,FY_initial_output
        
        result= scipy.optimize.least_squares(residuals_FY, initial_guess, args=((alpha_data,kappa_data,gamma_data,FZ_data,VX_data),FY_data), max_nfev=10000,bounds=(lower_bounds,upper_bounds))

        p_fit = result.x

        if full_output == 2:
            FY0_output = pacejka.FY_pure((alpha_data,kappa_data,gamma_data,FZ_data,VX_data),*p_FY_pure,FZ_nom)
            FY_initial = pacejka.FY_combined((alpha_data,kappa_data,gamma_data,FZ_data,VX_data),*initial_guess,FZ_nom,FY0_output)[0].ravel()
            FZ_data_output = [i[0] for i in FZ_data]
            FY_data_output = [FY_data[i:i+size] for i in range(0,len(FY_data),size)]
            FY_initial_output = [FY_initial[i:i+size] for i in range(0,len(FY_initial),size)]
            FY_fit = pacejka.FY_combined((alpha_data,kappa_data,gamma_data,FZ_data,VX_data),*p_fit,FZ_nom,FY0_output)[0].ravel()
            FY_fit_output = [FY_fit[i:i+size] for i in range(0,len(FY_fit),size)]
            
            return p_fit,initial_guess,FZ_nom,FZ_data_output,FY_data_output,kappa_data,alpha_data,gamma_data,FY_initial_output,FY_fit_output
        
        elif full_output == 1:
            return p_fit,initial_guess,FZ_nom
        else:
            return p_fit,FZ_nom
    @staticmethod    
    def MZ_combined(folder,R0,VX,p_FY_pure,p_FX_pure,p_MZ_pure,p_FY_combined,p_FX_combined,initial_guess,FZ_nom = None,full_output = 0,lower_bounds = None, upper_bounds = None):
        #Reading folder with .csv for FY
        """
        The folder must contains .csv files with columns SA and MZ. Each file shoud have the follow name structure:
        FZXXXX_kappaXXXXX_gamaXXXXX.csv
        Where XXXX is the value for the variable used in this test
        The user can follow the examples in the sample/fit   
        """
        FZ_list = []
        MZ_list = []
        kappa_list = []
        alpha_list = []
        gamma_list = []

        for csv_file in glob.glob(os.path.join(folder, '*.csv')):
            name_file = os.path.basename(csv_file)
            data = pd.read_csv(csv_file,sep=';').sort_values(by='SA')
            index_FZ = name_file.find('FZ')
            index_kappa = name_file.find('_kappa')
            index_gamma = name_file.find('_gamma')
            FZ_list.append(float(name_file[index_FZ+2:index_kappa]))
            kappa_list.append(float(name_file[index_kappa+ len('_kappa'):index_gamma]))
            gamma_list.append(float(name_file[index_gamma + len('_gamma'):-4]))
            MZ_list.append(data['MZ'])
            alpha_list.append(data['SA'])

        #Function used in the LS method
        if FZ_nom == None:
            FZ_nom = statistics.median(FZ_list)

        def residuals_MZ(params,x,y):
            alpha_data,kappa_data,gamma_data,FZ_data,VX_data = x
            FY0_output = pacejka.FY_pure((alpha_data,kappa_data,np.zeros(FZ_data.shape),FZ_data,VX_data),*p_FY_pure,FZ_nom)
            FX0_output = pacejka.FX_pure(x,*p_FX_pure,FZ_nom)
            MZ0_output = pacejka.MZ_pure(x,*p_MZ_pure,FZ_nom,R0,FY0_output)
            FY_output = pacejka.FY_combined((alpha_data,kappa_data,np.zeros(FZ_data.shape),FZ_data,VX_data),*p_FY_combined,FZ_nom,FY0_output)
            FX_output = pacejka.FX_combined(x,*p_FX_combined,FZ_nom,FX0_output)
            return y - pacejka.MZ_combined(x,*params,FZ_nom,R0,FX_output,FY_output,MZ0_output,FX0_output,FY0_output)[0].ravel()

        
        #Checking sizes for all csv (they should have the same lenght)
        size = min(len(lis) for lis in MZ_list)
        MZ_list = [i[:size] for i in MZ_list]
        MZ_data = np.array(MZ_list).ravel()
        alpha_list = [i[:size].to_numpy() for i in alpha_list]
        FZ_data = np.array([np.ones(size)*i for i in FZ_list])
        kappa_data = np.array([np.ones(size)*i for i in kappa_list])
        gamma_data = np.array([np.ones(size)*i for i in gamma_list])
        alpha_data = np.array(alpha_list)
        VX_data = np.ones(FZ_data.shape)*VX

        if lower_bounds == None:
            lower_bounds = [-np.inf, -np.inf, -np.inf, -np.inf]
        if upper_bounds == None:
            upper_bounds = [ np.inf, np.inf, np.inf, np.inf]
        
        #For the interface (app)
        if full_output=='data_only':
            FY0_output = pacejka.FY_pure((alpha_data,kappa_data,gamma_data,FZ_data,VX_data),*p_FY_pure,FZ_nom)
            FX0_output = pacejka.FX_pure((alpha_data,kappa_data,gamma_data,FZ_data,VX_data),*p_FX_pure,FZ_nom)
            MZ0_output = pacejka.MZ_pure((alpha_data,kappa_data,gamma_data,FZ_data,VX_data),*p_MZ_pure,FZ_nom,R0,FY0_output)
            FY_output = pacejka.FY_combined((alpha_data,kappa_data,gamma_data,FZ_data,VX_data),*p_FY_combined,FZ_nom,FY0_output)
            FX_output = pacejka.FX_combined((alpha_data,kappa_data,gamma_data,FZ_data,VX_data),*p_FX_combined,FZ_nom,FX0_output)
            MZ_initial = pacejka.MZ_combined((alpha_data,kappa_data,gamma_data,FZ_data,VX_data),*initial_guess,FZ_nom,R0,FX_output,FY_output,MZ0_output,FX0_output,FY0_output,)[0].ravel()
            FZ_data_output = [i[0] for i in FZ_data]
            MZ_data_output = [MZ_data[i:i+size] for i in range(0,len(MZ_data),size)]
            MZ_initial_output = [MZ_initial[i:i+size] for i in range(0,len(MZ_initial),size)]
            return FZ_data_output,MZ_data_output,alpha_data,gamma_data,MZ_initial_output

        result= scipy.optimize.least_squares(residuals_MZ, initial_guess, args=((alpha_data,kappa_data,gamma_data,FZ_data,VX_data),MZ_data), max_nfev=10000,bounds=(lower_bounds,upper_bounds))
        p_fit = result.x

        if full_output == 2:
            FY0_output = pacejka.FY_pure((alpha_data,kappa_data,gamma_data,FZ_data,VX_data),*p_FY_pure,FZ_nom)
            FX0_output = pacejka.FX_pure((alpha_data,kappa_data,gamma_data,FZ_data,VX_data),*p_FX_pure,FZ_nom)
            MZ0_output = pacejka.MZ_pure((alpha_data,kappa_data,gamma_data,FZ_data,VX_data),*p_MZ_pure,FZ_nom,R0,FY0_output)
            FY_output = pacejka.FY_combined((alpha_data,kappa_data,gamma_data,FZ_data,VX_data),*p_FY_combined,FZ_nom,FY0_output)
            FX_output = pacejka.FX_combined((alpha_data,kappa_data,gamma_data,FZ_data,VX_data),*p_FX_combined,FZ_nom,FX0_output)
            MZ_initial = pacejka.MZ_combined((alpha_data,kappa_data,gamma_data,FZ_data,VX_data),*initial_guess,FZ_nom,R0,FX_output,FY_output,MZ0_output,FX0_output,FY0_output,)[0].ravel()
            FZ_data_output = [i[0] for i in FZ_data]
            MZ_data_output = [MZ_data[i:i+size] for i in range(0,len(MZ_data),size)]
            MZ_initial_output = [MZ_initial[i:i+size] for i in range(0,len(MZ_initial),size)]
            MZ_fit = pacejka.MZ_combined((alpha_data,kappa_data,gamma_data,FZ_data,VX_data),*p_fit,FZ_nom,R0,FX_output,FY_output,MZ0_output,FX0_output,FY0_output,)[0].ravel()
            MZ_fit_output = [MZ_fit[i:i+size] for i in range(0,len(MZ_fit),size)]

            return p_fit,initial_guess,FZ_nom,FZ_data_output,MZ_data_output,alpha_data,gamma_data,MZ_initial_output,MZ_fit_output
        
        elif full_output == 1:
            return p_fit,initial_guess,FZ_nom
        else:
            return p_fit,FZ_nom