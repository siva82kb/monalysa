# Movement Smoothness

Smooth movements are a hallmark of well developed and learned motor behavior[^flash]. 
Movement smoothness is one of the most commonly used movement quality constrcuts 
that is of interest in various field, such as movement science, motor control/learning,
biomechanics, and neurorehabilitation. 

> **Definition.** **Movement smoothness** is a measure of the amount of intermittency 
> or fluency in a given movement.

Intuitively, movement smoothness is a easy consturct to understand. When shown two 
movements one can failry consistent rate the relative smoothness of two movements. However, 
a valid, robust and sensitive general measure of smoothness for use with 
different types of movements, measured movement variables, and technologies has been 
a struggle. Two candidate measures have emerged as the most popular measures of smoothness 
in the last 10 years[^sparc1] [^sparc2] [^ldlj]: **spectral arc length (SPARC)** 
and **log dimensionless jerk (LDLJ)**.

The smoothness module of the monalysa library contains functions for computing the smoothness 
of discrete movements using the SPARC and LDLJ; along with some variants of the LDLJ --  
dimensionless jerk and the LDLJ computed from accelerometer data. The detailed module 
documentation can be found [here](smoothnessdoc).

## Properties of Smoothness Measures
A measure of movement smoothness must satisfy the following properties:
1. **It is dimensionless**, i.e. the value of a smoothness of a movement must be 
independent of its amplitude and duration. 

    Let {math}`m(t)` by the kinematics of a movement {math}`M`, and let {math}`\lambda(m(t))` 
    be the smoothness of this movement; note, that {math}`\lambda\left(\cdot\right)` is a 
    smoothness measure. Then, uniform scaling of the amplitude and duration of {math}`m(t)` 
    does not impact the smoothness of the movement, i.e.
    ```{math}
        \lambda\left(A \cdot m\left(\frac{t}{T}\right)\right) = \lambda\left(m(t)\right)
    ```

2. **It decreases with the number of submovements**. When we view the movement as 
being composed of individual submovements, the smoothness of the movement should 
decrease with increase in the number of submovements.

3. **It decreases with increase in the inter-submovement interval**.

In addition to these, the measures must also be robust to noise and sensitive to 
small changes in the movement profile.

Balasubramanian et. al[^sparc1] showed that the SPARC and the LDLJ satisfy the above 
properties.

## Log Dimensionless Jerk (LDLJ)
Jerk -- the third derivative of position -- has become intimately associated with the 
concept of movement smoothness ever since Flash and Hogan published their minimum 
jerk model for describing discrte point-to-point reaching movements[^flash].




**References**
[^flash]: Flash, Tamar, and Neville Hogan. "The coordination of arm movements: an experimentally confirmed mathematical model." The Journal of Neuroscience 5.7 (1985): 1688-1703.
[^sparc1]: Balasubramanian, Sivakumar, Alejandro Melendez-Calderon, and Etienne Burdet. "A robust and sensitive metric for quantifying movement smoothness." IEEE transactions on biomedical engineering 59.8 (2011): 2126-2136.
[^sparc2]: Balasubramanian, S., Melendez-Calderon, A., Roby-Brami, A., & Burdet, E. (2015). On the analysis of movement smoothness. Journal of neuroengineering and rehabilitation, 12(1), 1-11.
[^ldlj]: Melendez-Calderon, Alejandro, Camila Shirota, and Sivakumar Balasubramanian. "Estimating movement smoothness from inertial measurement units." Frontiers in bioengineering and biotechnology 8 (2021): 558771.
