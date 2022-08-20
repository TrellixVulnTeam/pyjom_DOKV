# coding=utf-8
import re
import os
import math

# 设置
'''
skip_single_none
该选项控制是否跳过仅有一个时间标签并且没有文本内容的LRC行
'''
skip_single_none = True

'''
encoding
该选项控制读写时所用的文本编码
'''
read_encoding = 'utf-8'
write_encoding = 'utf-8'

'''
offset
默认歌词时间偏移，不会覆盖或叠加到文件中设置的偏移
单位为毫秒（ms），但实际处理时精度为厘秒（ms*10）
'''
offset = 0

'''
如果有需要更改ASS的默认Style
请到下方"ASS文件初始化"进行更改
'''

# 主程序

# 获取输入
# let's just fix this thing. shall we?
inputPath = "/root/Desktop/works/pyjom/tests/music_analysis/exciting_bgm.lrc" # presumeably it will output to the same dame directory.
realAssPath = "./output.ass"
print('FilePath:', inputPath)

# 规范化输入路径，去除前后双引号
lrc = os.path.normpath(inputPath).rstrip('\"').lstrip('\"')
exist = False
# 判断路径是否存在，若不存在，则请求用户再次输入直到其存在为止
if not os.path.exists(lrc):
    while exist is False:
        print('错误: 路径不可用')
        inputPath = input('FilePath:')
        lrc = os.path.normpath(inputPath).rstrip('\"').lstrip('\"')
        if os.path.exists(lrc):
            exist = True

# 分别获取文件名（无扩展名）和路径
lrc_name = os.path.splitext(os.path.basename(lrc))[0]
lrc_path = os.path.dirname(lrc) # oh shit...

# 打开LRC文件，读取所有行 为list，关闭文件
lrc_file = open(lrc, encoding=read_encoding)
lrc_line = lrc_file.readlines()
lrc_file.close()

# 定义需要使用的变量
line_indexs = []
ass_line = []
results = []
start_line = None
line_end = None
splitStr = None
# 编译正则表达式
pattern = re.compile('\\[[0-9]+:[0-9]+\\.[0-9]+\\]')
pattern2 = re.compile('\\[offset:-?[0-9]+\\]')

print('\n正在处理LRC计时标签...')

# 预处理
# 逐行输入LRC，搜索每一行的时间标签和时间标签所分割的文本，并添加到line_indexs
for i in range(0, len(lrc_line)):
    # 获取行
    s = lrc_line[i]
    # 初始化index
    index = []
    # 如果该行是空的就直接跳过
    if s is None:
        continue
    # 获取所有匹配正则表达式的字符串（即时间标签）
    results = pattern.findall(s)
    print("RESULTS:", results)
    # breakpoint()
    # 如果没有时间偏移信息，就尝试匹配时间偏移信息
    if offset == 0:
        offset_str = pattern2.findall(s)
        if len(offset_str) != 0:
            offset = int(offset_str[0].rstrip(']').lstrip('[').split(':')[1])
            print('找到歌词偏移值: {0:+}ms'.format(offset))
            continue
    # 如果没找到时间标签就跳过该行
    if len(results) == 0:
        continue
    # 获取时间标签分割的字符串
    splitStr = re.split(pattern, s)
    # 如果字符串组中有单独的换行符则移除
    if '\n' in splitStr:
        splitStr.remove('\n')
    # 写入index列表并输出进度
    for r in results:
        if s.find(r) != -1:
            index.append([s.find(r), r, len(s), i])
        print('\rLINE:{0} TAG:\"{3}\" INDEX:{1}'.format(i, str(s.find(r)), str(len(s) - 1 - 10), r), end='\n')
    # 写入line_indexs列表
    line_indexs.append([index, splitStr])

print('\n处理完成！正在进行ASS转换...\n')

# 初始化ASS文件头
# <editor-fold desc="ASS文件初始化">
ass_line.append('[Script Info]')
ass_line.append('; Script generated by lrc2ass_py3 1.0.0a')
ass_line.append('Title: {0}'.format(lrc_name))
ass_line.append('ScriptType: v4.00+')
ass_line.append('WrapStyle: 0')
ass_line.append('ScaledBorderAndShadow: yes')
ass_line.append('')
ass_line.append('[V4+ Styles]')
ass_line.append('Format: Name, Fontname, Fontsize, PrimaryColour, '
                'SecondaryColour, OutlineColour, BackColour, Bold, '
                'Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, '
                'Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, '
                'MarginR, MarginV, Encoding')
ass_line.append('Style: '
                'Default,Arial,20,&H00FFFFFF,&H000000FF,'
                '&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1')
ass_line.append('')
ass_line.append('[Events]')
ass_line.append('Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text')
# </editor-fold>

offset = int(offset / 10)


def tag_process(tag_str: str, line: int):
    # 时间标签处理函数
    # 去除时间标签首尾中括号
    tag_str = tag_str.lstrip('[').rstrip(']')
    # 切割分钟、秒、厘秒三个部分
    minute = int(tag_str.split(':')[0])
    second = int(tag_str.split(':')[1].split('.')[0])
    centisecond = int(tag_str.split('.')[1])
    # 计算总厘秒并添加偏移值
    tag_time = minute * 60 * 100 + second * 100 + centisecond + offset
    # 只有在添加偏移值后厘秒数为正数的，才会启用偏移
    if tag_time > 0:
        second, centisecond = divmod(tag_time, 100)
        if second > 0:
            minute, second = divmod(second, 60)
        else:
            minute = 0
    else:
        print('警告: 行\"{0}\"中时间标签\"{1}\"添加偏移值\"{2}ms\"后为负，该偏移不会被应用'
              .format(line, tag_str, offset * 10))
    # 再次计算厘秒数
    tag_time = minute * 60 * 100 + second * 100 + centisecond
    # 格式化输出
    if minute < 60:
        tag_str = '0:{0:0>2d}:{1:0>2d}.{2:0>2d}'.format(minute, second, centisecond)
    elif minute == 60:
        tag_str = '1:00:{0:0>2d}.{1:0>2d}'.format(second, centisecond)
    else:
        tag_str = '{0}:{1:0>2d}:{2:0>2d}.{3:0>2d}'\
            .format(int(math.modf(minute / 60)[1]), minute % 60, second, centisecond)
    # 返回结果
    # tag_time: 厘秒数
    # tag_str: 符合ASS格式的时间字符串
    return tag_time, tag_str


last_time = -1
start_time = -1
# 主要时间轴处理
'''
列表嵌套:
line_indexs[index[], splitStr[]]:
    index[[], [], ...]:
        [s.find(r), r, len(s), i]:
            s.find(r):  该时间标签在该行中的位置（以起始位置为准）
            r:          时间标签文本
            len(s):     该行长度
            i:          该行所在行数
    splitStr[]:
        == re.split()
'''
for i in range(0, len(line_indexs)):
    # 获取行数并定义基本参数
    line = line_indexs[i][0][0][3]
    ass_string = ''
    line_end = None
    backup_line_end = None
    single_tag = False
    # 检查是否需要跳过单个时间标签且没有实际内容的行
    if skip_single_none:
        if len(line_indexs[i][1]) == 1 and line_indexs[i][1][0].replace('\n', '') == '':
            print('警告: 已跳过单时间标签并且没有文本内容的行\"{0}\"\n'.format(line))
            continue
    # 索引index[]
    for iii in range(0, len(line_indexs[i][0])):
        # 获取时间标签递交处理
        tag = line_indexs[i][0][iii][1]
        str_time, tag = tag_process(tag, line)

        # 获取时间标签在字符串中的位置，字符串长度，该时间标签对应的字符
        index = int(line_indexs[i][0][iii][0])
        last_index = int(line_indexs[i][0][iii][2])
        str_lines = line_indexs[i][1][iii]
        last_index -= 11

        if index == 0:
            start_line = tag
            backup_line_end = tag
            start_time = str_time
            if len(line_indexs[i][0]) == 1:
                single_tag = True

                if iii + 1 < len(line_indexs[i][1]):
                    ass_string = '{0}{{\\k}}{1}'.format(str_time,
                                                        line_indexs[i][1][iii + 1]).replace('\n', '')
                else:
                    ass_string = ''

                print('警告: 行\"{0}\"是单时间标签LRC行，该行结束时间可能不准确'.format(line))
        elif index != last_index:
            if len(ass_string) > 0:
                ass_string = '{0}{{\\k{1}}}{2}'.format(ass_string, str(str_time - last_time), str_lines)
            else:
                ass_string = '{{\\k{0}}}{1}'.format(str(str_time - start_time), str_lines)
            last_time = str_time
            backup_line_end = tag
        else:
            line_end = tag
            if len(ass_string) > 0:
                ass_string = '{0}{{\\k{1}}}{2}'.format(ass_string, str(str_time - last_time), str_lines)
            else:
                ass_string = '{{\\k{0}}}{1}'.format(str(str_time - start_time), str_lines)

    if line_end is None:
        if not i + 1 == len(line_indexs):
            try:
                tag = line_indexs[i + 1][0][0][1]
                _, line_end = tag_process(tag)
            except Exception as e:
                print(e)
        else:
            if not backup_line_end is None:
                line_end = backup_line_end
            else:
                line_end = start_line
        print('警告: 行\"{0}\"没有结束时间标签，自动选择\"{1}\"作为结束时间\n'.format(line, line_end))

        line_end_time = int(line_end.split(':')[0]) * 60 + int(line_end.split(':')[1]) * 60 * 100 + \
                        int(line_end.split(':')[2].split('.')[0]) * 100 + int(line_end.split('.')[1])

        if single_tag and ass_string != '':
            str_time, str_line = ass_string.split('{\\k}')
            if str_line is not None:
                ass_string = '{{\\k{0}}}{1}'.format(str(int(line_end_time) - int(str_time)), str_line)

    ass_line.append('Dialogue: 0,{0},{1},Default,,0,0,0,,{2}'
                    .format(start_line, line_end, ass_string))

ass_fullpath = os.path.join(lrc_path, '{0}.ass'.format(lrc_name))


## overriding:
ass_fullpath = realAssPath
print("WRITING TO:", os.path.abspath(ass_fullpath))

if os.path.exists(ass_fullpath):
    print('已经有与\"{0}\"同名的文件了，是否要覆盖它？'.format('{0}.ass'.format(lrc_name)))
    print('\"是\"请输入任意字符，\"换个文件名输出\"请输入空值，\"否\"请关闭窗口:')
    check = input().replace(' ', '')
    if len(check) == 0:
        file_found_count = 0
        while os.path.exists(ass_fullpath):
            file_found_count += 1
            ass_fullpath = os.path.join(lrc_path, '{0}.s{1}.ass'.format(lrc_name, file_found_count))

try:
    ass_file = open(ass_fullpath, mode='w+', encoding=write_encoding)
    ass_file.write('\n'.join(ass_line))
    ass_file.close()
    print('成功输出ASS文件: \"{0}\"'.format(os.path.basename(ass_fullpath)))
except Exception as e:
    print(e)
