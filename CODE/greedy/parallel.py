
# run optimization in parallel for synthetic cases
from multiprocessing import Pool
import pandas as pd
import os
from main_syn import run_case


def run_case_size(size):
    print('------- Running size:{:.2f}'.format(size))
    run_case(size=size)
    return [size]


if __name__ == '__main__':
    size = list(range(600, 2100, 100))
    size.extend([2500, 3000])
    print(size)
    cpu_count = os.cpu_count()
    with Pool(cpu_count - 1) as p:
        msgs = p.map(run_case_size,size)

    M = pd.DataFrame(msgs, columns=['size', 't'])
    M.to_csv('./log_grid_mp_cp.csv', index=False)
