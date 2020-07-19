# -*- coding: utf-8 -*-
import time
import re
import sys
sys.path.append('plugins/')
from OnlinePlayerAPI import check_online

msg='''
§6======== SimpleOP Reforged ========
§5一个由佛冷的SimpleOP魔改而来的小插件
§5魔改的目的是供自己使用，万物皆可魔改~
§5--GamerNoTitle
§6!!op 可以获取OP权限（无权限要求§4危险§6）
§6!!restart 可以重启服务器（有10s倒计时）
§6!!stop 可以关闭服务器（有10s倒计时）
§6!!save 可以手动保存服务器世界
§6!!sr sp 可以将自己的出生点设置为当前位置（黑曜石机调试必备）
§6!!sr where <player> 可以获取某位玩家的坐标
§6Being Developed...
§6===================================
'''
prefix='!!sr'

def process_coordinate(text):
	data = text[1:-1].replace('d', '').split(', ')
	data = [(x + 'E0').split('E') for x in data]
	return tuple([float(e[0]) * 10 ** int(e[1]) for e in data])

def on_info(server, info):
    waiting_time=10	# 在这里设置重启或关服等待的时间
    time_left=waiting_time
    message=info.content.split()
    if prefix in info.content or 'op' in info.content or 'deop' in info.content or 'restart' in info.content or 'stop' in info.content or 'save' in info.content:
        if info.content == '!!sr':
            server.tell(info.player, msg)
        
        if message[0]=='!!sr':
            print(len(message))
            print(message[2])
            if info.is_player and message[1] == 'where' and len(message)==3:
                player_for_search=message[2]
                try:
                    position = process_coordinate(re.search(r'\[.*\]', server.rcon_query('data get entity {} Pos'.format(player_for_search))).group())
                    where='玩家§b{}§r在[§6{} §6{} §6{}§r]'.format(player_for_search,int(position[0]),int(position[1]),int(position[2]))
                    server.tell(info.player, where)
                    server.tell(player_for_search, '玩家{}正在寻找你,你将会被应用15秒的高亮效果'.format(info.player))
                    server.execute('effect give {} minecraft:glowing 15 0 true'.format(player_for_search))
                except:
                    server.tell(info.player,'玩家§b{}§r不在线'.format(player_for_search))
                
            if info.is_player and message[1] == 'sp':
                position = process_coordinate(re.search(r'\[.*\]', server.rcon_query('data get entity {} Pos'.format(info.player))).group())
                server.execute('spawnpoint ' + info.player + ' {} {} {}'.format(int(list(position)[0]),int(list(position)[1]),int(list(position)[2])))

        if info.is_player and info.content == '!!op':
            server.execute('op ' + info.player)

        if info.is_player and info.content == '!!deop':
            server.execute('deop ' + info.player)


        if info.content == '!!restart':
            restart_message=''
            while True:
                restart_message='Server will restart in {} second(s), please save your work!'.format(time_left)
                server.say(restart_message)
                if(time_left==0):
                    server.restart()
                    break
                else:
                    time.sleep(1)
                    time_left=time_left-1

        if info.content == '!!stop':
            stop_message=''
            while True:
                stop_message='Server will close in {} second(s), please save your work!'.format(time_left)
                server.say(stop_message)
                if(time_left==0):
                    server.stop_exit()
                    break
                else:
                    time.sleep(1)
                    time_left=time_left-1
                    
        if info.content == '!!save':
            server.execute('save-all')