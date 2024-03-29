# Movement Smoothness

Smooth movements are a hallmark of well-developed and learned motor behaviour [^flash]. Movement smoothness is one of the most commonly used movement quality constructs that are of interest in various fields, such as movement science, motor control/learning, biomechanics, and neurorehabilitation. 

> **Definition.** **Movement smoothness** is a measure of the amount of intermittency or fluency in a given movement.

Intuitively, movement smoothness is an easy construct to understand. When shown two movements one can fairly consistently rate the relative smoothness of two movements. However,  a valid, robust and sensitive general measure of smoothness for use with different types of movements, measured movement variables, and technologies has been 
a struggle. Two candidate measures have emerged as the most popular measures of smoothness in the last 10 years[^sparc1] [^sparc2] [^ldlj]: **spectral arc length (SPARC)** and **log dimensionless jerk (LDLJ)**.

The smoothness module of the monalysa library contains functions for computing the smoothness of discrete movements using the SPARC and LDLJ; along with some variants of the LDLJ --  dimensionless jerk and the LDLJ computed from accelerometer data. The detailed module documentation can be found [here](smoothnessdoc).

## Properties of Smoothness Measures
A measure of movement smoothness must satisfy the following properties:
1. **It is dimensionless**, i.e. the value of the smoothness of a movement must be independent of its amplitude and duration. 
Let {math}`m(t)` by the kinematics of a movement {math}`M`, and let {math}`\lambda(m(t))` be the smoothness of this movement; note, that {math}`\lambda\left(\cdot\right)` is a smoothness measure. Then, uniform scaling of the amplitude and duration of {math}`m(t)` does not impact the smoothness of the movement, i.e.
```{math}
	\lambda\left(A \cdot m\left(\frac{t}{T}\right)\right) = \lambda\left(m(t)\right)
```

2. **It decreases with the number of submovements**. When we view the movement as being composed of individual submovements, the value of the smoothness measure should decrease with an increase in the number of submovements.

3. **It decreases with an increase in the inter-submovement interval**. In the submovement view of movement, an increase in the inter-submovement interval between successive submovements should decrease with the value of the smoothness measure.

In addition to these, the measures must also be robust to noise and sensitive to small changes in the movement profile. Balasubramanian et. al[^sparc1] showed that the SPARC and the LDLJ satisfy the above properties.

## Dimensionless Jerk (DL)
Jerk -- the third derivative of position -- has become intimately associated with the concept of movement smoothness ever since Flash and Hogan published their minimum jerk model for describing discrete point-to-point reaching movements[^flash]. The dimensionless jerk measure computes the squared jerk of a given movement, while 
appropriately accounting for the amplitude and duration of the movement, so that the measure is dimensionless, i.e. the value is unitless. 

Let {math}`v(t)` be the velocity profile of a movement of interest, and the movement starts at {math}`t=0` and ends at {math}`t=T`. The dimensionless jerk (DJ) measure of movement smoothness for this movement is given by,
```{math}
    \text{DJ} := - \frac{T^5}{V^2} \int_{0}^{T} \left\Vert \frac{d^2 v(t)}{dt^2} \right\Vert^2 dt
```
where, {math}`V = \max_{t} \Vert v(t) \Vert` is the peak speed of the movement, and{math}`T` is the duration of the movement. The DJ measure can be computed using the `dimensionless_jerk` function in the `smoothness` module.

```{code} python
>>> import numpy as np
>>> from monalysa.movements import mjt_discrete_movement
>>> from monalysa.quality.smoothness import dimensionless_jerk
>>> from monalysa.quality.smoothness import dimensionless_jerk_factors
>>> fs = 100.
>>> t = np.arange(0, 1.0, 1/fs)
>>> vel = monalysa.movements.mjt_discrete_movement()
>>> dimensionless_jerk(vel, fs=fs, data_type="vel", rem_mean=False)
-185.70122547199867
```

We can obtain the three factors of the dimensionless jerk measure {math}`T^5`,{math}`A^2`, and {math}`\int_{0}^{T} \left\Vert \frac{d^2 v(t)}{dt^2} \right\Vert^2 dt` using the `dimensionless_jerk_factors` function in the `smoothness` module.

```{code} python
>>> dimensionless_jerk_factors(vel, fs=fs, data_type="vel", rem_mean=False)
(1.0, 3.5156249999999982, 652.8558707999949)
```

## Log Dimensionless Jerk (LDLJ)
However, the DJ measure's value changes by several orders of magnitude 
when the smoothness of a movement changes. The log dimensionless jerk (LDLJ) addresses this problem by taking the log of the absolute value of the dimensionless jerk.
```{math}
    \text{LDLJ} := - \ln \left( \frac{T^5}{V^2} \int_{0}^{T} \left\Vert \frac{d^2 v(t)}{dt^2} \right\Vert^2 dt \right)
```
This can be reformulated as the following,
```{math}
    \text{LDLJ} = - 5\ln T + 2\ln V - \ln \left( \int_{0}^{T} \left\Vert \frac{d^2 v(t)}{dt^2} \right\Vert^2 dt \right)
```
The individual terms of LDLJ can be computed using the function `log_dimensionless_jerk_factors` in the `smoothness` module, and LDLJ from the function `log_dimensionless_jerk`.

```{code} python
>>> from monalysa.quality.smoothness import log_dimensionless_jerk
>>> from monalysa.quality.smoothness import log_dimensionless_jerk_factors
>>> print("LDLJ: ", log_dimensionless_jerk(vel, fs=fs, data_type="vel"))
>>> print("LDLJ Factors: ", log_dimensionless_jerk_factors(vel, fs=fs, data_type="vel"))
>>> print("Sum of LDLJ Factors: ", np.sum(log_dimensionless_jerk_factors(vel, fs=fs, data_type="vel")))
LDLJ:  -5.224139067539895
LDLJ Factors:  (-0.0, 1.2572173188447482, -6.481356386384643)
Sum of LDLJ Factors:  -5.224139067539895
```

## Spectral Arc Length (SPARC)
The SPARC measure of smoothness computes the arc length of the magnitude of the Fourier transform of the movement profile.
```{math}
    \text{SPARC} := -\int_{0}^{\omega_{c}}\!\left[\!\!\left(\!\frac{1}{\omega_{c}}\!\right)^{2} \,+\, \left(\!\frac{d\hat{V}(\omega)}{d\omega}\!\right)^{2}\!\right]^{\frac{1}{2}}\!d\omega; \,\,\, \hat{V}(\omega) = \frac{V(\omega)}{V(0)}
```
```{math}
    \omega_{c} := \min\left\{\omega_{c}^{max}, \min\left\{\omega\,\,\,,\hat{V}(r)<\overline{V} \,\,\, \forall \,\,\, r >\omega \right\} \right\}
```
The arc length is a measure of the complexity of the Fourier magnitude spectrum of the speed profile. Increasing the number of submovements and the inter-submovement 
interval. The SPARC measure can be computed using the `sparc` function 
in the smoothness module.

```{code} python
>>> from monalysa.quality.smoothness import sparc
>>> fs = 100.
>>> ts = 1 / fs
>>> t = np.arange(0, 1.0, ts)
>>> vel = mjt(amp=1, dur=1.0, loc=0.5, time=t, data_type="vel")
>>> sparc(vel, fs=fs)[0]
-1.4058293244214655
```
The `sparc` function returns three values: the SPARC measure value, a tuple with the frequency and the magnitude spectrum of the movement profile, and another tuple with the frequency and the magnitude spectrum selected for computing the arc length.

```{code} python
>>> _, Vf, Vfsel = sparc(vel, fs=fs)
>>> # Plot Fourier spectrum
>>> fig = plt.figure(figsize=(10, 3))
>>> ax = plt.subplot(121)
>>> ax.plot(t, vel)
>>> ax.set_xlabel("Time $t$ (sec)")
>>> ax.set_ylabel(r"$v(t)$")
>>> ax = plt.subplot(122)
>>> ax.plot(Vf[0], Vf[1], label="Full Spectrum")
>>> ax.plot(Vfsel[0], Vfsel[1], lw=2, color="tab:red", label="Selected Spectrum")
>>> ax.axhline(0.05, lw=1, ls="dashed", color="k")
>>> ax.set_xlim(0, 12)
>>> ax.set_xlabel("Frequency $f$ (Hz)")
>>> ax.set_ylabel(r"$\vert V(2\pi f)\vert$")
>>> ax.legend(loc=1)
```
![Alt text](_static/sparc_demo_mjt.svg)

If you are feeling adventurous at this point, try computing the SPARC measure for a random movement using `generate_random_movement` function in the `movements` module, and look at its Fourier spectrum and the segment selected for computing the arc length. 


**References**
[^flash]: Flash, Tamar, and Neville Hogan. "The coordination of arm movements: an experimentally confirmed mathematical model." The Journal of Neuroscience 5.7 (1985): 1688-1703.
[^sparc1]: Balasubramanian, Sivakumar, Alejandro Melendez-Calderon, and Etienne Burdet. "A robust and sensitive metric for quantifying movement smoothness." IEEE transactions on biomedical engineering 59.8 (2011): 2126-2136.
[^sparc2]: Balasubramanian, S., Melendez-Calderon, A., Roby-Brami, A., & Burdet, E. (2015). On the analysis of movement smoothness. Journal of neuroengineering and rehabilitation, 12(1), 1-11.
[^ldlj]: Melendez-Calderon, Alejandro, Camila Shirota, and Sivakumar Balasubramanian. "Estimating movement smoothness from inertial measurement units." Frontiers in bioengineering and biotechnology 8 (2021): 558771.
