# bloch_pretty.py
# Beautiful Bloch Sphere with labeled states, clean info panel, and trail controls

from vpython import *
import numpy as np

# -----------------------
# State and scene setup
# -----------------------
state = np.array([1+0j, 0+0j])   # start at |0>

scene = canvas(title="✨ Bloch Sphere ✨",
               width=1100, height=750, background=vector(0.96,0.97,1))

# Reorient so Z is up
scene.up = vector(0,0,1)
scene.forward = vector(0,1,0)
# Lighting
distant_light(direction=vector(1,2,3), color=color.white)
local_light(pos=vector(2,2,2), color=color.gray(0.8))

# Sphere (semi-transparent, blueish)
bloch_sphere = sphere(radius=1, opacity=0.18,
                      color=vector(0.5,0.7,1), shininess=0.8)

# Gridlines
for theta in np.linspace(0, np.pi, 13):
    pts = [vector(np.sin(theta)*np.cos(phi), np.sin(theta)*np.sin(phi), np.cos(theta))
           for phi in np.linspace(0, 2*np.pi, 140)]
    curve(pos=pts, color=color.gray(0.7), radius=0.002)
for phi in np.linspace(0, 2*np.pi, 28):
    pts = [vector(np.sin(theta)*np.cos(phi), np.sin(theta)*np.sin(phi), np.cos(theta))
           for theta in np.linspace(0, np.pi, 140)]
    curve(pos=pts, color=color.gray(0.7), radius=0.002)

# Axes
arrow(pos=vector(0,0,0), axis=vector(1.25,0,0), shaftwidth=0.024, color=color.red, emissive=True)
arrow(pos=vector(0,0,0), axis=vector(0,1.25,0), shaftwidth=0.024, color=color.green, emissive=True)
arrow(pos=vector(0,0,0), axis=vector(0,0,1.25), shaftwidth=0.024, color=color.blue, emissive=True)
curve(pos=[vector(-1.3,0,0), vector(1.3,0,0)], color=color.red, radius=0.005, opacity=0.6)
curve(pos=[vector(0,-1.3,0), vector(0,1.3,0)], color=color.green, radius=0.005, opacity=0.6)
curve(pos=[vector(0,0,-1.3), vector(0,0,1.3)], color=color.blue, radius=0.005, opacity=0.6)

# State labels (with billboard effect)
state_labels = [
    label(pos=vector(0,0,1.25), text='|0⟩', height=16, box=False, color=color.black, opacity=0),
    label(pos=vector(0,0,-1.25), text='|1⟩', height=16, box=False, color=color.black, opacity=0),
    label(pos=vector(1.25,0,0), text='|+⟩', height=16, box=False, color=color.black, opacity=0),
    label(pos=vector(-1.25,0,0), text='|−⟩', height=16, box=False, color=color.black, opacity=0),
    label(pos=vector(0,1.25,0), text='|+i⟩', height=16, box=False, color=color.black, opacity=0),
    label(pos=vector(0,-1.25,0), text='|−i⟩', height=16, box=False, color=color.black, opacity=0),
]

# State arrow + tip sphere
state_arrow = arrow(pos=vector(0,0,0), axis=vector(0,0,1), shaftwidth=0.05,
                    color=vector(1,0.55,0.1), shininess=1, emissive=True)
tip = sphere(pos=state_arrow.axis, radius=0.06, color=vector(1,0.55,0.1), emissive=True)

# -----------------------
# Trail system
# -----------------------
trail_enabled = True
trail = curve(radius=0.01, color=vector(1.0, 0.6, 0.2))  # manual trail curve

def update_trail():
    """Append new point if trail is enabled"""
    if trail_enabled:
        trail.append(pos=tip.pos)

def toggle_trail(cb):
    """Toggle trail drawing"""
    global trail_enabled
    trail_enabled = cb.checked
    if not trail_enabled:
        trail.clear()   # clears instantly when unchecked

def clear_trail_btn(_=None):
    """Clear trail via button"""
    trail.clear()

# Info panel
info = wtext(text="<pre><b>State Info</b>\n</pre>")

# -----------------------
# Quantum gates & helpers
# -----------------------
X = np.array([[0,1],[1,0]], dtype=complex)
Y = np.array([[0,-1j],[1j,0]], dtype=complex)
Z = np.array([[1,0],[0,-1]], dtype=complex)
H = (1/np.sqrt(2))*np.array([[1,1],[1,-1]], dtype=complex)

def Rx(theta): return np.array([[np.cos(theta/2), -1j*np.sin(theta/2)],
                                [-1j*np.sin(theta/2), np.cos(theta/2)]], dtype=complex)
def Ry(theta): return np.array([[np.cos(theta/2), -np.sin(theta/2)],
                                [np.sin(theta/2),  np.cos(theta/2)]], dtype=complex)
def Rz(theta): return np.array([[np.exp(-1j*theta/2), 0],
                                [0, np.exp(1j*theta/2)]], dtype=complex)

def normalize(q):
    n = np.linalg.norm(q)
    return np.array([1+0j,0]) if n==0 else q/n

def bloch_coords(psi):
    psi_n = normalize(psi)
    alpha, beta = psi_n
    theta = 2*np.arccos(np.clip(np.abs(alpha),0,1))
    phi = (np.angle(beta)-np.angle(alpha)) % (2*np.pi)
    return vector(np.sin(theta)*np.cos(phi), np.sin(theta)*np.sin(phi), np.cos(theta)), theta, phi

def update_visuals():
    vec, theta, phi = bloch_coords(state)
    state_arrow.axis = vec
    tip.pos = vec
    prob0, prob1 = abs(state[0])**2, abs(state[1])**2
    info.text = (f"<pre><b>Bloch Sphere State</b>\n"
                 f"  |ψ⟩ = [{state[0]:.3f}, {state[1]:.3f}]\n"
                 f"  P(|0⟩) = {prob0:.3f}    P(|1⟩) = {prob1:.3f}\n"
                 f"  θ = {theta:.3f} rad  ({np.degrees(theta):.1f}°)\n"
                 f"  φ = {phi:.3f} rad  ({np.degrees(phi):.1f}°)\n</pre>")

def apply_gate(U):
    global state
    state = normalize(U @ state)
    update_visuals()

def reset_state():
    global state
    state = np.array([1+0j, 0+0j])
    trail.clear()
    update_visuals()

# -----------------------
# Controls
# -----------------------
wtext(text="<b>Gates:</b>  ")
button(text="X", bind=lambda _:apply_gate(X))
button(text="Y", bind=lambda _:apply_gate(Y))
button(text="Z", bind=lambda _:apply_gate(Z))
button(text="H", bind=lambda _:apply_gate(H))
button(text="Reset", bind=lambda _:reset_state())
wtext(text="   ")
button(text="Clear Trail", bind=clear_trail_btn)
checkbox(text=" Trail", bind=toggle_trail, checked=True)

wtext(text="<br><br><b>Rotations (θ in π units):</b><br>")
slider(bind=lambda s:(apply_gate(Rx(s.value*np.pi)), setattr(s,'value',0)),
       min=-0.5,max=0.5,step=0.05,value=0); wtext(text=" Rx  ")
slider(bind=lambda s:(apply_gate(Ry(s.value*np.pi)), setattr(s,'value',0)),
       min=-0.5,max=0.5,step=0.05,value=0); wtext(text=" Ry  ")
slider(bind=lambda s:(apply_gate(Rz(s.value*np.pi)), setattr(s,'value',0)),
       min=-0.5,max=0.5,step=0.05,value=0); wtext(text=" Rz<br>")

# Initialize
update_visuals()

# -----------------------
# Main loop
# -----------------------
while True:
    rate(60)
    update_trail()
    for lbl in state_labels:  # billboard effect
        lbl.align = "center"
        lbl.up = scene.forward
