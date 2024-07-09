# Upper Limb Use

Upper limb use assessment focuses only on measuring willed movements or postures of functional significance. Identifying such movements is a relatively trivial task for a human observing a subject performing various movements. A human’s ability to relate to the movements being observed allows him/her to make judgements about the nature of a subject’s movements.

Upper limb use is the fundamental construct of upper limb functioning [^david2021b]. It is essential for deriving the other constructs in upper limb functioning. 

The detailed module documentation for `uluse` can be found [here](ulusedoc).

> **Definition.** **Upper Limb Use** is a binary construct indicating the presence or absence of a voluntary, 
meaningful movement or posture

## Measures of Upper Limb Use
The most popular sensing modality is inertial sensing using inertial measurement units (IMUs) in the form of wristbands, which measure linear acceleration and angular velocities of the forearm. Various measures have been developed to quantify
upper limb use from only wrist-worn IMU data.

### Thresholded Activity Counts (AC)
The amount of acceleration is thresholded using a measure-specific threshold to estimate upper limb use. The computational simplicity of this measure makes it a quick and popular approach [^bailey2014] [^delucena2017]. However, while an increased amount of acceleration most likely correlates with increased upper-limb use, the feature is not unique to functional movements and thus overestimates upper-limb use. Two types of AC measures can be found in the literature: activity counting [^delucena2017], and vector magnitude [^bailey2014].

The `uluse` module contains two functions `from_vec_mag` and from `from_vec_mag_dblth` for computing UL use from the vector magnitude signal that is provided by sensors like the [ActiGraph](https://theactigraph.com/).

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
Plotting the different variables from the above code snippet, we get the following. The top row plots a simulated vector magnitude signal plotted in light blue. The horizontal lines in this plot show the thresholds used with the `from_vec_mag` and the `from_vec_mag_dblth` functions. The black dashed line corresponds to the single threshold of value {math}`v_{th}=3` used with the `from_vec_mag` function, which generates the UL use signal using the following rule (assume {math}`v[n]` is the value of the vector magnitude signal at time {math}`n`),
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
**Gross Movement (GM) Score**. GM measure [^leuen2017] uses yaw and pitch angles computed using the Madgwick algorithm from the raw acceleration and gyroscope data. If the overall absolute change in yaw and pitch angles is higher than 30° and the absolute pitch of the forearm is within ± 30° in a time window, GM is defined as 1 (indicating functional use), else it is 0. The GM measure exploits the nature of most functional movements to occur in this ‘functional space’, i.e., in the region in front of the subject around his/her chest height.

The AC measures are known to be highly sensitive while having very low specificity, and GM is highly specific but not sensitive [^subash2022]. The hybrid measure — GMAC combines the essential elements of TAC and GM measures. It employs counts with a modified GM measure; the counts are used instead of the absolute change in yaw and pitch angles. The ```from_gmac``` function in the ```uluse``` module uses an optimized version of the algorithm with a hysteresis threshold on the pitch angles [^bala2024]. This recently formulated GMAC requires only the raw acceleration data from the forearm. When optimized, it performs as well as a machine learning algorithm trained to work across subjects[^bala2024].

![Alt text](_static/gmac_accl.svg)

```{code} python
>>> from monalysa.ulfunc import uluse
>>> fs = 50 # sampling frequency
>>> T = 60 # total number of seconds
>>> t = np.arange(0, T, 1/fs)
>>> ax = 0.5 * np.sin(0.2 * 2 * np.pi * t)
>>> ay = 0.1 * np.sin(0.05 * 2 * np.pi * t)
>>> az = 0.8 * np.sin(0.02 * 2 * np.pi * t) + 0.01
>>> accl = np.array([ax, ay, az]).T
>>> accl_farm_inx = 0   # index of the column with acceleration along the forearm 
>>> elb_to_farm = True  # axis points from elbow to forearm
>>> _, use, pitch, amag = uluse.from_gmac(accl, fs=fs, accl_farm_inx=accl_farm_inx,
                                          elb_to_farm=elb_to_farm)
>>> print("Pitch: ", pitch)
>>> print("Accl. mag: ", amag)
>>> print("Use (GMAC): ", use)
Pitch:  [  0.          29.71040273  46.24725865 ... -21.63656029 -21.01257394
 -20.37245668]
Accl. mag:  [3.99644727e-04 1.09427227e-03 2.24360867e-03 ... 7.68940311e-01
 7.66124033e-01 7.63457863e-01]
Use (GMAC):  [0. 0. 0. ... 0. 0. 0.]
```
The plot of the different signals in the above code snippets is shown below. 

![Alt text](_static/gmac_use.svg)

The best performing UL use methods are machine learning methods that are optimized for individual subjects, which require training data from each subject. For more details, refer to the work by Subash et. al[^subash2022]. 

**References**
[^david2021b]: David, Ann, Tanya Subash, S. K. M. Varadhan, Alejandro Melendez-Calderon, and Sivakumar Balasubramanian. "A framework for sensor-based assessment of upper-limb functioning in hemiparesis." Frontiers in Human Neuroscience 15 (2021).
[^bailey2014]: Bailey, Ryan R., Joseph W. Klaesner, and Catherine E. Lang. "An accelerometry-based methodology for assessment of real-world bilateral upper extremity activity." PloS one 9, no. 7 (2014).
[^delucena2017]: de Lucena, Diogo S., Oliver Stoller, Justin B. Rowe, Vicky Chan, and David J. Reinkensmeyer. "Wearable sensing for rehabilitation after stroke: Bimanual jerk asymmetry encodes unique information about the variability of upper extremity recovery." In 2017 International Conference on Rehabilitation Robotics (ICORR), pp. 1603-1608. IEEE, 2017.
[^leuen2017]: Leuenberger, Kaspar, Roman Gonzenbach, Susanne Wachter, Andreas Luft, and Roger Gassert. "A method to qualitatively assess arm use in stroke survivors in the home environment." Medical & biological engineering & computing 55 (2017): 141-150.
[^subash2022]: Subash, Tanya, Ann David, StephenSukumaran ReetaJanetSurekha, Sankaralingam Gayathri, Selvaraj Samuelkamaleshkumar, Henry Prakash Magimairaj, Nebojsa Malesevic et al. "Comparing algorithms for assessing upper limb use with inertial measurement units." Frontiers in Physiology 13 (2022): 2611.
[^bala2024]: Balasubramanian, Sivakumar. "GMAC–A simple measure to quantify upper limb use from wrist-worn accelerometers." IEEE Transactions on Neural Systems and Rehabilitation Engineering (2024).
