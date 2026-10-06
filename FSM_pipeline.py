import pyFlightscript as pyfs
import os


# Define Solver/Freestream Variables
Altitude = 10000
airDensity = 1.225
airPressure = 101325.0
typeFreestream = 'CONSTANT' # set the type of free stream (Constant , Custom , Rotation)
LunitSolver = 'INCH'
teSweep = 0 # trailing edge sweep angle in degrees
aoa = 5 # angle of attack in degrees
bLayer = 'TRANSITIONAL' # boundary layer type
v = 100 # velocity for solver
numIter = 500 # number of iterations you want the solver to run through
refArea = 2000 # reference area of wing
refLength = 25 # reference length

# SW IGS file path (Flightstream only takes IGS)
sw_igs = (r"C:\Users\markk\OneDrive\Desktop\EpWingtest.IGS")
print(os.path.exists(sw_igs), ["Path to IGS file exists"])

# Flightstream path file
fsm = (r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Altair 2026.1\FlightStream2026.1.lnk")
print(os.path.exists(fsm), ["Flightstream path found"])

# Path to file save
fileSave = (r"C:\Users\markk\OneDrive\Desktop")

# initialize Flightstream
pyfs.fsinit.new_simulation()
pyfs.fsinit.open_fsm(fsm_filepath = fsm)
pyfs.fsinit.save_as_fsm(fsm_filepath = fileSave)
pyfs.fsinit.set_significant_digits()
pyfs.fsinit.set_base_region_bending_angle()
pyfs.fsinit.set_trailing_edge_sweep_angle(angle = teSweep)
pyfs.fsinit.set_simulation_length_units(units = LunitSolver)
pyfs.fsinit.set_vertex_merge_tolerance()


# import CAD file from SW
pyfs.import_cad(cad_filepath = sw_igs,
                tessellation_density= 'HIGH',
                unreferenced_patches = False,
                num_curvature = 120 )

# Mesh the CAD file, since this is a basic wing i will use the wing mesher
pyfs.cad_create_wing_mesh_from_ccs(name = 'epWing',
                                   mark_trailing_edges = 'True',
                                   te_geometry = 'Sharp',
                                   close_ends = 'True')

# Setup Free stream
pyfs.freestream.air_altitude(altitude = Altitude)
pyfs.freestream.fluid_properties(density = airDensity,
                                 pressure = airPressure)
pyfs.set_freestream(freestream_type = typeFreestream)

# Setup Solver
pyfs.set_solver.aoa(angle = aoa)
pyfs.set_solver.solver_velocity(velocity = v)
pyfs.set_solver.boundary_layer_type(type_value = bLayer)
pyfs.set_solver.solver_iterations(num_iterations = numIter)
pyfs.set_solver.ref_area(value = refArea)
pyfs.set_solver.ref_length(length = refLength)

# initialize solver
pyfs.solver.initialize_solver(solver_model = 'INCOMPRESSIBLE', surfaces = -1)


pyfs.exec_solver.start_solver()


# Write all of the FlightStream commands to a script file
pyfs.write_to_file()

# Execute that script using FlightStream
pyfs.execute_fsm_script(
    fsexe_path=fsm,
    hidden=False
)