# bloch_sphere_modular.py
# Bloch Sphere with Z-up, clean inputs, custom gates, and working rotations.

from vpython import *
import numpy as np

# -----------------------
# Scene setup
# -----------------------
scene = canvas(title="✨ Modular Bloch Sphere ✨",
               width=1150, height=760,
               background=vector(0.96, 0.97, 1.0))
scene.up = vector(0,0,1)    # Z is up
scene.forward = vector(-1.0, -0.8, -0.6)

# Sphere
bloch_sphere = sphere(radius=1.0, opacity=0.18,
                      color=vector(0.5,0.7,1.0), shininess=0.8)

# Gridlines
for theta in np.linspace(0, np.pi, 13):
    pts = [vector(np.sin(theta)*np.cos(phi), np.sin(theta)*np.sin(phi), np.cos(theta))
           for phi in np.linspace(0, 2*np.pi, 150)]
    curve(pos=pts, color=color.gray(0.7), radius=0.002)
for phi in np.linspace(0, 2*np.pi, 28):
    pts = [vector(np.sin(theta)*np.cos(phi), np.sin(theta)*np.sin(phi), np.cos(theta))
           for theta in np.linspace(0, np.pi, 150)]
    curve(pos=pts, color=color.gray(0.7), radius=0.002)

# Axes
AX = 1.25
arrow(pos=vector(0,0,0), axis=vector(AX,0,0), shaftwidth=0.024, color=color.red,   emissive=True)
arrow(pos=vector(0,0,0), axis=vector(0,AX,0), shaftwidth=0.024, color=color.green, emissive=True)
arrow(pos=vector(0,0,0), axis=vector(0,0,AX), shaftwidth=0.024, color=color.blue,  emissive=True)
curve(pos=[vector(-1.3,0,0), vector(1.3,0,0)], color=color.red,   radius=0.005, opacity=0.55)
curve(pos=[vector(0,-1.3,0), vector(0,1.3,0)], color=color.green, radius=0.005, opacity=0.55)
curve(pos=[vector(0,0,-1.3), vector(0,0,1.3)], color=color.blue,  radius=0.005, opacity=0.55)

# Labels
labels = [
    label(pos=vector(0,0,1.25),  text='|0⟩',  height=16, box=False, color=color.black, opacity=0),
    label(pos=vector(0,0,-1.25), text='|1⟩',  height=16, box=False, color=color.black, opacity=0),
    label(pos=vector(1.25,0,0),  text='|+⟩',  height=16, box=False, color=color.black, opacity=0),
    label(pos=vector(-1.25,0,0), text='|−⟩',  height=16, box=False, color=color.black, opacity=0),
    label(pos=vector(0,1.25,0),  text='|+i⟩', height=16, box=False, color=color.black, opacity=0),
    label(pos=vector(0,-1.25,0), text='|−i⟩', height=16, box=False, color=color.black, opacity=0),
]

# -----------------------
# Helpers
# -----------------------
def normalize(q):
    n = np.linalg.norm(q)
    return np.array([1+0j, 0+0j]) if n == 0 else q/n

def bloch_coords(psi):
    psi = normalize(psi)
    alpha, beta = psi
    theta = 2*np.arccos(np.clip(np.abs(alpha),0,1))
    phi = (np.angle(beta) - np.angle(alpha)) % (2*np.pi)
    x = np.sin(theta)*np.cos(phi)
    y = np.sin(theta)*np.sin(phi)
    z = np.cos(theta)
    return vector(x,y,z), theta, phi

# -----------------------
# Gates
# -----------------------
def Rx(theta): return np.array([[np.cos(theta/2), -1j*np.sin(theta/2)],
                                [-1j*np.sin(theta/2), np.cos(theta/2)]])
def Ry(theta): return np.array([[np.cos(theta/2), -np.sin(theta/2)],
                                [np.sin(theta/2), np.cos(theta/2)]])
def Rz(theta): return np.array([[np.exp(-1j*theta/2),0],
                                [0,np.exp(1j*theta/2)]])

GATES = {
    "X": np.array([[0,1],[1,0]]),
    "Y": np.array([[0,-1j],[1j,0]]),
    "Z": np.array([[1,0],[0,-1]]),
    "H": (1/np.sqrt(2))*np.array([[1,1],[1,-1]]),
    # Add more: "Name": matrix
}

# -----------------------
# State + visuals
# -----------------------
state = np.array([1+0j,0+0j])  # start |0⟩

arrow_vec = arrow(pos=vector(0,0,0), axis=vector(0,0,1),
                  shaftwidth=0.05, color=vector(1,0.55,0.1), emissive=True)
tip = sphere(pos=arrow_vec.axis, radius=0.06,
             color=vector(1,0.55,0.1), emissive=True,
             make_trail=True, retain=1200, trail_radius=0.006,
             trail_color=vector(1.0,0.6,0.2))

def update_visuals():
    vec, theta, phi = bloch_coords(state)
    arrow_vec.axis = vec
    tip.pos = vec
    p0, p1 = abs(state[0])**2, abs(state[1])**2
    info.text = (f"<pre><b>State</b>\n"
                 f"|ψ⟩ = [{state[0]:.3f}, {state[1]:.3f}]\n"
                 f"P(|0⟩)={p0:.3f}, P(|1⟩)={p1:.3f}\n"
                 f"θ={theta:.3f} rad ({np.degrees(theta):.1f}°)\n"
                 f"φ={phi:.3f} rad ({np.degrees(phi):.1f}°)</pre>")

def apply_gate(U):
    global state
    state = normalize(U @ state)
    update_visuals()

def reset_state():
    global state
    state = np.array([1+0j,0+0j])
    tip.clear_trail()
    update_visuals()

# -----------------------
# Input Handlers
# -----------------------
def set_state(box=None):
    global state
    try:
        txt = state_box.text.replace(" ", "")
        parts = txt.split(",")
        if len(parts) != 2:
            info.text = "<pre><b>Error:</b> Enter two numbers like 1,0 or 1,i</pre>"
            return
        alpha = complex(parts[0].replace("i", "j"))
        beta  = complex(parts[1].replace("i", "j"))
        state = normalize(np.array([alpha, beta], dtype=complex))
        tip.clear_trail()
        update_visuals()
        state_box.text = f"{state[0]:.3f}, {state[1]:.3f}"
    except Exception as e:
        info.text = f"<pre><b>Error parsing state:</b> {e}</pre>"

def apply_custom_gate(box=None):
    global state
    try:
        txt = custom_gate_box.text.strip().replace(" ", "")
        rows = txt.split(";")
        if len(rows) != 2:
            info.text = "<pre><b>Error:</b> Enter matrix as a,b;c,d</pre>"
            return

        mat = []
        for r in rows:
            parts = r.split(",")
            if len(parts) != 2:
                info.text = "<pre><b>Error:</b> Each row must have 2 entries</pre>"
                return
            row = []
            for x in parts:
                try:
                    row.append(complex(x.replace("i","j")))
                except:
                    info.text = f"<pre><b>Error parsing entry:</b> {x}</pre>"
                    return
            mat.append(row)

        U = np.array(mat, dtype=complex)

        # (Optional) check for 2x2 shape
        if U.shape != (2,2):
            info.text = "<pre><b>Error:</b> Must be 2x2 matrix</pre>"
            return

        # (Optional) check unitarity
        if not np.allclose(U.conj().T @ U, np.eye(2), atol=1e-6):
            info.text = "<pre><b>Warning:</b> Matrix not unitary</pre>"

        # Apply gate
        state = normalize(U @ state)
        update_visuals()

    except Exception as e:
        info.text = f"<pre><b>Error parsing gate:</b> {e}</pre>"

# -----------------------
# UI
# -----------------------
wtext(text="<br><b>Custom Gate Input (2×2):</b><br>")
custom_gate_box = winput(type="string", text="1,0;0,1", width=220, bind=lambda box: None)
button(text="Apply Gate", bind=lambda _: apply_custom_gate())

wtext(text="<b>Gates:</b> ")
for name,U in GATES.items():
    button(text=name, bind=lambda _,U=U: apply_gate(U))
button(text="Reset |0⟩", bind=lambda _: reset_state())

wtext(text="   ")
button(text="Clear Trail", bind=lambda _: tip.clear_trail())
checkbox(text=" Trail", bind=lambda cb: setattr(tip,"make_trail",cb.checked), checked=True)

wtext(text="<br><br><b>Custom state:</b><br>")
state_box = winput(type="string", text="1,0", width=150, bind=set_state)

button(text="Set", bind=lambda _: set_state())

# -----------------------
# Sliders + Input Boxes
# -----------------------
wtext(text="<br><br><b>Rotations (θ in π units)</b><br>")

rx_label = wtext(text="Rx=0.00π  ")
ry_label = wtext(text="Ry=0.00π  ")
rz_label = wtext(text="Rz=0.00π  <br>")

# Sliders
rx_slider = slider(min=-1, max=1, value=0, step=0.01, bind=lambda s: update_rotations())
ry_slider = slider(min=-1, max=1, value=0, step=0.01, bind=lambda s: update_rotations())
rz_slider = slider(min=-1, max=1, value=0, step=0.01, bind=lambda s: update_rotations())

# Inputs
rx_input = winput(type="string", text="0.00", width=60, bind=lambda box: on_input(box, rx_slider))
ry_input = winput(type="string", text="0.00", width=60, bind=lambda box: on_input(box, ry_slider))
rz_input = winput(type="string", text="0.00", width=60, bind=lambda box: on_input(box, rz_slider))

def update_rotations():
    """Recompute state from absolute slider values"""
    global state
    # reset to |0>
    state = np.array([1+0j, 0+0j])
    tip.clear_trail()

    # Apply rotations in order Rx -> Ry -> Rz
    theta_x = np.pi * rx_slider.value
    theta_y = np.pi * ry_slider.value
    theta_z = np.pi * rz_slider.value

    state = normalize(Rz(theta_z) @ Ry(theta_y) @ Rx(theta_x) @ state)

    # Update labels & inputs
    rx_label.text = f"Rx={rx_slider.value:.2f}π  "
    ry_label.text = f"Ry={ry_slider.value:.2f}π  "
    rz_label.text = f"Rz={rz_slider.value:.2f}π<br>"
    rx_input.text = f"{rx_slider.value:.2f}"
    ry_input.text = f"{ry_slider.value:.2f}"
    rz_input.text = f"{rz_slider.value:.2f}"

    update_visuals()

def on_input(box, slider_obj):
    """Sync manual entry to slider"""
    try:
        val = float(box.text)
        # Clamp to slider range
        val = max(min(val, slider_obj.max), slider_obj.min)
        slider_obj.value = val
    except:
        box.text = f"{slider_obj.value:.2f}"
    update_rotations()





info = wtext(text="<pre><b>State info</b></pre>")
update_visuals()

# Loop
while True: rate(60)
