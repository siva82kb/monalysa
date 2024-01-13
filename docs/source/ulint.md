
# UL Intensity of Use

UL use only tells us if a functional movement is being performed or not at a given instant. It contains no information about how intensely, how fast, how strongly a functional movement is being performed. This is captured by the UL intensity of use measures.

The detailed module documentation for `ulint` can be found [here](ulintdoc).

> **Definition.** **Instantaneous Intensity of Use** is a construct that reflects how strenuous a movement/posture is at a particular instant of time, when the upper-limb is in use.

The magnitude of movement velocity, acceleration, interaction force, muscle activity, etc. are potential measures of instantaneous intensity of use. The instantaneous intensity of use is a non-negative signal, which is 0, when UL use is 0 (by definition).

The following code snippet shows how to compute the instantaneous intensity of use from th vector magntidue signal.

```{code} python
>>> import numpy as np
>>> from monalysa.ulfunc import uluse
>>> fs = 100
>>> t = np.arange(0, 10, 1. / fs)
>>> vmag = np.square(np.sin(2 * t) + np.cos(0.4 * t) + 2) * np.random.rand(len(t))
>>> th1, th2l, th2h = 3, 1, 4
>>> _, u1 = uluse.from_vec_mag(vmag, thresh=th1)
>>> _, u2 = uluse.from_vec_mag_dblth(vmag, thresh_l=th2l, thresh_h=th2h)
```
Plotting the different variables from the above code snippet, we get the following. The top row plots a simulated vector magnitude signal plotted in light blue. The horizontal lines in this plot show the thressholds used with the `from_vec_mag` and the `from_vec_mag_dblth` functions. The black dashed line corresponds to the single threshold of value {math}`v_{th}=3` used with the `from_vec_mag` function, which generates the UL use signal using the following rule (assume {math}`v[n]` is the value of the vector magnitude signl at time {math}`n`),
```{math}
    u[n] = \begin{cases}
        1 & v[n] \geq v_{th} \\
        0 & \text{otherwise}
    \end{cases}
``` 

The red dashed lines in this plot are the two thresholds of values {math}`v_{th}^{l}=1` and {math}`v_{th}^{h}=1` used with the `from_vec_mag_dblth` function, which generates the UL use signal using the following rule,
```{math}
    u[n] = \begin{cases}
        1 & v[n] \geq v_{th, h} \\
        0 & v[n] < v_{th, l} \\
        u[n - 1] & \text{otherwise}
    \end{cases}
```

The red dashed lines correspond to the double threshold of values 1 and 4 used with the `from_vec_mag_dblth` function. The bottom row plots the binary UL use output from the two functions. 

![Alt text](_static/uluse_vec_mag.svg)

The corresponding UL use outputs from the `from_vec_mag` and `from_vec_mag_dlbth` functions are shown in the plots in rows 2 and 3, respectively in the above figure.

### GMAC (= GM + AC)
**Gross Movement (GM) Score**. GM measure [^leuen2017] uses yaw and pitch angles computed using the Madgwick algorithm from the raw acceleration and gyroscope data. If the overall absolute change in yaw and pitch angles is higher than 30° and the absolute pitch of the forearm is within ± 30° in a time window, GM is defined as 1 (indicating functional use), else it is 0. The GM measure exploits the nature of most functional movements to occur in this ‘functional space’, i.e., in the region in front of subject around his/her chest height.

The AC measures are known to be highly sensitive while having very low specificity, and GM is highly specific but not sensitive [^subash2022]. The hybrid measure — GMAC combines the essential elements of TAC and GM measures. It employs counts with a modified GM measure; the counts are used instead of the absolute change in yaw and pitch angles. The ```from_gmac``` function in the ```uluse``` module uses an optimized version of the algorithm with a hysteresis threshold on the pitch angles [^gmac]. This recently formulated GMAC requires only the raw acceleration data from the forearm. When optimized, it performs as well as a machine learning algorithms trained to work across subjects[^gmac].

![Alt text](_static/gmac_accl.svg)

```{code} python
>>> from monalysa.ulfunc import uluse
>>> fs = 50 # sampling frequency
>>> T = 60 # total number of seconds
>>> t = np.arange(0, T, 1/fs)
>>> ax = 0.5 * np.sin(0.2 * 2 * np.pi * t)
>>> ay = 0.1 * np.sin(0.05 * 2 * np.pi * t)
>>> az = 0.8 * np.sin(0.02 * 2 * np.pi * t)
>>> accl = np.array([ax, ay, az]).T
>>> accl_farm_inx = 0   # index of column with acceleration along the forearm 
>>> elb_to_farm = True  # axis points from elbow to forearm
>>> pitch, amag, use = uluse.from_gmac(accl, fs, accl_farm_inx, elb_to_farm)
>>> print("Pitch: ", pitch)
>>> print("Accl. mag: ", amag)
>>> print("Use (GMAC): ", use)
Pitch:  [         nan  80.48298345  80.48104485 ... -13.55580179 -12.70897362
 -11.85026972]
Accl. mag:  [0.00000000e+00 5.05107719e-05 1.50603641e-04 ... 3.11586714e-01
 3.11590258e-01 3.11593662e-01]
Use (GMAC):  [0. 0. 0. ... 0. 0. 0.]
```
The plot of the different signals in the above code snippets is shown below.

![Alt text](_static/gmac_use.svg)

The best performing UL use methods are machine learning methods that are optimized for 
individual subjects, which require training data from each subject. For more details, 
refer to the work by Subash et. al[^subash2022]. 

**References**
[^david2021b]: David, Ann, Tanya Subash, S. K. M. Varadhan, Alejandro Melendez-Calderon, and Sivakumar Balasubramanian. "A framework for sensor-based assessment of upper-limb functioning in hemiparesis." Frontiers in Human Neuroscience 15 (2021).
[^bailey2014]: Bailey, Ryan R., Joseph W. Klaesner, and Catherine E. Lang. "An accelerometry-based methodology for assessment of real-world bilateral upper extremity activity." PloS one 9, no. 7 (2014).
[^delucena2017]: de Lucena, Diogo S., Oliver Stoller, Justin B. Rowe, Vicky Chan, and David J. Reinkensmeyer. "Wearable sensing for rehabilitation after stroke: Bimanual jerk asymmetry encodes unique information about the variability of upper extremity recovery." In 2017 International Conference on Rehabilitation Robotics (ICORR), pp. 1603-1608. IEEE, 2017.
[^leuen2017]: Leuenberger, Kaspar, Roman Gonzenbach, Susanne Wachter, Andreas Luft, and Roger Gassert. "A method to qualitatively assess arm use in stroke survivors in the home environment." Medical & biological engineering & computing 55 (2017): 141-150.
[^subash2022]: Subash, Tanya, Ann David, StephenSukumaran ReetaJanetSurekha, Sankaralingam Gayathri, Selvaraj Samuelkamaleshkumar, Henry Prakash Magimairaj, Nebojsa Malesevic et al. "Comparing algorithms for assessing upper limb use with inertial measurement units." Frontiers in Physiology 13 (2022): 2611.
[^gmac]: Balasubramanian, Sivakumar. "GMAC: A simple measure to quantify upper limb use from wrist-worn accelerometers." medRxiv (2023): 2023-11. -->
