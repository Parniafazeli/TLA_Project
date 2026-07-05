from logic_gates import GliderLogicGates

gate = GliderLogicGates()

print("AND Gate")
print("0 0 ->", gate.run_and_gate(False, False))
print("0 1 ->", gate.run_and_gate(False, True))
print("1 0 ->", gate.run_and_gate(True, False))
print("1 1 ->", gate.run_and_gate(True, True))

print()

print("NOT Gate")
print("0 ->", gate.run_not_gate(False))
print("1 ->", gate.run_not_gate(True))


#g = gate.setup_and_gate(
#    input_a_present=True,
#    input_b_present=True)
#
#for i in range(100):
#    g.evolve()
#
#print(g.grid[15:17, 12:14])
