import sys
import init, make, datetime

def help():
    print('make: ヘルプを表示します')
    print('')
    print('    ./make')
    print('        - 今日の予定を出力します。')
    print('')
    print('    ./make [日付; YYYY-MM-DD]')
    print('        - 指定した日付の予定を出力します。')
    print('')
    print('    ./make daily [開始日; YYYY-MM-DD] [終了日; YYYY-MM-DD]')
    print('        - 指定した期間の予定を一日分ずつ表示します。')
    print('')
    print('    ./make total [開始日; YYYY-MM-DD] [終了日; YYYY-MM-DD]')
    print('        - 指定した期間の予定を集計して出力します。')
    print('')


def entry():
    args = sys.argv

    arg1 = None
    arg2 = None
    arg3 = None
    try:
        arg1 = args[1]
        arg2 = args[2]
        arg3 = args[3]
    except IndexError:
        pass

    if arg1 == None:
        arg1 = 'daily'

    if arg1 == 'init':
        init.initmain()
        return
    if arg1 == 'daily':
        make.daily(arg2, arg3)
        return
    if arg1 == 'total':
        make.total(arg2, arg3)
        return
    if arg1 == 'time':
        make.timebased(arg2, arg3)
        return
    try:
        _ = datetime.datetime.strptime(arg1, '%Y-%m-%d')
    except:
        help()
    else:
        try:
            _ = datetime.datetime.strptime(arg2, '%Y-%m-%d')
        except:
            make.daily(arg1, arg1)
        else:
            make.daily(arg1, arg2)

if __name__ == '__main__':
    entry()
    