from vpython import *
import random
import math

N = 50
L = 5
dt = 0.01

scene = canvas(title='Entropy simulation', width=800, height=600)

particles = []
for i in range(N):
    p = sphere(
        pos=vector(random.uniform(-L, -L / 2), random.uniform(-L, -L / 2), random.uniform(-L, -L / 2)),
        radius=0.2,
        color=color.cyan,
        make_trail=False
    )
    p.v = vector(random.uniform(-2, 2), random.uniform(-2, 2), random.uniform(-2, 2))
    particles.append(p)


def edges(L, edge_color):
    c1 = [vector(-2*L, -L, -L), vector(2*L, -L, -L), vector(2*L, -L, L), vector(-2*L, -L, L), vector(-2*L, -L, -L)]
    c2 = [vector(-2*L, L, -L), vector(2*L, L, -L), vector(2*L, L, L), vector(-2*L, L, L), vector(-2*L, L, -L)]

    curve(pos=c1, color=edge_color, radius=0.05)
    curve(pos=c2, color=edge_color, radius=0.05)

    for i in range(4):
        curve(pos=[c1[i], c2[i]], color=edge_color, radius=0.05)


def calculate_entropy():
    counts = [0] * 8
    for p in particles:
        ix = 0 if p.pos.x < 0 else 1
        iy = 0 if p.pos.y < 0 else 2
        iz = 0 if p.pos.z < 0 else 4
        counts[ix + iy + iz] += 1

    # W = N! / (n1! * n2! * ... * n8!)
    # ln(W) = ln(N!) - sum(ln(ni!))
    # ln(n!) is math.lgamma(n+1)
    ln_W = math.lgamma(N + 1)
    for n in counts:
        if n > 0:
            ln_W -= math.lgamma(n + 1)
    return ln_W


room = box(pos=vector(0, 0, 0),
           size=vector(4 * L, 2 * L, 2 * L),
           opacity=0.1,
           color=color.white)

edges(L, color.cyan)
t = 0


def handle_self_collisions(particles):
    n = len(particles)
    for i in range(n):
        for j in range(i + 1, n):
            p1 = particles[i]
            p2 = particles[j]

            diff = p1.pos - p2.pos
            dist = diff.mag

            r = p1.radius
            if dist < 2 * r:
                overlap = 2 * r - dist
                direction = diff.norm()
                p1.pos += direction * (overlap / 2)
                p2.pos -= direction * (overlap / 2)

                v_rel = p1.v - p2.v
                if v_rel.dot(direction) < 0:
                    v_impact = v_rel.dot(direction) * direction
                    p1.v -= v_impact
                    p2.v += v_impact


def handle_wall_collisions(particles):
    for p in particles:
        p.pos += p.v * dt
        if abs(p.pos.x) >= L:
            p.v.x *= -1
            p.pos.x = L if p.pos.x > 0 else -L
        if abs(p.pos.y) >= L:
            p.v.y *= -1
            p.pos.y = L if p.pos.y > 0 else -L
        if abs(p.pos.z) >= L:
            p.v.z *= -1
            p.pos.z = L if p.pos.z > 0 else -L


def update_particle_colors(particles):
    MAX_V = 15.0
    for p in particles:
        v_mag = p.v.mag
        ratio = min(v_mag / MAX_V, 1.0)

        r = ratio
        g = 0.0
        b = 1.0 - ratio
        p.color = vector(r, g, b)


while True:
    rate(60)
    handle_wall_collisions(particles)
    handle_self_collisions(particles)
    update_particle_colors(particles)
    t += dt
