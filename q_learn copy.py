


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
                q = random.gauss(0,0.1)
                aql.append(q)
            q_list.append(aql)

        self.__q_list = q_list

        return

    def take_action(self,perception,epsilon):
        # perception q表中，这里要输入一个自然数。用来取状态动作价值表。

        # explore
        # exploit
        ev = 2**10
        ra = random.randint(0,ev-1)
        if(ra/ev<epsilon):
            explore = 0
        else:
            explore = 1
        
        if(explore):
            action = random.randint(0,self.__action_dimension-1)
        else:
            # exploit
            saql = self.__q_list[perception]
            action = saql.index(max(saql))



        return action
    
    def store(self,exp_list):

        self.__exp_list = exp_list
        self.__update()


        ####
        # for i ,sql in enumerate(self.__q_list):
        #     # print(sql)
        #     print(i,end = ' ')
        #     for _,q in enumerate(sql):
        #         if(q<0.1):
        #             print('_',end = ' ')
        #         else:
        #             print(q,end= ' ')
        #     print('')
        # print('\n____________________________________________')

        
        # for i ,sql in enumerate(self.__q_list):
        #     # print(sql)
        #     print(i,sql.index(max(sql)))
        # print('\n____________________________________________')

        return
    
    def __update(self):
        alpha = 0.1

        for _,exp in enumerate(self.__exp_list):

            perception = exp[0] # 索引 ，自然数
            action = exp[1]
            r = exp[2]

            q = self.__q_list[perception][action]

            q = (1-alpha)*q + alpha* r

            self.__q_list[perception][action] = q

        return 

