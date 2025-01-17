#!/usr/bin/python3
# RegisterSprite  Copyright (C) 2020  jessenhua (h1657802074@gmail.com)

# This file is part of RegisterSprite
#   ____ ____  _      __     _______  ___
#  / ___|  _ \| |     \ \   / /___ / / _ \
# | |  _| |_) | |      \ \ / /  |_ \| | | |
# | |_| |  __/| |___    \ V /  ___) | |_| |
#  \____|_|   |_____|    \_/  |____(_)___/
#
# RegisterSprite is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
''''''
"""
 ____            _     _              ____             _ _
|  _ \ ___  __ _(_)___| |_ ___ _ __  / ___| _ __  _ __(_) |_ ___
| |_) / _ \/ _` | / __| __/ _ \ '__| \___ \| '_ \| '__| | __/ _ \
|  _ <  __/ (_| | \__ \ ||  __/ |     ___) | |_) | |  | | ||  __/
|_| \_\___|\__, |_|___/\__\___|_|    |____/| .__/|_|  |_|\__\___|
           |___/                           |_|

https://gitee.com/JensenHua/register_sprite

    _    ____  __  __     _     _
   / \  |  _ \|  \/  |   | |   (_)_ __  _   ___  __
  / _ \ | |_) | |\/| |   | |   | | '_ \| | | \ \/ /
 / ___ \|  _ <| |  | |   | |___| | | | | |_| |>  <
/_/   \_\_| \_\_|  |_|   |_____|_|_| |_|\__,_/_/\_\

 _____                               _
| ____|_   _____ _ __ _   ___      _| |__   ___ _ __ ___
|  _| \ \ / / _ \ '__| | | \ \ /\ / / '_ \ / _ \ '__/ _ \
| |___ \ V /  __/ |  | |_| |\ V  V /| | | |  __/ | |  __/
|_____| \_/ \___|_|   \__, | \_/\_/ |_| |_|\___|_|  \___|
                      |___/                                                                    
"""

# import **************************************************
import os
import tkinter as tk
from tkinter import *
from tkinter import messagebox

from lib import _color_operations
from lib import _debug
from lib import _file_operations


class MyGui(Frame):
    # kv结构体
    class Namedvariable(object):
        def __init__(self, name, value):
            self.name = name
            self.value = value

    # event start ***************************************************

    # 16进制Entry回车事件处理函数
    def update_btn_val_by_entry(self, event):
        origin_data = self.hex_output.get()
        # 尝试去除0x前缀
        if origin_data[0:2] == "0x":
            origin_data = origin_data[2:]

        # 数据处理
        # 16进制转10进制

        hex_data = origin_data
        dec_data = 0
        weight = len(hex_data) - 1  # 权
        # 遍历十六进制数据各位（从左边开始）,递减权重
        for bit in hex_data:
            # 判断数据有效性，累加十进制数据
            if bit in list(self.upper_str_hex_after9) or bit in list(self.upper_str_hex_after9.lower()):
                dec_data += self.dict_hex_after9[bit] * pow(16, weight)
            else:
                # 打印错误信息
                print(self.fontstyle.color_font("ERROR, Unrecognized HEX <{}> From User Input!", 7, 31, 40).format(bit))

            weight-=1

        # 获取数据二进制字符串
        dec_data = int(dec_data)
        dec_data = int(dec_data)
        str_bin_data = str(bin(dec_data))[2:]

        # 设置按钮位
        btn_cnt = 32
        data_length = len(str_bin_data)
        for btn in self.btn_list:
            if btn_cnt > data_length:
                btn['text'] = '0'
                btn_cnt -= 1
                continue
            btn['text'] = str_bin_data[0]
            str_bin_data = str_bin_data[1:]

        # 更新样式以及数据
        self.update_btn_style()
        self.show_data()

    # event end ***************************************************

    # 结构体生成函数
    def make_struct(self, name, value):
        return self.Namedvariable(name=name, value=value)

    def __init__(self, master=None):
        super().__init__(master)
        self.main_window_title = 'Register Sprite'
        self.Window = master  # 主窗体
        self.pack()

        self.flag_user_config = False  # 用户配置文件标识，False为不存在
        self.path_user_config = r'./user-config.ini'  # 用户配置文件路径
        self.fops = _file_operations.FileOperations()  # 配置文件操作
        self.fontstyle = _color_operations.FontStyle()  # 终端打印样式

        self.lbl_list = []  # 按钮上label列表
        self.btn_list = []  # 位按钮列表
        self.placeholder_list = []  # 占位控件列表
        self.btn_num = 31  # 按钮顶部label字符
        # self.cpu_word_length = DWORD  # 默认CPU字长

        # 31-16 和 15-0 位按钮
        self.frame_btn_row1 = Frame(self.Window)
        self.frame_btn_row2 = Frame(self.Window)

        self.bg_color = self.make_struct('backgroundcolor', "#f0f0f0")
        self.btn_color = self.make_struct('buttoncolor', '#f3f1ef')
        self.text_color = self.make_struct('textcolor', '#000000')

        self.color_dict = {}
        self.color_dict['backgroundcolor'] = self.bg_color.value
        self.color_dict['buttoncolor'] = self.btn_color.value
        self.color_dict['textcolor'] = self.text_color.value

        # 初始化16进制字典
        self.dict_hex_after9 = {}
        self.upper_str_hex_after9 = "0123456789ABCDEF"
        lower_str_hex_after9 = self.upper_str_hex_after9.lower()
        for i in range(0, 16):
            self.dict_hex_after9[self.upper_str_hex_after9[i]] = i
            self.dict_hex_after9[lower_str_hex_after9[i]] = i

        # 初始化操作
        self.init_user_config()
        self.init_frame()
        self.init_menu()
        self.init_color()
        self.init_view()

        # print(self.ChangeBackgroundColor(self.bg_color))

    @_debug.printk()
    def init_user_config(self):
        if os.path.exists(self.path_user_config):
            self.flag_user_config = True
        else:
            print(f'{self.path_user_config}not found, creating')
            with open(self.path_user_config, 'w') as config:
                self.flag_user_config = True
                config.close()

    @_debug.printk()
    def init_frame(self):
        if self.flag_user_config:
            # 尝试获取Main窗口标题属性值
            try:
                self.main_window_title = self.fops.read_config(path=self.path_user_config,
                                                               section='Title',
                                                               key='MainWindowTitle')
                print(self.main_window_title)
            except:
                print('Title section not found! Using default window title')

            self.fops.write_config(self.path_user_config, 'Title', 'MainWindowTitle', self.main_window_title)
            pass
        else:
            # 将默认标题属性值写入配置文件
            self.fops.write_config(self.path_user_config, 'Title', 'MainWindowTitle', self.main_window_title)
            pass
        # 设置标题
        self.Window.title(self.main_window_title)

        self.frame_show = Frame(self.Window)
        self.frame_choice = Frame(self.frame_show)
        self.frame_label = Frame(self.frame_show)
        self.frame_entry = Frame(self.frame_show)

    @_debug.printk()
    def init_menu(self):
        menu_font_type = "黑体"
        menu_font_size = 10
        menu_font_tuple = (menu_font_type, menu_font_size)

        menuBar = Menu(self.Window, font=menu_font_tuple)

        self.Window.config(menu=menuBar)

        # 设置菜单
        settingBar = Menu(menuBar, tearoff=0)
        settingBar.add_command(label="背景色",
                               command=self.BackgroundColorCommand,
                               font=menu_font_tuple)

        # 文件菜单
        fileBar = Menu(menuBar, tearoff=0)
        fileBar.add_cascade(label="设置", menu=settingBar, font=menu_font_tuple)
        fileBar.add_separator()
        fileBar.add_command(label="退出", command=self.my_quit, font=menu_font_tuple)
        menuBar.add_cascade(label='文件', menu=fileBar, font=menu_font_tuple)

        # 帮助菜单
        helpBar = Menu(menuBar, tearoff=0)
        helpBar.add_command(label="关于", command=self.about, font=menu_font_tuple)
        menuBar.add_cascade(label="帮助", menu=helpBar, font=menu_font_tuple)

    def my_quit(self):
        message = self.fontstyle.color_font(text="Bye",
                                            display_type=7,
                                            foreground_color=31,
                                            backgroud_color=46)
        print(message)
        self.quit()

    def about(self):
        about_info = \
            """
                寄存器小精灵 | Register Sprite 
                项目地址： http://www.gitee.com/JensenHua/register_sprite
                版本： v2021.1
            """
        messagebox.showinfo("关于", about_info)

    @_debug.printk()
    def init_color(self):
        if self.flag_user_config:
            try:
                color_dict = self.fops.read_config_section(path=self.path_user_config,
                                                           section='Color')

                for color in color_dict:
                    if color == self.bg_color.name:
                        self.bg_color.value = color_dict[color]
                        print(self.bg_color.value)
                    elif color == self.btn_color.name:
                        self.btn_color.value = color_dict[color]
                    elif color == self.text_color.name:
                        self.text_color.value = color_dict[color]
            except:
                print('Section not found.')

            self.Window.configure(bg=self.bg_color.value)
            pass
        else:
            self.fops.write_config_section(path=self.path_user_config,
                                           section='Color',
                                           data_dict=self.color_dict)
            pass

    @_debug.printk()
    def create_obj_group(self, frame, row, column):
        # 4次循环
        for i in range(4):
            lbl = tk.Label(frame,
                           background=self.bg_color.value,
                           text=self.btn_num,
                           font=("宋体", 9, "bold")
                           )
            lbl.grid(row=row,
                     column=column + i,
                     sticky=W + E + N + S, padx=7, pady=7)

            # 创建按钮
            obj = Button(frame,
                         text='0',
                         width='3',
                         height='2',
                         background=self.btn_color.value,
                         font=("宋体", 9, "bold"))

            '''
                这是for循环生成按钮，同时单独操作每个按钮的解决方案
                lambda button=obj: self_bit(button)
                这样每个按钮被点击时都会有自己独立的调用方式——将自己传给处理函数

            '''
            obj.config(command=lambda button=obj: self.set_bit(button))
            obj.grid(row=row + 1, column=column + i)

            # label上显示的字符减一
            self.btn_num -= 1
            # 将按钮添加到 总按钮列表用  数据更新函数会遍历列表取得二进制数据
            self.btn_list.append(obj)
            self.lbl_list.append(lbl)

    '''
        控件生成函数
    '''

    @_debug.printk()
    def init_view(self):
        '''
            这两个for循环并不涉及数据的更改和显示
            仅仅作为占位控件来使按钮易于布局
        '''
        for i in range(19):
            lbl = Label(self.frame_btn_row1,
                        background=self.bg_color.value,
                        text='  ',
                        font=("宋体", 8, "bold"))
            self.placeholder_list.append(lbl)
            lbl.grid(row=5,
                     column=i,
                     sticky=W + E + N + S, padx=7, pady=7)
        for i in range(19):
            lbl = Label(self.frame_btn_row2,
                        background=self.bg_color.value,
                        text='  ',
                        font=("宋体", 8, "bold"))
            self.placeholder_list.append(lbl)
            lbl.grid(row=5,
                     column=i,
                     sticky=W + E + N + S, padx=7, pady=7)
        '''第一部分用来生成31-16位的label和button'''
        pad = 0
        call_mode = 0  # 用来设置是否为第一组控件
        for i in range(4):
            if call_mode == 0:
                self.create_obj_group(self.frame_btn_row1, 0, pad)
                pad += 4
                call_mode = 1  # 第一组控件生成完毕，更改标志位
            else:
                # 生成其余组控件
                self.create_obj_group(self.frame_btn_row1, 0, pad + 1)
                pad += 5

        # 将第一部分控件pack
        self.frame_btn_row1.pack(side=TOP)
        self.frame_btn_row1.configure(bg=self.bg_color.value)

        '''第二部分用来生成15-0位的label和button， 相关解释看第一部分'''
        pad = 0
        call_mode = 0
        for i in range(4):
            if call_mode == 0:
                self.create_obj_group(self.frame_btn_row2, 2, pad)
                pad += 4
                call_mode = 1
            else:
                self.create_obj_group(self.frame_btn_row2, 2, pad + 1)
                pad += 5

        # 将第二部分控件pack
        self.frame_btn_row2.pack(side=TOP)
        self.frame_btn_row2.configure(bg=self.bg_color.value)

        '''
        以下代码用来创建下半部分空间，包括x进制的label、Entry和复选框功能区
        frame_show继承自Window

        frame_label用来存放进制的提示区
        frame_entry用来存放进制的回显区
        frame_choice用来存放复选功能
        以上三者继承自frame_show
        '''

        self.frame_show.pack()
        self.frame_show.configure(bg=self.bg_color.value)

        # 进制label区
        self.hex = Label(self.frame_label,
                         background=self.bg_color.value,
                         text="16进制",
                         font=("宋体", 12, "bold"))
        self.hex.pack(side=TOP)
        self.decimal = Label(self.frame_label,
                             background=self.bg_color.value,
                             text="10进制",
                             font=("宋体", 12, "bold"))
        self.decimal.pack(side=TOP)
        self.octal = Label(self.frame_label,
                           background=self.bg_color.value,
                           text="8进制",
                           font=("宋体", 12, "bold"))
        self.octal.pack(side=TOP)
        self.binary = Label(self.frame_label,
                            background=self.bg_color.value,
                            text="2进制",
                            font=("宋体", 12, "bold"))
        self.binary.pack(side=TOP)

        # 进制换算区
        self.hex_output = Entry(self.frame_entry,
                                background='#f0f0f0',
                                width=40,
                                font=("宋体", 12, "bold"))
        self.hex_output.bind('<Return>', func=self.update_btn_val_by_entry)
        self.hex_output.pack(side=TOP)

        self.decimal_output = Entry(self.frame_entry,
                                    background='#f0f0f0',
                                    width=40,
                                    font=("宋体", 12, "bold"))
        # self.decimal_output.bind('<Return>', func=self.update_btn_val_by_entry)
        self.decimal_output.pack(side=TOP)

        self.octal_output = Entry(self.frame_entry,
                                  background='#f0f0f0',
                                  width=40,
                                  font=("宋体", 12, "bold"))
        # self.octal_output.bind('<Return>', func=self.update_btn_val_by_entry)
        self.octal_output.pack(side=TOP)

        self.binary_output = Entry(self.frame_entry,
                                   background='#f0f0f0',
                                   width=40,
                                   font=("宋体", 12, "bold"))
        # self.binary_output.bind('<Return>
        self.binary_output.pack(side=TOP)

        '''
            拓展功能区，主要拓展如下
            十六进制以位位移形式显示
        '''
        # 置位
        self.label_hex_shift_set = Label(self.frame_label,
                                         background=self.bg_color.value,
                                         text="置位",
                                         font=("宋体", 10))
        self.label_hex_shift_set.pack(side=TOP, pady=5)

        self.entry_hex_shift_set = Entry(self.frame_entry,
                                         background='#f0f0f0',
                                         width=45,
                                         font=("宋体", 10, "bold"))
        self.entry_hex_shift_set.pack(side=TOP, pady=5)

        # 清零
        self.label_hex_shift_clear = Label(self.frame_label,
                                           background=self.bg_color.value,
                                           text="清零",
                                           font=("宋体", 10))

        self.label_hex_shift_clear.pack(side=TOP)

        self.entry_hex_shift_clear = Entry(self.frame_entry,
                                           background='#f0f0f0',
                                           width=45,
                                           font=("宋体", 10, "bold"))
        self.entry_hex_shift_clear.pack(side=TOP)

        self.frame_label.pack(side=LEFT)
        self.frame_entry.pack(side=LEFT)

        self.frame_label.configure(bg=self.bg_color.value)
        self.frame_entry.configure(bg=self.bg_color.value)

        self.init_value()

        # 这里创建复选框功能区
        self.CheckVar = IntVar()
        self.ck_btn = Checkbutton(self.frame_choice,
                                  text="窗口保持在全屏幕的顶部",
                                  background=self.bg_color.value,
                                  variable=self.CheckVar,
                                  onvalue=1, offvalue=0,
                                  command=self.isChecked)
        self.ck_btn.pack(side=TOP)

        self.pro_btn_frame = Frame(self.frame_choice)
        # 左移功能按钮
        self.lsh_btn = Button(self.pro_btn_frame,
                              background=self.btn_color.value,
                              text="左移")
        self.lsh_btn.config(command=self.left_shift)
        self.lsh_btn.pack(side=LEFT)

        # 右移功能按键
        self.rsh_btn = Button(self.pro_btn_frame,
                              background=self.btn_color.value,
                              text="右移")
        self.rsh_btn.config(command=self.right_shift)
        self.rsh_btn.pack(side=LEFT)

        # 求非功能按键
        self.not_btn = Button(self.pro_btn_frame,
                              background=self.btn_color.value,
                              text="求非")
        self.not_btn.config(command=self.calc_not)
        self.not_btn.pack(side=LEFT)

        # 复位功能按键
        self.rst_btn = Button(self.pro_btn_frame,
                              background=self.btn_color.value,
                              text="复位")
        self.rst_btn.config(command=self.bit_reset)
        self.rst_btn.pack(side=LEFT)

        self.pro_btn_frame.pack(side=TOP)

        self.frame_data_size = Frame(self.frame_choice)
        # 数据大小，单位KB
        self.label_bin_size = Label(self.frame_data_size,
                                    background=self.bg_color.value,
                                    text="数据大小",
                                    font=("宋体", 9, "bold"))
        self.label_bin_size.pack(side=LEFT)
        self.entry_bin_size = Entry(self.frame_data_size,
                                    background='#f0f0f0',
                                    width=10,
                                    font=("宋体", 12, "bold"))

        self.entry_bin_size.pack(side=LEFT)
        self.label_unit_size = Label(self.frame_data_size,
                                     background=self.bg_color.value,
                                     text="bits",
                                     font=("宋体", 9, "bold"))
        self.label_unit_size.pack(side=LEFT)
        self.frame_data_size.configure(bg=self.bg_color.value)
        self.frame_data_size.pack(side=TOP, pady=5, anchor='e')
        # 复选框区域打包
        self.frame_choice.pack(side=TOP)
        self.frame_choice.configure(bg=self.bg_color.value)

    @_debug.printk()
    def CWL_change(self, cwl):
        print("CPU WORD LENGTH: ", cwl)
        pass

    '''
        数据初始化函数
    '''

    @_debug.printk()
    def init_value(self):
        # 这部分代码用来向回显区插入初始数据，并无实际作用
        self.binary_output['state'] = 'normal'
        self.hex_output.insert(0, '0x00000000')
        self.decimal_output.insert(0, '0')
        self.octal_output.insert(0, '0o0')
        self.binary_output['state'] = 'normal'
        self.binary_output.insert(0, '0000 0000 0000 0000 0000 0000 0000 0000')
        self.binary_output['state'] = 'readonly'

        self.entry_hex_shift_set.insert(0, '0')
        self.entry_hex_shift_clear.insert(0, '0')
        self.binary_output['state'] = 'readonly'

    '''
        数据清除函数
    '''

    @_debug.printk()
    def clear_value(self):
        '''清空各进制回显区，每次修改前都要先清空'''
        self.binary_output['state'] = 'normal'
        self.hex_output.delete(0, END)
        self.decimal_output.delete(0, END)
        self.octal_output.delete(0, END)
        self.binary_output.delete(0, END)

        self.entry_hex_shift_set.delete(0, END)
        self.entry_hex_shift_clear.delete(0, END)
        self.entry_bin_size.delete(0, END)
        self.binary_output['state'] = 'readonly'

    '''
        show_data 数据显示函数
        该函数用来将按钮数据处理后显示到进制换算区
    '''

    @_debug.printk()
    def show_data(self):
        self.clear_value()
        self.binary_output['state'] = 'normal'  # 将二进制回显区设置为可写

        # 初始化
        _bin = self.get_bin_value(mode='normal')
        not_bin = self.get_bin_value(mode='not')
        _oct = ''
        _hex = ''
        bin_show = self.get_bin_value(mode='show')

        # 进制转换
        dec = int(_bin, 2)
        not_dec = int(not_bin, 2)
        _hex = hex(dec)
        not_hex = hex(not_dec)
        '''
            直接使用hex()函数会得到一个这样的数据 0x7
            而我们要显示这样的                   0x00000007
            其实两者相等，只不过后者更加便于查看
        '''
        temp_str = ''  # 临时字符串，用来存放0
        temp_str_not = ''
        # 根据hex()得到最低为3位的数据，可以得出0的个数，累加到temp_str中
        for n in range(10 - len(_hex)):
            temp_str += '0'

        # 拼接字符串，以'x'隔开字符串，取后半部分
        # 0x + n0(n=7) + 0x7.split('x')[1] 等于 7 即 0x00000007
        _hex = '0x' + temp_str + _hex.split('x')[1]
        not_hex = '0x' + temp_str_not + not_hex.split('x')[1]

        # 得到8进制数据
        _oct = oct(dec)

        '''
            进阶功能区数据处理
            这部分的思路是将二进制数据每四个分为一组处理，32位模式下共8组
            这里并没有考虑其他字长模式cpu的情况，后期如果添加其他字长模式要修改这部分代码
        '''
        # 置位数据处理
        hex_bit_dict = {}  # 总16进制数据字典
        hex_bit_list = bin_show.split(' ')[:8]
        bit_index = 7  # 32位模式  8组4位二进制数据

        # 遍历列表将数据以如下形式保存到字典中
        # 7:0000  6:0000
        for hex_bit in hex_bit_list:
            hex_bit_dict[bit_index] = hex_bit
            bit_index -= 1

        # 获取有效值，即不为0的组
        current_value_dict = {}  # 有效值字典

        # 遍历上一步得到的字典，得到有效值字典
        for key in hex_bit_dict:
            if hex_bit_dict[key] != '0000':
                current_value_dict[key] = hex_bit_dict[key]

        # 获得字典长度，后边判断显示格式会用到
        len_current_value_dict = len(current_value_dict)

        # 要拼接显示的到置位区的字符串，格式如下
        # （1 << 10） | (3 << 12)
        current_value_str = ''

        # 根据字典长度处理字符串格式
        if len_current_value_dict == 1:
            for pkey in current_value_dict:
                current_hex_value = hex(int(current_value_dict[pkey], 2))
                current_value_str += '({0}<<{1})'.format(current_hex_value, pkey * 4)
        elif len_current_value_dict > 1:
            for pkey in current_value_dict:
                current_hex_value = hex(int(current_value_dict[pkey], 2))
                current_value_str += '|({0}<<{1})'.format(current_hex_value, pkey * 4)
            current_value_str = current_value_str[1:]
        else:
            pass

        # 清零数据处理在遍历按钮和进制转换时已经处理完成

        '''
            更新数据
        '''
        self.hex_output.insert(0, _hex)
        self.decimal_output.insert(0, dec)
        self.octal_output.insert(0, _oct)
        self.binary_output.insert(0, bin_show)

        # 更新进阶功能区
        self.entry_hex_shift_set.insert(0, current_value_str)
        self.entry_hex_shift_clear.insert(0, not_hex)

        # 这里要注意，如果将十进制数据进行大小计算，需要在原数据上+1
        this_dec = dec
        result = 0
        # 一些单位换算，后期可以独立出来作为功能甘薯
        if this_dec < 8:
            result = this_dec
            self.label_unit_size['text'] = "bits"
        elif this_dec >= 8 and this_dec < 1024:
            result = this_dec / 8
            self.label_unit_size['text'] = "Byte"
        elif this_dec >= 1024 and this_dec < 0x100000:
            result = this_dec / 1024
            self.label_unit_size['text'] = "KByte"
        elif this_dec >= 0x100000 and this_dec < 0x40000000:
            result = this_dec / 0x100000
            self.label_unit_size['text'] = "MByte"
        else:
            this_dec = dec + 1
            result = this_dec / 0x40000000
            self.label_unit_size['text'] = "GByte"

        self.entry_bin_size.insert(0, result)
        self.binary_output['state'] = 'readonly'  # 将二进制回显区设置为只读

    '''
        按钮每次点击都会调用该函数，执行完样式更改后调用数据更新函数
    '''

    @_debug.printk()
    def set_bit(self, obj):

        # 根据按钮值更改按钮显示信息
        if obj['text'] == '0':
            obj.config(text='1')
        elif obj['text'] == '1':
            obj.config(text='0')

        # 调用数据更新函数
        self.update_btn_style()
        self.show_data()

    '''
        mode
            normal : 二进制数据
            not    : 求非后的二进制数据
            bin_show  :  用于显示给用户的二进制数据
    '''

    @_debug.printk()
    def get_bin_value(self, mode):
        # 遍历按钮数组，将按钮值拼接为字符串，得到一个二进制数据
        # _bin为初始数据
        # bin_show为显示到回显区的数据，因为便于查看，每隔4位插入了一个空格，不能用于进制转换,仅作显示
        _bin = ''
        not_bin = ''
        bin_show = ''
        space_cnt = 0

        for i in self.btn_list:
            if i['text'] == '1':
                _bin += i['text']
                bin_show += i['text']
                not_bin += '0'
                space_cnt += 1
            elif i['text'] == '0':
                _bin += i['text']
                bin_show += i['text']
                not_bin += '1'
                space_cnt += 1

            if space_cnt == 4:
                bin_show += ' '
                space_cnt = 0

        if mode == 'normal':
            return _bin
        elif mode == 'not':
            return not_bin
        else:
            return bin_show

    '''
        按钮样式更新函数
    '''

    @_debug.printk()
    def update_btn_style(self):
        for btn in self.btn_list:
            if btn['text'] == '0':
                btn.config(relief='raised')  # 设置按钮样式为升起
                btn.config(bg='#f0f0f0')
            else:
                btn.config(relief='sunken')  # 设置按钮样式为按下
                btn.config(bg='gray')

    '''
        复位功能函数
    '''

    @_debug.printk()
    def bit_reset(self):
        # 遍历按钮列表，将按钮恢复至初始状态，即数值0样式为升起
        for btn in self.btn_list:
            btn.config(text='0')

        self.update_btn_style()
        '''
            复位的数据处理其实可以有很多种方法，这里提供了两种
            1.先清除显示区，再插入初始值
            2.直接调用show_data()函数处理按钮数据
            两种方法最终效果都差不多，但是前者的资源开销应该小一点
        '''
        self.clear_value()  # 清除数据
        self.init_value()  # 初始化数据
        # self.show_data()

    '''
        求非功能函数
    '''

    @_debug.printk()
    def calc_not(self):
        # 遍历按钮列表,反转按钮值和样式
        for btn in self.btn_list:
            if btn['text'] == '0':
                btn.config(text='1')
            else:
                btn.config(text='0')

        self.update_btn_style()
        # 这里直接调用数据处理显示函数就行了
        self.show_data()

    '''
        左右移位功能
    '''

    @_debug.printk()
    def left_shift(self):
        # 得到二进制数据
        _bin = self.get_bin_value(mode='normal')

        # 判断数据是否有效
        if int(_bin) == 0:
            return

        # 左移数据
        _bin += '0'
        _bin = _bin[1:]

        # 更新数据
        cnt = 0
        for bit in _bin:
            self.btn_list[cnt]['text'] = bit
            cnt += 1

        # 显示更新
        self.update_btn_style()
        self.show_data()

    @_debug.printk()
    def right_shift(self):
        # print(' called！')
        # 得到二进制数据
        _bin = self.get_bin_value(mode='normal')

        # 判断数据是否有效
        if int(_bin) == 0:
            return

        # 右移数据处理
        origin_bin = '0'
        origin_bin += _bin
        _bin = origin_bin[:32]

        # 更新数据
        cnt = 0
        for bit in _bin:
            self.btn_list[cnt]['text'] = bit
            cnt += 1

        # 显示更新
        self.update_btn_style()
        self.show_data()

    '''
        窗口置顶函数
    '''

    @_debug.printk()
    # 窗口置顶复选框调用函数
    def isChecked(self):
        val = self.CheckVar.get()
        if val == 1:
            # 窗口保持在全屏幕的顶部
            self.Window.attributes("-toolwindow", 1)
            self.Window.wm_attributes("-topmost", 1)
        else:
            # 取消 窗口保持在全屏幕的顶部
            self.Window.attributes("-toolwindow", 0)
            self.Window.wm_attributes("-topmost", 0)

    @_debug.printk()
    # 背景色切换窗口生成函数
    def askColorInfo(self):
        color_input = _color_operations.ColorChoiceFrame(master=self.Window)
        self.Window.wait_window(color_input)
        # print(color_input.color_data_list)
        return color_input.current_btn_value

    @_debug.printk()
    # 代码复用，作用是遍历列表，设置背景色
    def TraverseTargetList(self, list_):
        for obj in list_:
            obj.config(bg=self.bg_color.value)

    @_debug.printk()
    # 菜单项背景色调用函数
    def BackgroundColorCommand(self):
        # 拉起颜色选择窗口
        target_color = self.askColorInfo()
        print(target_color)
        if target_color != "None":
            self.ChangeBackgroundColor(target_color)

    @_debug._timeit
    # 背景色切换函数
    def ChangeBackgroundColor(self, color):
        '''
            @author: hz
        :param color: 用户将要切换的背景颜色
        :return: 程序执行状态
        '''
        err = 1
        try:
            # 窗体背景颜色更换
            self.bg_color.value = _color_operations.GetColor(color)
            # 将背景颜色写入配置文件
            self.fops.write_config(path=self.path_user_config,
                                   section='Color',
                                   key='BackGroundColor',
                                   value=self.bg_color.value)

            # 背景颜色更换操作
            self.Window.configure(bg=self.bg_color.value)
            self.frame_btn_row1.configure(bg=self.bg_color.value)
            self.frame_btn_row2.configure(bg=self.bg_color.value)
            self.frame_label.configure(bg=self.bg_color.value)
            self.frame_show.configure(bg=self.bg_color.value)
            self.frame_entry.configure(bg=self.bg_color.value)
            self.frame_choice.configure(bg=self.bg_color.value)

            # label及占位符背景颜色更换
            self.TraverseTargetList(self.lbl_list)
            self.TraverseTargetList(self.placeholder_list)

            # 进制label背景颜色更换
            self.hex.config(bg=self.bg_color.value)
            self.octal.config(bg=self.bg_color.value)
            self.decimal.config(bg=self.bg_color.value)
            self.binary.config(bg=self.bg_color.value)

            # 置位及清零label背景颜色更换
            self.label_hex_shift_set.config(bg=self.bg_color.value)
            self.label_hex_shift_clear.config(bg=self.bg_color.value)

            # checkbox背景颜色更换
            self.ck_btn.config(bg=self.bg_color.value)

            # 数据大小背景色更换
            self.frame_data_size.config(bg=self.bg_color.value)
            self.label_bin_size.config(bg=self.bg_color.value)
            self.label_unit_size.config(bg=self.bg_color.value)

            return err
        except:
            return -err


@_debug.printk()
def main():
    root = Tk()
    # 设置窗口大小不可更改
    root.resizable(0, 0)

    # 适配高分屏下程序界面、字体模糊
    # 注意以下设置仅适用于windows系统
    # 调用api设置成由应用程序缩放
    # ctypes.windll.shcore.SetProcessDpiAwareness(1)
    # # 调用api获得当前的缩放因子
    # ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
    # # 设置缩放因子
    # root.tk.call('tk', 'scaling', ScaleFactor / 75)

    app = MyGui(master=root)
    app.mainloop()


if __name__ == '__main__':
    main()
