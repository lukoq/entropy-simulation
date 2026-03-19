from vpython import *
import random
import math
import numpy as np
from concurrent.futures import ProcessPoolExecutor
import os

NUM_WORKERS = os.cpu_count()


def edges(L, edge_color):
    c1 = [vector(-2 * L, -L, -L), vector(2 * L, -L, -L), vector(2 * L, -L, L), vector(-2 * L, -L, L),
          vector(-2 * L, -L, -L)]
    c2 = [vector(-2 * L, L, -L), vector(2 * L, L, -L), vector(2 * L, L, L), vector(-2 * L, L, L),
          vector(-2 * L, L, -L)]

    curve(pos=c1, color=edge_color, radius=0.05)
    curve(pos=c2, color=edge_color, radius=0.05)

    for i in range(4):
        curve(pos=[c1[i], c2[i]], color=edge_color, radius=0.05)


def calculate_entropy(pos, N, L):
    counts = [0] * 16
    for p in pos:
        ix = 0 if p[0] < -L else (1 if p[0] < 0 else (2 if p[0] < L else 3))
        iy = 0 if p[1] < 0 else 4
        iz = 0 if p[2] < 0 else 8
        counts[ix + iy + iz] += 1

    ln_W = math.lgamma(N + 1)
    for n in counts:
        if n > 0:
            ln_W -= math.lgamma(n + 1)
    return ln_W


def collision_chunk(args):
    i_start, i_end, pos, r = args
    results = []
    for i in range(i_start, i_end):
        j_indices = np.arange(i + 1, len(pos))
        if len(j_indices) == 0:
            continue
        diffs = pos[i] - pos[j_indices]
        dists = np.linalg.norm(diffs, axis=1)
        colliding = np.where((dists > 0) & (dists < 2 * r))[0]
        for k in colliding:
            j = int(j_indices[k])
            d = float(dists[k])
            direction = (diffs[k] / d).tolist()
            results.append((i, j, direction, d))
    return results


def apply_collisions(pos, vel, all_results, r):
    for results in all_results:
        for i, j, direction, dist in results:
            d = np.array(direction)
            overlap = 2 * r - dist
            pos[i] += d * (overlap / 2)
            pos[j] -= d * (overlap / 2)

            v_rel = vel[i] - vel[j]
            dot = float(np.dot(v_rel, d))
            if dot < 0:
                v_impact = dot * d
                vel[i] -= v_impact
                vel[j] += v_impact


def handle_wall_collisions_np(pos, vel, dt, L):
    pos += vel * dt

    for axis, limit in [(0, 2 * L), (1, L), (2, L)]:
        over = pos[:, axis] > limit
        under = pos[:, axis] < -limit
        vel[over, axis] *= -1
        vel[under, axis] *= -1
        pos[over, axis] = limit
        pos[under, axis] = -limit


def update_vpython(particles, pos, vel):
    MAX_V = 2.0 * 3 ** 0.5
    for i, p in enumerate(particles):
        p.pos = vector(float(pos[i, 0]), float(pos[i, 1]), float(pos[i, 2]))
        v_mag = float(np.linalg.norm(vel[i]))
        ratio = min(v_mag / MAX_V, 1.0)
        p.color = vector(ratio, 0.0, 1.0 - ratio)


def update_histogram(vel, hist_bars):
    bin_width = 0.5
    max_v_range = 5.0
    num_bins = int(max_v_range / bin_width)
    speeds = np.linalg.norm(vel, axis=1)
    counts, _ = np.histogram(speeds, bins=num_bins, range=(0, max_v_range))
    hist_bars.data = [(i * bin_width + bin_width / 2, int(counts[i])) for i in range(num_bins)]


if __name__ == '__main__':
    scene = canvas(title='Entropy simulation',
                   width=800,
                   height=600,
                   align='left')
    N = 1000
    L = 5
    dt = 0.01
    r = 0.2
    particles = []

    for i in range(N):
        p = sphere(
            pos=vector(random.uniform(-L, -L / 2), random.uniform(-L, -L / 2), random.uniform(-L, -L / 2)),
            radius=r,
            color=color.cyan,
            make_trail=False
        )
        p.v = vector(random.uniform(-2, 2), random.uniform(-2, 2), random.uniform(-2, 2))
        particles.append(p)

    pos = np.array([[p.pos.x, p.pos.y, p.pos.z] for p in particles], dtype=np.float64)
    vel = np.array([[p.v.x, p.v.y, p.v.z] for p in particles], dtype=np.float64)

    room = box(pos=vector(0, 0, 0),
               size=vector(4 * L, 2 * L, 2 * L),
               opacity=0.1,
               color=color.white)

    graph_entropy = graph(title=f'The increase of Entropy (N={N})',
                          xtitle="Time",
                          ytitle="S",
                          width=400,
                          height=300,
                          align='left')
    graph_hist = graph(title=f"Maxwell-Boltzmann distribution (N={N})",
                       xtitle="Speed",
                       ytitle="Number of particles",
                       width=400,
                       height=300,
                       align='left')

    s_curve = gcurve(graph=graph_entropy, color=color.red)
    hist_bars = gvbars(graph=graph_hist, color=color.blue, delta=0.5)

    edges(L, color.cyan)

    chunk_size = N // NUM_WORKERS
    chunks = [(w * chunk_size, N if w == NUM_WORKERS - 1 else (w + 1) * chunk_size)
              for w in range(NUM_WORKERS)]

    t = 0
    with ProcessPoolExecutor(max_workers=NUM_WORKERS) as executor:
        while True:
            rate(60)

            handle_wall_collisions_np(pos, vel, dt, L)

            args = [(start, end, pos, r) for start, end in chunks]
            all_results = list(executor.map(collision_chunk, args))
            apply_collisions(pos, vel, all_results, r)

            update_vpython(particles, pos, vel)

            if int(t / dt) % 10 == 0:
                update_histogram(vel, hist_bars)
                s_curve.plot(t, calculate_entropy(pos, N, L))

            t += dt
