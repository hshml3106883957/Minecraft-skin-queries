import PyInstaller.__main__
import os

# 确保资源文件存在
if not os.path.exists('temp_preview.html'):
    with open('temp_preview.html', 'w', encoding='utf-8') as f:
        f.write('')  # 创建空文件，程序会在运行时生成内容

PyInstaller.__main__.run([
    'mcskin.py',
    '--name=MC皮肤查询器',
    '--windowed',  # 不显示控制台窗口
    '--icon=icon.ico',  # 如果你有图标的话
    '--add-data=temp_preview.html;.',  # 添加资源文件
    '--clean',
    '--noconfirm',
    '--onefile'  # 打包成单个文件
]) 