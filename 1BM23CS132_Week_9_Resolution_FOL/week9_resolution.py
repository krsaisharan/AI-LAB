def is_variable(x):
    return isinstance(x, str) and x[0].islower() and x.isalpha()

def unify(x, y, subst=None):
    if subst is None:
        subst = {}
    if x == y:
        return subst
    if is_variable(x):
        return unify_var(x, y, subst)
    if is_variable(y):
        return unify_var(y, x, subst)
    if isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y):
        for a, b in zip(x, y):
            subst = unify(a, b, subst)
            if subst is None:
                return None
        return subst
    return None

def unify_var(var, x, subst):
    if var in subst:
        return unify(subst[var], x, subst)
    elif x in subst:
        return unify(var, subst[x], subst)
    else:
        subst[var] = x
        return subst

def parse_predicate(pred):
    pred = pred.strip()
    if '(' in pred:
        name, args = pred.split('(')
        args = args[:-1].split(',')
        return (name.strip(), tuple(a.strip() for a in args if a.strip()))
    else:
        return (pred, ())

def apply_subst(clause, subst):
    new_clause = set()
    for lit in clause:
        neg = lit.startswith('~')
        atom = lit[1:] if neg else lit
        name, args = parse_predicate(atom)
        new_args = []
        for a in args:
            while a in subst:
                a = subst[a]
            new_args.append(a)
        arg_str = ','.join(new_args)
        new_clause.add(('~' if neg else '') + (f"{name}({arg_str})" if new_args else name))
    return new_clause

def resolve(ci, cj):
    resolvents = set()
    for di in ci:
        for dj in cj:
            neg_di = di.startswith('~')
            neg_dj = dj.startswith('~')
            p1 = di[1:] if neg_di else di
            p2 = dj[1:] if neg_dj else dj
            name1, args1 = parse_predicate(p1)
            name2, args2 = parse_predicate(p2)
            if name1 == name2 and neg_di != neg_dj and len(args1) == len(args2):
                subst = unify(list(args1), list(args2))
                if subst is not None:
                    new_clause = (ci - {di}) | (cj - {dj})
                    new_clause = apply_subst(new_clause, subst)
                    resolvents.add(frozenset(new_clause))
    return resolvents

def resolution(kb, query):
    clauses = kb.copy()
    clauses.append({f"~{query}"})
    new = set()
    step = 1
    print("\nStarting Resolution Process...\n")
    while True:
        n = len(clauses)
        pairs = [(clauses[i], clauses[j]) for i in range(n) for j in range(i + 1, n)]
        for (ci, cj) in pairs:
            resolvents = resolve(ci, cj)
            if frozenset() in resolvents:
                print(f"\n✅ Empty clause derived at step {step}! Query is PROVED TRUE.\n")
                return True
            if resolvents:
                print(f"Step {step}: {ci} + {cj} → {resolvents}")
            new |= resolvents
            step += 1
        if new.issubset(set(map(frozenset, clauses))):
            print("\n❌ No new clauses generated. Query CANNOT be proved.\n")
            return False
        for c in new:
            if c not in clauses:
                clauses.append(set(c))

print("Enter the number of clauses in the Knowledge Base:")
n = int(input("KB count: "))
KB = []
print("\nEnter each clause in CNF form (e.g., ~Food(x) Likes(John,x)):")
for i in range(n):
    clause_input = input(f"Clause {i+1}: ").strip().split()
    KB.append(set(clause_input))
query = input("\nEnter the query (e.g., Likes(John,Peanuts)): ").strip()
result = resolution(KB, query)
print("\nFinal Result:", "Proved ✅" if result else "Not Proved ❌")
