import numpy as np

class pacejka:
    @staticmethod
    def FX_pure(alpha_kappa_gamma_FZ_VX,pcx1,pdx1,pdx2,pdx3,pex1,pex2,pex3,pex4,pkx1,pkx2,pkx3,phx1,phx2,pvx1,pvx2,FZ0,scaling_coefficients=None):

        """
        This function calculates the FX0 for a pure longitudinal situation:
        """

        _,kappa_input,gamma_input,FZ_input,_    =   alpha_kappa_gamma_FZ_VX #inputs for FX0 calculation
        #Scaling coefficients from tir file
        if scaling_coefficients != None: 
            lambda_Cx   =     scaling_coefficients.LCX
            lambda_FZ0  =     scaling_coefficients.LFZO
            lambda_mux  =     scaling_coefficients.LMUX
            lambda_Ex   =     scaling_coefficients.LEX
            lambda_Kx   =     scaling_coefficients.LKX
            lambda_Hx   =     scaling_coefficients.LHX
            lambda_VX   =     scaling_coefficients.LVX
        else:
            lambda_Cx  =    1
            lambda_FZ0 =    1 
            lambda_mux =    1
            lambda_Ex  =    1
            lambda_Kx  =    1
            lambda_Hx  =    1
            lambda_VX  =    1
        
        #No star correction:
        kappa   =   kappa_input
        gamma   =   gamma_input
        FZ      =   FZ_input

            
        #Epsilon is necessary to avoid division by 0
        epsilon = 0.001

        
        ##Vertical load
        FZ0_    =   lambda_FZ0*FZ0 #FZ0 - Nominal load with scaling factor (4.E1)
        dfz     =   (FZ - FZ0_)/(FZ0_) #dfz0 - Normalised change in vertical load (4.E2a)
        

        ##Magic Formula

        """
        FX equation for pure longitudinal:

        FX0 = Dx*sin(Cx*arctan(Bx*kappax - Ex*(Bx*kappax - arctan(Bx*kappax)))) + SVX  

        """

        ##Dx
        mux =   (pdx1 + pdx2*dfz)*(1-pdx3*gamma**2)*lambda_mux #(4.E13) But no pressure -> MF52
        Dx  =   mux*FZ #(4.E12)

        ##Cx 
        Cx  =   pcx1*lambda_Cx #(4.E12)

        ##Bx:
        Kx  =    FZ*(pkx1 + pkx2*dfz)*np.exp(pkx3*dfz)*lambda_Kx #(4.E15)
        Bx  =   Kx/(Cx*Dx + epsilon*np.where(Cx*Dx==0,1,0)) #(4.E16)

        ##kappax
        SHx =   (phx1 + phx2*dfz)*lambda_Hx #(4.E17)
        kappax  =   kappa + SHx #(4.E10)

        ##Ex
        Ex  =   (pex1 + pex2*dfz + pex3*dfz**2)*(1-pex4*np.sign(kappax))*lambda_Ex #(4.E14)

        #SVX
        SVX =   FZ*(pvx1 + pvx2*dfz)*lambda_VX*lambda_mux #(4.E18)

        #FX0
        FX0 =   Dx*np.sin(Cx*np.arctan(Bx*kappax - Ex*(Bx*kappax - np.arctan(Bx*kappax)))) + SVX #(4.E9)

        return FX0,mux,kappax,Bx,Cx,Dx,Ex,SVX,SHx,Kx
    
    @staticmethod
    def FY_pure(alpha_kappa_gamma_FZ_VX,pcy1,pdy1,pdy2,pdy3,pey1,pey2,pey3,pey4,pky1,pky2,pky3,
                          phy1,phy2,phy3,pvy1,pvy2,pvy3,pvy4,FZ0,star_correction=False,scaling_coefficients=None):

        """
        This function calculates the FY0 for a pure cornering situation:
        """

        alpha_input,_,gamma_input,FZ_input,_ = alpha_kappa_gamma_FZ_VX #inputs for FY0 calculation
        if scaling_coefficients != None:
            lambda_Cy   =   scaling_coefficients.LCY
            lambda_FZ0  =   scaling_coefficients.LFZO
            lambda_muy  =   scaling_coefficients.LMUY
            lambda_Ky   =   scaling_coefficients.LKY
            lambda_Hy   =   scaling_coefficients.LHY
            lambda_Vy   =   scaling_coefficients.LVY
            lambda_Ey   =   scaling_coefficients.LEY
        else:
            lambda_Cy   =   1
            lambda_FZ0  =   1
            lambda_muy  =   1
            lambda_Ky   =   1
            lambda_Hy   =   1
            lambda_Vy   =   1
            lambda_Ey   =   1


        #Epsilon is necessary to avoid division by 0
        epsilon = 0.001

        ##Star correction
        if star_correction == True:
            gamma   =   np.sin(gamma_input) #(4.E4)
            alpha   =   np.tan(alpha_input) #(4.E3) obs: Vcx >0 (no backwards), so sign(Vcx) will be always 1
            FZ      =   FZ_input
        else:
            gamma   =   gamma_input
            alpha   =   alpha_input
            FZ      =   FZ_input

        ##Vertical load
        FZ0_        =   lambda_FZ0*FZ0 #FZ0 - Nominal load with scaling factor (4.E1)
        dfz         =   (FZ - FZ0_)/(FZ0_) #dfz0 - Normalised change in vertical load (4.E2a)
        ##########################

        

        ##Magic Formula

        """
        FY equations for pure cornering movement:

        FY0 =  Dy*sin(Cy*arctan(By*alphay - Ey*(By*alphay - arctan(By*alphay)))) + SVy 

        """
        ##Dy
        mu_y    =   lambda_muy*(pdy1 + pdy2*dfz)*(1-pdy3*gamma**2) #(4.E23)
        Dy      =   mu_y*FZ #(4.E22)

        ##Cy
        Cy      =   pcy1*lambda_Cy #(4.E21)
    
        ##By
        pky4    =   2
        Ky      =   lambda_Ky*pky1*FZ0_*np.sin(pky4*np.arctan(FZ/(pky2*FZ0_)))*(1 - pky3*np.abs(gamma)) #(4.E25)
        #Kyalpha = Kyalpha + epsilon*np.where(Kyalpha==0,1,0)
        By      =   Ky/(Cy*Dy + epsilon*np.where(Cy*Dy==0,1,0))  #(4.E26)

        ##alphay
        SHy     =   (phy1 + phy2*dfz)*lambda_Hy +phy3*gamma #(4.E27)
        alphay  =   alpha + SHy #(4.E20)

        ##Ey
        Ey      =   (pey1 + pey2*dfz)*(1 -(pey3+pey4*gamma)*np.sign(alphay))*lambda_Ey #(4.E24)

        ##SVy
        SVy     =   FZ*((pvy1 + pvy2*dfz)*lambda_Vy + (pvy3 + pvy4*dfz)*gamma)*lambda_muy #(4.E29)

        ##FY0
        FY0     =   Dy*np.sin(Cy*np.arctan(By*alphay - Ey*(By*alphay - np.arctan(By*alphay)))) + SVy #(4.E19)

        return FY0,mu_y,alphay,By,Cy,Dy,Ey,SVy,SHy,Ky
    
    @staticmethod
    def MZ_pure(alpha_kappa_gamma_FZ_VX,qbz1,qbz2,qbz3,qbz4,qbz5,qbz9,qbz10,qcz1,qdz1,qdz2,qdz3,qdz4,qdz6,qdz7,qdz8,qdz9,
                qez1,qez2,qez3,qez4,qez5,
                qhz1,qhz2,qhz3,qhz4,
                FZ0,R0,FY0_output,star_correction=False,scaling_coefficients=None):
        

        """
        This function calculates the MZ0 for a pure cornering situation:
        """ 
        FY0,_,_,By,Cy,_,_,SVy,SHy,Ky                =   FY0_output #gamma should be 0 for this output
        alpha_input,_,gamma_input,FZ_input,VX_input =   alpha_kappa_gamma_FZ_VX

        if scaling_coefficients != None:
            lambda_t    =   scaling_coefficients.LTR
            lambda_FZ0  =   scaling_coefficients.LFZO
            lambda_Ky   =   scaling_coefficients.LKY
            lambda_Mr   =   scaling_coefficients.LRES
            lambda_muy  =   scaling_coefficients.LMUY
        else:
            lambda_t    =   1
            lambda_FZ0  =   1
            lambda_Ky   =   1
            lambda_Mr   =   1
            lambda_muy  =   1
        

        #Epsilon is necessary to avoid division by 0
        epsilon = 0.001


        ##Star correction
        if star_correction == True:
            gamma   =    np.sin(gamma_input) #(4.E4)
            alpha   =    np.tan(alpha_input) #(4.E3) obs: Vcx >0 (no backwards), so sign(Vcx) will be always 1
            FZ      =    FZ_input
            VX      =    VX_input
        else:
            gamma   =    gamma_input
            alpha   =    alpha_input
            FZ      =    FZ_input
            VX      =    VX_input

        ##Vertical load
        FZ0_        =    lambda_FZ0*FZ0 #FZ0 - Nominal load with scaling factor (4.E1)
        dfz         =    (FZ - FZ0_)/(FZ0_) #dfz0 - Normalised change in vertical load (4.E2a)
        ##########################

        


        ##########################
        ##Magic Formula
        """
        MZ equations for pure cornering movement:

        t0 = Dt*np.cos(Ct*np.arctan(Bt*alphat - Et*(Bt*alphat - np.arctan(Bt*alphat))))

        MZr = Dr*cos(Cr*arctan(Br*alphar))

        MZ0 = -t*FY0 + MZr

        """

        ##Dt
        Dt0         =    FZ*(R0/FZ0_)*(qdz1 + qdz2*dfz)*lambda_t #(4.E42)
        Dt          =    Dt0*(1+qdz3*gamma + qdz4*gamma**2) #(4.E43)

        ##Ct
        Ct          =     qcz1 #(4.E41)

        ##Bt
        Bt          =    (qbz1 + qbz2*dfz + qbz3*dfz**2)*(1+qbz5*abs(gamma) + qbz4*gamma)*lambda_Ky/lambda_muy #(4.E40)

        ##alphat
        SHt         =    qhz1 + qhz2*dfz + (qhz3 + qhz4*dfz)*gamma #(4.E35)
        alphat      =    alpha + SHt #(4.E34)

        ##Et
        Et          =    (qez1 + qez2*dfz + qez3*dfz**2)*(1 + (qez4 + qez5*gamma)*(2/np.pi)*np.arctan(Bt*Ct*alphat)) #(4.E44)

        ##t0
        #cos'alpha = Vcx/Vc (Vcx = VX)
        Vcx         =    VX
        Vsy         =    np.tan(alpha_input)*Vcx
        Vcy         =    Vsy
        Vc          =    (Vcy**2 + Vcx**2)**0.5

        t0          =    Dt*np.cos(Ct*np.arctan(Bt*alphat - Et*(Bt*alphat - np.arctan(Bt*alphat))))*(Vcx/Vc) #(4.E33)
        #t0 = Dt*np.cos(Ct*np.arctan(Bt*alphat - Et*(Bt*alphat - np.arctan(Bt*alphat))))*np.cos(alpha)
        #t0 =  Dt*np.cos(Ct*np.arctan(Bt*alphat - Et*(Bt*alphat - np.arctan(Bt*alphat))))*(1-(alpha**2)/2) #(4.E33) aproximmation to improve fit performance

        ##Dr
        Dr          =    FZ*R0*((qdz6 + qdz7*dfz)*lambda_Mr + (qdz8 + qdz9*dfz)*gamma)*(Vcx/Vc)#(4.E47)

        ##Cr
        Cr          =    1 #(4.E46)

        ##Br
        Br          =    (qbz9*lambda_Ky/lambda_muy + qbz10*By*Cy)

        ##alphar
        SHr         =    SHy + SVy/(Ky + epsilon*np.where(Ky==0,1,0)) #(4.E38)
        alphar      =    alpha + SHr #(4.E37)

        ##MZr
        MZr0        =    Dr*np.cos(Cr*np.arctan(Br*alphar))*(Vcx/Vc) #(4.E36)

        ##MZ0

        MZ0         =    -t0*FY0 + MZr0 #(4.E31 and 4.E32)

        return MZ0,MZr0,t0,alphat,Bt,Ct,Dt,Et,SHt,alphar,Br,Cr,Dr
    
    @staticmethod
    def FX_combined(alpha_kappa_gamma_FZ_VX,rbx1,rbx2,rcx1,rex1,rex2,rhx1,FZ0,FX0_output,star_correction=False,scaling_coefficients=None):

        """
        This function calculates the FX for a combined slip situation:
        """

        alpha_input,kappa_input,_,FZ_input,_ = alpha_kappa_gamma_FZ_VX
        FX0,_,_,_,_,_,_,_,_,_   =    FX0_output

        if scaling_coefficients != None:
            lambda_xalpha   =   scaling_coefficients.LXAL
            lambda_FZ0      =   scaling_coefficients.LFZO
        else:
            lambda_xalpha   =   1
            lambda_FZ0      =   1

        ##Star correction
        if star_correction == True:
            alpha   =    np.tan(alpha_input) #(4.E3) obs: Vcx >0 (no backwards), so sign(Vcx) will be always 1
            FZ      =    FZ_input
            kappa   =    kappa_input
        else:
            alpha   =    alpha_input
            FZ      =    FZ_input
            kappa   =    kappa_input

        ##Vertical load
        FZ0_ = lambda_FZ0*FZ0 #FZ0 - Nominal load with scaling factor (4.E1)
        dfz = (FZ - FZ0_)/(FZ0_) #dfz0 - Normalised change in vertical load (4.E2a)
        ##########################

        ##########################
        ##Magic Formula
        """
        FX equation for combined movement:

        FX = FX0*Gxalpha 

        Gxalpha = cos(Cxalpha*arctan(Bxalpha*alpha_s - Exalpha*(Bxalpha*alpha_s - arctan(Bxalpha*alpha_s))))/Gxalpha_0

        """ 

        ##Bxalpha
        Bxalpha     =    rbx1*np.cos(np.arctan(rbx2*kappa))*lambda_xalpha #(4.E54)

        ##Cxalpha
        Cxalpha     =    rcx1 #(4.E55)

        ##Exalpha
        Exalpha     =    rex1 + rex2*dfz #(4.E56)

        ##SHxalpha
        SHxalpha    =    rhx1 #(4.E57)

        #alphas
        alphas      =    alpha + SHxalpha #(4.E53) 

        ##Gxalpha_0
        Gxalpha_0   =    np.cos(Cxalpha*np.arctan(Bxalpha*SHxalpha - Exalpha*(Bxalpha*SHxalpha - np.arctan(Bxalpha*SHxalpha )))) #(4.E52) 
        
        ##Gxalpha
        Gxalpha     =    np.cos(Cxalpha*np.arctan(Bxalpha*alphas - Exalpha*(Bxalpha*alphas - np.arctan(Bxalpha*alphas))))/Gxalpha_0 #(4.E51) 

        ##FX
        FX          =    FX0*Gxalpha #(4.E50) 

        return FX, Gxalpha
    
    @staticmethod
    def FY_combined(alpha_kappa_gamma_FZ_VX,rby1,rby2,rby3,rcy1,rey1,rey2,rhy1,rhy2,
                    rvy1,rvy2,rvy3,rvy4,rvy5,rvy6,FZ0,FY0_output,star_correction=False,scaling_coefficients=None):
        """
        This function calculates the FY for a combined (lat and long) situation:
        """
        FY0,mu_y,_,_,_,_,_,_,_,_    =    FY0_output

        alpha_input,kappa_input,gamma_input,FZ_input,_  =    alpha_kappa_gamma_FZ_VX

        if scaling_coefficients != None:
            lambda_vykappa  =    scaling_coefficients.LVYKA
            lambda_ykappa   =    scaling_coefficients.LYKA
            lambda_FZ0      =    scaling_coefficients.LFZO

        else:
            lambda_vykappa  =    1
            lambda_ykappa   =    1
            lambda_FZ0      =    1
        

        ##Star correction
        if star_correction == True:
            gamma   =    np.sin(gamma_input)
            alpha   =    np.tan(alpha_input) #(4.E3) obs: Vcx >0 (no backwards), so sign(Vcx) will be always 1
            FZ      =    FZ_input
            kappa   =    kappa_input
        else:
            gamma   = gamma_input
            alpha   = alpha_input
            FZ      = FZ_input
            kappa   = kappa_input

        ##Vertical load
        FZ0_        = lambda_FZ0*FZ0 #FZ0 - Nominal load with scaling factor (4.E1)
        dfz         = (FZ - FZ0_)/(FZ0_) #dfz0 - Normalised change in vertical load (4.E2a)
        ##########################

        ##########################
        ##Magic Formula
        """
        FY equation for combined movement:

        FY = FY0*Gykappa + SVykappa

        Gykappa = cos(Cykappa*arctan(Bykappa*alpha_s - Eykappa*(Bykappa*alpha_s - arctan(Bykappa*alpha_s))))/Gykappa_0

        """ 

        ##Bykappa
        Bykappa     =    rby1*np.cos(np.arctan(rby2*(alpha - rby3)))*lambda_ykappa #(4.E62)

        ##Cykappa
        Cykappa     =    rcy1 #(4.E63)

        ##Eykappa
        Eykappa     =    rey1 + rey2*dfz #(4.E64)

        ##SHykappa
        SHykappa    =    rhy1 + rhy2*dfz #(4.E65)

        ##Dvykappa
        Dvykappa    =    mu_y*FZ*(rvy1 + rvy2*dfz + rvy3*gamma)*np.cos(np.arctan(rvy4*alpha)) #(4.E67)

        ##SVykappa
        SVykappa    =    Dvykappa*np.sin(rvy5*np.arctan(rvy6*kappa))*lambda_vykappa #(4.E66)

        ##kappa_s
        kappa_s     =    kappa + SHykappa #(4.E61)

        ##Gykappa_0
        Gykappa_0   =    np.cos(Cykappa*np.arctan(Bykappa*SHykappa - Eykappa*(Bykappa*SHykappa - np.arctan(Bykappa*SHykappa )))) #(4.E60) 
        
        ##Gykappa
        Gykappa     =    np.cos(Cykappa*np.arctan(Bykappa*kappa_s - Eykappa*(Bykappa*kappa_s - np.arctan(Bykappa*kappa_s))))/Gykappa_0 #(4.E59) 

        ##FY
        FY          =    FY0*Gykappa + SVykappa #(4.E58)

        return FY,Gykappa,SVykappa
    
    @staticmethod
    def MZ_combined(alpha_kappa_gamma_FZ_VX,ssz1,ssz2,ssz3,ssz4,FZ0,R0,FX_output,FY_output,MZ0_output,FX0_output,FY0_output,star_correction=False,scaling_coefficients=None):
        """
        This function calculates MZ combined (lat and long) :
        """
        FX, _           =    FX_output
        FY,_,SVykappa   =    FY_output
        _,_,_,alphat,Bt,Ct,Dt,Et,_,alphar,Br,Cr,Dr =    MZ0_output
        _,_,_,_,_,_,_,_,_,Kx    =    FX0_output
        _,_,_,_,_,_,_,_,_,Ky    =    FY0_output
        alpha_input,kappa_input,gamma_input,FZ_input,VX_input   =    alpha_kappa_gamma_FZ_VX

        if scaling_coefficients != None:
            lambda_s    =    scaling_coefficients.LS
            lambda_FZ0  =    scaling_coefficients.LFZO
        else:
            lambda_s    =    1
            lambda_FZ0  =    1
        

        ##Star correction
        if star_correction == True:
            gamma   =    np.sin(gamma_input)
            alpha   =    np.tan(alpha_input) #(4.E3) obs: Vcx >0 (no backwards), so sign(Vcx) will be always 1
            FZ  =    FZ_input
            kappa   =    kappa_input
            VX  =    VX_input
        else:
            gamma   =    gamma_input
            alpha   =    alpha_input
            FZ      =    FZ_input
            kappa   =    kappa_input
            VX      =    VX_input

        #Epsilon is necessary to avoid division by 0
        epsilon     =    0.001

        ##########################
        ##Vertical load
        FZ0_    =    lambda_FZ0*FZ0 #FZ0 - Nominal load with scaling factor (4.E1)
        dfz     =    (FZ - FZ0_)/(FZ0_) #dfz0 - Normalised change in vertical load (4.E2a)

        ##########################
        #Magic Formula
        """
        MZ = -t*FY_ + MZr + s*FX

        """

        ##FY_
        FY_     =    FY - SVykappa #(4.E74) = Gykappa*FY0 (gamma should be 0)
        
        ##t
        #cos'alpha = Vcx/Vc (Vcx = VX)
        Vcx     =    VX
        Vsy     =    np.tan(alpha_input)*Vcx
        Vcy     =    Vsy
        Vc      =    (Vcy**2 + Vcx**2)**0.5
        alpha_teq   =    (alphat**2 + (Kx/(Ky + epsilon*np.where(Ky==0,1,0) ))**2*kappa**2)**0.5*np.sign(alphat) #(4.E77)
        t   =    Dt*np.cos(Ct*np.arctan(Bt*alpha_teq - Et*(Bt*alpha_teq - np.arctan(Bt*alpha_teq))))*(Vcx/Vc) #(4.E73)

        ##MZr
        alpha_req   =    (alphar**2 + (Kx/(Ky + epsilon*np.where(Ky==0,1,0) ))**2*kappa**2)**0.5 #(4.E78)
        MZr     =    Dr*np.cos(Cr*np.arctan(Br*alpha_req)) #(4.E75)

        ##s
        s   =    (ssz1 + ssz2*(FY/FZ0) + (ssz3 + ssz4*dfz)*gamma)*R0*lambda_s #(4.E76)

        ##MZ
        MZ  =    -t*FY_ + MZr + s*FX #(4.E71)

        return MZ,t,s,MZr
    
    @staticmethod
    def MX_overturning(gamma_FZ_VX,qsx1,qsx2,qsx3,FZ0,R0,FY_output,scaling_coefficients=None):
        """
        This function calculates MX overturning torque :
        """
        
        gamma,FZ,_  =    gamma_FZ_VX
        FY,_,_      =    FY_output
        if scaling_coefficients != None:
            lambda_MX       =    scaling_coefficients.LMX
            lambda_FZ0      =   scaling_coefficients.LFZO
        else:
            lambda_MX       =    1
            lambda_FZ0      =   1

        ##Vertical load
        FZ0_ = lambda_FZ0*FZ0 #FZ0 - Nominal load with scaling factor (4.E1)

        MX          =    FZ*R0*(qsx1 - qsx2*gamma + qsx3*FY/FZ0_)*lambda_MX #(4.E69)

        return [MX]

    @staticmethod
    def MY_RR(FZ_VX,qsy1,qsy2,qsy3,qsy4,FZ0,R0,V0,FX_output,scaling_coefficients=None):
        """
        This function calculates MY rolling resistance torque :
        """
        FZ,VX   =    FZ_VX
        FX,_    =    FX_output
        if scaling_coefficients != None:
            lambda_MY       =    scaling_coefficients.LMY
            lambda_FZ0      =    scaling_coefficients.LFZO

        lambda_MY       =    1
        lambda_FZ0      =    1

        ##Vertical load
        FZ0_    =    lambda_FZ0*FZ0 #FZ0 - Nominal load with scaling factor (4.E1)

        MY      =    -FZ*R0*(qsy1 + qsy2*FX/FZ0_ + qsy3*abs(VX/V0) + qsy4*(VX/V0)**4)*lambda_MY #(11.E70)

        return [MY]
        
    @staticmethod
    def Radius(FZ_VX,Cz,B,D,F,FZ0_,R0):
        """
    This function calculates the deflection, the effective rolling radius and the omega (rotational speed of the tire):
    """
        FZ,VX   =    FZ_VX
        rho     =    FZ/Cz
        rho_FZ0 =    FZ0_/Cz
        rho_d   =    rho/rho_FZ0

        Re      =    R0 - rho_FZ0*(D*np.arctan(B*rho_d) + F*rho_d)

        omega       = VX/Re

        return Re,rho,omega
