RETURN_CODE = "$ret"

t_i = "int"
t_b = "boolean"
t_f = ("int", ["int", "boolean"] )  # funcao que recebe um int e um boolean e devolve um int

stack = [ {"a": t_i}, {}  ,{"a":t_i, "b":t_b}]

"""
int a;
boolean b;
int k;

int f1(boolean a, boolean c) {
    if (a) {
        int a;
        print(a);
    }
    print(b);
    return f1(a, a);
}

int f2(boolean x) {
    return a;
}

"""

class TypeError(Exception):
    pass

class Context(object):
    def __init__(self):
        self.stack = [{}]
    
    def get_type(self, name):
        for scope in self.stack:
            if name in scope:
                return scope[name]
        raise TypeError(f"Variavel {name} nao esta no contexto")
    
    def set_type(self, name, value):
        scope = self.stack[0]
        scope[name] = value

    def has_var(self, name):
        for scope in self.stack:
            if name in scope:
                return True
        return False

    def has_var_in_current_scope(self, name):
        return name in self.stack[0]

    def enter_scope(self):
        self.stack.insert(0, {})

    def exit_scope(self):
        self.stack.pop(0)


def verify(ctx:Context, node):
    if node["nt"] == "program":
        for decl in node["global_vars"]:
            verify(ctx, decl)
        # Double pass. primeiro assinatura, depois verificacao
        for fun in node["functions"]:
            name = fun["name"]
            if ctx.has_var(name):
                raise TypeError(f"Funcao {name} ja esta definida no contexto")
            assinatura = (fun["type"], [ par["type"] for par in fun["parameters"] ] )
            ctx.set_type(name, assinatura)
        for fun in node["functions"]:
            verify(ctx, fun)
    elif node["nt"] == "vardecl":
        name = node["name"]
        if ctx.has_var_in_current_scope(name):
            raise TypeError(f"Variavel {name} ja esta definida no contexto")
        ctx.set_type(name, node["type"])
    elif node["nt"] == "function":
        ctx.enter_scope()
        ctx.set_type(RETURN_CODE, node["type"])
        for par in node["parameters"]:
            ctx.set_type(par["name"], par["type"])
        ctx.enter_scope()
        for st in node["body"]:
            verify(ctx, st)
        ctx.exit_scope()
        ctx.exit_scope()
    elif node["nt"] == "print":
        verify(ctx, node["e"])
    elif node["nt"] == "var":
        name = node["name"]
        if not ctx.has_var(name):
            raise TypeError(f"Variavel {name} nao esta definida no contexto")
        return ctx.get_type(name)
    elif node["nt"] == "if":
        cond = node["cond"]
        if verify(ctx, cond) != t_b:
            raise TypeError(f"Condicao do if {cond} nao e boolean")
        ctx.enter_scope()
        for st in node["body"]:
            verify(ctx, st)
        ctx.exit_scope()
    elif node["nt"] == "return":
        t = verify(ctx, node["e"])
        expected_t = ctx.get_type(RETURN_CODE)
        if t != expected_t:
            raise TypeError(f"Return esperava {expected_t} mas recebe {t}")
    elif node["nt"] == "call":
        (expected_return, parameter_types) = ctx.get_type(node["name"])
        for (i, (arg, par_t)) in enumerate(zip(node["arguments"], parameter_types)):
            arg_t = verify(ctx, arg)
            if arg_t != par_t:
                index = i+1
                raise TypeError(f"Argumento #{index} esperava {par_t} mas recebe {arg_t}") 
        return expected_return
    else:
        t = node["nt"]
        print(f"E preciso tratar do node {t}")
        
"""
{
                        "nt": "call",
                        "name": "f2",
                        "arguments": [{"nt": "var", "name": "a"}],
                    },
"""
        

example_tree = {
    "nt": "program",
    "global_vars": [
        {"nt": "vardecl", "name": "a", "type": t_i},
        {"nt": "vardecl", "name": "b", "type": t_b},
        {"nt": "vardecl", "name": "k", "type": t_i},
    ],
    "functions": [{
            "nt": "function",
            "name": "f1",
            "parameters": [
                {"nt": "vardecl", "name": "a", "type": t_b},
                {"nt": "vardecl", "name": "c", "type": t_b},
            ],
            "type": t_i,
            "body": [
                {
                    "nt": "if",
                    "cond": {"nt": "var", "name": "a"},
                    "body": [
                        {"nt": "vardecl", "name": "a", "type": t_i},
                        {"nt": "print", "e": {"nt": "var", "name": "a"}},
                    ]},
                {"nt": "print", "e": {"nt": "var", "name": "b"}},
                {
                    "nt": "return",
                    "e": {
                        "nt": "call",
                        "name": "f2",
                        "arguments": [{"nt": "var", "name": "a"}],
                    },
                },
            ],
        },{
            "nt": "function",
            "name": "f2",
            "type": t_i,
            "parameters": [
                {"nt": "vardecl", "name": "x", "type": t_b},
            ],
            "body": [{"nt": "return", "e": {"nt": "var", "name": "a"}}],
        },
    ],
}


verify(Context(), example_tree)