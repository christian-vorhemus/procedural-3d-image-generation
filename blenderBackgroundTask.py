import bpy
import os
import sys
import math
import random
import numpy as np
import uuid
import datetime

argv = sys.argv
argv = argv[argv.index("--") + 1:]

package_serial_no = argv[1]
file_base_path = argv[2]

print(f"Started processing package {package_serial_no} at {datetime.datetime.now()}")

def context_override():
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == 'VIEW_3D':
                for region in area.regions:
                    if region.type == 'WINDOW':
                        return {'window': window, 'screen': screen, 'area': area, 'region': region, 'scene': bpy.context.scene} 

# Set the location of the object randomly
def random_location():
    x = random.uniform(-0.04, 0.04)
    y = random.uniform(-0.07, 0.07)
    bpy.data.objects["Package"].location = (x,y,0)

def random_rotation():
    angle = random.randint(-20, 20)
    bpy.data.objects["Package"].rotation_euler[2] = math.radians(angle)

# Function returns num_points (x,y,z) points with fixed z_point following start and end coordinates and two control points c1 and c2 as (x,y) tuple
def get_cubic_bezier_points(start, end, c1, c2, num_points=10, z_point=0):
    points = []
    for t in np.arange(0.0, 1.0, 1/num_points):
        x = math.pow((1-t),3)*start[0] + 3*t*math.pow((1-t),2)*c1[0] + 3*t*t*(1-t)*c2[0] + t*t*t*end[0]
        y = math.pow((1-t),3)*start[1] + 3*t*math.pow((1-t),2)*c1[1] + 3*t*t*(1-t)*c2[1] + t*t*t*end[1]
        points.append((x,y,z_point))
    return points

# Randomly set the start, end and control points within a defined range. Control points can lie out of range by factor 1.5
def get_points_in_range(min_x, min_y, max_x, max_y, num_points, z_point):
    start_x = random.uniform(min_x, max_x)
    start_y = random.uniform(min_y, max_y)
    c1_x = random.uniform(min_x*1.5, max_x*2)
    c1_y = random.uniform(min_y*1.5, max_y*1.5)
    c2_x = random.uniform(min_x*1.5, max_x*1.5)
    c2_y = random.uniform(min_y*1.5, max_y*1.5)
    end_x = random.uniform(min_x, max_x)
    end_y = random.uniform(min_y, max_y)
    points = get_cubic_bezier_points((start_x, start_y), (end_x, end_y), (c1_x, c1_y), (c2_x, c2_y), num_points=num_points, z_point=z_point)
    return points

# Applies brush strokes in blender based on the coordinates passed
def sculpt(brush, coordinates, strength=0.5, pen_flip=True):
    bpy.ops.paint.brush_select(sculpt_tool=brush, toggle=False)
    bpy.data.brushes["SculptDraw"].strength = strength
    strokes = []
    for i, coordinate in enumerate(coordinates):
        stroke = {
            "name": "stroke",
            "mouse": (0,0),
            "pen_flip" : pen_flip,
            "is_start": True if i==0 else False,
            "location": coordinate,
            "size": 50,
            "pressure": 1,
            "time": float(i)
        }
        strokes.append(stroke)

    bpy.ops.sculpt.brush_stroke(context_override(), stroke=strokes)
    print("Finished sculpting")

# Change to Blender sculpt mode
bpy.ops.sculpt.sculptmode_toggle()
bpy.data.objects["Package"].select_set(True)
bpy.context.scene.tool_settings.sculpt.use_symmetry_x = False

package_type = argv[0]
if package_type not in ["damaged", "intact"]:
    raise Exception("First argument must be either 'damaged' or 'intact'")

if package_type == "damaged":
    # If package is damaged, we add 3 pressure strokes with medium strength
    for i in range(0,3):
        strength = np.random.normal(0.35, 0.05)
        points = get_points_in_range(-0.05, -0.025, 0.05, 0.025, 10, 0.015)
        sculpt("DRAW", points, strength)
else:
    # If package is intact, we add 2 pressure strokes with light strength (just to add variation to each package)
    for i in range(0,2):
        strength = np.random.normal(0.2, 0.05)
        points = get_points_in_range(-0.05, -0.025, 0.05, 0.025, 10, 0.015)
        sculpt("DRAW", points, strength)

random_location()
random_rotation()

bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_pattern(pattern="Package")
bpy.ops.object.shade_smooth()

# Apply animation so belt appears to be moving
frame_no = random.randint(1, 8)
bpy.context.scene.frame_set(frame_no)

bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.render.image_settings.color_mode = 'RGB'
bpy.context.scene.render.resolution_x = 960
bpy.context.scene.render.resolution_y = 540

bpy.data.objects['Camera.Side'].data.dof.aperture_fstop = np.random.normal(16, 3)
bpy.data.objects['Camera.Top'].data.dof.aperture_fstop = np.random.normal(16, 3)

for i, cam in enumerate([obj for obj in bpy.data.objects if obj.type == 'CAMERA']):
    if cam.name == "Camera.Side":
        cam_name = "side"
    else:
        cam_name = "top"
    bpy.context.scene.camera = cam

    file_path = os.path.join(file_base_path, f'{package_type}/{package_serial_no}_{cam_name}.jpg')
    bpy.context.scene.render.filepath = file_path
    bpy.ops.render.render(write_still = True)

print(f"Finished processing package {package_serial_no} at {datetime.datetime.now()}")
bpy.ops.wm.quit_blender()