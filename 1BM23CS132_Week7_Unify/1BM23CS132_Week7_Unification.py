from dataclasses import dataclass
from typing import Tuple, Dict, Optional

@dataclass(frozen=True)
class Var:
    name: str

@dataclass(frozen=True)
class Const:
    name: str

@dataclass(frozen=True)
class Func:
    name: str
    args: Tuple

@dataclass(frozen=True)
class Pred:
    name: str
    args: Tuple

def split_args(s: str):
    res=[]
    d=0
    cur=[]
    for ch in s:
        if ch==',' and d==0:
            res.append(''.join(cur).strip()); cur=[]
        else:
            if ch=='(': d+=1
            if ch==')': d-=1
            cur.append(ch)
    if cur: res.append(''.join(cur).strip())
    return res

def parse_term(s: str):
    s=s.strip()
    if '(' in s:
        i=s.find('('); name=s[:i].strip(); inside=s[i+1:-1]
        parts=split_args(inside)
        return Func(name, tuple(parse_term(p) for p in parts))
    return Var(s) if s and s[0].islower() else Const(s)

def parse_pred(s: str):
    s=s.strip()
    if '(' not in s: return Pred(s,())
    i=s.find('('); name=s[:i].strip(); inside=s[i+1:-1]
    parts=split_args(inside)
    return Pred(name, tuple(parse_term(p) for p in parts))

def substitute(x, theta: Dict[str, object]):
    if isinstance(x, Var):
        if x.name in theta: return substitute(theta[x.name], theta)
        return x
    if isinstance(x, Func):
        return Func(x.name, tuple(substitute(a, theta) for a in x.args))
    if isinstance(x, Pred):
        return Pred(x.name, tuple(substitute(a, theta) for a in x.args))
    return x

def occurs_check(v: Var, x, theta: Dict[str, object]):
    x=substitute(x, theta)
    if isinstance(x, Var): return x.name==v.name
    if isinstance(x, Func): return any(occurs_check(v,a,theta) for a in x.args)
    return False

def unify(x, y, theta: Optional[Dict[str, object]] = None) -> Optional[Dict[str, object]]:
    if theta is None: theta={}
    x=substitute(x, theta); y=substitute(y, theta)
    if isinstance(x, Var) and isinstance(y, Var) and x.name==y.name: return theta
    if isinstance(x, Var):
        if occurs_check(x, y, theta): return None
        new=dict(theta); new[x.name]=y; return new
    if isinstance(y, Var):
        if occurs_check(y, x, theta): return None
        new=dict(theta); new[y.name]=x; return new
    if isinstance(x, Const) and isinstance(y, Const):
        return theta if x.name==y.name else None
    if isinstance(x, Func) and isinstance(y, Func):
        if x.name!=y.name or len(x.args)!=len(y.args): return None
        for a,b in zip(x.args,y.args):
            theta=unify(a,b,theta)
            if theta is None: return None
        return theta
    if isinstance(x, Pred) and isinstance(y, Pred):
        if x.name!=y.name or len(x.args)!=len(y.args): return None
        for a,b in zip(x.args,y.args):
            theta=unify(a,b,theta)
            if theta is None: return None
        return theta
    return None

def term_to_str(t):
    if isinstance(t, Var): return t.name
    if isinstance(t, Const): return t.name
    if isinstance(t, Func): return f"{t.name}(" + ",".join(term_to_str(a) for a in t.args) + ")"
    if isinstance(t, Pred): return f"{t.name}(" + ",".join(term_to_str(a) for a in t.args) + ")"
    return str(t)

if __name__=="__main__":
    s1=input().strip()
    s2=input().strip()
    p1=parse_pred(s1)
    p2=parse_pred(s2)
    res=unify(p1,p2,{})
    if res is None:
        print("None")
    else:
        out={k:term_to_str(v) for k,v in res.items()}
        print(out)
