
# UL Functioning

The `ulfunc` package contains modules for quantifying the different constructs of UL functioning from wearable sensors. 

This pacakge contains the following modules, each of which implements functions for quantifying differnt constructs of UL functioning.

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
| `from_vector_magnitude1` | Compute instantaneous UL use from vector magnitude signal from the [ActiGraph](https://theactigraph.com/) sensor using single threshold. |
| `from_vector_magnitude2` | Compute instantaneous UL use from vector magnitude signal from the [ActiGraph](https://theactigraph.com/) sensor using double threshold. |
| `from_gmac` | Compute UL use from raw accelerometer data by combining information from the Gross Movement score and Activity Counts. |
| `average_uluse` | Compute average UL use.|

## [UL Intensity](ulint)
Module for quantifying instantaneous and avearge UL intensity of use. This module has the following classes and function:
|
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
| `average_ulactivity` | Compute average UL activity from instanenous intensity of use. |
| `Hq` | Computes the overall UL activity fron the average UL activity. |
| `Rq` | Computes the relative UL use. |
| `instantaneous_latindex` | Computes the instantaneous laterality index. |
| `average_latindex` | Computes the average laterality index. |

## [UL Visualizations](ulvisual)
Module for visualization of various UL functioning constructs.
