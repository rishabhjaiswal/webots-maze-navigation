"""lab_controller controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot, Supervisor
import poineer_nav as pn
import poineer_proxsensors as pps
import occupancy_grid as ogrid


def run_robot(robot):

    # get the time step of the current world.
    timestep = int(robot.getBasicTimeStep())

    camera = robot.getDevice('top_camera')
    if camera is True:
        camera.enable(timestep)
        
     sensor_display = robot.getDevice('sensor_display')
     prox_sensors = pps.PoineerProxSensors(robot, sensor_display)
     
     nav.go_forward(30)
     
     while robot.step(timestep) != -1:
         prox_sensors.paint(nav.get_robot_pose())
         
   
    
if __name__ == '__main__':
    print('in controller')
    my_robot = Supervisor()
    run_robot(my_robot)
