from vpython import *
import random

N1, m1, T1 = 10, 1, 300
N2, m2, T2 = 10, 3, 500

L = 10
dt = 0.01
divider_width = 0.5

kb = 1.38e-2

scene = canvas(width=800, height=400)
divider_active = True
partition = box(pos=vector(0, 0, 0), size=vector(0.5, 20, 20), color=color.white, opacity=divider_width)

particles = []


def edges(L, edge_color):
    c1 = [vector(-2 * L, -L, -L), vector(2 * L, -L, -L), vector(2 * L, -L, L), vector(-2 * L, -L, L),
          vector(-2 * L, -L, -L)]
    c2 = [vector(-2 * L, L, -L), vector(2 * L, L, -L), vector(2 * L, L, L), vector(-2 * L, L, L), vector(-2 * L, L, -L)]

    curve(pos=c1, color=edge_color, radius=0.05)
    curve(pos=c2, color=edge_color, radius=0.05)

    for i in range(4):
        curve(pos=[c1[i], c2[i]], color=edge_color, radius=0.05)


def handle_divider_collisions(particles):
    for p in particles:
        prev_x = p.pos.x
        p.pos += p.v * dt
        if divider_active:
            if p.v.x > 0 and prev_x <= -divider_width < p.pos.x:
                p.v.x = -abs(p.v.x)
                p.pos.x = - divider_width - 0.01
            elif p.v.x < 0 and prev_x >= divider_width > p.pos.x:
                p.v.x = abs(p.v.x)
                p.pos.x = divider_width + 0.01


def handle_wall_collisions(particles):
    for p in particles:
        if abs(p.pos.x) >= 2 * L:
            p.v.x *= -1
            p.pos.x = 2 * L if p.pos.x > 0 else -2 * L
        if abs(p.pos.y) >= L:
            p.v.y *= -1
            p.pos.y = L if p.pos.y > 0 else -L
        if abs(p.pos.z) >= L:
            p.v.z *= -1
            p.pos.z = L if p.pos.z > 0 else -L


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


def update_particle_colors(particles):
    MAX_V = 2.0 * sqrt(3)
    for p in particles:
        v_mag = p.v.mag
        ratio = min(v_mag / MAX_V, 1.0)

        r = ratio
        g = 0.0
        b = 1.0 - ratio
        p.color = vector(r, g, b)


def spawn_gas(N, mass, temp, x_range, p_color):
    v_mag = sqrt(3 * kb * temp / mass)
    for i in range(N):
        p = sphere(pos=vector(random.uniform(x_range[0], x_range[1]),
                              random.uniform(-2, 2), random.uniform(-2, 2)),
                   radius=0.2, color=p_color)
        p.m = mass
        p.v = vector.random() * v_mag
        particles.append(p)


def open_divider():
    global divider_active
    divider_active = False
    partition.visible = False


button(bind=open_divider, text="Otwórz ścianę")
edges(L, color.cyan)
spawn_gas(N1, m1, T1, [-18, -1], color.blue)
spawn_gas(N2, m2, T2, [1, 18], color.red)


t = 0
while True:
    rate(60)
    handle_divider_collisions(particles)
    handle_wall_collisions(particles)
    handle_self_collisions(particles)
    update_particle_colors(particles)

    t += dt
