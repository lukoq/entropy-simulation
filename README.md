# Entropy simulation

This program calculates the entropy of the particles contained within the simulated room. Particles begin to spread out from a single point (Low Entropy) to others parts of the room (High Entropy). 
They have random speeds and directions which is requeired in simulation.

In my simulation, my cuboid measures 20x10x10 and a single particle has a radius of 0.2. I divided my entire room into 16 equal parts and I am checking how many partciles are in the each part at a given moment.

Spread out particles realize a specific macrostate. The number of possible microstates in a given macrostate is

$$
W = \frac{N!}{n_1!n_2!...n_m!}
$$

Where:
- $N$ – number of partciles
- $n_i$ – number of particles in the $i$-th part.
- $m$ – total number of parts

$$
\ln(W) = \ln(\frac{N!}{n_1!n_2!...n_m!})
$$

$$
\ln(W) = \ln(N!) - (ln(n_1!)+ln(n_2!)+...+ln(n_m!))
$$

From Boltzmann's entropy formula (where we can ignore $k$)

$$
S = k\cdot\ln(W)
$$

We can calculate the propability of reaching a specific macrostate by

$$
P(A) = \frac{N!}{n_1!n_2!...n_m!\cdot m^N} = \frac{W}{m^N}
$$

It's really hard to calculate for larger numbers so we can approximate the result using a formula

TODO
$$
P(A)\approx\sqrt\frac{2}{\pi N}\cdot e^\frac{-2(m-N/2)^2}{N}
$$


