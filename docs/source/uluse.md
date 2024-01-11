# Upper Limb Use


Upper limb use assessment focuses only on measuring willed movements or postures of functional significance. Identifying such movements is a relatively trivial task for a human observing a subject performing various movements. A human’s ability to relate  to the movements being observed allows him/her to make judgements about the nature of a subject’s movements.

Upper limb use is the fundamental construct of upper limb functioning 
[^david2021b]. It is essential for deriving the other constructs in upper limb functioning.

> **Definition.** **Upper Limb Use** a binary construct indicating the presence or absence of a voluntary, 
meaningful movement or posture

## Measures of Upper Limb Use
The most popular sensing modality is inertial sensing using inertial measurement units (IMUs) in the form of wristbands, which measure linear acceleration and angular velocities of the forearm. Various measures have been developed to quantify
upper limb use from only wrist-worn IMU data.

**Thresholded Activity Counts (AC)** The amount of acceleration is thresholded using a measure specific threshold to estimate upper limb use. The computational
simplicity of this measure makes it a quick and popular approach
(Bailey et al., 2014), (Uswatte et al., 2000), (De Lucena et al.,
2017). However, while an increased amount of acceleration most likely correlates with increased upper-limb use, the feature is not unique to functional movements, and thus overestimates upper limb use. Two types of TAC measures were evaluated in this study: activity counting (De Lucena et al., 2017), and vector magnitude (Bailey et al., 2014).

**Gross Movement (GM) Score**. GM measure (Leuenberger et al., 2017) uses yaw and pitch angles computed using the Madgwick algorithm from the raw acceleration and gyroscope data. If the overall absolute change in yaw and pitch angles is higher than 30° and the absolute pitch of the forearm is within ± 30° in a time window, GM is defined as 1 (indicating functional use), else it is 0. The GM measure exploits the nature of most functional movements to occur in this ‘functional space’, i.e., in the region in front of subject around
his/her chest height.

## GMAC
The AC measures are known to be highly sensitive while having very low specificity, and GM is highly specific but not sensitive (Subash et al., 2022). The hybrid measure — GMAC combines the essential elements of TAC and GM measures. It employs counts with a modified GM measure; the counts are used instead of the absolute change in yaw and pitch angles.

![Alt text](_static/opt_gmac.png)

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

You can obtain the three factors of the dimensionless jerk measure {math}`T^5`,
{math}`A^2`, and {math}`\int_{0}^{T} \left\Vert \frac{d^2 v(t)}{dt^2} \right\Vert^2 dt` 
using the `dimensionless_jerk_factors` function in the `smoothness` module.

```{code} python
>>> dimensionless_jerk_factors(vel, fs=fs, data_type="vel", rem_mean=False)
(1.0, 3.5156249999999982, 652.8558707999949)
```


**References**
[^david2021b]: Flash, Tamar, and Neville Hogan. "The coordination of arm movements: an experimentally confirmed mathematical model." The Journal of Neuroscience 5.7 (1985): 1688-1703.
[^sparc1]: Balasubramanian, Sivakumar, Alejandro Melendez-Calderon, and Etienne Burdet. "A robust and sensitive metric for quantifying movement smoothness." IEEE transactions on biomedical engineering 59.8 (2011): 2126-2136.
[^sparc2]: Balasubramanian, S., Melendez-Calderon, A., Roby-Brami, A., & Burdet, E. (2015). On the analysis of movement smoothness. Journal of neuroengineering and rehabilitation, 12(1), 1-11.
[^ldlj]: Melendez-Calderon, Alejandro, Camila Shirota, and Sivakumar Balasubramanian. "Estimating movement smoothness from inertial measurement units." Frontiers in bioengineering and biotechnology 8 (2021): 558771.
