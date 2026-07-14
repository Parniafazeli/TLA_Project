from logic_gates import GliderLogicGates
from pygame_viewer import run_pygame_life

gate = GliderLogicGates()

AND1 = gate.setup_and_gate(
    input_a_present=True,
    input_b_present=True
)
AND2=gate.setup_and_gate(
    input_a_present=True,
    input_b_present=False
)
AND3=gate.setup_and_gate(
    input_a_present=False,
    input_b_present=False
)
NOT1=gate.setup_not_gate(input_a_present=False)
NOT2=gate.setup_not_gate(input_a_present=True)
#run_pygame_life(AND1,cell_scale=10,fps=8,max_frames=120,title="AND Gate")
#run_pygame_life(AND2,cell_scale=10,fps=8,max_frames=120,title="AND Gate")
#run_pygame_life(AND3,cell_scale=10,fps=8,max_frames=120,title="AND Gate")
run_pygame_life(NOT1,cell_scale=10,fps=8,max_frames=120,title="NOT Gate")
#run_pygame_life(NOT2,cell_scale=10,fps=8,max_frames=120,title="NOT Gate")