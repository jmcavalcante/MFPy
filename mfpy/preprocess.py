from collections import namedtuple

class preprocessing:
    def __MF52_structure52():
        MF52 = namedtuple('MF52',['MDI_HEADER','UNITS','MODEL','DIMENSION','VERTICAL','LONG_SLIP_RANGE',
                                  'SLIP_ANGLE_RANGE','INCLINATION_ANGLE_RANGE','VERTICAL_FORCE_RANGE',
                                  'SCALING_COEFFICIENTS','LONGITUDINAL_COEFFICIENTS','LATERAL_COEFFICIENTS',
                                  'OVERTURNING_COEFFICIENTS','ROLLING_COEFFICIENTS','ALIGNING_COEFFICIENTS'])
        
        mdi_header = namedtuple('mdi_header',('FILE_TYPE','FILE_VERSION','FILE_FORMAT'))
        units = namedtuple('units',['LENGTH','FORCE','ANGLE','MASS','TIME'])
        model = namedtuple('model',['FITTYP','USE_MODE','VXLOW','LONGVL','TYRESIDE'])
        dimension = namedtuple('dimension',['UNLOADED_RADIUS','WIDTH','ASPECT_RATIO','RIM_RADIUS','RIM_WIDTH'])
        vertical = namedtuple('vertical',['FNOMIN','VERTICAL_STIFFNESS','VERTICAL_DAMPING','BREFF','DREFF','FREFF'])
        long_slip_range = namedtuple('long_slip_range',['KPUMIN','KPUMAX'])
        slip_angle_range = namedtuple('slip_angle_range',['ALPMIN','ALPMAX'])
        inclination_angle_range = namedtuple('inclination_angle_range',['CAMMIN','CAMMAX'])
        vertical_force_range = namedtuple('vertical_force_range',['FZMIN','FZMAX'])
        scaling_coeficients = namedtuple('scaling_coeficients',['LFZO','LCX','LMUX','LEX','LKX','LHX','LVX','LGAX',
                                'LCY','LMUY','LEY','LKY','LHY','LVY','LGAY','LTR','LRES','LGAZ','LMX','LVMX',
                                'LMY','LXAL','LYKA','LVYKA','LS'])
        longitudinal_coeficients = namedtuple('longitudinal_coeficients',['PCX1','PDX1','PDX2','PDX3','PEX1',
                            'PEX2','PEX3','PEX4','PKX1','PKX2','PKX3','PHX1','PHX2','PVX1','PVX2','RBX1','RBX2',
                            'RCX1','REX1','REX2','RHX1'])
        lateral_coeficients = namedtuple('lateral_coeficients',['PCY1','PDY1','PDY2','PDY3','PEY1','PEY2','PEY3',
                            'PEY4','PKY1','PKY2','PKY3','PHY1','PHY2','PHY3','PVY1','PVY2','PVY3','PVY4','RBY1','RBY2',
                            'RBY3','RCY1','REY1','REY2','RHY1','RHY2','RVY1','RVY2','RVY3','RVY4','RVY5','RVY6'])
        aligning_coeficients = namedtuple('aligning_coeficients',['QBZ1','QBZ2','QBZ3','QBZ4','QBZ5','QBZ9','QBZ10','QCZ1','QDZ1','QDZ2','QDZ3','QDZ4','QDZ6','QDZ7',
                        'QDZ8','QDZ9','QEZ1','QEZ2','QEZ3','QEZ4','QEZ5','QHZ1','QHZ2','QHZ3','QHZ4',
                        'SSZ1','SSZ2','SSZ3','SSZ4'])
        rolling_coeficients = namedtuple('rolling_coeficients',['QSY1','QSY2','QSY3','QSY4'])
        overtuning_coeficients = namedtuple('overtuning_coeficients',['QSX1','QSX2','QSX3'])

        mf_52 = MF52(MDI_HEADER=mdi_header(*[None] * len(mdi_header._fields)),
                     UNITS=units(*[None] * len(units._fields)),
                     MODEL=model(*[None] * len(model._fields)),
                     DIMENSION=dimension(*[None] * len(dimension._fields)),
                     VERTICAL=vertical(*[None] * len(vertical._fields)),
                     LONG_SLIP_RANGE=long_slip_range(*[None] * len(long_slip_range._fields)),
                     SLIP_ANGLE_RANGE=slip_angle_range(*[None] * len(slip_angle_range._fields)),
                     INCLINATION_ANGLE_RANGE=inclination_angle_range(*[None] * len(inclination_angle_range._fields)),
                     VERTICAL_FORCE_RANGE=vertical_force_range(*[None] * len(vertical_force_range._fields)),
                     SCALING_COEFFICIENTS=scaling_coeficients(*[None] * len(scaling_coeficients._fields)),
                     LONGITUDINAL_COEFFICIENTS=longitudinal_coeficients(*[None] * len(longitudinal_coeficients._fields)),
                     LATERAL_COEFFICIENTS=lateral_coeficients(*[None] * len(lateral_coeficients._fields)),
                     ALIGNING_COEFFICIENTS=aligning_coeficients(*[None] * len(aligning_coeficients._fields)),
                     ROLLING_COEFFICIENTS=rolling_coeficients(*[None] * len(rolling_coeficients._fields)),
                     OVERTURNING_COEFFICIENTS=overtuning_coeficients(*[None] * len(overtuning_coeficients._fields))
                     )
        return mf_52

    def __dict_namedtuple_structure(namedtuple_structure, data):
        #Creating namedTuple with a dict (came from tir) using the correct structure (MF version)
        filled_data = {}
        for field in namedtuple_structure._fields:
            if field in data:
                value = data[field]
                if isinstance(value, dict) and hasattr(namedtuple_structure, field):
                    # Se o valor for um dicionário, cria uma estrutura aninhada
                    nested_namedtuple_class = getattr(namedtuple_structure, field)
                    filled_data[field] = preprocessing.__dict_namedtuple_structure(nested_namedtuple_class, value)
                else:
                    filled_data[field] = value
            else:
                filled_data[field] = None
        return namedtuple_structure.__class__(**filled_data)
    
    def __has_none(nt):
        # Search for Nones in the namedTuple
        if isinstance(nt, tuple) and hasattr(nt, '_fields'):
            for field in nt._fields:
                value = getattr(nt, field)
                if value is None:
                    return True
                if preprocessing.__has_none(value):
                    return True
        return False
    @staticmethod
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
                            key_value,_ = line.split('$',1)
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
            #HEADERS -> DICT from .tir file
            #Check the version MF
            if headers['MODEL']['FITTYP'] != 6:
                print('Incompatible version (not 5.2). If not all the coefficients are present, it will not be possible to perform the calculation; if they have extra coefficients, they will not be counted.')
            mf52 = preprocessing.__MF52_structure52() #mf52 structure
            #Dict to namedTuple:
            mf52_namedTuple = preprocessing.__dict_namedtuple_structure(mf52, headers)
            #Search for Nones:
            if preprocessing.__has_none(mf52_namedTuple) == True:
                raise TypeError('Missing coefficients. Check the sample.tir to find the difference.')
            
            return mf52_namedTuple #Using namedTuple to improve the equation part.
        
        except Exception as e:
            print('Error reading the .tir file')
            raise
    
    @staticmethod
    def __write_tir(tir_file, headers):
        try:
            with open(tir_file, 'w') as file:
                for header, values in headers.items():
                    file.write('$-----------------------------------------------------'+header.lower()+'\n')
                    file.write(f'[{header}]\n')
                    for key, value in values.items():
                        if isinstance(value, float):
                            file.write(f'{key}                     = {value}\n')
                        else:
                            file.write(f'{key}                     = {value}\n')
        except Exception as e:
            print('Error writing the .tir file')
            raise
