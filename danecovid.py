import math
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from excel import OpenExcel


NAZWA_PLIKU = 'dane-covid-usa.xlsx'


print('Obliczanie regresji liniowej,')
print('dane są czytane z pliku', NAZWA_PLIKU)


rozszerzenie = NAZWA_PLIKU[-5:].lower()

if rozszerzenie == '.xlsx':
    plik = OpenExcel(NAZWA_PLIKU)
    x = plik.read('A')
    y = plik.read('B')
    
    for i in range(len(y)):
        if type(y[i]) == str:
            y[i] = float(y[i].replace('\xa0', ''))
            
    x = np.array(x)
    y = np.array(np.log10(y))
            
elif rozszerzenie == '.txt':
    x, y = np.loadtxt(NAZWA_PLIKU, unpack=True)
else:
    raise RuntimeError('nieznany typ pliku')

n = len(x)
print('liczba punktów =', n)
print('liczba stopni swobody dof =', n - 2)

confidence = 0.95
tcoeff = stats.t.ppf(confidence, n - 2)
print('poziom ufności =', confidence*100.0, '%')
print('współczynnik Studenta =', tcoeff)

a, b, r, p_value, da = stats.linregress(x, y)
da = tcoeff * da
db = da * math.sqrt(np.sum(x**2) / n)
da_rel = da/math.fabs(a)*100.0 if a else '???'
db_rel = db/math.fabs(b)*100.0 if b else '???'

print('y = a * x + b')
print('a = {} ± {}  ({:.4}%)'.format(a, da, da_rel))
print('b = {} ± {}  ({:.4}%)'.format(b, db, db_rel))
print('r =', r)
print('p-value =', p_value)

# Obliczanie dopasowanych krzywych
#
npts = 500
x_min = np.min(x)
x_max = np.max(x)
little_more = (x_max - x_min) *0.10;
x_lo = x_min - little_more
x_hi = x_max + little_more

xi = np.linspace(x_lo, x_hi, npts)
yi = a * xi + b
x_mean = np.mean(x)
variance = np.var(x, ddof=1)
delta_conf = da * np.sqrt(variance + (xi-x_mean)**2)
delta_pred = da * np.sqrt((n-1)*variance + (xi-x_mean)**2)
yi_conf_lo = yi - delta_conf
yi_conf_hi = yi + delta_conf
yi_pred_lo = yi - delta_pred
yi_pred_hi = yi + delta_pred


# Rysowanie wykresów
#
plt.plot(xi, yi, 'r.',
         xi, yi_conf_lo, 'g--',
         xi, yi_pred_lo, 'c:',
         xi, yi_conf_hi, 'g--',
         xi, yi_pred_hi, 'c:',
         x, y, 'b-')
plt.grid()
plt.title('Regresja liniowa')
plt.xlabel('zmienna niezależna')
plt.ylabel('zmienna zależna')
plt.show()



# loga = np.log(a)
# y = np.array(np.log10(y))
