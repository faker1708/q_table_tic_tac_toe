


import random

class agent():

    def __init__(self,sc,na):
        # sc 所有可能的状态的总数
        # na 每个状态下动作的个数

        self.__state_dimension = sc
        self.__action_dimension = na
        q_list = list()
        for _ in range(self.__state_dimension):
            aql = list()
            for _ in range(self.__action_dimension):
                # q = random.gauss(0,0.1)
                q = random.uniform(0.0, 1.0)
                q = random.uniform(0.45, 0.55)
                
                # q = 0
                # q = 1
                aql.append(q)
            q_list.append(aql)

        self.__q_list = q_list

        return
    
    def get_ql(self):
        return self.__q_list

    def take_action(self,perception,plate,epsilon):
        # perception q表中，这里要输入一个自然数。用来取状态动作价值表。

        # explore
        # exploit
        ev = 2**10
        ra = random.randint(0,ev-1)
        if(ra/ev<epsilon):
            explore = 0
        else:
            explore = 1
        
        bql = list()
        if(explore):
            action = random.randint(0,self.__action_dimension-1)
        else:
            # exploit
            saql = self.__q_list[perception]
            bql = saql

            # bql = list()
            # for i,flag in enumerate(plate):
            #     if(flag>0):
            #         bql.append(-2**10)
            #     else:
            #         bql.append(saql[i])

            action = bql.index(max(bql))



        return action,bql
    
    def store(self,exp_list):

        self.__exp_list = exp_list
        self.__update()

        return
    
    def __update(self):
        alpha = 0.1

        for _,exp in enumerate(self.__exp_list):

            perception = exp[0] # 索引 ，自然数
            action = exp[1]
            reward = exp[2]

            q = self.__q_list[perception][action]

            q = (1-alpha)*q + alpha* reward

            self.__q_list[perception][action] = q

        return 

