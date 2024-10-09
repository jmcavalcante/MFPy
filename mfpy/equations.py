import numpy as np

class Pacejka:
    @staticmethod
    def Fx_pure(kappa_Fz,pcx1,pdx1,pdx2,pex1,pex2,pex3,pex4,pkx1,pkx2,pkx3,phx1,phx2,pvx1,pvx2,Fz0_):

        """
        This function will calculate the Fx0 for a pure longitudinal situation:
        """

        kappa,Fz = kappa_Fz
        lambda_Cx=1
        lambda_Fz0=1
        lambda_mux=1
        lambda_Kx=1
        lambda_Hx=1
        lambda_Vx=1
        lambda_Ex=1

        
        ##Vertical load
        Fz0 = lambda_Fz0*Fz0_ #Fz0 - Nominal load with scaling factor (4.E1)
        dfz = (Fz - Fz0)/(Fz0) #dfz0 - Normalised change in vertical load (4.E2)
        ##########################
        ##Magic Formula

        """
        Fx equation for pure longitudinal:

        Fx0 = Dx*sin(Cx*arctan(Bx*kappax - Ex*(Bx*kappax - arctan(Bx*kappax)))) + SVx  

        """
        ##Dx
        mux = (pdx1 + pdx2*dfz)*lambda_mux #(4.E13)
        Dx = mux*Fz #(4.E12)

        ##Cx 
        Cx = pcx1*lambda_Cx #(4.E12)

        ##Bx:
        epsilon_x = 0.0001
        Kxkappa = Fz*(pkx1 + pkx2*dfz)*np.exp(pkx3*dfz)*lambda_Kx #(4.E15)
        Bx = Kxkappa/(Cx*Dx + epsilon_x*np.where(Cx*Dx==0,1,0)) #(4.E16)

        ##kappax
        SHx = (phx1 + phx2*dfz)*lambda_Hx #(4.E17)
        kappax = kappa + SHx #(4.E10)

        ##Ex
        Ex = (pex1 + pex2*dfz + pex3*dfz**2)*(1-pex4*np.sign(kappax))*lambda_Ex #(4.E14)

        #SVx
        SVx = Fz*(pvx1 + pvx2*dfz)*lambda_Vx #(4.E18) obs: the lambda' and (Vcx/(epsilong + Vcx)) will be neglected

        #Fx0
        Fx0 = Dx*np.sin(Cx*np.arctan(Bx*kappax - Ex*(Bx*kappax - np.arctan(Bx*kappax)))) + SVx #(4.E9)

        return Fx0,mux,kappax,Bx,Cx,Dx,Ex,SVx,SHx,Kxkappa
    
    @staticmethod
    def Fy_pure(alpha_gamma_Fz,pcy1,pdy1,pdy2,pdy3,pey1,pey2,pey3,pey4,pey5,pky1,pky2,pky3,pky4,pky5,pky6,pky7,
                          phy1,phy2,pvy1,pvy2,pvy3,pvy4,Fz0_):

        """
        This function will calculate the Fy0 for a pure cornering situation:
        """

        alpha,gamma,Fz = alpha_gamma_Fz
        lambda_Cy=1
        lambda_Fz0=1
        lambda_muy=1
        lambda_Ky=1
        lambda_Hy=1
        lambda_Vy=1
        lambda_Ey=1


        ##Vertical load
        Fz0 = lambda_Fz0*Fz0_ #Fz0 - Nominal load with scaling factor (4.E1)
        dfz = (Fz - Fz0)/(Fz0) #dfz0 - Normalised change in vertical load (4.E2)
        ##########################
        ##Magic Formula

        """
        Fy equations for pure cornering mouvement:

        Fy0 =  Dy*sin(Cy*arctan(By*alphay - Ey*(By*alphay - arctan(By*alphay)))) + SVy 

        """
        ##Dy
        gamma_star = np.sin(gamma) #(4.E4)
        mu_y = lambda_muy*(pdy1 + pdy2*dfz)/(1+pdy3*gamma_star**2) #(4.E23)
        Dy = mu_y*Fz #(4.E22)

        ##Cy
        Cy = pcy1*lambda_Cy #(4.E21)
    
        ##By
        epsilon_y = 0.0001
        Kyalpha = lambda_Ky*pky1*Fz0_*np.sin(pky4*np.arctan(Fz/((pky2 + pky5*gamma_star**2)*Fz0_)))/(1+pky3*gamma_star**2) #(4.E25)
        Kyalpha = Kyalpha + epsilon_y*np.where(Kyalpha==0,1,0)
        By = Kyalpha/(Cy*Dy + epsilon_y*np.where(Cy*Dy==0,1,0))  #(4.E26)

        ##alphay
        alpha_star = np.tan(alpha) #(4.E3) obs: Vcx >0 (no backwards), so sign(Vcx) will be always 1
        Kygamma_0 = Fz*(pky6 + pky7*dfz)*lambda_Ky #(4.E30)
        SVygamma = Fz*(pvy3 + pvy4*dfz)*gamma_star*lambda_Ky #(4.E28) obs: lambda' will be neglected
        SHy = (phy1 + phy2*dfz)*lambda_Hy +(Kygamma_0*gamma_star - SVygamma)/(Kyalpha) #(4.E27)
        alphay = alpha_star + SHy #(4.E20)

        ##Ey
        Ey = (pey1 + pey2*dfz)*(1+pey5*gamma_star**2-(pey3+pey4*gamma_star)*np.sign(alphay))*lambda_Ey #(4.E24)

        ##SVy
        SVy = Fz*(pvy1 + pvy2*dfz)*lambda_Vy + SVygamma #(4.E29)

        ##Fy0
        Fy0 =  Dy*np.sin(Cy*np.arctan(By*alphay - Ey*(By*alphay - np.arctan(By*alphay)))) + SVy #(4.E19)

        return Fy0,mu_y,alphay,By,Cy,Dy,Ey,SVy,SHy,SVygamma,Kyalpha,Kygamma_0
    
    @staticmethod
    def Mz_pure(alpha_gamma_Fz,qbz1,qbz2,qbz3,qbz4,qbz5,qbz9,qbz10,qcz1,qdz1,qdz2,qdz3,qdz4,qdz6,qdz7,qdz8,qdz9,qdz10,qdz11,
                qez1,qez2,qez3,qez4,qez5,
                qhz1,qhz2,qhz3,qhz4,
                Fz0_,R0,Fy0_output):
        
        

        """
        This function will calculate the Mz0 for a pure cornering situation:
        """
        Fy0,mu_y,alphay,By,Cy,Dy,Ey,SVy,SHy,SVygamma,Kyalpha,Kygamma_0 = Fy0_output
        alpha,gamma,Fz = alpha_gamma_Fz
        lambda_t=1
        lambda_Fz0=1
        lambda_Ky=1
        lambda_Mr=1
        lambda_Kzgamma=1

        ##Vertical load
        Fz0 = lambda_Fz0*Fz0_ #Fz0 - Nominal load with scaling factor (4.E1)
        dfz = (Fz - Fz0)/(Fz0) #dfz0 - Normalised change in vertical load (4.E2)


        ##########################
        ##Magic Formula
        """
        Mz equations for pure cornering mouvement:

        t0 = Dt*np.cos(Ct*np.arctan(Bt*alphat - Et*(Bt*alphat - np.arctan(Bt*alphat))))

        Mzr = Dr*cos(Cr*arctan(Br*alphar))

        Mz0 = -t*Fy0 + Mzr

        """

        ##Dt
        Dt0 = Fz*(R0/Fz0_)*(qdz1 + qdz2*dfz)*lambda_t #(4.E42)
        gamma_star = np.sin(gamma) #(4.E4)
        Dt = Dt0*(1+qdz3*abs(gamma_star) + qdz4*gamma_star**2) #(4.E43)

        ##Ct
        Ct =  qcz1 #(4.E41)

        ##Bt
        Bt = (qbz1 + qbz2*dfz + qbz3*dfz**2)*(1+qbz5*abs(gamma_star) + qbz4*gamma_star**2)*lambda_Ky #(4.E40)

        ##alphat
        alpha_star = np.tan(alpha) #(4.E3) obs: Vcx >0 (no backwards), so sign(Vcx) will be always 1
        SHt = qhz1 + qhz2*dfz + (qhz3 + qhz4*dfz)*gamma_star #(4.E35)
        alphat = alpha_star + SHt #(4.E34)

        ##Et
        Et = (qez1 + qez2*dfz + qez3*dfz**2)*(1 + (qez4 + qez5*gamma_star)*(2/3.14)*np.arctan(Bt*Ct*alphat)) #(4.E44)

        ##t0
        t0 = Dt*np.cos(Ct*np.arctan(Bt*alphat - Et*(Bt*alphat - np.arctan(Bt*alphat)))) #(4.E33)


        ##Dr
        Dr = Fz*R0*((qdz6 + qdz7*dfz)*lambda_Mr + (qdz8 + qdz9*dfz)*gamma_star*lambda_Kzgamma + (qdz10 + qdz11*dfz)*gamma_star*abs(gamma_star)) #(4.E47)

        ##Cr
        Cr = 1 #(4.E46)

        ##Br
        Br = (qbz9*lambda_Ky + qbz10*By*Cy)

        ##alphar
        epsilon_K = 0.0001
        K_yalpha_ = Kyalpha + epsilon_K*np.where(Kyalpha==0,1,0) #(4.E39)
        SHf = SHy + SVy/K_yalpha_ #(4.E38)
        alphar = alpha_star + SHf #(4.E37)

        ##Mzr
        Mzr0 = Dr*np.cos(Cr*np.arctan(Br*alphar)) #(4.E36)

        ##Mz0

        Mz0 = -t0*Fy0 + Mzr0 #(4.E31 and 4.E32)

        return Mz0,Mzr0,t0,alphat,Bt,Ct,Dt,Et,SHt,alphar,Br,Cr,Dr
    
    @staticmethod
    def Fx_combined(alpha_kappa_gamma_Fz,rbx1,rbx2,rbx3,rcx1,rex1,rex2,rhx1,Fz0_,Fx0_output):

        """
        This function will calculate the Fx for a combined (lat and long) situation:
        """

        alpha,kappa,gamma,Fz = alpha_kappa_gamma_Fz
        Fx0,mux,kappax,Bx,Cx,Dx,Ex,SVx,SHx,Kxkappa = Fx0_output
        lambda_xalpha = 1
        lambda_Fz0 = 1

        ##Vertical load
        Fz0 = lambda_Fz0*Fz0_ #Fz0 - Nominal load with scaling factor (4.E1)
        dfz = (Fz - Fz0)/(Fz0) #dfz0 - Normalised change in vertical load (4.E2)

        ##########################
        ##Magic Formula
        """
        Fx equation for combined mouvement:

        Fx = Fx0*Gxalpha 

        Gxalpha = cos(Cxalpha*arctan(Bxalpha*alpha_s - Exalpha*(Bxalpha*alpha_s - arctan(Bxalpha*alpha_s))))/Gxalpha_0

        """ 

        ##Bxalpha
        gamma_star = np.sin(gamma) #(4.E4)
        Bxalpha = (rbx1 + rbx3*gamma_star**2)*np.cos(np.arctan(rbx2*kappa))*lambda_xalpha #(4.E54)

        ##Cxalpha
        Cxalpha = rcx1 #(4.E55)

        ##Exalpha
        Exalpha = rex1 + rex2*dfz #(4.E56)

        ##SHxalpha
        SHxalpha = rhx1 #(4.E57)

        #alphas
        alpha_star = np.tan(alpha) #(4.E3) obs: Vcx >0 (no backwards), so sign(Vcx) will be always 1
        alphas = alpha_star + SHxalpha #(4.E53) 

        ##Gxalpha_0
        Gxalpha_0 = np.cos(Cxalpha*np.arctan(Bxalpha*SHxalpha - Exalpha*(Bxalpha*SHxalpha - np.arctan(Bxalpha*SHxalpha )))) #(4.E52) 
        
        ##Gxalpha
        Gxalpha = np.cos(Cxalpha*np.arctan(Bxalpha*alphas - Exalpha*(Bxalpha*alphas - np.arctan(Bxalpha*alphas))))/Gxalpha_0 #(4.E51) 

        ##Fx
        Fx = Fx0*Gxalpha #(4.E50) 

        return Fx, Gxalpha
    
    @staticmethod
    def Fy_combined(alpha_kappa_gamma_Fz,rby1,rby2,rby3,rby4,rcy1,rey1,rey2,rhy1,rhy2,
                    rvy1,rvy2,rvy3,rvy4,rvy5,rvy6,Fz0_,Fy0_output):
        """
        This function will calculate the Fy for a combined (lat and long) situation:
        """
        Fy0,mu_y,alphay,By,Cy,Dy,Ey,SVy,SHy,SVygamma,Kyalpha,Kygamma_0 = Fy0_output
        alpha,kappa,gamma,Fz = alpha_kappa_gamma_Fz
        lambda_vykappa = 1
        lambda_ykappa = 1
        lambda_Fz0 = 1

        ##Vertical load
        Fz0 = lambda_Fz0*Fz0_ #Fz0 - Nominal load with scaling factor (4.E1)
        dfz = (Fz - Fz0)/(Fz0) #dfz0 - Normalised change in vertical load (4.E2)

        ##########################
        ##Magic Formula
        """
        Fy equation for combined mouvement:

        Fy = Fy0*Gykappa + SVykappa

        Gykappa = cos(Cykappa*arctan(Bykappa*alpha_s - Eykappa*(Bykappa*alpha_s - arctan(Bykappa*alpha_s))))/Gykappa_0

        """ 

        ##Bykappa
        gamma_star = np.sin(gamma) #(4.E4)
        alpha_star = np.tan(alpha) #(4.E3) obs: Vcx >0 (no backwards), so sign(Vcx) will be always 1
        Bykappa = (rby1 + rby4*gamma_star**2)*np.cos(np.arctan(rby2*(alpha_star - rby3)))*lambda_ykappa #(4.E62)

        ##Cykappa
        Cykappa = rcy1 #(4.E63)

        ##Eykappa
        Eykappa = rey1 + rey2*dfz #(4.E64)

        ##SHykappa
        SHykappa = rhy1 + rhy2*dfz #(4.E65)

        ##Dvykappa
        Dvykappa = mu_y*Fz*(rvy1 + rvy2*dfz + rvy3*gamma_star)*np.arctan(rvy4*alpha_star) #(4.E67)

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

        return Fy,SVykappa
    
    @staticmethod
    def Mz_combined(alpha_kappa_gamma_Fz,ssz1,ssz2,ssz3,ssz4,Fz0_,R0,Fx_output,Fy_output,Mz0_output,Fx0_output,Fy0_output):
        """
        This function will calculate Mz combined (lat and long) :
        """
        Fx, Bxalpha = Fx_output
        Fy,SVykappa = Fy_output
        Mz0,Mzr0,t0,alphat,Bt,Ct,Dt,Et,SHt,alphar,Br,Cr,Dr = Mz0_output
        Fx0,mux,kappax,Bx,Cx,Dx,Ex,SVx,SHx,Kxkappa = Fx0_output
        Fy0,mu_y,alphay,By,Cy,Dy,Ey,SVy,SHy,SVygamma,Kyalpha,Kygamma_0 = Fy0_output
        alpha,kappa,gamma,Fz = alpha_kappa_gamma_Fz
        lambda_s = 1
        lambda_Fz0 = 1


        ##########################
        ##Vertical load
        Fz0 = lambda_Fz0*Fz0_ #Fz0 - Nominal load with scaling factor (4.E1)
        dfz = (Fz - Fz0)/(Fz0) #dfz0 - Normalised change in vertical load (4.E2)

        ##########################
        #Magic Formula
        """
        Mz = -t*Fy_ + Mzr + s*Fx

        """

        ##Fy_
        Fy_ = Fy - SVykappa #(4.E74)
        
        ##t
        alpha_teq = (alphat**2 + (Kxkappa/Kyalpha)**2*kappa**2)**0.5*np.sign(alphat) #(4.E77)
        t = Dt*np.cos(Ct*np.arctan(Bt*alpha_teq - Et*(Bt*alpha_teq - np.arctan(Bt*alpha_teq)))) #(4.E73)

        ##Mzr
        alpha_req = (alphar**2 + (Kxkappa/Kyalpha)**2*kappa**2)**0.5 #(4.E78)
        Mzr = Dr*np.cos(Cr*np.arctan(Br*alpha_req)) #(4.E75)

        ##s
        gamma_star = np.sin(gamma) #(4.E4)
        s = (ssz1 + ssz2*(Fy/Fz0_) + (ssz3 + ssz4*dfz)*gamma_star)*R0*lambda_s #(4.E76)

        ##Mz
        Mz = -t*Fy_ + Mzr + s*Fx #(4.E71)

        return Mz,t,s
    
    @staticmethod
    def My_RR(Fz_Vx,Fz0_,R0,V0,Fx_output,qsy1,qsy2,qsy3,qsy4):
        """
        This function will calculate My rolling resistance torque :
        """
        Fz,Vx = Fz_Vx
        Fx, Gxalpha = Fx_output
        lambda_My = 1

        My = -Fz*R0*(qsy1 + qsy2*Fx/Fz0_ + qsy3*abs(Vx/V0) + qsy4*(Vx/V0)**4)*lambda_My #(11.E70)

        return [My]
    
    @staticmethod
    def Mx_overturning(gamma_Fz_Vx,Fz0_,R0,Fy_output,qsx1,qsx2,qsx3):
        """
        This function will calculate Mx overturning torque :
        """
        gamma,Fz,Vx = gamma_Fz_Vx
        Fy, Gyalpha = Fy_output
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
