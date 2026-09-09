# Webots MVP model notes

This directory is the home for the Webots world and robot assets. The initial PR intentionally keeps the model minimal and generated from primitives so the behavior stack can evolve without coupling to a specific CAD mesh.

The target visual design is a small cute alien: oversized rounded head, two large forward-facing optical cameras, compact torso, short arms, broad feet, and a low center of mass.

Next simulation slice should add the actual Webots `.wbt` and `.proto` assets plus ROS 2 bridge. The core behavior tests in `ros2/alien_robot/alien_robot/core.py` are simulator-independent and form the contract for that integration.
