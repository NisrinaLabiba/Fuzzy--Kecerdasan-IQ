import pandas as pd
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Membaca data dari file Excel
data = pd.read_excel('data_anak.xlsx')

# Inisialisasi variabel input dan output fuzzy
PR = ctrl.Antecedent(np.arange(0, 151, 1), 'PR')
PO = ctrl.Antecedent(np.arange(0, 151, 1), 'PO')
PB = ctrl.Antecedent(np.arange(0, 151, 1), 'PB')
PV = ctrl.Antecedent(np.arange(0, 151, 1), 'PV')

IQ = ctrl.Consequent(np.arange(0, 201, 1), 'IQ')

# Generate membership functions
PR.automf(3)
PO.automf(3)
PB.automf(3)
PV.automf(3)

# Fungsi keanggotaan untuk variabel output status
IQ['low'] = fuzz.trimf(IQ.universe, [0, 0, 60])
IQ['medium'] = fuzz.trimf(IQ.universe, [50, 70, 100])
IQ['high'] = fuzz.trimf(IQ.universe, [100, 150, 200])

# Aturan fuzzy
rule1 = ctrl.Rule(PR['poor'] | PO['poor'] | PB['poor'] | PV['poor'], IQ['low'])
rule2 = ctrl.Rule(PR['average'] | PO['average'] | PB['average'] | PV['average'], IQ['medium'])
rule3 = ctrl.Rule(PR['good'] | PO['good'] | PB['good'] | PV['good'], IQ['high'])

# Create control system
system = ctrl.ControlSystem([rule1, rule2, rule3])
IQ_sim = ctrl.ControlSystemSimulation(system)

# inisialisasi list untuk menyimpan hasil
hasil_IQ = []

# Fitting data
for index, row in data.iterrows():
    IQ_sim.input['PR'] = row ['PR']
    IQ_sim.input['PO'] = row ['PO']
    IQ_sim.input['PB'] = row ['PB']
    IQ_sim.input['PV'] = row ['PV']

    IQ_sim.compute()

    hasil_IQ.append(IQ_sim.output['IQ'])

    # Output results
def nilai_iq(iq_value) : 
    if iq_value <= 70:
        return 'low'
    elif iq_value <= 120:
        return  'medium'
    else:
        return  'high'


data['IQ']=hasil_IQ
data['hasil_simulator'] = data['IQ'].apply(nilai_iq)

# Save the results to Excel file
data.to_excel('hasil_data.xlsx', index=False)
