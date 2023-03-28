<center><strong> Investigating the Effects on Convergence of Various Optimizers on a VQC with an Efficient SU(2) on a NISQ Superconducting Quantum Computer</strong></center>  
### Introduction
$\qquad$ Quantum computing has the potential to impact a broad array of industries, from finance, to chemistry, to machine learning [0-2]. Theoretical computing speedups are proven due to a quantum computer's ability to utilize the infinite dimensional Hilbert space, offering $2^n$ simultaneously nonreal accessible states for every $n$ qubits as opposed to $1$ simultaneously real accessible state on a classical system. Not only do quantum computers scale exponentially in informational state capability, they can realize varying magnitudes, as long as they are orthogonal and normalized, as opposed to classical bits having one element of the wavefunction have a magnitude of $\approx1$. Managing to produce a quantum state in practicality is extremely difficult due to the sensitivity of quantum states, isolation of the quantum system, and the precise operations needed to control our qubits [2]. As a result, current quantum devices are riddled with noise and errors far above the threshold for fault-tolerance [0-4]. Current quantum devices are also far too small to gain computational advantage outside of very specific instances.  In this work, we will be using superconducting transmon qubits and respective simulators, a leading candidate in advancing quantum computers. Transmon qubits are quantum electrodynamic devices (QED), which implement electromagnetic fields in superconducting circuits [3]. What separates a transmon qubit from a charge-coupled qubit is the presence Josephson junction, a small insulator between Cooper pairs; this enables coherent quantum states to tunnel across the junction without extra voltage [3]. Transmon qubits are cooled at $<10 mK$, and conduction electrons alternate between regions of high and low charge density, creating waves called phonons [3],[5]; this enables infinite conductivity. Microwaves are sent through a gate capacitor, exciting the transmon qubit to an excited state. 
$\qquad$ Numerous models have been proposed to create a variational quantum classifier (VQC) that provide performance boosts over fair classical classifier algorithms [4, 1,  1804.11326]; yet, current VQC algorithms do not present quantum advantage and behave similarly to linear neural networks. In this work, we will focus on quantum optimizers as they apply to the performance of a variational quantum classifier. The efficient $SU(2)$ provides as a simple, hardware efficient ansatz (HEA) for our experiment [4] and the second-order $Z$ evolution circuit applied to the adhoc dataset provides for effective implementation of  higher-order data encoding [1] The purpose of this research is not to demonstrate quantum advantage over classical classifiers or to prove supremacy of a particular optimizer, but to explore how many epochs it takes for various optimization algorithms find the global minima. 

### Literature Review
**Overview of Variational Quantum Classifier Circuit** 
$\qquad$There are 4 main components of our VQC circuit [s41467-018-07090-4], [1804.11326]: the encoding (feature map) circuit, the ansatz,  the measurement scheme, and repetition. First, we must take data from our dataset and project it into a quantum state: 
$$\ket{\psi(\vec{x_i})}}=U_{\phi(x_i)}\ket0 $$
$x_i$ is every feature in the dataset, represented as elements in vector $x$, $U_{\phi(x_i)}$ is the feature map, and $\ket{0}$ is the ground state our qubits. The purpose implementing $U_{\phi(x_i)}$ is to project $x_i$ into a feature space that is fully separable. This separation is important as it dictates how the model will learn, failure to sperate the data makes convergence difficult.
![[feature map.png]]
**fig** Graphic representation of a feature map projecting data into a higher-order space. 

The $ZZ$ feature map is acting as our $U_{\phi(x_i)}$, and takes the following form [1804.11326]:$$\mathcal{U_\Phi}(\overrightarrow{x})=\exp(i\sum_{S\subseteq[n]}\phi_s(\overrightarrow{x})\prod_{i\in S}Z_i)$$Further, $\mathcal{U_\Phi}(\overrightarrow{x})$ is preceded by $H^{\otimes n}$, and repeated for some repetitions. In the instance of our circuit, $\phi_s$ has two elements. Our feature dimensions are $n$, and we use the following map for $\phi_s$: $\phi_i(\overrightarrow{x}) = x_i$ After every entangling gate $CX$: $\phi_{\{1,2\}}(\overrightarrow{x}) = (\pi - x_1)(\pi - x_2)$. Next, we must implement the ansatz  [1804.11326]. As a rough analogy, every $\theta$ in the ansatz correlates to a neuron in layer $\{i\}$. For our ansatz we use a two-local variational circuit  [1804.11326],




**Optimizers Used and Their Forms**
$\qquad$ In this work, we are using $5$ different optimizers: simultaneous perturbation stochastic approximation (SPSA), quantum natural simultaneous perturbation stochastic approximation (QNSPSA), constrained optimization by linear approximation (COBYLA), Adam, and Adam-AMSGrad. These optimizers were chosen due to their commonality, performance, and efficient use of memory in quantum machine learning demonstrations. The SPSA has garnered recent attention for its accurate approximation in working with high-dimensional spaces [https://www.jhuapl.edu/SPSA/]

### <strong>Methodology </strong>
$\qquad$ Isolating the effectiveness of an optimizer on a VQC is a rigorous process. Successful implementation will require controlling all other aspects of the VQC, but changing the optimization methods. After every epoch, results are stored in a log by callback. Each batch of shots to our quantum computer or simulator are branched into jobs. Every job is measured over $1024$ shots and a $\langle Z \rangle$ expectation is calculated. The aforementioned expectation values are fed into our varying optimizers, and a cost is found from a cross-entropy loss function. 
$\qquad$ 
**Global Settings**
$\qquad$ While the adhoc dataset and initial optimization points are randomly generated, they have a controlled random seed of $3142$; the specific choice of seed is arbitrary and will not have an effect on computation. Consequentially, all experiments will have the same dataset and initial points; allowing us to reproduce behavior. Further, our quantum simulators will not have a constant random seed, as we want to mimic the stochastic properties of our qubits in an attempt to have as realistic of a quantum simulator as possible. The device we submit jobs to will not change; switching devices from epoch to epoch will introduce confounding variables such as inconsistency in quantum architecture, wildly changing error rates, and qubit mapping conflicts. Due to device inhomogeneity, our ability to control quantum computers is limited due to precision in microwave control, readout, and coupling [2], [4]. As a result, our job counts are subject to noise and will hamper the performance of the model when running on IBM quantum systems. All optimizers will be trialed for varying learning rates, this is because different learning rates are more effective on different conditions of the model and the dataset being learned.

**On the Use of Quantum Simulators**
$\qquad$ We will use QASM 3 for this experiment, namely due to its accuracy of approximating IBM Quantum systems. Since IBM's quantum computers are a highly limited resource, using quantum simulators provides a time-efficient solution. We will still run the fastest converging and slowest converging models as a means of reference to our simulators.

**Adhoc Dataset Generation to Avoid Confounding Variables**
$\qquad$ The purpose of using an adhoc dataset is to isolate the performance of the optimizer. The adhoc is useful because it is a toy dataset designed to have the ability to be fully separated from the second-order $Z$ evolution circuit that will be used to encode our data in the preprocessing stage of the model. This is so as we are not examining the model on the encoding of the $ZZ$ feature map. So, we can eliminate the encoder's ability to accurately project the dataset into the feature space affecting the performance of the model. In generating the dataset, we have a gap, $\Delta = 0.3$, and the dataset and classification set will consist of 20 examples, complete with data points and labels. ![[output3.png]]
**fig** Plot of adhoc dataset $x_1$ v. $x_0$, blue data point correlates to a label of $1$, while red correlates to a label of $0$. 


**Higher-Order Encoding with the Second-Order $Z$ Evolution and Preprocessing**
$\qquad$ The $ZZ$ feature map will act as a quantum 'cast' for our efficient $SU(2)$, mapping the classical adhoc dataset to a higher-order space. Our adhoc dataset is encoded via scipy's `OneHotEncoder` for 
![[output.png]]
**fig** Circuit demonstration of $ZZ$ feature map. The circuit is repeated twice to have further span over the Bloch sphere. 
Our data is now mapped to a higher-order space within our feature space

**Efficient $SU(2)$ Ansatz**
Our $SU(2)$ is repeated $2$ times so we can encode more parameters into our ansatz, allowing for a more complex model. 

**Measurement Scheme**


**Optimization**

**Predictions** 




### Data Analysis











### Appendix
**1. Drawing the Feature Map Circuit**
```
ad_hoc_in_circ=ZZFeatureMap(
    feature_dimension=N,
    reps=2
)
ad_hoc_in_circ.decompose().draw(output='mpl')
```
**2. Drawing the Ansatz Circuit**
```
var_form=EfficientSU2(
    num_qubits=N,
    su2_gates=['ry', 'rz'],
    reps=2
)
var_form.decompose().draw()
```
**3. Mapping the Data Points**
```
N=2

train_data, train_label, test_data, test_label = ad_hoc_data(

    training_size=20,

    test_size=5,

    n=N,

    gap=0.3,

    one_hot=False)

  

plt.figure(figsize=(5,5))

colors=[]

for i in range(len(train_label)): plt.scatter(train_data[i][0], train_data[i][1], color='red' if train_label[i] == 0 else 'blue')

plt.title('Adhoc Dataset')

plt.xlabel('x_0')

plt.ylabel('x_1')
```
