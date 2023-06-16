
# UL Functioning

The `ulfunc` package contains modules for quantifying the different constructs of UL functioning from wearable sensors. 

This pacakge contains the following modules, each of which implements functions for quantifying differnt constructs of UL functioning.

```{toctree}
:caption: 'Contents:'
:maxdepth: 1

uluse
ulint
```


## UL Use [{py:mod}`monalysa.ulfunc.uluse`]
Module for quantifying instantaneous and average UL use. This module has the following classes and function:
|
### Functions
| Name | Description |
|:-----|:------------|
| `from_vector_magnitude1`| Compute instantaneous UL use from vector magnitude signal from the [ActiGraph](https://theactigraph.com/) sensor using single threshold. |
| `from_vector_magnitude2` | Compute instantaneous UL use from vector magnitude signal from the [ActiGraph](https://theactigraph.com/) sensor using double threshold. |
| `from_gmac` | Compute UL use from raw accelerometer data by combining information from the Gross Movement score and Activity Counts. |
| `average_uluse` | Compute average UL use.|

## UL Intensity [{py:mod}`monalysa.ulfunc.ulint`]
Module for quantifying instantaneous and avearge UL intensity of use. This module has the following classes and function:
|
### Functions
| Name | Description |
|:-----|:------------|
| `from_vector_magnitude`| Compute instantaneous UL intensity of use from the vector magnitude signal from the [ActiGraph](https://theactigraph.com/) sensor. |
| `average_intuse` | Compute average UL intensity of use.|

