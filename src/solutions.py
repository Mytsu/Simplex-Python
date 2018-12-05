from simplex import Simplex


def interpretation(simplex: Simplex, variables, y: int, type_: str) -> str:
    if y != 0:
        if any(i != 0 for i in list(simplex.solution)[-y:]):
            message = non_existent_solution()

    if simplex.multiple_solutions:
        message = multiple_optimal(simplex, variables, type_)
    elif all(x >= 0 for x in simplex.direction):
        message = unlimited_solution()
    else:
        message = optimal_solution(simplex, variables, type_)

    print(message)


def solution_interpretation(simplex, variables, solution, type_):
    lucro = simplex.cost.dot_product(solution)
    if type_ == 'max':
        lucro = -lucro

    values = [v for n, v in zip(variables, solution)]
    values.append(lucro)
    return str.format(
        'Contratar {6} funcionários para torno e {7} para solda.\n'
        'Produzir {0} unidades de cano com rosca 1/2", '
        '{1} unidades de cano com rosca 4", '
        '{2} unidades de faca-copo 30x60, '
        '{3} unidades de faca-copo 160x70, '
        '{4} tanques de 3000 litros" e '
        '{5} tanques de 10000 litros. '
        'O lucro é de R${8}', *values)


def non_existent_solution() -> str:
    return ('Não existe solução que respeite as restrições dadas.')


def multiple_optimal(simplex: Simplex, variables, type_) -> str:
    return (
        'Foram encontradas múltiplas soluções para o problema. Uma solução '
        f'seria: {solution_interpretation(simplex, variables, simplex.solution, type_)}\n'
        'Outra solução seria:'
        f'{solution_interpretation(simplex, variables, simplex.second_solution, type_)}\n'
        'Qualquer solução dentro da combinação convexa entre estas duas seria'
        'ótima.')


def unlimited_solution() -> str:
    return ('Nenhum componente do vetor direção tem valor negativo. '
            'Logo, a solução do problema temde ao infinito, com custo ótimo '
            'menos infinito')


def optimal_solution(simplex: Simplex, variables, type_: str) -> str:

    return (
        'Foi encontrada uma solução ótima.'
        f'{solution_interpretation(simplex, variables, simplex.solution, type_)}')
