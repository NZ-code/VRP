import scipy
from scipy.optimize import linprog
from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable, LpInteger


def test():
    chair_problem_pulp()


def chair_problem_pulp():
    lux_chair_price = 20
    norm_chair_price = 10

    lux_chair_wood = 3
    norm_chair_wood = 3

    lux_chair_hours = 40
    norm_chair_hours = 10

    problem = LpProblem("Chair factory", LpMaximize)
    n = LpVariable("Normal Chair", lowBound=0, cat=LpInteger)
    l = LpVariable("Lux Chair", lowBound=0,cat=LpInteger)
    profit = n * norm_chair_price + l * lux_chair_price
    problem += profit

    problem += (lux_chair_wood * l + norm_chair_wood * n <= 120, "wood constraint")
    problem += (lux_chair_hours * l + norm_chair_hours * n <= 1000, "time constraint")

    problem.solve()

    print(f'{problem.objective} = {problem.objective.value()}')
    for var in problem.variables():
        print(f'{var} = {var.value()}')

def potato_problem_pulp():
    problem = LpProblem("Harvesting problem", LpMaximize)
    p = LpVariable("Potato", lowBound=0, upBound=3000, cat=LpInteger)
    c = LpVariable("Carrot", lowBound=0, upBound=4000, cat=LpInteger)

    eq_restriction = (p + c <= 5000, "fetile contraint")
    problem += eq_restriction

    objective_function = p * 1.2 + c * 1.7
    problem += objective_function
    problem.solve()
    print(f'{problem.objective} =  {problem.objective.value()}')

    for var in problem.variables():
        print(f'{var} = {var.value()}')


def workers_scipy():
    obj = [-20, -12, -40, -25]

    lhs_ineq = [[1, 1, 1, 1],
                [3, 2, 1, 0],
                [0, 1, 2, 3]]
    rhs_ineq = [50,
                100,
                90]
    bnd = [(0, scipy.inf), (0, scipy.inf), (0, scipy.inf), (0, scipy.inf)]
    opt = linprog(c=obj, A_ub=lhs_ineq, b_ub=rhs_ineq, method="revised simplex", bounds=bnd)
    print(opt)


def simple_scipy():
    obj = [-1, 2]

    lhs_ineq = [[2, 1],
                [-4, 5],
                [1, -2]]
    rhs_ineq = [20,
                10,
                2]
    lhs_eq = [[-1, 5]]
    rhs_eq = [15]

    bnd = [(0, scipy.inf), (0, scipy.inf)]

    opt = linprog(c=obj, A_ub=lhs_ineq, b_ub=rhs_ineq, A_eq=lhs_eq, b_eq=rhs_eq, bounds=bnd, method="revised simplex")
    print(opt.x)
def simple_gulp():
    model = LpProblem(name="small-problem", sense=LpMaximize)
    x = LpVariable(name="x", lowBound=0)
    y = LpVariable(name="y", lowBound=0)
    model += (2 * x + y <= 20, "red constraint")
    model += ((-4) * x + 5*y <= 10, "blue constraint")
    model += (-x + 2*y >= -2, "yellow constraint")
    model += (-x + 5*y == 15, "green constraint")

    obj_function = lpSum([x, 2*y])
    model += obj_function

    status = model.solve()

    print(f'{model.objective} =  {model.objective.value()}')

    for var in model.variables():
        print(f'{var} = {var.value()}')