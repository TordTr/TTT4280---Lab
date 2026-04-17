import numpy as np


#muabo = np.genfromtxt("/Users/hakoncarlsen/Downloads/Optikk-lab-filer-26/muabo.txt", delimiter=",")
#muabd = np.genfromtxt("/Users/hakoncarlsen/Downloads/Optikk-lab-filer-26/muabd.txt", delimiter=",")

muabo = np.genfromtxt("/Users/tordtranum/Desktop/6.semester/Sensorer/Lab/Lab_3_Optikk/Testing&PI_filer/muabo.txt", delimiter=",")
muabd = np.genfromtxt("/Users/tordtranum/Desktop/6.semester/Sensorer/Lab/Lab_3_Optikk/Testing&PI_filer/muabd.txt", delimiter=",")

red_wavelength = 600 # Replace with wavelength in nanometres
green_wavelength = 520 # Replace with wavelength in nanometres
blue_wavelength = 460 # Replace with wavelength in nanometres

wavelength = np.array([red_wavelength, green_wavelength, blue_wavelength])

def mua_blood_oxy(x): return np.interp(x, muabo[:, 0], muabo[:, 1])
def mua_blood_deoxy(x): return np.interp(x, muabd[:, 0], muabd[:, 1])

bvf = 0.01 # Blood volume fraction, average blood amount in tissue
oxy = 0.8 # Blood oxygenation

# Absorption coefficient ($\mu_a$ in lab text)
# Units: 1/m
mua_other = 25 # Background absorption due to collagen, et cetera
mua_blood = (mua_blood_oxy(wavelength)*oxy # Absorption due to
            + mua_blood_deoxy(wavelength)*(1-oxy)) # pure blood
mua = mua_blood*bvf + mua_other

# reduced scattering coefficient ($\mu_s^\prime$ in lab text)
# the numerical constants are thanks to N. Bashkatov, E. A. Genina and
# V. V. Tuchin. Optical properties of skin, subcutaneous and muscle
# tissues: A review. In: J. Innov. Opt. Health Sci., 4(1):9-38, 2011.
# Units: 1/m
musr = 100 * (17.6*(wavelength/500)**-4 + 18.78*(wavelength/500)**-0.22)

print(f"musr (1/m): {musr}")
# mua and musr are now available as shape (3,) arrays
# Red, green and blue correspond to indexes 0, 1 and 2, respectively

# TODO calculate penetration depth
C = np.sqrt(3*(musr+mua)*mua)
delta = 1/C
print("Penetrasjonsdybde (m):", delta)
print("Penetrasjonsdybde (mm):", delta * 1000)

d_finger = 0.012 #meter

T = np.exp(-C*d_finger)
print("Transmittans (mm):", T) 
print("Transmittans (prosent):", T * 100) 

R = np.exp(-2*C*d_finger)
print("Reflekstans (mm):", R) 
print("Reflekstans (prosent):", R * 100) 

d_vessel = 300e-6  # 300 µm

# Normal tissue
C_normal = np.sqrt(3*(musr+mua)*mua)
T_normal = np.exp(-C_normal*d_vessel)

# Blood vessel (100% blood)
mua_vessel = mua_blood
C_vessel = np.sqrt(3*(musr+mua_vessel)*mua_vessel)
T_vessel = np.exp(-C_vessel*d_vessel)

print("T normal:", T_normal)
print("T vessel:", T_vessel)

K = abs(T_vessel - T_normal)/T_normal
print("Kontrast:", K)


