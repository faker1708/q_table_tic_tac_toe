

from tic_tac_toe import game as g0
from q_learn import agent as agent0
import random

import time

class main_class():

    def __init__(self):
        self.__main()


    def __encode_plate(self,plate):
        serial_state = 0    # 用自然数表示状态，适用于 q表；
        # 如果是mlp，则建议用向量组，每个位置用3个bit表示 ，9个位置一共27
        for i,flag in enumerate(plate):
            serial_state+= flag * 3** i
        return serial_state


    def __fm(self,mode,n_ep):
        debug = 1
        debug = 0
        game = self.game

        if(mode =='train'):
            epsilon = 0.9
            game.render_on = 0
        elif(mode=='test'):
            epsilon = 1
            game.render_on = 0
        elif(mode == 'show'):
            epsilon = 1
            game.render_on = 1
        else:
            raise(BaseException('game mode error'))
        
        if(debug ==1):
            # game.render_on = 1
            pass

        ell = list()
        ell.append(0)
        ell.append(list())  # flag 1
        ell.append(list())

        epl = list()
        epl.append(0)
        epl.append(0.9)
        epl.append(0.9)


        learn_flag_list = [2]
        # lazy_record= [0,1,2,0,0,0,0]
        # lazy_record= [0,1,2,0,0,0,0]
        # lazy_record= [0,4,8,2,6,0,0]
        lazy_record= list()


        # component_record = [1,4,7]
        # component_record = [1,4]
        # component_record = [1]
        component_record = []

        result = [0,0,0]

        
        agent = self.agent_list[2]
        agent.action_record = list()


        for i_ep in range(n_ep):
            [plate,flag] = self.game.reset()
            # print(plate)
            tg = 0
            tg_2 = 0
            while(1):
                
                # print(plate)
                
                ss = self.__encode_plate(plate)
                agent = self.agent_list[flag]


                # if(mode == 'test' or mode == 'show'):
                # if(flag not in learn_flag_list):
                #         epl[flag] = 0 # 测试模式中，2阵营随机落子，期望1的胜率为100 %
                action,saql = agent.take_action(ss,epl[flag])
                # if(flag==2):
                #     print(action)
                # if(flag in learn_flag_list):
                    # print('ss',ss,flag)

                # if(i_ep <= 8):
                if(1):
                # if(saql):
                    if(flag in learn_flag_list):
                        if(tg_2<=len(component_record)-1):
                            action = component_record[tg_2]
                        tg_2 +=1

                if(flag not in learn_flag_list):
                    action = random.randint(0,2)
                    # if(tg<=len(lazy_record)-1):
                    #     action = lazy_record[tg]
                    # tg +=1
                if(flag in learn_flag_list):
                    
                    if(saql):
                        if(debug):
                            print(action,ss,saql)
                        pass
                
                [next_plate,next_flag,terminate,winner] = game.step(action)
                
                exp = [ss,action,0]

                exp_list = ell[flag]    
                exp_list.append(exp)

                
                if(terminate):
                    break
                else:
                    flag = next_flag
                    plate= next_plate

            for flag in range(3):
                if(flag in learn_flag_list):
                    exp_list = ell[flag]    
                    for _,exp in enumerate(exp_list):
                        if(flag == winner): # 如果本方赢了，奖励计一
                            exp[2] = 1
                    agent = self.agent_list[flag]
                    agent.store(exp_list)

                    # ql = agent.get_ql()
                    # print(ql[1])
                    if(debug):
                        print('debug time.sleep \n\n')
                        # time.sleep(1)
            result[winner]+=1
        if(mode ==  'test'):
            for i,ele in enumerate(result):
                result[i]/=n_ep
            print('result',result)
            


    def __main(self):

        self.game = g0()

        # self.agent = agent()

        sc = 3**9
        na = 9

        al = list()
        al.append(0)
        al.append(agent0(sc,na))
        al.append(agent0(sc,na))
        self.agent_list = al

        
        while(1):
            self.__fm('train',2**10)
            self.__fm('test',2**8)
            self.__fm('show',2**0)

        

        return


if __name__ == '__main__':
    main_class()