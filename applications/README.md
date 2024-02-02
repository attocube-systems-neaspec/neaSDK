# Applications

The folder contains more complex procedures which implement typical 
applications of the SDK.

### Tip Based Approach Curve

Measurement mode "Retraction Curve (Tip)" of Raman sphere. The sample 
is kept a static position while the tip is moved upwards step by step. 
A Raman spectrum is recorded after each step. There are two Storyboards, 
one for Contact Mode and Tapping Mode each.

### Jumping Mode

Measurement mode "Jumping Mode" of Raman sphere. 2D hyperspectral imaging 
mode where a Raman spectrum is recorded in contact and out of contact at 
each pixel position. Tip retraction is done by moving the tip upwards while 
the sample is at a static position. There are two Storyboards, one for 
Contact Mode and Tapping Mode each.

### Parabola Scan

Python script to spatially map the laser beam by scanning the parabolic
mirror in 3 axes. Connects to microscope as stand-alone script and
returns scan results as `.png` and `.h5`.