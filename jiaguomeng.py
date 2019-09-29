# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 12:50:13 2019

@author: sqr_p
"""

import numpy as np
from tqdm import tqdm
import itertools
from queue import PriorityQueue as PQ
from scipy.special import comb

Mode = 'Online'

commercial = '便利店 五金店 服装店 菜市场 学校 图书城 商贸中心 加油站 民食斋 媒体之声'
residence = '木屋 居民楼 钢结构房 平房 小型公寓 人才公寓 花园洋房 中式小楼 空中别墅 复兴公馆'
industry  = '木材厂 食品厂 造纸厂 水厂 电厂 钢铁厂 纺织厂 零件厂 企鹅机械 人民石油'

OneStars = ' 企鹅机械 人民石油 空中别墅 媒体之声 复兴公馆 人才公寓'
TwoStars = ' 零件厂 图书城 中式小楼 商贸中心 民食斋 花园洋房 加油站 钢铁厂'
TriStars = ' 纺织厂'
QuaStars = ' 木材厂 食品厂 电厂 小型公寓 菜市场 水厂'
PenStars = ' 居民楼 木屋 平房 便利店 学校 服装店 五金店 造纸厂 钢结构房'

last_result=(('人才公寓', '木屋', '居民楼'), ('五金店', '菜市场', '便利店'), ('食品厂', '电厂', '木材厂'))

######星级 * 照片 * 政策 * 任务
'''
    在这里填写你的政策和照片加成
'''
Policy = {
            'Global':  6,
            'Online':  2,
            'Offline': 2,
            'Residence': 3,
            'Commercial': 6,
            'Industry': 15,
            'JiaGuoZhiGuang': 0.2+0.1
        }
Photos = {
            'Global':  0.7,
            'Online':  0.5,
            'Offline': 1.0,
            'Residence': 1.5,
            'Commercial': 0.6,
            'Industry': 1.5,
        }

class UndefinedError(Exception): pass

if Mode == 'Online':
    BlackList=set(' 小型公寓 复兴公馆 水厂'.split())
elif Mode == 'Offline':
# TODO:
    raise UndefinedError('离线收益等我有空再写，真的用得到吗')
    BlackList=set(' 小型公寓 电厂'.split())

ListDifference=lambda a,b: [item for item in a if not item in b]
commercial=ListDifference(commercial.split(),BlackList)
residence=ListDifference(residence.split(),BlackList)
industry=ListDifference(industry.split(),BlackList)

OneStars=ListDifference(OneStars.split(),BlackList)
TwoStars=ListDifference(TwoStars.split(),BlackList)
TriStars=ListDifference(TriStars.split(),BlackList)
QuaStars=ListDifference(QuaStars.split(),BlackList)
PenStars=ListDifference(PenStars.split(),BlackList)

#
star = dict()
for item in OneStars:
    star[item] = 1
for item in TwoStars:
    star[item] = 2
for item in TriStars:
    star[item] = 3
for item in QuaStars:
    star[item] = 4
for item in PenStars:
    star[item] = 5

startDict = {1:1, 2:2, 3:6, 4:24, 5:120}

start = dict()
for item in residence:#住宅
    start[item] = startDict[star[item]]*\
        (1+Policy['Global']+Policy['Online']+Policy['Residence']+Policy['JiaGuoZhiGuang'])*\
        (1+Photos['Global']+Photos['Online']+Photos['Residence'])
for item in commercial:#商业
    start[item] = startDict[star[item]]*\
        (1+Policy['Global']+Policy['Online']+Policy['Commercial']+Policy['JiaGuoZhiGuang'])*\
        (1+Photos['Global']+Photos['Online']+Photos['Commercial'])
for item in industry:#工业
    start[item] = startDict[star[item]]*\
        (1+Policy['Global']+Policy['Online']+Policy['Industry']+Policy['JiaGuoZhiGuang'])*\
        (1+Photos['Global']+Photos['Online']+Photos['Industry'])


#收益调整
start['花园洋房'] *= 1.022
start['商贸中心'] *= 1.022
start['平房'] *= 1.097
start['电厂'] *= 1.18
start['水厂'] *= 1.26
start['加油站'] *= 1.2
start['企鹅机械'] *= 1.33
start['人才公寓'] *= 1.4
start['中式小楼'] *= 1.4
start['民食斋'] *= 1.52
start['空中别墅'] *= 1.52
start['媒体之声'] *= 1.615

#任务加成调整
#start['小型公寓'] *= 0
#start['人才公寓'] *= 0
#start['居民楼'] *= 0
#start['木屋'] *= 0

#start['纺织厂'] *= 0
#start['木材厂'] *= 0
start['食品厂'] *= 0
start['菜市场'] *= 0

#start['商贸中心'] *= 2
# start['服装店'] *= 0
# start['造纸厂'] *= 0

#start['民食斋'] *= 0
# start['钢铁厂'] *= 0
#start['木材厂'] *= 0

buffs_100 = {
                '木屋': ['木材厂'],
                '居民楼': ['便利店'],
                '钢结构房': ['钢铁厂'],
                '花园洋房': ['商贸中心'],
                '空中别墅': ['民食斋'],

                '便利店': ['居民楼'],
                '五金店': ['零件厂'],
                '服装店': ['纺织厂'],
                '菜市场': ['食品厂'],
                '学校':  ['图书城'],
                '图书城': ['学校', '造纸厂'],
                '商贸中心': ['花园洋房'],

                '木材厂': ['木屋'],
                '食品厂': ['菜市场'],
                '造纸厂': ['图书城'],
                '钢铁厂': ['钢结构房'],
                '纺织厂': ['服装店'],
                '零件厂': ['五金店'],
                '企鹅机械':['零件厂'],
                '人民石油':['加油站']
            }

buffs_50 = {'零件厂': ['企鹅机械'],
            '加油站':['人民石油']}

bufflist_258 = [.2, .5, .8, 1.1, 1.4]
bufflist_246 = [.2, .4, .6, .8, 1.0]
bufflist_015 = [0.75*x for x in [.2, .4, .6, .8, 1.0]]
bufflist_010 = [0.5*x for x in [.2, .4, .6, .8, 1.0]]
bufflist_005 = [0.25*x for x in [.2, .4, .6, .8, 1.0]]
bufflist_035 = [1.75*x for x in [.2, .4, .6, .8, 1.0]]

buffs_com = {
             '媒体之声': bufflist_005,
             '企鹅机械': bufflist_015,
             '民食斋': bufflist_246,
             '纺织厂': bufflist_015,
             '人才公寓': bufflist_246,
             '中式小楼': bufflist_246,
             '空中别墅': bufflist_258,
             '电厂': bufflist_258
             }
buffs_ind = {
             '媒体之声': bufflist_005,
             '钢铁厂': bufflist_015,
             '中式小楼': bufflist_246,
             '民食斋': bufflist_246,
             '空中别墅': bufflist_258,
             '电厂': bufflist_258,
             '企鹅机械': bufflist_258,
             '人才公寓': bufflist_035
             }
buffs_res = {
             '媒体之声': bufflist_005,
             '企鹅机械':bufflist_010,
             '民食斋': bufflist_246,
             '人才公寓': bufflist_246,
             '平房': bufflist_246,
             '空中别墅': bufflist_258,
             '电厂': bufflist_258,
             '中式小楼': bufflist_035
             }

def calculateComb(buildings):
    buildtuple = buildings[0] + buildings[1] + buildings[2]
    starts = [start[x] for x in buildtuple]
    results = [1] * 9
    for item in buildtuple:
        if item in buffs_100:
            for buffed in buffs_100[item]:
                if buffed in buildtuple:
                    results[buildtuple.index(buffed)] += star[item]
        if item in buffs_50:
            for buffed in buffs_50[item]:
                if buffed in buildtuple:
                    results[buildtuple.index(buffed)] += star[item]*0.5
        if item in buffs_com:
            results[0:3] = np.add(results[0:3], buffs_com[item][star[item]-1])
        if item in buffs_ind:
            results[3:6] = np.add(results[3:6], buffs_ind[item][star[item]-1])
        if item in buffs_res:
            results[6:9] = np.add(results[6:9], buffs_res[item][star[item]-1])
#        print(item, results)
    return (np.sum([v*results[i] for i, v in enumerate(starts)]),
            [v*results[i]/startDict[star[buildtuple[i]]] for i, v in enumerate(starts)])
#
results = PQ()
#
class Result(object):
    def __init__(self, priority, builds):
        self.priority = priority
        self.builds = builds
        return
    def __lt__(self, other):
        return self.priority < other.priority
    def __eq__(self, other):
        return self.priority == other.priority

search_space=itertools.product(itertools.combinations(residence, 3), itertools.combinations(commercial, 3), itertools.combinations(industry, 3))
search_space_size=comb(len(industry), 3)*comb(len(commercial), 3)*comb(len(residence), 3)
print('Total iterations:', search_space_size)
for item in tqdm(search_space,total=search_space_size,bar_format='{percentage:3.0f}%,{elapsed}<{remaining}|{bar}|{n_fmt}/{total_fmt},{rate_fmt}{postfix}',ncols=70):
    prod = calculateComb(item)
#    if prod > Max:
#        print('\n', prod, item)
#        Max = prod
    results.put(Result(-prod[0], (item, prod[1])))
    pass

cdict = dict()
#for i in range(2):
#    cdict[i] = results.get()
#    print(-cdict[i].priority, cdict[i].builds)
print('==============')
Rec = results.get()
print('最优策略：', Rec.builds[0])
print('总加成倍率', np.round(sum([x*startDict[star[Rec.builds[0][i//3][i%3]]] for i, x in enumerate(Rec.builds[1])]), 2))
print('各建筑加成倍率', np.round(Rec.builds[1], 2))
print('升级优先级', np.round([x*startDict[star[Rec.builds[0][i//3][i%3]]] for i, x in enumerate(Rec.builds[1])], 2))

def getNext():
    print('==============')
    Rec = results.get()
    print('次优策略：', Rec.builds[0])
    print('总加成倍率', np.round(sum([x*startDict[star[Rec.builds[0][i//3][i%3]]] for i, x in enumerate(Rec.builds[1])]), 2))
    print('各建筑加成倍率', np.round(Rec.builds[1], 2))
    print('升级优先级', np.round([x*startDict[star[Rec.builds[0][i//3][i%3]]] for i, x in enumerate(Rec.builds[1])], 2))

last_result=[list(item) for item in last_result]
now_result=Rec.builds[0]
now_result=[list(item) for item in now_result]
for class_num in range(3):
    for item in last_result[class_num][:]:
        if item in now_result[class_num]:
            last_result[class_num].remove(item)
            now_result[class_num].remove(item)
print(last_result,'被')
print(now_result,'替换')

upgrade_order=np.argsort([x*startDict[star[Rec.builds[0][i//3][i%3]]] for i, x in enumerate(Rec.builds[1])])[::-1]
print('升级顺序:(',end='')
for item in upgrade_order[:-1]:
    print(item,',',sep='',end='')
print(upgrade_order[-1],')',sep='')
