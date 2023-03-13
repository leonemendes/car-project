import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

'''
The code also implements the net force and torque on the vehicle, 
integrates the velocities and positions using the midpoint method, 
and computes the roll, pitch, and yaw angles as well as the lateral 
and longitudinal velocities.
'''

# Define vehicle parameters
m = 1000.0  # mass in kg
Ixx = 2000.0  # moment of inertia around x-axis in kg-m^2
Iyy = 3000.0  # moment of inertia around y-axis in kg-m^2
Izz = 4000.0  # moment of inertia around z-axis in kg-m^2
lf = 1.5  # distance from CG to front axle in m
lr = 1.5  # distance from CG to rear axle in m
Cf = 80000.0  # cornering stiffness of front tires in N/rad
Cr = 120000.0  # cornering stiffness of rear tires in N/rad
vx = 10.0  # longitudinal velocity of the vehicle in m/s

# Define initial conditions
x0 = 0.0  # initial x position in meters
y0 = 0.0  # initial y position in meters
z0 = 0.0  # initial z position in meters
phi0 = 0.0  # initial roll angle in radians
theta0 = 0.0  # initial pitch angle in radians
psi0 = 0.0  # initial yaw angle in radians
v0 = vx  # initial velocity in m/s

# Define simulation parameters
dt = 0.01  # time step in seconds
T = 10.0  # total simulation time in seconds

# Define net force and moment functions
def net_force(t):
    # Example function that returns a constant force of 1000 N
    return 1000.0

def net_moment(t):
    # Example function that returns a constant moment of 100 Nm around z-axis
    return np.array([0.0, 0.0, 100.0])

# Initialize arrays to store simulation results
t_array = np.arange(0, T, dt)
x_array = np.zeros_like(t_array)
y_array = np.zeros_like(t_array)
z_array = np.zeros_like(t_array)
phi_array = np.zeros_like(t_array)
theta_array = np.zeros_like(t_array)
psi_array = np.zeros_like(t_array)
v_array = np.zeros_like(t_array)

# Set initial conditions
x_array[0] = x0
y_array[0] = y0
z_array[0] = z0
phi_array[0] = phi0
theta_array[0] = theta0
psi_array[0] = psi0
v_array[0] = v0

# Loop over time steps
for i in range(1, len(t_array)):
    # Compute slip angles
    alpha_f = np.arctan2((vy + lf * psi_dot), vx) - delta
    alpha_r = np.arctan2((vy - lr * psi_dot), vx)
    
    # Compute lateral forces
    Fyf = Cf * alpha_f
    Fyr = Cr * alpha_r
    
    # Compute net force and moment
    Fx = net_force(t_array[i])
    Fy = Fyf + Fyr
    M = net_moment(t_array[i])
    
    # Compute acceleration and angular acceleration
    R = np.array([
        np.cos(theta_array[i-1])*np.cos(psi_array[i-1]), 
        np.sin(phi_array[i-1])*np.sin(theta_array[i-1])*np.cos(psi_array[i-1]) - np.cos(phi_array[i-1]) *np.sin(psi_array[i-1]),
        np.sin(phi_array[i-1])*np.cos(theta_array[i-1]),
        np.sin(phi_array[i-1])*np.sin(theta_array[i-1])*np.sin(psi_array[i-1]) + np.cos(phi_array[i-1])*np.cos(psi_array[i-1]),
        np.sin(phi_array[i-1])*np.sin(theta_array[i-1])*np.cos(psi_array[i-1]) - np.cos(phi_array[i-1])*np.sin(psi_array[i-1]),
        np.cos(phi_array[i-1])*np.cos(theta_array[i-1]),
        np.cos(phi_array[i-1])*np.sin(theta_array[i-1])*np.sin(psi_array[i-1]) + np.sin(phi_array[i-1])*np.cos(psi_array[i-1]),
        np.cos(phi_array[i-1])*np.sin(theta_array[i-1])*np.cos(psi_array[i-1]) - np.sin(phi_array[i-1])*np.sin(psi_array[i-1]),
        np.sin(theta_array[i-1]),
        np.cos(theta_array[i-1])*np.sin(psi_array[i-1]),
        np.cos(theta_array[i-1])*np.cos(psi_array[i-1])
    ]).reshape((3, 3))

    a = np.array([0.0, 0.0, Fx/m])
    v_cg = R.T @ np.array([vx, vy, vz])
    a_cg = a + (M @ R).T @ np.array([0.0, 0.0, 1.0]).T/m - np.cross(psi_dot*np.array([0.0, 0.0, 1.0]), v_cg)

    # Integrate velocities and positions using midpoint method
    v_cg_half = v_cg + a_cg * dt/2
    v_cg = v_cg + a_cg * dt
    x_array[i] = x_array[i-1] + v_cg_half[0] * dt
    y_array[i] = y_array[i-1] + v_cg_half[1] * dt
    z_array[i] = z_array[i-1] + v_cg_half[2] * dt
    
    # Integrate roll, pitch, and yaw angles
    p_dot = phi_dot + (theta_dot * np.sin(phi_array[i-1]) + psi_dot * np.cos(phi_array[i-1])) * np.tan(theta_array[i-1])
    q_dot = theta_dot * np.cos(phi_array[i-1]) - psi_dot * np.sin(phi_array[i-1])
    r_dot = (theta_dot * np.sin(phi_array[i-1]) + psi_dot * np.cos(phi_array[i-1])) / np.cos(theta_array[i-1])
    phi_array[i] = phi_array[i-1] + p_dot * dt
    theta_array[i] = theta_array[i-1] + q_dot * dt
    psi_array[i] = psi_array[i-1] + r_dot * dt
    
    # Integrate velocity
    v_array[i] = np.linalg.norm(v_cg)
    vx = v_array[i]
    
    # Compute angular velocities
    phi_dot = p_dot
    theta_dot = q_dot
    psi_dot = r_dot
    
    # Compute lateral and longitudinal velocities
    vy = v_cg[1]
    vz = v_cg[2]

fig = plt.figure()
ax = fig.gca(projection='3d')

# Plot vehicle trajectory
ax.plot(x_array, y_array, z_array)

# Set axis labels
ax.set_xlabel('X (m)')
ax.set_ylabel('Y (m)')
ax.set_zlabel('Z (m)')

plt.show()