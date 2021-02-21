# fake-fluid

Main purpose of this case is to help us debugging. 

# Setup

The case provides the following load at the left face of the flat:

```
F(y) = (y*F_max/H, 0)
```

The force is linearly increasing from 0 to `F_max` and constant over time.

One can easily run this case together with other cases.

At the end of the simulation the script plots the displacement in x and y direction of the top-left corner of the flap.

# Use FEniCS as Solid:

Run

```
~/tutorials/perpendicular-flap/fluid-fake$ python3 fake-fluid.py 
```

and

```
~/tutorials/perpendicular-flap/solid-fenics$ python3 perp-flap.py 
```

![](flap_fenics.png)

# Use CalculiX as Solid:

Run

```
~/tutorials/perpendicular-flap/fluid-fake$ python3 fake-fluid.py
```

and

```
~/tutorials/perpendicular-flap/solid-calculix$ ./run.sh
```

![](flap_ccx.png)

# Some Observations

* Frequency for CalculiX is slightly higher
* Amplitude for FEnICS is slightly higher
