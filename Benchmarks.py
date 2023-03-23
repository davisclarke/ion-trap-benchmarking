from qiskit_braket_provider import AWSBraketProvider
from qiskit import *
import numpy as np
from qiskit.providers.fake_provider import FakeMumbaiV2
from qiskit.quantum_info import random_unitary
from qiskit.circuit.library import QuantumVolume
from qiskit.providers.aer.noise import NoiseModel
from qiskit.providers.aer.noise.errors import pauli_error, depolarizing_error
from azure.quantum.qiskit import AzureQuantumProvider
provider = AzureQuantumProvider(
    resource_id="/subscriptions/6648b6bc-19eb-4d18-9855-d527b2cc7f29/resourceGroups/AzureQuantum/providers/Microsoft.Quantum/Workspaces/iontrap",
    location='East US'
)
#provider.get_backend('IonQ Device') 

QuantumVolume(2).decompose().decompose().decompose().draw(output='mpl')
#np.random.seed(8122)

def get_noise(p_meas,p_gate, p_gate2):

    error_meas = pauli_error([('X',p_meas), ('I', 1 - p_meas)])
    error_gate1 = depolarizing_error(p_gate, 1)
    error_gate2 = error_gate1.tensor(depolarizing_error(p_gate2, 1))

    noise_model = NoiseModel()
    noise_model.add_all_qubit_quantum_error(error_meas, "measure") # measurement error is applied to measurements
    noise_model.add_all_qubit_quantum_error(error_gate1, ["x"]) # single qubit gate error is applied to x gates
    noise_model.add_all_qubit_quantum_error(error_gate2, ["cx"]) # two qubit gate error is applied to cx gates
        
    return noise_model

SHOTS=1024
num_qubits = 11
control_qubit = 10

ion_chain=QuantumRegister(num_qubits)
readout=ClassicalRegister(2)
qc=QuantumCircuit(ion_chain, readout)
errors=[]
backend=provider.get_backend('microsoft.estimator')
init_vector = np.zeros(2**num_qubits)
init_vector[0] = 1

from qiskit import transpile
for x in range(num_qubits-1):
    qc.initialize(init_vector)
    qc.x(control_qubit)
    qc.cx(control_qubit,x)
    qc.measure([ion_chain[control_qubit], ion_chain[x]], readout)
    #circuit = transpile(qc, backend)
    counts=backend.run(qc, noise_model=get_noise(0.0018,0.004, 0.027)).result().get_counts()
    errors.append(counts)
def get_error_rates(error_list):
    return [1-(errors[i]['11']/SHOTS) for i in range(len(error_list))]
    
get_error_rates(errors)