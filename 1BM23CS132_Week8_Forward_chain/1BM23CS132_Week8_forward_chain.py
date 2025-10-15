from dataclasses import dataclass
from typing import Tuple,List,Dict,Optional
import sys

@dataclass(frozen=True)
class Var:
    name:str

@dataclass(frozen=True)
class Const:
    name:str

@dataclass(frozen=True)
class Func:
    name:str
    args:Tuple

@dataclass(frozen=True)
class Pred:
    name:str
    args:Tuple

def split_args(s:str):
    res=[];d=0;cur=[]
    for ch in s:
        if ch==',' and d==0:
            res.append(''.join(cur).strip());cur=[]
        else:
            if ch=='(':d+=1
            if ch==')':d-=1
            cur.append(ch)
    if cur:res.append(''.join(cur).strip())
    return res

def parse_term(s:str):
    s=s.strip()
    if not s: return None
    if '(' in s:
        i=s.find('(');name=s[:i].strip();inside=s[i+1:-1]
        parts=split_args(inside)
        return Func(name,tuple(parse_term(p) for p in parts))
    return Var(s) if s and s[0].islower() else Const(s)

def parse_pred(s:str):
    s=s.strip()
    if not s: return None
    if '(' not in s: return Pred(s,())
    i=s.find('(');name=s[:i].strip();inside=s[i+1:-1]
    parts=split_args(inside)
    return Pred(name,tuple(parse_term(p) for p in parts))

def substitute(x,theta):
    if x is None: return None
    if isinstance(x,Var):
        if x.name in theta: return substitute(theta[x.name],theta)
        return x
    if isinstance(x,Func):
        return Func(x.name,tuple(substitute(a,theta) for a in x.args))
    if isinstance(x,Pred):
        return Pred(x.name,tuple(substitute(a,theta) for a in x.args))
    return x

def occurs_check(v,x,theta):
    x=substitute(x,theta)
    if x is None: return False
    if isinstance(x,Var): return x.name==v.name
    if isinstance(x,Func): return any(occurs_check(v,a,theta) for a in x.args)
    return False

def unify(x,y,theta=None):
    if theta is None: theta={}
    if x is None or y is None: return None
    x=substitute(x,theta); y=substitute(y,theta)
    if isinstance(x,Var) and isinstance(y,Var) and x.name==y.name: return theta
    if isinstance(x,Var):
        if occurs_check(x,y,theta): return None
        new=dict(theta); new[x.name]=y; return new
    if isinstance(y,Var):
        if occurs_check(y,x,theta): return None
        new=dict(theta); new[y.name]=x; return new
    if isinstance(x,Const) and isinstance(y,Const):
        return theta if x.name==y.name else None
    if isinstance(x,Func) and isinstance(y,Func):
        if x.name!=y.name or len(x.args)!=len(y.args): return None
        for a,b in zip(x.args,y.args):
            theta=unify(a,b,theta)
            if theta is None: return None
        return theta
    if isinstance(x,Pred) and isinstance(y,Pred):
        if x.name!=y.name or len(x.args)!=len(y.args): return None
        for a,b in zip(x.args,y.args):
            theta=unify(a,b,theta)
            if theta is None: return None
        return theta
    return None

varcount=0
def standardize(ants,cons):
    global varcount
    varcount+=1
    mapping={}
    def st(t):
        if t is None: return None
        if isinstance(t,Var):
            if t.name not in mapping: mapping[t.name]=Var(f"{t.name}_{varcount}")
            return mapping[t.name]
        if isinstance(t,Func):
            return Func(t.name,tuple(st(a) for a in t.args))
        return t
    ants2=[Pred(a.name,tuple(st(x) for x in a.args)) for a in ants]
    cons2=Pred(cons.name,tuple(st(x) for x in cons.args))
    return ants2,cons2

def forward_chain(facts,rules,query):
    if query is None: 
        print("Error: no query provided"); return False
    F=set(facts)
    added=True
    while added:
        added=False
        for ants,cons in rules:
            ants_s,cons_s=standardize(ants,cons)
            thetas=[]
            def bt(i,theta):
                if i==len(ants_s):
                    thetas.append(theta); return
                a=substitute(ants_s[i],theta)
                for f in list(F):
                    th=unify(a,f,dict(theta))
                    if th is not None: bt(i+1,th)
            bt(0,{})
            for th in thetas:
                nf=substitute(cons_s,th)
                if nf not in F:
                    F.add(nf); added=True
                    if unify(query,nf,{}) is not None: return True
    return any(unify(query,f,{}) is not None for f in F)

data=sys.stdin.read().strip()
if data:
    lines=data.splitlines()
    if len(lines)<4:
        lines += ['']*(4-len(lines))
else:
    lines=[]
    for _ in range(4):
        lines.append(input().rstrip('\n'))
facts=[]
for line in lines[0:2]:
    for part in line.split(';'):
        p=parse_pred(part.strip())
        if p: facts.append(p)
rules=[]
query=None
for line in lines[2:4]:
    left=line
    if '::' in line:
        left,qp=line.split('::',1)
        query=parse_pred(qp.strip())
    for rule in left.split('|'):
        if not rule.strip(): continue
        if '->' not in rule: continue
        a,c=rule.split('->',1)
        ants=[parse_pred(x.strip()) for x in a.split(';') if x.strip()]
        cons=parse_pred(c.strip())
        rules.append((ants,cons))
if query is None:
    query=parse_pred(lines[3].split('::')[-1].strip())
print(forward_chain(facts,rules,query))
