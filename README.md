# Entropy simulation

This program calculates the entropy of the particles contained within the simulated room. Particles begin to spread out from a single point (Low Entropy) to others parts of the room (High Entropy). 
They have random speeds and directions which is requeired in simulation.

In my simulation, my cuboid measures $4L$ x $2L$ x $2L$ ($L=5$) and a single particle has a radius of $0.2$. I divided my entire room into $16$ equal parts and I am checking how many partciles are in the each part at a given moment.
<p align="left">
  <img width="300" height="300" alt="1" src="https://github.com/user-attachments/assets/e631213b-2fd3-4d83-9dee-2bed20283019" />
  <img width="300" height="300" alt="2" src="https://github.com/user-attachments/assets/c96b7eae-9c23-4ede-a47c-64268c8db507" />
  <img width="300" height="300" alt="3" src="https://github.com/user-attachments/assets/1452ef51-25e7-47c8-ba62-3029387b83f7" />
</p>


```
def calculate_entropy():
    counts = [0] * 16

    # counting...
    
    # W = N! / (n1! * n2! * ... * n8!)
    # ln(W) = ln(N!) - sum(ln(ni!))
    # ln(n!) is math.lgamma(n+1)
    ln_W = math.lgamma(N + 1)
    for n in counts:
        if n > 0:
            ln_W -= math.lgamma(n + 1)
    return ln_W
```

I ran my simulation for various number of particles ($N$). For $N ≥ 1000$ it is better to use multiprocessing in the file `entropy-simul-multiprocessing.py`. The results in the table show the value calculated based on the computer simulation compared with the result expected according to theoretical predictions.

| Number of partciles (N) | Stirling's approximation | Simulation results | Difference (%) |
|-----------------------|--------------------------|---------------------------|-------------|
| 50                    | ~138.63                  |      113                  | 18.49%      |
| 100                   | ~277.26                  |      248                  | 10.55%      |
| 500                   | ~1386.29                 |      1350                 | 2.62%       |
| 1000                  | ~2772.59                 |      2720                 | 1.19%       |
| 5000                  | ~13862.94                |      13900                | 0.27%       |

## The math behind

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
S = k \cdot \ln(W)
$$

We can calculate the propability of reaching a specific macrostate by

$$
P(A) = \frac{N!}{n_1!n_2!...n_m! \cdot m^N} = \frac{W}{m^N}
$$

It's really hard to calculate for larger numbers. For the 2-parts system, we can approximate the result using a formula (Gaussian PDF):

$$
P(A_x) \approx \sqrt\frac{2}{\pi N} \cdot e^{-2(x-N/2)^2/N}
$$

<div align="center">
<img width="648" height="442" alt="Figure_1" src="https://github.com/user-attachments/assets/9745e5e4-d249-40a9-b5bc-47909693aa79" />
</div>
<br>

As we can see the highest point of the graph lies at $x=5$. This is the state with the highest entropy and the largest number of microstates. With that in mind, the result for a larger number of parts ($m>2$) can be predicted. We will always achieve maximum Entropy in the state with the greatest dispersion and this is the most likely case. Entropy will always triumph.

The greatest dispersion of particles across a room means

$$
n_{ideal} = \frac{N}{m}
$$

- $n_{ideal}$ – the integer value that each part ($n_1$, $n_2$,... $n_m$) must contain to reach maximum Entropy by entire cuboid.

$$
S_{max} = \ln(N!) - \sum_{i=0}^{m}(\ln(n_{ideal}!))
$$

$$
S_{max} = \ln(N!) - m\cdot \ln(\frac{N}{m}!)
$$

According to Stirling's approximation $$\ln(n!) \approx n \cdot \ln(n) - n$$

$$
S_{max} \approx N\cdot\ln(N) - N - m \cdot [\frac{N}{m} \cdot \ln(\frac{N}{m}) - \frac{N}{m}]
$$

$$
S_{max} \approx N\cdot\ln(N) - N \cdot \ln(\frac{N}{m})
$$

$$
S_{max} \approx N(\ln(N) - \ln(\frac{N}{m}))
$$

$$
S_{max} \approx N \cdot \ln(m)
$$
