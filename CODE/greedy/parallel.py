
# run optimization in parallel for synthetic cases
from multiprocessing import Pool
import pandas as pd
import os
# from not_used_main_syn import run_case
from main_syn import run_case


def run_case_size(size):
    print('------- Running size:{:.2f}'.format(size))
    run_case(size=size)
    return [size]

# def run_case_size_new(num_of_individuals,size,new_plans_num):
#     print('------- Running size,Lmax,new_plans:{:.2f,.2f,.2f}'.format(size,num_of_individuals,new_plans_num))
#     run_case(num_of_individuals=num_of_individuals,size=size,new_plans_num=new_plans_num)
#     return [num_of_individuals,size,new_plans_num]

if __name__ == '__main__':
    # size = list(range(100, 2100, 100))
    # size.extend([2500, 3000])
    size=[100,500,1000,1500,2000,2500,3000]

    print(size)
    cpu_count = os.cpu_count()

    with Pool(cpu_count - 1) as p:
        msgs = p.map(run_case_size,size)

    # M = pd.DataFrame(msgs, columns=['size', 't'])
    # M.to_csv('./log_grid_mp_cp.csv', index=False)
