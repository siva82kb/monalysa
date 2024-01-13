
# UL Functioning

The `ulfunc` package contains modules for quantifying the different constructs of UL functioning from wearable sensors. 

This package contains the following modules, each of which implements functions for quantifying different constructs of UL functioning.

```{toctree}
:caption: 'Contents:'
:maxdepth: 1

uluse
ulint
ulmeasures
ulvisual
```

## [UL Use](uluse)
Module for quantifying instantaneous and average UL use. This module has the following classes and function:

### Functions
| Name | Description |
|:-----|:------------|
| `from_vector_mag` | Compute instantaneous UL use from vector magnitude signal from the [ActiGraph](https://theactigraph.com/) sensor using single threshold. |
| `from_vector_mag_dblth` | Compute instantaneous UL use from vector magnitude signal from the [ActiGraph](https://theactigraph.com/) sensor using double threshold. |
| `from_gmac` | Compute UL use from raw accelerometer data by computing the forearm pitch angle and acceleration magnitude. |
| `estimate_accl_pitch` | Compute the forearm pitch angle from a wrist-worn accelerometer. |
| `estimate_accl_mag` | Compute the acceleration magnitude from the accelerometer by removing gravity through highpass filtering. |
| `detector_with_hystersis` | Compute the binary output from a signal by using a decision rule with hysteresis. |
| `average_uluse` | Compute average UL use.|

## [UL Intensity](ulint)
Module for quantifying instantaneous and average UL intensity of use. This module has the following classes and function:

### Functions
| Name | Description |
|:-----|:------------|
| `from_vector_magnitude`| Compute instantaneous UL intensity of use from the vector magnitude signal from the [ActiGraph](https://theactigraph.com/) sensor. |
| `average_intuse` | Compute average UL intensity of use.|

## [UL Measures](ulmeasures)
Module for quantifying different UL functioning measures. This module has the following classes and function:
|
### Functions
| Name | Description |
|:-----|:------------|
| `average_ulactivity` | Compute average UL activity from instantaneous intensity of use. |
| `Hq` | Computes the overall UL activity from the average UL activity. |
| `Rq` | Computes the relative UL use. |
| `instantaneous_latindex` | Computes the instantaneous laterality index. |
| `average_latindex` | Computes the average laterality index. |

## [UL Visualizations](ulvisual)
Module for visualization of various UL functioning constructs.
