#!/usr/bin/python3
import switch, os, time

def check_different(res_succ):
    with open('/home/meidl/python/project_switch/autoBackup/log', 'w') as log:
        diff_list = []
        for each in res_succ:
            curr_config = each['config']
            try:
                with open(root_path+each['save_path']+'/'+each['name']+'.txt', 'r') as f:
                    last_config = f.read()
            except FileNotFoundError:
                os.system('mkdir -p '+root_path+each['save_path'])
                os.system('touch '+root_path+each['save_path']+'/'+each['name']+'.txt')
                last_config = ''
            diff_list.append((each, check_diff(curr_config, last_config)))

        changed_list = []
        non_changed_list = []

        for each in diff_list:
            if len(each[1][0]) == 0 and len(each[1][1]) == 0:
                non_changed_list.append(each)
            else:
                changed_list.append(each)

        print('There is %s device has changed config' % len(changed_list))

        log.write('*** Non changed list ***\n')
        for each in non_changed_list:
            log.write(('[%s] %s\n' % (each[0]['name'], each[0]['ip'])))

        log.write('*** Changed list ***\n')
        for each in changed_list:
            log.write(('[%s] %s\n' % (each[0]['name'], each[0]['ip'])))
            for each_add in each[1][0]:
                log.write('    [add] : ' + each_add + '\n')
            for each_delete in each[1][1]:
                log.write('    [delete] : ' + each_delete + '\n')
        log.write('\n')

def check_diff(curr, last):
    curr_list = curr.split('\n')
    curr_list = [x.replace('\r','') for x in curr_list]
    last_list = last.split('\n')

    add_list = []
    delete_list = []

    tmp_list = last_list.copy()
    for each in curr_list:
        try:
            tmp_list.pop(tmp_list.index(each))
        except ValueError:
            add_list.append(each)

    tmp_list = curr_list.copy()
    for each in last_list:
        try:
            tmp_list.pop(tmp_list.index(each))
        except ValueError:
            delete_list.append(each)

    return (add_list, delete_list)

def YesOrNo(context='please input [yes/no]'):
    while True:
        choose = input(context).lower()
        if choose in ['y','n','yes','no']:
            break
        else:
            print('input error !')
            time.sleep(1)
    if choose in ['y','yes']:
        return True
    if choose in ['n','no']:
        return False

def getInfo(**args):

    if args['vendor'] == 'huawei':
        SW = switch.switch_huawei(**args)
        infoList = ['dis curr']

    if args['vendor'] == 'maipu':
        SW = switch.switch_maipu(**args)
        infoList = ['sh run']

    if args['vendor'] == 'cisco':
        SW = switch.switch_cisco(**args)
        infoList = ['sh run']

    args.update(SW.getInfo(infoList))

    for i in ['dis curr', 'sh run']:
        if args.get(i, None):
            args['config'] = args[i]
            args.pop(i)

    args['name'] = SW.name
    return args

# main
Path = '/home/meidl/python/project_switch/autoBackup/switches.txt'
root_path = '/home/meidl/python/project_switch/autoBackup/configs/'
Switches = switch.getSW(Path)

# 将要执行的函数和参数分别组合成字典存入数组 tasks
tasks = [{'func':getInfo, 'args':each} for each in Switches]

while True:
# threadRunner 以多线程方式执行传入的数组里的函数以及对应的参数
    thread_runner = switch.threadRunner(tasks)
    result = thread_runner.run()
    failed_tasks = []
    res_succ = []    # save result witch successed

    for index, each in enumerate(result):
        if each.get('error', None):
            print('%s --- [failed] : %s' % (each['ip'], each['error']))
            failed_tasks.append(tasks[index])
        else:
            print('%s --- [success]' % each['ip'])
            res_succ.append(each)

    if len(failed_tasks) == 0 or not YesOrNo(('There are %s switches was failed, do you want recover ? [yes/no] ' % len(failed_tasks))):
        break

# check configs different
check_different(res_succ)

# save configs to file
if YesOrNo('Do you want to save config ? [yes/no] '):
    for each in res_succ:
        with open(root_path+each['save_path']+'/'+each['name']+'.txt', 'w') as f:
            f.write(each['config'])
else:
    exit()
