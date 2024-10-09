import numpy as np

class PreProcessing:
    def read_tir(tir_file):
        headers = {}
        current_header = None
        try:   
            with open(tir_file, 'r') as file:
                data = file.readlines()

            for line in data:
                line = line.strip()
                if line.startswith('$--'):
                    continue
                if line.startswith('[') and line.endswith(']'):
                    current_header = line[1:-1]
                    headers[current_header] = {}
                else:
                        if line.startswith('!') or line.startswith("'") or line.startswith("{"):
                            continue
                        if '$' in line and not line.startswith('$'):
                            key_value,comment = line.split('$',1)
                            key, value = key_value.split('=')
                            headers[current_header][key.strip()] = value.strip()
                        elif '=' in line:
                            key, value = line.split('=')
                            headers[current_header][key.strip()] = value.strip()
        
            for h in headers.keys():
                for key in headers[h].keys():
                    try:
                        headers[h][key] = float(headers[h][key])
                    except:
                        continue
            headers = headers
            return headers
        except Exception as e:
            print('Error reading the .tir file')
            raise

    @staticmethod
    def check_coeff(headers):
        headers_checked = headers
        ##keys:
        model_keys = ['VXLOW']

        dimension_keys = ['UNLOADED_RADIUS']

        long_slip_keys = ['KPUMIN','KPUMAX']

        slip_angle_keys = ['ALPMIN','ALPMAX']

        inclination_angle_keys = ['CAMMIN','CAMMAX']

        vertical_force_keys = ['FZMIN','FZMAX']

        vertical_keys = ['FNOMIN','VERTICAL_STIFFNESS','VERTICAL_DAMPING','BREFF','DREFF','FREFF']

        scaling_keys = ['LCX','LFZO','LGAX','LKX','LHX','LVX','LEX',
                        'LCY','LGAY','LKY','LHY','LVY','LEY','LTR',
                        'LRES','LKZC','LXAL','LVYKA','LYKA','LS','LMY','LMX'] 
        
        longitudinal_keys = ['PCX1','PDX1','PDX2','PEX1','PEX2','PEX3','PEX4',
                             'PKX1','PKX2','PKX3','PHX1','PHX2','PVX1','PVX2',
                            'RBX1','RBX2','RBX3','RCX1','REX1','REX2','RHX1']
        
        lateral_keys = ['PCY1','PDY1','PDY2','PDY3','PEY1','PEY2','PEY3','PEY4','PEY5','PKY1','PKY2','PKY3','PKY4','PKY5','PKY6','PKY7',
                        'PHY1','PHY2','PVY1','PVY2','PVY3','PVY4',
                        'RBY1','RBY2','RBY3','RBY4','RCY1','REY1','REY2','RHY1','RHY2','RVY1','RVY2','RVY3','RVY4','RVY5','RVY6']
        
        aligning_keys = ['QDZ1','QDZ2','QDZ3','QDZ4','QDZ6','QDZ7',
                        'QDZ8','QDZ9','QDZ10','QDZ11','QCZ1','QBZ1','QBZ2',
                        'QBZ3','QBZ5','QBZ9','QBZ10','QHZ1','QHZ2','QHZ3',
                        'QHZ4','QEZ1','QEZ2','QEZ3','QEZ4','QEZ5','SSZ1','SSZ2','SSZ3','SSZ4']
        
        overturning_keys = ['QSX1','QSX2','QSX3']
        
        rolling_keys = ['QSY1','QSY2','QSY3']

        if model_keys[0] not in headers['MODEL']:
            print('Speed. {}  does not exist. It will replaced by 10 m/s'.format(model_keys[0]))
            headers_checked['MODEL'][i] = 10

        if dimension_keys[0] not in headers['DIMENSION']:
            print('Unloaded radius. {}  does not exist. It will replaced by 0.3 m'.format(dimension_keys[0]))
            headers_checked['MODEL'][i] = 10
        
        if long_slip_keys[0] not in headers['LONG_SLIP_RANGE']:
            print('Slip ratio min. {}  does not exist. It will replaced by -1'.format(long_slip_keys[0]))
            headers_checked['MODEL'][i] = -1
        if long_slip_keys[1] not in headers['LONG_SLIP_RANGE']:
            print('Slip ratio max. {}  does not exist. It will replaced by 1'.format(long_slip_keys[1]))
            headers_checked['MODEL'][i] = 1

        if slip_angle_keys[0] not in headers['SLIP_ANGLE_RANGE']:
            print('Slip angle min. {}  does not exist. It will replaced by -0.5'.format(slip_angle_keys[0]))
            headers_checked['MODEL'][i] = -0.5
        if slip_angle_keys[1] not in headers['SLIP_ANGLE_RANGE']:
            print('Slip angle max. {}  does not exist. It will replaced by 0.5'.format(slip_angle_keys[1]))
            headers_checked['MODEL'][i] = 0.5
        
        if inclination_angle_keys[0] not in headers['INCLINATION_ANGLE_RANGE']:
            print('Inclination angle min. {}  does not exist. It will replaced by -0.5'.format(inclination_angle_keys[0]))
            headers_checked['MODEL'][i] = -0.5
        if inclination_angle_keys[1] not in headers['INCLINATION_ANGLE_RANGE']:
            print('Inclination angle max. {}  does not exist. It will replaced by 0.5'.format(inclination_angle_keys[1]))
            headers_checked['MODEL'][i] = 0.5

        if vertical_force_keys[0] not in headers['VERTICAL_FORCE_RANGE']:
            print('Fz min. {}  does not exist. It will replaced by 10 N'.format(inclination_angle_keys[0]))
            headers_checked['MODEL'][i] = 10
        if vertical_force_keys[1] not in headers['VERTICAL_FORCE_RANGE']:
            print('Fz max. {}  does not exist. It will replaced by 10000N'.format(inclination_angle_keys[1]))
            headers_checked['MODEL'][i] = 10000
        
        if vertical_keys[0] not in headers['VERTICAL']:
            print('Nonimal load. {}  does not exist. It will replaced by 5000 N'.format(vertical_keys[0]))
            headers_checked['MODEL'][i] = 5000
        if vertical_keys[1] not in headers['VERTICAL']:
            print('Vertical stifness. {}  does not exist. It will replaced by 300000'.format(vertical_keys[1]))
            headers_checked['MODEL'][i] = 300000
        if vertical_keys[2] not in headers['VERTICAL']:
            print('Vertical damping. {}  does not exist. It will replaced by 50'.format(vertical_keys[2]))
            headers_checked['MODEL'][i] = 50
        if vertical_keys[3] not in headers['VERTICAL']:
            print('BREFF. {}  does not exist. It will replaced by 10'.format(vertical_keys[3]))
            headers_checked['MODEL'][i] = 10
        if vertical_keys[4] not in headers['VERTICAL']:
            print('DREFF. {}  does not exist. It will replaced by 0.3'.format(vertical_keys[4]))
            headers_checked['MODEL'][i] = 0.3
        if vertical_keys[5] not in headers['VERTICAL']:
            print('FREFF. {}  does not exist. It will replaced by 0.1'.format(vertical_keys[5]))
            headers_checked['MODEL'][i] = 0.1

        for i in scaling_keys:
            if i not in headers['SCALING_COEFFICIENTS']:
                print('scalling coef. {}  does not exist. It will replaced by 1'.format(i))
                headers_checked['SCALING_COEFFICIENTS'][i] = 1         

        for i in longitudinal_keys:
            if i not in headers['LONGITUDINAL_COEFFICIENTS']:
                print('longitudinal coef. {} does not exist. It will replaced by 0'.format(i))
                headers_checked['LONGITUDINAL_COEFFICIENTS'][i] = 0      

        for i in lateral_keys:
            if i not in headers['LATERAL_COEFFICIENTS']:
                if i == 'PKY4':
                    print('lateral coef. {} does not exist. It will replaced by 2'.format(i))
                    headers_checked['LATERAL_COEFFICIENTS'][i] = 2
                else:
                    print('lateral coef. {} does not exist. It will replaced by 0'.format(i))
                    headers_checked['LATERAL_COEFFICIENTS'][i] = 0

        for i in aligning_keys:
            if i not in headers['ALIGNING_COEFFICIENTS']:
                print('aligning coef. {} not exist. It will replaced by 0'.format(i))
                headers_checked['ALIGNING_COEFFICIENTS'][i] = 0

        for i in overturning_keys:
            if i not in headers['OVERTURNING_COEFFICIENTS']:
                print('aligning coef. {} not exist. It will replaced by 0'.format(i))
                headers_checked['OVERTURNING_COEFFICIENTS'][i] = 0
             
        for i in rolling_keys:
            if i not in headers['ROLLING_COEFFICIENTS']:
                print('aligning coef. {} not exist. It will replaced by 0'.format(i))
                headers_checked['ROLLING_COEFFICIENTS'][i] = 0               
        return headers_checked

    @staticmethod
    def check_input_size(input):
        input_array = [np.array(i) if isinstance(i,(list)) else np.array([i]) for i in input]
        first_len = input_array[0].size
        if all(element.size == first_len for element in input_array) == False:
            raise ValueError('Inputs with differents sizes.')

    @staticmethod
    def check_limits(headers,input):

        Fz_max,Fz_min = headers['VERTICAL_FORCE_RANGE']['FZMAX'],headers['VERTICAL_FORCE_RANGE']['FZMIN']
        alpha_max,alpha_min = headers['SLIP_ANGLE_RANGE']['ALPMAX'],headers['SLIP_ANGLE_RANGE']['ALPMIN']
        kappa_max,kappa_min = headers['LONG_SLIP_RANGE']['KPUMAX'],headers['LONG_SLIP_RANGE']['KPUMIN']
        gamma_max,gamma_min = headers['INCLINATION_ANGLE_RANGE']['CAMMAX'],headers['INCLINATION_ANGLE_RANGE']['CAMMIN']

        input_lim = input.copy()

        lim_list = [[alpha_max,alpha_min],[kappa_max,kappa_min],[gamma_max,gamma_min],[Fz_max,Fz_min]]
        name = ['alpha','kappa','gamma','Fz']
        for i in range(4):
            if isinstance(input_lim[i],(int,float)):
                if input_lim[i] < lim_list[i][1]:
                    print('The {} input is outside the range value. The result will be saturated'.format(name[i]))
                    input_lim[i] = lim_list[i][1]
                elif input_lim[i] > lim_list[i][1]:
                    print('The {} input is outside the range value. The result will be saturated'.format(name[i]))
                    input_lim[i] = lim_list[i][0]
            elif isinstance(input_lim[i],(list,np.ndarray)):
                input_lim[i] = np.array(input_lim[i])
                if np.all((lim_list[i][1] < input[i]) & (lim_list[i][0] > input[i])) == False:
                    print('The {} input is outside the range value. The result will be saturated'.format(name[i]))
                input_lim[i][input_lim[i] < lim_list[i][1]] = lim_list[i][1]
                input_lim[i][input_lim[i] > lim_list[i][0]] = lim_list[i][0]
            else:
                raise TypeError("Inputs should be list, np.ndarray, float or int")
        return input_lim
    
    @staticmethod
    def creating_coefs(headers):
        nominal = {'V0':headers['MODEL']['LONGVL'],'FZ0':headers['VERTICAL']['FNOMIN'],'R0':headers['DIMENSION']['UNLOADED_RADIUS']}

        Radius_keys = ['VERTICAL_STIFFNESS','BREFF','DREFF','FREFF']
        Radius_values = [headers['VERTICAL'][key] for key in Radius_keys]


        Fx_pure_keys = ['PCX1','PDX1','PDX2','PEX1','PEX2','PEX3','PEX4','PKX1','PKX2','PKX3','PHX1','PHX2','PVX1','PVX2']
        Fx_pure_values = [headers['LONGITUDINAL_COEFFICIENTS'][key] for key in Fx_pure_keys]


        Fy_pure_keys = ['PCY1','PDY1','PDY2','PDY3','PEY1','PEY2','PEY3','PEY4','PEY5','PKY1','PKY2','PKY3','PKY4','PKY5','PKY6','PKY7',
                        'PHY1','PHY2','PVY1','PVY2','PVY3','PVY4']
        Fy_pure_values = [headers['LATERAL_COEFFICIENTS'][key] for key in Fy_pure_keys]

        Mz_pure_keys = ['QBZ1','QBZ2','QBZ3','QBZ4','QBZ5','QBZ9','QBZ10','QCZ1','QDZ1','QDZ2','QDZ3','QDZ4','QDZ6','QDZ7','QDZ8','QDZ9','QDZ10','QDZ11',
                        'QEZ1','QEZ2','QEZ3','QEZ4','QEZ5','QHZ1','QHZ2','QHZ3','QHZ4']
        Mz_pure_values = [headers['ALIGNING_COEFFICIENTS'][key] for key in Mz_pure_keys]

        Fx_combined_keys = ['RBX1','RBX2','RBX3','RCX1','REX1','REX2','RHX1']
        Fx_combined_values = [headers['LONGITUDINAL_COEFFICIENTS'][key] for key in Fx_combined_keys]

        Fy_combined_keys = ['RBY1','RBY2','RBY3','RBY4','RCY1','REY1','REY2','RHY1','RHY2','RVY1','RVY2','RVY3','RVY4','RVY5','RVY6']
        Fy_combined_values = [headers['LATERAL_COEFFICIENTS'][key] for key in Fy_combined_keys]

        Mz_combined_keys = ['SSZ1','SSZ2','SSZ3','SSZ4']
        Mz_combined_values = [headers['ALIGNING_COEFFICIENTS'][key] for key in Mz_combined_keys]

        My_keys = ['QSY1','QSY2','QSY3','QSY4']
        My_values = [headers['ROLLING_COEFFICIENTS'][key] for key in My_keys]

        Mx_keys = ['QSX1','QSX2','QSX3']
        Mx_values = [headers['OVERTURNING_COEFFICIENTS'][key] for key in Mx_keys]
        
        return nominal,Radius_values,Fx_pure_values,Fy_pure_values,Mz_pure_values,Fx_combined_values,Fy_combined_values,Mz_combined_values,My_values,Mx_values

    def write_tir(tir_file, headers):
        try:
            with open(tir_file, 'w') as file:
                for header, values in headers.items():
                    file.write('$---------------------------------------------------------------------'+header+'\n')
                    file.write(f'[{header}]\n')
                    for key, value in values.items():
                        if isinstance(value, float):
                            file.write(f'{key} = {value}\n')
                        else:
                            file.write(f'{key} = {value}\n')
        except Exception as e:
            print('Error writing the .tir file')
            raise
