import numpy as np

class Pacejka:
    @staticmethod
    def Fx_pure(alpha_kappa_gamma_Fz_Vx,pcx1,pdx1,pdx2,pdx3,pex1,pex2,pex3,pex4,pkx1,pkx2,pkx3,phx1,phx2,pvx1,pvx2,Fz0,scaling_coeficients=None):

        """
        This function will calculate the Fx0 for a pure longitudinal situation:
        """

        _,kappa_input,gamma_input,Fz_input,_ = alpha_kappa_gamma_Fz_Vx #inputs for Fx0 calculation
        #Scaling coeficients from tir file
        if scaling_coeficients != None: 
            lambda_Cx= scaling_coeficients['LCX']
            lambda_Fz0 = scaling_coeficients['LFZO']
            lambda_mux = scaling_coeficients['LMUX']
            lambda_Ex = scaling_coeficients['LEX']
            lambda_Kx = scaling_coeficients['LKX']
            lambda_Hx = scaling_coeficients['LHX']
            lambda_Vx = scaling_coeficients['LVX']
        else:
            lambda_Cx= 1
            lambda_Fz0 = 1
            lambda_mux = 1
            lambda_Ex = 1
            lambda_Kx = 1
            lambda_Hx = 1
            lambda_Vx = 1
        
        #No star correction:
        kappa = kappa_input
        gamma = gamma_input
        Fz = Fz_input

            
        #Epsilon is necessary to avoid division by 0
        epsilon = 0.001

        
        ##Vertical load
        Fz0_ = lambda_Fz0*Fz0 #Fz0 - Nominal load with scaling factor (4.E1)
        dfz = (Fz - Fz0_)/(Fz0_) #dfz0 - Normalised change in vertical load (4.E2a)
        

        ##Magic Formula

        """
        Fx equation for pure longitudinal:

        Fx0 = Dx*sin(Cx*arctan(Bx*kappax - Ex*(Bx*kappax - arctan(Bx*kappax)))) + SVx  

        """

        ##Dx
        mux = (pdx1 + pdx2*dfz)*(1-pdx3*gamma**2)*lambda_mux #(4.E13) But no pressure -> MF52
        Dx = mux*Fz #(4.E12)

        ##Cx 
        Cx = pcx1*lambda_Cx #(4.E12)

        ##Bx:
        Kx = Fz*(pkx1 + pkx2*dfz)*np.exp(pkx3*dfz)*lambda_Kx #(4.E15)
        Bx = Kx/(Cx*Dx + epsilon*np.where(Cx*Dx==0,1,0)) #(4.E16)

        ##kappax
        SHx = (phx1 + phx2*dfz)*lambda_Hx #(4.E17)
        kappax = kappa + SHx #(4.E10)

        ##Ex
        Ex = (pex1 + pex2*dfz + pex3*dfz**2)*(1-pex4*np.sign(kappax))*lambda_Ex #(4.E14)

        #SVx
        SVx = Fz*(pvx1 + pvx2*dfz)*lambda_Vx*lambda_mux #(4.E18)

        #Fx0
        Fx0 = Dx*np.sin(Cx*np.arctan(Bx*kappax - Ex*(Bx*kappax - np.arctan(Bx*kappax)))) + SVx #(4.E9)

        return Fx0,mux,kappax,Bx,Cx,Dx,Ex,SVx,SHx,Kx
    
    @staticmethod
    def Fy_pure(alpha_kappa_gamma_Fz_Vx,pcy1,pdy1,pdy2,pdy3,pey1,pey2,pey3,pey4,pky1,pky2,pky3,
                          phy1,phy2,phy3,pvy1,pvy2,pvy3,pvy4,Fz0,star_correction=False,scaling_coeficients=None):

        """
        This function will calculate the Fy0 for a pure cornering situation:
        """

        alpha_input,_,gamma_input,Fz_input,_ = alpha_kappa_gamma_Fz_Vx #inputs for Fy0 calculation
        if scaling_coeficients != None:
            lambda_Cy = scaling_coeficients['LCY']
            lambda_Fz0 = scaling_coeficients['LFZO']
            lambda_muy = scaling_coeficients['LMUY']
            lambda_Ky = scaling_coeficients['LKY']
            lambda_Hy = scaling_coeficients['LHY']
            lambda_Vy = scaling_coeficients['LVY']
            lambda_Ey = scaling_coeficients['LEY']
        else:
            lambda_Cy = 1
            lambda_Fz0 = 1
            lambda_muy = 1
            lambda_Ky = 1
            lambda_Hy = 1
            lambda_Vy = 1
            lambda_Ey = 1


        #Epsilon is necessary to avoid division by 0
        epsilon = 0.001

        ##Star correction
        if star_correction == True:
            gamma = np.sin(gamma_input) #(4.E4)
            alpha = np.tan(alpha_input) #(4.E3) obs: Vcx >0 (no backwards), so sign(Vcx) will be always 1
            Fz = Fz_input
        else:
            gamma = gamma_input
            alpha = alpha_input
            Fz = Fz_input

        ##Vertical load
        Fz0_ = lambda_Fz0*Fz0 #Fz0 - Nominal load with scaling factor (4.E1)
        dfz = (Fz - Fz0_)/(Fz0_) #dfz0 - Normalised change in vertical load (4.E2a)
        ##########################

        

        ##Magic Formula

        """
        Fy equations for pure cornering mouvement:

        Fy0 =  Dy*sin(Cy*arctan(By*alphay - Ey*(By*alphay - arctan(By*alphay)))) + SVy 

        """
        ##Dy
        mu_y = lambda_muy*(pdy1 + pdy2*dfz)/(1-pdy3*gamma**2) #(4.E23)
        Dy = mu_y*Fz #(4.E22)

        ##Cy
        Cy = pcy1*lambda_Cy #(4.E21)
    
        ##By
        pky4 = 2
        Ky = lambda_Ky*pky1*Fz0_*np.sin(pky4*np.arctan(Fz/(pky2*Fz0_)))/(1 - pky3*np.abs(gamma)) #(4.E25)
        #Kyalpha = Kyalpha + epsilon*np.where(Kyalpha==0,1,0)
        By = Ky/(Cy*Dy + epsilon*np.where(Cy*Dy==0,1,0))  #(4.E26)

        ##alphay
        SHy = (phy1 + phy2*dfz)*lambda_Hy +phy3*gamma #(4.E27)
        alphay = alpha + SHy #(4.E20)

        ##Ey
        Ey = (pey1 + pey2*dfz)*(1 -(pey3+pey4*gamma)*np.sign(alphay))*lambda_Ey #(4.E24)

        ##SVy
        SVy = (Fz*(pvy1 + pvy2*dfz)*lambda_Vy + (pvy3 + pvy4*dfz))*lambda_muy #(4.E29)

        ##Fy0
        Fy0 =  Dy*np.sin(Cy*np.arctan(By*alphay - Ey*(By*alphay - np.arctan(By*alphay)))) + SVy #(4.E19)

        return Fy0,mu_y,alphay,By,Cy,Dy,Ey,SVy,SHy,Ky
    
    @staticmethod
    def Mz_pure(alpha_kappa_gamma_Fz_Vx,qbz1,qbz2,qbz3,qbz4,qbz5,qbz9,qbz10,qcz1,qdz1,qdz2,qdz3,qdz4,qdz6,qdz7,qdz8,qdz9,
                qez1,qez2,qez3,qez4,qez5,
                qhz1,qhz2,qhz3,qhz4,
                Fz0,R0,Fy0_output,star_correction=False,scaling_coeficients=None):
        

        """
        This function will calculate the Mz0 for a pure cornering situation:
        """ 
        Fy0,_,_,By,Cy,_,_,SVy,SHy,Ky = Fy0_output #gamma should be 0 for this output
        alpha_input,_,gamma_input,Fz_input,Vx_input = alpha_kappa_gamma_Fz_Vx

        if scaling_coeficients != None:
            lambda_t= scaling_coeficients['LTR']
            lambda_Fz0=scaling_coeficients['LFZO']
            lambda_Ky=scaling_coeficients['LKY']
            lambda_Mr=scaling_coeficients['LRES']
            lambda_muy = scaling_coeficients['LMUY']
        else:
            lambda_t=1
            lambda_Fz0=1
            lambda_Ky=1
            lambda_Mr=1
            lambda_muy = 1
        

        #Epsilon is necessary to avoid division by 0
        epsilon = 0.001


        ##Star correction
        if star_correction == True:
            gamma = np.sin(gamma_input) #(4.E4)
            alpha = np.tan(alpha_input) #(4.E3) obs: Vcx >0 (no backwards), so sign(Vcx) will be always 1
            Fz = Fz_input
            Vx = Vx_input
        else:
            gamma = gamma_input
            alpha = alpha_input
            Fz = Fz_input
            Vx =  Vx_input

        ##Vertical load
        Fz0_ = lambda_Fz0*Fz0 #Fz0 - Nominal load with scaling factor (4.E1)
        dfz = (Fz - Fz0_)/(Fz0_) #dfz0 - Normalised change in vertical load (4.E2a)
        ##########################

        


        ##########################
        ##Magic Formula
        """
        Mz equations for pure cornering mouvement:

        t0 = Dt*np.cos(Ct*np.arctan(Bt*alphat - Et*(Bt*alphat - np.arctan(Bt*alphat))))

        Mzr = Dr*cos(Cr*arctan(Br*alphar))

        Mz0 = -t*Fy0 + Mzr

        """

        ##Dt
        Dt0 = Fz*(R0/Fz0)*(qdz1 + qdz2*dfz)*lambda_t #(4.E42)
        Dt = Dt0*(1+qdz3*gamma + qdz4*gamma**2) #(4.E43)

        ##Ct
        Ct =  qcz1 #(4.E41)

        ##Bt
        Bt = (qbz1 + qbz2*dfz + qbz3*dfz**2)*(1+qbz5*abs(gamma) + qbz4*gamma)*lambda_Ky/lambda_muy #(4.E40)

        ##alphat
        SHt = qhz1 + qhz2*dfz + (qhz3 + qhz4*dfz)*gamma #(4.E35)
        alphat = alpha + SHt #(4.E34)

        ##Et
        Et = (qez1 + qez2*dfz + qez3*dfz**2)*(1 + (qez4 + qez5*gamma)*(2/np.pi)*np.arctan(Bt*Ct*alphat)) #(4.E44)

        ##t0
        #cos'alpha = Vcx/Vc (Vcx = Vx)
        Vcx = Vx
        Vsy = np.tan(alpha_input)*Vcx
        Vcy  = Vsy
        Vc = (Vcy**2 + Vcx**2)**0.5

        t0 = Dt*np.cos(Ct*np.arctan(Bt*alphat - Et*(Bt*alphat - np.arctan(Bt*alphat))))*(Vcx/Vc) #(4.E33)
        #t0 = Dt*np.cos(Ct*np.arctan(Bt*alphat - Et*(Bt*alphat - np.arctan(Bt*alphat))))*np.cos(alpha)
        #t0 =  Dt*np.cos(Ct*np.arctan(Bt*alphat - Et*(Bt*alphat - np.arctan(Bt*alphat))))*(1-(alpha**2)/2) #(4.E33) aproximmation to improve fit performance

        ##Dr
        Dr = Fz*R0*((qdz6 + qdz7*dfz)*lambda_Mr + (qdz8 + qdz9*dfz)*gamma)#(4.E47)

        ##Cr
        Cr = 1 #(4.E46)

        ##Br
        Br = (qbz9*lambda_Ky/lambda_muy + qbz10*By*Cy)

        ##alphar
        SHr = SHy + SVy/(Ky + epsilon*np.where(Ky==0,1,0)) #(4.E38)
        alphar = alpha + SHr #(4.E37)

        ##Mzr
        Mzr0 = Dr*np.cos(Cr*np.arctan(Br*alphar))*np.cos(alpha) #(4.E36)

        ##Mz0

        Mz0 = -t0*Fy0 + Mzr0 #(4.E31 and 4.E32)

        return Mz0,Mzr0,t0,alphat,Bt,Ct,Dt,Et,SHt,alphar,Br,Cr,Dr
    
    @staticmethod
    def Fx_combined(alpha_kappa_gamma_Fz_Vx,rbx1,rbx2,rcx1,rex1,rex2,rhx1,Fz0,Fx0_output,star_correction=False,scaling_coeficients=None):

        """
        This function will calculate the Fx for a combined slip situation:
        """

        alpha_input,kappa_input,_,Fz_input,_ = alpha_kappa_gamma_Fz_Vx
        Fx0,_,_,_,_,_,_,_,_,_ = Fx0_output

        if scaling_coeficients != None:
            lambda_xalpha= scaling_coeficients['LXAL']
            lambda_Fz0=scaling_coeficients['LFZO']
        else:
            lambda_xalpha=1
            lambda_Fz0=1

        ##Star correction
        if star_correction == True:
            alpha = np.tan(alpha_input) #(4.E3) obs: Vcx >0 (no backwards), so sign(Vcx) will be always 1
            Fz = Fz_input
            kappa = kappa_input
        else:
            alpha = alpha_input
            Fz = Fz_input
            kappa = kappa_input

        ##Vertical load
        Fz0_ = lambda_Fz0*Fz0 #Fz0 - Nominal load with scaling factor (4.E1)
        dfz = (Fz - Fz0_)/(Fz0_) #dfz0 - Normalised change in vertical load (4.E2a)
        ##########################

        ##########################
        ##Magic Formula
        """
        Fx equation for combined mouvement:

        Fx = Fx0*Gxalpha 

        Gxalpha = cos(Cxalpha*arctan(Bxalpha*alpha_s - Exalpha*(Bxalpha*alpha_s - arctan(Bxalpha*alpha_s))))/Gxalpha_0

        """ 

        ##Bxalpha
        Bxalpha = rbx1*np.cos(np.arctan(rbx2*kappa))*lambda_xalpha #(4.E54)

        ##Cxalpha
        Cxalpha = rcx1 #(4.E55)

        ##Exalpha
        Exalpha = rex1 + rex2*dfz #(4.E56)

        ##SHxalpha
        SHxalpha = rhx1 #(4.E57)

        #alphas
        alphas = alpha + SHxalpha #(4.E53) 

        ##Gxalpha_0
        Gxalpha_0 = np.cos(Cxalpha*np.arctan(Bxalpha*SHxalpha - Exalpha*(Bxalpha*SHxalpha - np.arctan(Bxalpha*SHxalpha )))) #(4.E52) 
        
        ##Gxalpha
        Gxalpha = np.cos(Cxalpha*np.arctan(Bxalpha*alphas - Exalpha*(Bxalpha*alphas - np.arctan(Bxalpha*alphas))))/Gxalpha_0 #(4.E51) 

        ##Fx
        Fx = Fx0*Gxalpha #(4.E50) 

        return Fx, Gxalpha
    
    @staticmethod
    def Fy_combined(alpha_kappa_gamma_Fz_Vx,rby1,rby2,rby3,rcy1,rey1,rey2,rhy1,rhy2,
                    rvy1,rvy2,rvy3,rvy4,rvy5,rvy6,Fz0,Fy0_output,star_correction=False,scaling_coeficients=None):
        """
        This function will calculate the Fy for a combined (lat and long) situation:
        """
        Fy0,mu_y,_,_,_,_,_,_,_,_ = Fy0_output

        alpha_input,kappa_input,gamma_input,Fz_input,_ = alpha_kappa_gamma_Fz_Vx

        if scaling_coeficients != None:
            lambda_vykappa = scaling_coeficients['LVYKA']
            lambda_ykappa = scaling_coeficients['LYKA']
            lambda_Fz0 = scaling_coeficients['LFZO']

        else:
            lambda_vykappa = 1
            lambda_ykappa = 1
            lambda_Fz0 = 1
        

        ##Star correction
        if star_correction == True:
            gamma = np.sin(gamma_input)
            alpha = np.tan(alpha_input) #(4.E3) obs: Vcx >0 (no backwards), so sign(Vcx) will be always 1
            Fz = Fz_input
            kappa = kappa_input
        else:
            gamma = gamma_input
            alpha = alpha_input
            Fz = Fz_input
            kappa = kappa_input

        ##Vertical load
        Fz0_ = lambda_Fz0*Fz0 #Fz0 - Nominal load with scaling factor (4.E1)
        dfz = (Fz - Fz0_)/(Fz0_) #dfz0 - Normalised change in vertical load (4.E2a)
        ##########################

        ##########################
        ##Magic Formula
        """
        Fy equation for combined mouvement:

        Fy = Fy0*Gykappa + SVykappa

        Gykappa = cos(Cykappa*arctan(Bykappa*alpha_s - Eykappa*(Bykappa*alpha_s - arctan(Bykappa*alpha_s))))/Gykappa_0

        """ 

        ##Bykappa
        Bykappa = rby1*np.cos(np.arctan(rby2*(alpha - rby3)))*lambda_ykappa #(4.E62)

        ##Cykappa
        Cykappa = rcy1 #(4.E63)

        ##Eykappa
        Eykappa = rey1 + rey2*dfz #(4.E64)

        ##SHykappa
        SHykappa = rhy1 + rhy2*dfz #(4.E65)

        ##Dvykappa
        Dvykappa = mu_y*Fz*(rvy1 + rvy2*dfz + rvy3*gamma)*np.arctan(rvy4*alpha) #(4.E67)

        ##SVykappa
        SVykappa = Dvykappa*np.sin(rvy5*np.arctan(rvy6*kappa))*lambda_vykappa #(4.E66)

        ##kappa_s
        kappa_s = kappa + SHykappa #(4.E61)

        ##Gykappa_0
        Gykappa_0 = np.cos(Cykappa*np.arctan(Bykappa*SHykappa - Eykappa*(Bykappa*SHykappa - np.arctan(Bykappa*SHykappa )))) #(4.E60) 
        
        ##Gykappa
        Gykappa = np.cos(Cykappa*np.arctan(Bykappa*kappa_s - Eykappa*(Bykappa*kappa_s - np.arctan(Bykappa*kappa_s))))/Gykappa_0 #(4.E59) 

        ##Fy
        Fy = Fy0*Gykappa + SVykappa #(4.E58)

        return Fy,Gykappa,SVykappa
    
    @staticmethod
    def Mz_combined(alpha_kappa_gamma_Fz_Vx,ssz1,ssz2,ssz3,ssz4,Fz0,R0,Fx_output,Fy_output,Mz0_output,Fx0_output,Fy0_output,star_correction=False,scaling_coeficients=None):
        """
        This function will calculate Mz combined (lat and long) :
        """
        Fx, _ = Fx_output
        Fy,_,SVykappa = Fy_output
        _,_,_,alphat,Bt,Ct,Dt,Et,_,alphar,Br,Cr,Dr = Mz0_output
        _,_,_,_,_,_,_,_,_,Kx = Fx0_output
        _,_,_,_,_,_,_,_,_,Ky = Fy0_output
        alpha_input,kappa_input,gamma_input,Fz_input,Vx_input = alpha_kappa_gamma_Fz_Vx

        if scaling_coeficients != None:
            lambda_s = scaling_coeficients['LS']
            lambda_Fz0 = scaling_coeficients['LFZO']
        else:
            lambda_s = 1
            lambda_Fz0 = 1
        

        ##Star correction
        if star_correction == True:
            gamma = np.sin(gamma_input)
            alpha = np.tan(alpha_input) #(4.E3) obs: Vcx >0 (no backwards), so sign(Vcx) will be always 1
            Fz = Fz_input
            kappa = kappa_input
            Vx = Vx_input
        else:
            gamma = gamma_input
            alpha = alpha_input
            Fz = Fz_input
            kappa = kappa_input
            Vx = Vx_input

        #Epsilon is necessary to avoid division by 0
        epsilon = 0.001

        ##########################
        ##Vertical load
        Fz0_ = lambda_Fz0*Fz0 #Fz0 - Nominal load with scaling factor (4.E1)
        dfz = (Fz - Fz0_)/(Fz0_) #dfz0 - Normalised change in vertical load (4.E2a)

        ##########################
        #Magic Formula
        """
        Mz = -t*Fy_ + Mzr + s*Fx

        """

        ##Fy_
        Fy_ = Fy - SVykappa #(4.E74) = Gykappa*Fy0 (gamma should be 0)
        
        ##t
        #cos'alpha = Vcx/Vc (Vcx = Vx)
        Vcx = Vx
        Vsy = np.tan(alpha_input)*Vcx
        Vcy  = Vsy
        Vc = (Vcy**2 + Vcx**2)**0.5
        alpha_teq = (alphat**2 + (Kx/(Ky + epsilon*np.where(Ky==0,1,0) ))**2*kappa**2)**0.5*np.sign(alphat) #(4.E77)
        t = Dt*np.cos(Ct*np.arctan(Bt*alpha_teq - Et*(Bt*alpha_teq - np.arctan(Bt*alpha_teq))))*(Vcx/Vc) #(4.E73)

        ##Mzr
        alpha_req = (alphar**2 + (Kx/(Ky + epsilon*np.where(Ky==0,1,0) ))**2*kappa**2)**0.5 #(4.E78)
        Mzr = Dr*np.cos(Cr*np.arctan(Br*alpha_req)) #(4.E75)

        ##s
        s = (ssz1 + ssz2*(Fy/Fz0) + (ssz3 + ssz4*dfz)*gamma)*R0*lambda_s #(4.E76)

        ##Mz
        Mz = -t*Fy_ + Mzr + s*Fx #(4.E71)

        return Mz,t,s
    
    @staticmethod
    def My_RR(Fz_Vx,Fz0_,R0,V0,Fx_output,qsy1,qsy2,qsy3,qsy4):
        """
        This function will calculate My rolling resistance torque :
        """
        Fz,Vx = Fz_Vx
        Fx,_ = Fx_output
        lambda_My = 1

        My = -Fz*R0*(qsy1 + qsy2*Fx/Fz0_ + qsy3*abs(Vx/V0) + qsy4*(Vx/V0)**4)*lambda_My #(11.E70)

        return [My]
    
    @staticmethod
    def Mx_overturning(gamma_Fz_Vx,Fz0_,R0,Fy_output,qsx1,qsx2,qsx3):
        """
        This function will calculate Mx overturning torque :
        """
        gamma,Fz,_ = gamma_Fz_Vx
        Fy,_,_ = Fy_output
        lambda_Mx = 1

        Mx = Fz*R0*(qsx1 - qsx2*gamma + qsx3*Fy/Fz0_)*lambda_Mx #(4.E69)

        return [Mx]

    def Radius(Fz_Vx,Cz,B,D,F,Fz0_,R0):
        """
    This function will calculate the deflection, the effective rolling radius and the omega (rotational speed of the tire):
    """
        Fz,Vx = Fz_Vx
        rho = Fz/Cz
        rho_Fz0 = Fz0_/Cz
        rho_d = rho/rho_Fz0

        Re = R0 - rho_Fz0*(D*np.arctan(B*rho_d) + F*rho_d)

        omega = Vx/Re

        return Re,rho,omega
