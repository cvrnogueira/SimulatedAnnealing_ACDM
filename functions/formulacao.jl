# Formulação matemática ACDM
import Pkg
Pkg.add("JuMP")
Pkg.add("GLPK")
Pkg.add("GLPKMathProgInterface")
using LinearAlgebra
using JuMP
using GLPKMathProgInterface
using GLPK
file_name = "../instances/trsp_50_1.dat"
file = open(file_name)
lines = readlines(file)
close(file)
firstLine = split(lines[1])
n = parse(Int64, firstLine[1])
p = zeros(n)
#p = transpose(p)
for i=1:n
    line_to_read = split(lines[i+1])
    p[i] = parse(Float64, line_to_read[1])
end
xij = Matrix{Int64}(I, n, n)
for i=1:n
    for j=1:n
       xij[i, j] = min(p[i], p[j])
       xij[j, i] = min(p[i], p[j])
    end
end
M = sum(p[i] for i in 1:n) #+ xij[i, j]
m = Model(with_optimizer(GLPK.Optimizer))
@variable(m, dij[1:n,1:n],Bin)
@variable(m, T >=0, Int)
@variable(m, s[1:n] >=0, Int)
@objective(m, Min, T) 
@constraint(m, [i in 1:n, j in 1:n], s[i] >= xij[i,j] + s[j] - M * (1 - dij[i,j]))
@constraint(m, [i in 1:n], T >= s[i] + p[i]) 
@constraint(m, [i in 1:n, j in 1:n], dij[i,j] + dij[j,i] <= 1)  
optimize!(m)
if termination_status(m) == MOI.OPTIMAL
    optimal_solution = value.(s[1:n])
    optimal_objective = objective_value(m)
elseif termination_status(m) == MOI.TIME_LIMIT && has_values(m)
    suboptimal_solution = value.(s[1:n])
    suboptimal_objective = objective_value(m)
else
    error("The model was not solved correctly.")
end
