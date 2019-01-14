from ..geant4 import Expression as _Expression
from matplotlib.cbook import is_numlike
import numpy as _np

def expressionStringScalar(obj1,obj2) : 
    # nubmer/varible/expression
    if is_numlike(obj2) :                       # number
        return str(obj2)
    try :
        obj1.registry.defineDict[obj2.name]     # variable already defined in registry
        return obj2.name
    except KeyError : 
        return obj2.expr.expression             # just an object as an expression

class ScalarBase(object) :
    def __init__(self) : 
        pass

    def __add__(self, other) :
                
        v1 = expressionStringScalar(self,self)
        v2 = expressionStringScalar(self,other)

        v = Constant("var_{}_add_{}".format(v1,v2), '({}) + ({})'.format(v1, v2),registry=None)
        v.registry      = self.registry
        v.expr.registry = self.registry
        return v


    def __sub__(self, other) :
        v1 = expressionStringScalar(self,self)
        v2 = expressionStringScalar(self,other)

        v = Constant("var_{}_sub_{}".format(v1,v2), '({}) - ({})'.format(v1, v2),registry=None)
        v.registry      = self.registry
        v.expr.registry = self.registry
        return v

    def __mul__(self, other):
        
        # check to see if other is a vector 
        if isinstance(other,VectorBase) : 
            return other*self

        v1 = expressionStringScalar(self,self)
        v2 = expressionStringScalar(self,other)

        v = Constant("var_{}_mul_{}".format(v1,v2), '({}) * ({})'.format(v1, v2),registry=None)
        v.registry      = self.registry
        v.expr.registry = self.registry
        return v

    def __div__(self, other):
        v1 = expressionStringScalar(self,self)
        v2 = expressionStringScalar(self,other)

        v = Constant("var_{}_div_{}".format(v1,v2), '({}) / ({})'.format(v1, v2),registry=None)
        v.registry      = self.registry
        v.expr.registry = self.registry
        return v

    def __neg__(self):
        v1 = expressionStringScalar(self,self)

        v = Constant("var_neg_{}".format(v1), '(-{})'.format(v1),registry=None)
        v.registry      = self.registry
        v.expr.registry = self.registry
        return v

    __radd__ = __add__
    __rsub__ = __sub__
    __rmul__ = __mul__

    def setName(self, name) : 
        self.name          = name
        self.expr.name     = 'expr_{}'.format(name)
        self.expr.registry = self.registry
        self.registry.addDefine(self)

def sin(arg) : 
    v1 = expressionStringScalar(arg,arg)
    v = Constant("sin_{}".format(v1), 'sin({})'.format(v1),registry=None)
    v.registry      = arg.registry
    v.expr.registry = arg.registry    
    return v

def cos(arg) : 
    v1 = expressionStringScalar(arg,arg)
    v = Constant("cos_{}".format(v1), 'cos({})'.format(v1),registry=None)
    v.registry      = arg.registry
    v.expr.registry = arg.registry    
    return v

def tan(arg) : 
    v1 = expressionStringScalar(arg,arg)
    v = Constant("tan_{}".format(v1), 'tan({})'.format(v1),registry=None)
    v.registry      = arg.registry
    v.expr.registry = arg.registry    
    return v

def exp(arg) : 
    v1 = expressionStringScalar(arg,arg)
    v = Constant("exp_{}".format(v1), 'exp({})'.format(v1),registry=None)
    v.registry      = arg.registry
    v.expr.registry = arg.registry    
    return v

def log(arg) : 
    v1 = expressionStringScalar(arg,arg)
    v = Constant("log_{}".format(v1), 'log({})'.format(v1),registry=None)
    v.registry      = arg.registry
    v.expr.registry = arg.registry    
    return v

def log10(arg) : 
    v1 = expressionStringScalar(arg,arg)
    v = Constant("log10_{}".format(v1), 'log10({})'.format(v1),registry=None)
    v.registry      = arg.registry
    v.expr.registry = arg.registry    
    return v

class Constant(ScalarBase) :
    def __init__(self, name, value, registry = None, addRegistry = True) :
        self.name  = name
        self.expr = _Expression("expr_{}".format(name), str(value), registry=registry)

        if registry != None: 
            self.registry = registry
            if addRegistry :
                registry.addDefine(self)

    def eval(self) :
        return self.expr.eval()

    def __float__(self) :
        return self.expr.eval()
    
    def __repr__(self) :
        return "Constant : {} = {}".format(self.name, str(self.expr))

class Quantity(ScalarBase) :
    def __init__(self, name, value, unit, type, registry = None, addRegistry = True) :
        self.name  = name
        self.expr  = _Expression("expr_{}".format(name), str(value), registry=registry)
        self.unit  = unit
        self.type  = type

        if registry != None: 
            self.registry = registry
            if addRegistry :
                registry.addDefine(self)

    def eval(self) :
        return self.expr.eval()

    def __float__(self) :
        return self.expr.eval()

    def __repr__(self) :
        return "Quantity: {} = {} [{}] {}".format(self.name, str(self.expr), self.unit, self.type)

class Variable(ScalarBase) :
    def __init__(self, name, value, registry = None, addRegistry = True) :
        self.name  = name
        self.expr  = _Expression("expr_{}".format(name), str(value), registry=registry)

        if registry != None: 
            self.registry = registry
            if addRegistry : 
                registry.addDefine(self)

    def eval(self) :
        return self.expr.eval()

    def __float__(self) :
        return self.expr.eval()

    def __repr__(self) :
        return "Variable: {} = {}".format(self.name, str(self.expr))

class Expression(ScalarBase) : 
    def __init__(self, name, value, registry = None) :
        self.name  = name
        self.expr  = _Expression("expr_{}".format(name), str(value), registry=registry)

        if registry != None: 
            self.registry = registry
            registry.addDefine(self)

    def eval(self) :
        return self.expr.eval()

    def __float__(self) :
        return self.expr.eval()

    def __repr__(self) :
        return "Expression: {} = {}".format(self.name, str(self.expr))    

class VectorBase(object) :
    def __init__() :
        pass
    
    def __add__(self,other) :
        p  = Position("vec_{}_add_{}".format(self.name,other.name),
                      '({})+({})'.format(self.x.expression,other.x.expression),
                      '({})+({})'.format(self.y.expression,other.y.expression),
                      '({})+({})'.format(self.z.expression,other.z.expression),
                      None)
        p.registry      = self.registry
        p.x.registry    = self.registry
        p.y.registry    = self.registry
        p.z.registry    = self.registry
        return p

    def __sub__(self,other) : 
        p  = Position("vec_{}_sub_{}".format(self.name,other.name),
                      '({})-({})'.format(self.x.expression,other.x.expression),
                      '({})-({})'.format(self.y.expression,other.y.expression),
                      '({})-({})'.format(self.z.expression,other.z.expression),
                      None)
        p.registry      = self.registry
        p.x.registry    = self.registry
        p.y.registry    = self.registry
        p.z.registry    = self.registry
        return p

    def __mul__(self,other) : 
        print type(self),type(other)
        v1 = expressionStringScalar(self,self)
        v2 = expressionStringScalar(self,other)
        
        p = Position("vec_{}_mul_{}".format(self.name,v2),
                     '({})*({})'.format(self.x.expression,v2),
                     '({})*({})'.format(self.y.expression,v2),
                     '({})*({})'.format(self.z.expression,v2),
                     None)
        p.registry      = self.registry
        p.x.registry    = self.registry
        p.y.registry    = self.registry
        p.z.registry    = self.registry
        return p                     

    __rmul__ = __mul__

    def __div__(self,other) : 
        v1 = expressionStringScalar(self,self)
        v2 = expressionStringScalar(self,other)
        
        p = Position("vec_{}_div_{}".format(self.name,v2),
                     '({})/({})'.format(self.x.expression,v2),
                     '({})/({})'.format(self.y.expression,v2),
                     '({})/({})'.format(self.z.expression,v2),
                     None)
        p.registry      = self.registry
        p.x.registry    = self.registry
        p.y.registry    = self.registry
        p.z.registry    = self.registry
        return p                     
    
    def setName(self, name) : 
        self.name          = name
        self.x.registry    = self.registry 
        self.y.registry    = self.registry 
        self.z.registry    = self.registry 
        self.x.name        = 'expr_{}_vec_x'.format(name)
        self.y.name        = 'expr_{}_vec_y'.format(name)
        self.z.name        = 'expr_{}_vec_z'.format(name)
        self.registry.addDefine(self)

    def eval(self) :
        return [self.x.eval(), self.y.eval(), self.z.eval()]

    def __getitem__(self, key):
        if key == 0 : 
            return self.x
        elif  key == 1 : 
            return self.y 
        elif  key == 2 :
            return self.z
        else :
            raise IndexError

def expressionStringVector(var) : 

    if isinstance(var,ScalarBase) :                
        try :                
            var.registry.defineDict[var.name]
            return var.name
        except KeyError : 
            return var.expr.expression
    else :
        return var
    
class Position(VectorBase) :
    def __init__(self,name,x,y,z, registry = None, addRegistry = True) :
        self.name = name

        self.x = _Expression("expr_{}_pos_x".format(name), expressionStringVector(x), registry=registry)
        self.y = _Expression("expr_{}_pos_y".format(name), expressionStringVector(y), registry=registry)
        self.z = _Expression("expr_{}_pos_z".format(name), expressionStringVector(z), registry=registry)
               
        if registry != None: 
            self.registry = registry
            if addRegistry : 
                registry.addDefine(self)

    def __repr__(self) :
        return "Position : {} = [{} {} {}]".format(self.name, str(self.x), str(self.y), str(self.z))

class Rotation(VectorBase) : 
    def __init__(self,name,rx,ry,rz, registry = None, addRegistry = True) :
        self.name = name
        self.x = _Expression("expr_{}_rot_x".format(name), expressionStringVector(rx), registry=registry)
        self.y = _Expression("expr_{}_rot_y".format(name), expressionStringVector(ry), registry=registry)
        self.z = _Expression("expr_{}_rot_z".format(name), expressionStringVector(rz), registry=registry)

        if registry != None : 
            self.registry = registry
            if addRegistry :
                registry.addDefine(self)

    def __repr__(self) :
        return "Rotation : {} = [{} {} {}]".format(self.name, str(self.x), str(self.y), str(self.z))

class Scale(VectorBase) : 
    def __init__(self,name,sx,sy,sz, registry = None, addRegistry = True) :
        self.name = name
        self.x = _Expression("expr_{}_scl_x".format(name), expressionStringVector(sx), registry=registry)
        self.y = _Expression("expr_{}_scl_y".format(name), expressionStringVector(sy), registry=registry)
        self.z = _Expression("expr_{}_scl_z".format(name), expressionStringVector(sz), registry=registry)

        if registry != None: 
            self.registry = registry
            if addRegistry : 
                registry.addDefine(self)        

    def __repr__(self) :
        return "Scale : {} = [{} {} {}]".format(self.name, str(self.x), str(self.y), str(self.z))

class Matrix :
    def __init__(self,name, coldim, values, registry = None, addRegistry = True) :
        self.name = name
        self.coldim = coldim

        self.values = [] 
        for i, v in enumerate(values) :
            self.values.append(Expression("expr_{}_idx{}_val".format(name,i), expressionStringVector(v),registry=registry))

        self.values_asarray = _np.array(self.values, dtype=_np.object)
        if self.coldim > 1:
            self.values_asarray = self.values_asarray.reshape(coldim, len(values)/coldim)

        if registry != None:
            self.registry = registry
            if addRegistry :
                registry.addDefine(self)
            
    def eval(self) :
        return [ e.eval() for e in self.values ]

    def __repr__(self) :
        return "Matrix : {} = {} {}".format(self.name, str(self.coldim), str(self.values))

    def __getitem__(self, key):
        return self.values_asarray[key]
