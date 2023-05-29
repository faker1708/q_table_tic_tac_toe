

from tic_tac_toe import game as g0
from q_learn import agent as agent0

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

        ell = list()
        ell.append(0)
        ell.append(list())  # flag 1
        ell.append(list())

        epl = list()
        epl.append(0)
        epl.append(0)
        epl.append(epsilon)


        learn_flag_list = [2]
        lazy_record= [0,1,2]

        result = [0,0,0]

        for i_ep in range(n_ep):
            [plate,flag] = self.game.reset()
            # print(plate)
            tg = 0
            while(1):
                
                # print(plate)
                ss = self.__encode_plate(plate)
                agent = self.agent_list[flag]

                # if(mode == 'test' or mode == 'show'):
                # if(flag not in learn_flag_list):
                #         epl[flag] = 0 # 测试模式中，2阵营随机落子，期望1的胜率为100 %
                action,saql = agent.take_action(ss,epl[flag])
                

                if(flag in learn_flag_list):
                    # print(saql)
                    # print(epsilon)
                    if(saql):
                        print(saql)

                if(flag not in learn_flag_list):
                    if(tg<=len(lazy_record)-1):
                        action = lazy_record[tg]
                    tg +=1
                
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
            result[winner]+=1
        if(mode ==  'test'):
            for i,ele in enumerate(result):
                result[i]/=n_ep
            # print(result)
            


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