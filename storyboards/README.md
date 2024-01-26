# Storyboard Examples

This is a collection of various storyboard definitions which do not have a standard application within neaSCAN. Available Examples are

### AdjustTappingAmplitudeInContact.json

Alternative demodulation mode based on standard Fourier demodulation. Extends the standard definition of the Z feedback loop. This allows to change the tapping voltage while in contact by estimating and adjusting the tapping setpoint.

### ApproachRetractionCurve.json

Extension to standard approach curve. Initially, performs a true approach curve and continues with a retraction curve as soon as AFM setpoint is reached. Uses identical scan parameters as standard approach curve but performs both approach and retraction motion without changing scan state. This means if 100 px are used for z range, about 50 px are used for approach motion and remaining pixels for retraction motion. 

### HeadZRegulation.json

Performs standard AFM imaging but uses the piezo of the head to regulate AFM height while sample Z is frozen on a fixed value throughout the scan. AFM height (= calibrated Head Offset) is written to channel M5A. 

### HysteresisCorrection.json

Scan procedure aiming to open-loop XY scanner like the cryo-neaSCOPE. Allows defining a polynom of 3rd order which defines a non-linear scan motion in fast axis (x axis).

### SpiralScan.json

Defines a scan route which is an Archimeadean spiral.
