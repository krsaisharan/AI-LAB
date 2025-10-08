from itertools import product

def convert_expr(expr):
    expr = expr.replace('~', 'not ')
    expr = expr.replace('^', ' and ')
    expr = expr.replace('v', ' or ')
    while '->' in expr:
        parts = expr.split('->', 1)
        expr = f"(not ({parts[0]})) or ({parts[1]})"
    return expr

def evaluate(sentence, model):
    expr = convert_expr(sentence)
    return eval(expr, {}, model)

def tt_entails(kb, query, symbols):
    n = len(symbols)
    entails = True
    print("\nTruth Table:")
    header = ' | '.join(symbols) + ' | KB | Query | KB⇒Query'
    print(header)
    print('-'*len(header)*2)
    
    for values in product([False, True], repeat=n):
        model = dict(zip(symbols, values))
        kb_val = all(evaluate(s, model) for s in kb)
        query_val = evaluate(query, model)
        entails_val = not kb_val or query_val
        row = ' | '.join(str(model[s]) for s in symbols)
        row += f' | {kb_val} | {query_val} | {entails_val}'
        print(row)
        if kb_val and not query_val:
            entails = False
    return entails

kb = []
num_sentences = int(input("Enter number of sentences in Knowledge Base: "))
print("Enter each sentence (use -> for implies, ~ for NOT, ^ for AND, v for OR):")
for i in range(num_sentences):
    kb.append(input(f"KB Sentence {i+1}: ").strip())

query = input("Enter the Query: ").strip()

symbols = sorted({ch for s in kb+[query] for ch in s if ch.isalpha() and ch.isupper()})

result = tt_entails(kb, query, symbols)
print(f"\nDoes KB entail the query? {result}")
