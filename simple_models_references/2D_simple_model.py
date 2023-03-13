import numpy as np
import matplotlib.pyplot as plt

'''
This code plots the vehicle's trajectory, yaw angle, and velocity over time. 
You can modify the vehicle parameters, initial conditions, and net force/moment 
functions to model different vehicles and driving scenarios. 
'''

# Define vehicle parameters
m = 1000.0  # mass in kg
Iz = 2500.0  # moment of inertia around z-axis in kg-m^2
lf = 1.5  # distance from CG to front axle in m
lr = 1.5  # distance from CG to rear axle in m
Cf = 80000.0  # cornering stiffness of front tires in N/rad
Cr = 120000.0  # cornering stiffness of rear tires in N/rad
vx = 10.0  # longitudinal velocity of the vehicle in m/s

# Define initial conditions
x0 = 0.0  # initial x position in meters
y0 = 0.0  # initial y position in meters
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
    # Example function that returns a constant moment of 100 Nm
    return 100.0

# Initialize arrays to store simulation results
t_array = np.arange(0, T, dt)
x_array = np.zeros_like(t_array)
y_array = np.zeros_like(t_array)
psi_array = np.zeros_like(t_array)
v_array = np.zeros_like(t_array)

# Set initial conditions
x_array[0] = x0
y_array[0] = y0
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
    Mz = net_moment(t_array[i])
    
    # Compute acceleration and angular acceleration
    a = (Fx * np.cos(psi_array[i-1]) - Fy * np.sin(psi_array[i-1])) / m
    alpha = (Fyf * lf * np.cos(delta) - Fyr * lr) / Iz
    
    # Update velocity, position, and yaw angle using Euler integration
    v_array[i] = v_array[i-1] + a * dt
    psi_array[i] = psi_array[i-1] + psi_dot * dt
    x_array[i] = x_array[i-1] + (v_array[i-1] + v_array[i]) / 2 * np.cos(psi_array[i-1]) * dt
    y_array[i] = y_array[i-1] + (v_array[i-1] + v_array[i]) / 2 * np.sin(psi_array[i-1]) * dt
    
    # Update yaw rate using Euler integration
    psi_dot = psi_dot + alpha * dt

# Plot x-y trajectory
plt.figure()
plt.plot(x_array, y_array)
plt.xlabel('x (m)')
plt.ylabel('y (m)')
plt.axis('equal')
plt.title('Vehicle Trajectory')
plt.show()

# Plot yaw angle
plt.figure()
plt.plot(t_array, psi_array)
plt.xlabel('Time (s)')
plt.ylabel('Yaw angle (rad)')
plt.title('Yaw Angle vs. Time')
plt.show()

# Plot velocity
plt.figure()
plt.plot(t_array, v_array)
plt.xlabel('Time (s)')
plt.ylabel('Velocity (m/s)')
plt.title('Velocity vs. Time')
plt.show()