#from collections import namedtuple
from dataclasses import fields, is_dataclass
from .mf52_structure import mf_52

class preprocessing:
    def __fill_dataclass_from_dict(dataclass_instance, data):
        filled_data = {}
        for field in fields(dataclass_instance):  # Usando fields para acessar campos da dataclass
            field_name = field.name
            if field_name in data:
                value = data[field_name]
                if is_dataclass(field.type) and isinstance(value, dict):
                    # Se o valor for um dicionário e o campo é uma dataclass, faz chamada recursiva
                    nested_dataclass_instance = getattr(dataclass_instance, field_name)
                    filled_data[field_name] = preprocessing.__fill_dataclass_from_dict(nested_dataclass_instance, value)
                else:
                    filled_data[field_name] = value
            else:
                filled_data[field_name] = getattr(dataclass_instance, field_name)  # Manter o valor padrão
        return dataclass_instance.__class__(**filled_data)
    
    def __has_none(nt):
        # Search for Nones in the dataClass
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
            #mf52 = preprocessing.MF52_structure52() #mf52 structure
            #Dict to dataClass:
            mf52_dataClass = preprocessing.__fill_dataclass_from_dict(mf_52, headers)
            #Search for Nones:
            if preprocessing.__has_none(mf52_dataClass) == True:
                raise TypeError('Missing coefficients. Check the sample.tir to find the difference.')
            
            return mf52_dataClass #Using dataClass to improve the equation part.
        
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
