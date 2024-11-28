# MFPy
Using the Magic Formula equations (Tyre and Vehicle Dynamics by Hans Pacejka - second edition), this repository contains some tools to read a .tir file (5.2 protocol) with examples (notebooks) and how to fit a tyre test data (notebook and PyQt5 app) to create a .tir file (5.2 protocol). 

## General informations

**All sample files do not represent the actual behaviour of tyres, they are files whose purpose is simply to use the library.**

**All the equations used can be seen in the file mfpy/equations.py . Next to each one you will find comments and the book reference.**


## Installation and requirements

**The fit_interface folder is only needed if the user wants to run the fit_app.py file.**

```bash
# Clone the repository
git clone https://github.com/jmcavalcante/MFPy

# Install the requirements
pip install -r requirements.txt
```

## How to use it

### Read tir notebook (read_tir.ipynb)
This notebook teaches you how to read a .tir file that follows the 5.2 protocol. By default, it will read a sample file, but it can be changed to read another file. You can also see some interesting graphs that can be generated from the .tir file, such as the traction circle.

!print traction circle

### Fit tir notebook (read_tir.ipynb)
This notebook teaches you how to fit a tire test data that following the 5.2 protocol. By default, it will read some samples files, but it can be changed to read another files. It is important to check that for each folder, there is a correct nomenclature for the csv (**with ; as separator**) files that will be inside:

- FX pure slip longitudinal: FZXXXX_gammaYYYY.csv
    where XXXX means the value for the FZ(N) for this test, and YYYY means the value for the inclination angle (rads) for this test.It doesn't matter how many characters are in XXXX or YYYY.
- FY pure slip cornering: FZXXXX_gammaYYYY.csv
    where XXXX means the value for the FZ(N) for this test, and YYYY means the value for the inclination angle (rads) for this test.It doesn't matter how many characters are in XXXX or YYYY.
- MZ pure slip cornering: FZXXXX_gammaYYYY.csv
    where XXXX means the value for the FZ(N) for this test,and YYYY means the value for the inclination angle (rads) for this test.It doesn't matter how many characters are in XXXX or YYYY.
- FX combined: FZXXXX_alphaYYYY.csv
    where XXXX means the value for the FZ(N) for this test,and YYYY means the value for the slip angle (rads) for this test.It doesn't matter how many characters are in XXXX or YYYY.
- FY combined: FZXXXX_kappaYYYY_gammaKKKK.csv
    where XXXX means the value for the FZ(N) for this test,YYYY means the value for the slip ratio (%/100) for this test and KKKK means the value for the inclination angle (rads) .It doesn't matter how many characters are in XXXX or YYYY.
- MZ combined: FZXXXX_kappaYYYY_gammaKKKK.csv
    where XXXX means the value for the FZ(N) for this test,YYYY means the value for the slip ratio (%/100) for this test and KKKK means the value for the inclination angle (rads) .It doesn't matter how many characters are in XXXX or YYYY.

You can always use the files available in the sample folder as an example!


### Fit interface (fit_app.py or MFPy fit.exe)

!print imagem interface
The interface follows the same logic as the notebook, for each test you need to indicate the folder containing the .csv files. However, with an interface, you can better control each parameter of the fit, such as the initial kick, the boundary values and make any corrections before writing the .tir file.

#### Pyinstaller
If you want to recompile and regenerate the executable, this is the command that takes the additional interface files into account.
```bash
pyinstaller --onefile --noconsole --icon=fit_interface/design/logo.ico --add-data "fit_interface/design;fit_interface/design" --add-data "fit_interface/tir;fit_interface/tir" --distpath . --workpath . --name "MFPy fit" fit_app.py
```

### Contact

Feel free to contact me by mail if you have question or open a issues request.
### Reference
> **Tyre and Vehicle Dynamics - 2nd edition**  
> Author: Hans Pacejka  

