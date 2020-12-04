#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pathlib
import json


###################################################################
#LOADING EGOK360 DATASET FOR TRAINING/TESTING                     #
###################################################################

PATH_TO_EGOK_ROOT = "/home/keshav/Desktop/egokData/EgoK360_Data/"
TEST_PERCENT  = 10

def get_all_actions():
    paths = pathlib.Path(PATH_TO_EGOK_ROOT)
    actions = [*paths.glob('*/*')]
    return actions

def write_to_file(filename, train, test):
    data = dict(train=train, test=test)
    with open(filename, 'w') as f:
        json.dump(data, f)
    print(f"Train/Test files are saved at:{filename}")

def verify(datalist):
    for i in datalist:
        assert pathlib.Path(i['path']).exists(), f"FILE {i['path']} DOESN NOT EXISTS!"

def read_data(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    train, test = data['train'], data['test']
    verify(train)
    verify(test)
    return train, test

def get_train_test():
    actions = get_all_actions()
    actions = map(lambda action:sorted(action.glob('*')), actions)
    train, test = zip(*map(lambda x:(x[:-len(x)//TEST_PERCENT], x[-len(x)//TEST_PERCENT:]), actions))
    train = list(map(lambda x:{'path':x.as_posix(), 'action':x.parent.name, 'activity':x.parent.parent.name}, sum(train, [])))
    test = list(map(lambda x:{'path':x.as_posix(), 'action':x.parent.name, 'activity':x.parent.parent.name}, sum(test, [])))
    
    verify(train)
    verify(test)
    
    return train, test

if __name__ == '__main__':
    train, test = get_train_test()
    write_to_file('GOK.txt', train, test)

###################################################################
#PATH DIRECTORY STRUCTURE SHOULD LOOK LIKE FOLLOWING              #
###################################################################
"""
EgoK360_Data/
├── Desk_work
│   ├── Desk_work
│   ├── Napping
│   ├── Sit_down
│   ├── Stand_up
│   ├── Turn_left
│   ├── Turn_right
│   └── Writing
├── Driving
│   ├── Accelerate
│   ├── Decelerate
│   ├── Driving
│   ├── Still
│   ├── Stop
│   ├── Turn_left
│   └── Turn_right
├── Lunch
│   ├── Drinking
│   ├── Eating
│   ├── Ordering
│   ├── Turn_left
│   └── Turn_right
├── Office_talk
│   ├── Check_phone
│   ├── Office_talk
│   ├── Reach
│   ├── Turn_left
│   └── Turn_right
├── Ping-Pong
│   ├── Bounce_ball
│   ├── Hit
│   ├── Pickup_ball
│   ├── Ping-Pong
│   └── Serve
├── Playing_cards
│   ├── Playing_cards
│   ├── Put_card
│   ├── Shuffle
│   └── Take_card
├── Playing_pool
│   ├── Chalk_up
│   ├── Check_phone
│   ├── Playing_pool
│   ├── Reach
│   ├── Shooting
│   ├── Turn_left
│   └── Turn_right
├── Running
│   ├── Looking_at
│   ├── Running
│   └── Turn_around
├── Sitting
│   ├── At_computer
│   ├── Check_phone
│   ├── Follow_obj
│   ├── Reach
│   ├── Sitting
│   ├── Turn_left
│   └── Turn_right
├── Stairs
│   ├── Doorway
│   ├── Down_stairs
│   ├── Reach
│   ├── Turn_left
│   ├── Turn_right
│   └── Up_stairs
├── Standing
│   ├── Leaning
│   └── Standing
└── Walking
    ├── Breezeway
    ├── Crossing_street
    ├── Doorway
    ├── Hallway
    └── Walking
"""
###################################################################