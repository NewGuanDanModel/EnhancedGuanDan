#!/bin/bash
#1000000000000
nohup /home/steventse7340/Danzero_pulus-main/actor_n/guandan 100 >/dev/null 2>&1 &
sleep 0.5s
nohup /home/steventse7340/anaconda3/envs/guandan37/bin/python -u /home/steventse7340/Danzero_plus-main/actor_n/actor.py > /home/steventse7340/actor_out.log 2>&1 &
sleep 0.5s
nohup /home/steventse7340/anaconda3/envs/guandan37/bin/python -u /home/steventse7340/Danzero_plus-main/actor_n/game.py > /home/steventse7340/game_out.log 2>&1 &