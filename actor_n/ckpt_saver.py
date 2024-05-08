import os
import shutil
import time

from multiprocessing import Process

from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('--src_path', type=str, default='Danzero_plus-main/actor_n/log/Client0/ckpt',
                    help='Directory to save logging data, model parameters and config file')
parser.add_argument('--ckpt_path', type=str, default='Danzero_plus-main/actor_n/ckpt',
                    help='Directory to save logging data, model parameters and config file')
parser.add_argument('--waiting_time', type=float, default=600.0,
                    help='Time to break the loop')

def find_ckpt(src_path, ckpt_path, waiting_time, start_index : int = 1):
    while True:
        if os.path.exists(src_path):
            break

    if not os.path.exists(ckpt_path):
        os.mkdir(ckpt_path)
        
    origin_time = time.time()
    new_time = time.time()
    
    while True:
        if os.path.exists(f"{src_path}/{start_index}.ckpt"):
            shutil.copy(f"{src_path}/{start_index}.ckpt", ckpt_path)
            start_index += 1
            origin_time = time.time()
            new_time = time.time()
        if new_time - origin_time > waiting_time:
            print("Time out!")
            break

def main():
    args, _ = parser.parse_known_args()
    print(args.ckpt_path)
    print(args)
    ckpt_saver = Process(target=find_ckpt, args=(args.src_path, args.ckpt_path, args.waiting_time))
    ckpt_saver.start()
    ckpt_saver.join()

if __name__ == "__main__":
    main()