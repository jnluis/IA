#encoding: utf8

# YOUR NAME: João Nuno da Silva Luís
# YOUR NUMBER: 107403

# COLLEAGUES WITH WHOM YOU DISCUSSED THIS ASSIGNMENT (names, numbers):
# - ... José Gameiro 108840
# - ... Rafael Ferreira 107340


from semantic_network import *
from constraintsearch import *
class MySN(SemanticNetwork):

    def __init__(self):
        SemanticNetwork.__init__(self)
        # ADD CODE HERE IF NEEDED
        self.assoc_stats = {}
        pass

    def query_local(self,user=None,e1=None,rel=None,e2=None, assocBool=False):
        # IMPLEMENT HERE
        self.query_result = []
        lst = []

        for utili,decl in self.declarations.items():            
            for relation, ent2 in decl.items():
                if user is None or utili == user:                
                    if e1 == None or relation[0] == e1:
                        if rel == None or relation[1] == rel:
                            if e2== None or ent2 == e2:
                                ent1= relation[0]
                                lst.append([utili,relation[1],ent1,ent2])        
        for declaration in lst:
            if assocBool and (declaration[1] == 'subtype' or declaration[1] == 'member'):
                continue
            else:
                if declaration[1] == 'subtype':
                        self.query_result.append(Declaration(declaration[0],Subtype(declaration[2],declaration[-1])))
                elif declaration[1] == 'member':
                        self.query_result.append(Declaration(declaration[0],Member(declaration[2],declaration[-1])))
                elif isinstance(declaration[-1], set):
                    for item in declaration[-1]:
                        self.query_result.append(Declaration(declaration[0],Association(declaration[2],declaration[1],item)))
                else:
                    self.query_result.append(Declaration(declaration[0],Association(declaration[2],declaration[1],declaration[-1])))

        return self.query_result # Your code must leave the output in
                          # self.query_result, which is returned here

    def query(self,entity,assoc=None):
        # IMPLEMENT HERE
        self.query_result = []

        decl = self.query_local(e1= entity, rel='member')+ self.query_local(e1= entity, rel='subtype')
        local =self.query_local(e1=entity,rel=assoc, assocBool= True) + self.query_local(e2=entity,rel=assoc, assocBool= True)
        
        predecessors = [d.relation.entity2 for d in decl]

        filter_predecessors = lambda p: self.query(entity=p, assoc=assoc)
        # Recursively query for each predecessor with the same assoc
        local += sum(map(filter_predecessors, predecessors), [])
        
        self.query_result = local    
        return self.query_result # Your code must leave the output in
                          # self.query_result, which is returned here
    
    def predecessors_path(self, parent, user):
        decl = self.query_local(e1= parent, rel="subtype", user=user)

        if len(decl) == 0:
            return [parent]
        
        for obj in decl:
            if not obj.relation.entity2 == None:
                res = self.predecessors_path(obj.relation.entity2, user)
                return res + [parent] 
            else: 
                return [obj.relation.entity2, parent]

    def update_assoc_stats(self, assoc, user=None):
        listUsers = []
        list_Assocs = []

        assocs1 = {}
        assocs2 = {}

        statistics1= {}
        statistics2= {}

        def c_predecessor_path(self, predecessors, associations, list,stats ):
            if predecessors:
                for predecessor in predecessors:
                    last = predecessor[-1]
                    stats[last] = (associations.get(last)/len(list))
                    for elem in predecessor[::-1]:
                        if elem == last:
                            continue
                        if elem not in stats:
                            stats[elem] = stats[last]
                        else:
                            stats[elem] += stats[last]

        def prof_Function(N,K, val):
            tmp1 = N-K+K**(1/2)
            res = val / tmp1
            return res

        declarations = self.query_local(user=user, rel=assoc)
        for decl in declarations:
            if isObjectName(decl.relation.entity1):    
                listUsers.append(decl.relation.entity1)
            if isObjectName(decl.relation.entity2):
                list_Assocs.append(decl.relation.entity2)

        for ent1 in listUsers:
            query1 = self.query_local(user=user, rel='member',e1=ent1)
            if query1:
                entity1 = query1[0].relation.entity2
                if entity1 not in assocs1:
                    assocs1[entity1] = 1
                else:
                    assocs1[entity1] += 1

        for ent2 in list_Assocs:
            query2 = self.query_local(user=user, rel='member',e1=ent2)
            if query2:
                entity2 = query2[0].relation.entity2
                if entity2 not in assocs2:
                    assocs2[entity2] = 1
                else:
                    assocs2[entity2] += 1

        if assocs1: # à esquerda
            for key, value in assocs1.items():
                statistics1[key] = value / len(listUsers)
        predecessors1 = []
        for t in statistics1.keys():
            predecessors1 += [self.predecessors_path(t, user)]
        c_predecessor_path(self, predecessors1, assocs1, listUsers, statistics1)

        if assocs2: # à direita
            for key, value in assocs2.items():
                statistics2[key] = value / len(list_Assocs)
        predecessors2 = []
        for t in statistics2.keys():
            predecessors2 += [self.predecessors_path(t, user)]
        c_predecessor_path(self, predecessors2, assocs2, list_Assocs, statistics2)

        N1= 0
        for elem in assocs1.keys():
            N1 += assocs1.get(elem)
        K1 = len(listUsers) -N1
        N1+=K1
        for key in assocs1.keys():
            statistics1[key] = prof_Function(N1,K1, assocs1[key])

        N2= 0
        for elem in assocs2.keys():
            N2 += assocs2.get(elem)
        K2 = len(list_Assocs) -N2
        N2+=K2
        for key in assocs2.keys():
            statistics2[key] = prof_Function(N2,K2, assocs2[key])

        self.assoc_stats[(assoc, user)] = (statistics1, statistics2)



class MyCS(ConstraintSearch):

    def __init__(self,domains,constraints):
        ConstraintSearch.__init__(self,domains,constraints)
        # ADD CODE HERE IF NEEDED
        pass

    def propagate_restrictions(self, newdomains, var):
            val = newdomains[var][0]
            propagate = [(var, val)]

            for vr, d in newdomains.items():
                if vr == var:
                    continue
                if (vr, var) in self.constraints:
                    newdomains[vr] = [v for v in d if self.constraints[(vr, var)](vr, v, var, val)]
                    if len(newdomains[vr]) == 0:
                        return None

            return newdomains
    
    def search_all(self,domains=None,xpto=None):
        # If needed, you can use argument 'xpto'
        # to pass information to the function
        #
        # IMPLEMENTAR AQUI
        self.calls += 1
        if domains==None:
            domains = self.domains
        
        #Use xpto to save all solutions
        xpto = []

        # se alguma variavel tiver lista de valores vazia, falha
        if any(lv == [] for lv in domains.values()):
            return None

        if all([len(lv)==1 for lv in list(domains.values())]):
            for (var1,var2) in self.constraints:
                constraint = self.constraints[var1,var2]
                if not constraint(var1,domains[var1][0],var2,domains[var2][0]):
                    return None
            return { v:lv[0] for (v,lv) in domains.items() }
       
        for var in domains.keys():
            if len(domains[var])>1:
                for val in domains[var]:
                    newdomains = dict(domains)
                    newdomains[var] = [val]
                    newdomains = self.propagate_restrictions(newdomains, var)
                    if newdomains == None:
                        continue
                    
                    solution = self.search_all(newdomains)
                    if solution != None:
                            if solution not in xpto:
                                if not isinstance(solution, dict):
                                   #add each value of the solution
                                    [ xpto.append(v) for v in solution ]
                                else:
                                    xpto.append(solution)
                                    
                return xpto