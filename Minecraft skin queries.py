import requests
import json
import base64
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Optional, Dict, Any
from PIL import Image, ImageTk
from io import BytesIO
import webbrowser
import os

class MinecraftSkinGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Minecraft 皮肤查询器")
        self.root.geometry("800x700")  # 调整窗口大小
        self.root.iconbitmap("awa.ico")

        # 设置主题样式
        style = ttk.Style()
        style.configure(
            "TButton",
            padding=10,
            relief="flat",
            background="#2196F3",
            font=("Microsoft YaHei UI", 10)
        )
        style.configure(
            "TEntry",
            padding=8,
            font=("Microsoft YaHei UI", 10)
        )
        style.configure(
            "TFrame",
            background="#f5f5f5"
        )
        style.configure(
            "Title.TLabel",
            font=("Microsoft YaHei UI", 24, "bold"),
            foreground="#1976D2",
            background="#f5f5f5"
        )
        style.configure(
            "URL.TLabel",
            font=("Microsoft YaHei UI", 9),
            foreground="#666666",
            background="#f5f5f5"
        )
        
        self.skin_finder = MinecraftSkin()
        self.current_skin_url = None
        self.webview_window = None
        self.setup_ui()

    def setup_ui(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="30", style="TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 标题
        title_label = ttk.Label(
            main_frame, 
            text="Minecraft 皮肤查询",
            style="Title.TLabel"
        )
        title_label.pack(pady=(0, 30))

        # 输入区域
        input_frame = ttk.Frame(main_frame, style="TFrame")
        input_frame.pack(fill=tk.X, pady=(0, 20))

        # 添加输入提示标签
        input_label = ttk.Label(
            input_frame,
            text="请输入正版玩家ID：",
            font=("Microsoft YaHei UI", 11),
            foreground="#333333",
            background="#f5f5f5"
        )
        input_label.pack(side=tk.LEFT, padx=(0, 10))

        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(
            input_frame, 
            textvariable=self.username_var,
            width=30,  # 稍微减小宽度
            font=("Microsoft YaHei UI", 11)
        )
        self.username_entry.pack(side=tk.LEFT, padx=(0, 10))

        search_button = ttk.Button(
            input_frame,
            text="查询",
            command=self.search_skin,
            style="TButton"
        )
        search_button.pack(side=tk.LEFT)

        # 内容区域
        content_frame = ttk.Frame(main_frame, style="TFrame")
        content_frame.pack(fill=tk.BOTH, expand=True)

        # 皮肤URL显示
        self.url_var = tk.StringVar()
        self.url_label = ttk.Label(
            content_frame,
            textvariable=self.url_var,
            wraplength=700,
            style="URL.TLabel"
        )
        self.url_label.pack(pady=(0, 20))

        # 图片预览区域
        preview_frame = ttk.Frame(content_frame, style="TFrame")
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.image_label = ttk.Label(preview_frame)
        self.image_label.pack(expand=True)

        # 按钮区域
        button_frame = ttk.Frame(main_frame, style="TFrame")
        button_frame.pack(fill=tk.X, pady=(20, 10))  # 调整下边距

        # 3D预览按钮
        self.preview_button = ttk.Button(
            button_frame,
            text="3D 预览",
            command=self.show_3d_preview,
            state=tk.DISABLED
        )
        self.preview_button.pack(side=tk.LEFT, padx=(0, 10))

        # 下载按钮
        self.download_button = ttk.Button(
            button_frame,
            text="下载皮肤",
            command=self.download_skin,
            state=tk.DISABLED
        )
        self.download_button.pack(side=tk.LEFT)

        # 添加版权信息
        copyright_label = ttk.Label(
            main_frame,
            text="由红石或命令开发",
            font=("Microsoft YaHei UI", 9),
            foreground="#888888",
            background="#f5f5f5"
        )
        copyright_label.pack(pady=(10, 0))  # 在底部添加一些间距

    def search_skin(self):
        username = self.username_var.get().strip()
        if not username:
            messagebox.showwarning("警告", "请输入玩家名！")
            return

        skin_url = self.skin_finder.get_skin_url(username)
        if skin_url:
            self.current_skin_url = skin_url
            self.url_var.set(f"皮肤URL: {skin_url}")
            self.display_skin_preview(skin_url)
            self.download_button.configure(state=tk.NORMAL)
            self.preview_button.configure(state=tk.NORMAL)  # 启用3D预览按钮
        else:
            self.url_var.set("未找到该玩家的皮肤信息")
            self.clear_image()
            self.current_skin_url = None
            self.download_button.configure(state=tk.DISABLED)
            self.preview_button.configure(state=tk.DISABLED)  # 禁用3D预览按钮

    def display_skin_preview(self, url):
        try:
            response = requests.get(url)
            image = Image.open(BytesIO(response.content))
            
            # 调整图片大小
            image = image.resize((300, 300), Image.Resampling.LANCZOS)  # 更大的预览图
            
            # 转换为PhotoImage
            photo = ImageTk.PhotoImage(image)
            
            self.image_label.configure(image=photo)
            self.image_label.image = photo
        except Exception as e:
            messagebox.showerror("错误", f"加载皮肤预览失败: {str(e)}")

    def download_skin(self):
        if not self.current_skin_url:
            return
            
        try:
            # 创建文件选择对话框
            username = self.username_var.get().strip()
            default_filename = f"{username}_skin.png"
            
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                initialfile=default_filename
            )
            
            if file_path:  # 如果用户选择了保存位置
                response = requests.get(self.current_skin_url)
                response.raise_for_status()  # 检查请求是否成功
                
                # 保存文件
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                
                messagebox.showinfo("成功", f"皮肤已保存到:\n{file_path}")
        except Exception as e:
            messagebox.showerror("错误", f"下载皮肤时出错:\n{str(e)}")

    def show_3d_preview(self):
        if not self.current_skin_url:
            return
            
        # 生成HTML内容
        html_content = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Minecraft 皮肤预览</title>
            <style>
                body {{ margin: 0; }}
                canvas {{ width: 100%; height: 100% }}
                #container {{ width: 100%; height: 100vh; }}
            </style>
        </head>
        <body>
            <div id="container"></div>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/skinview3d@3.0.0-alpha.1/bundles/skinview3d.bundle.js"></script>
            <script>
                const skinViewer = new skinview3d.SkinViewer({{
                    canvas: document.createElement("canvas"),
                    width: 300,
                    height: 400
                }});
                document.getElementById("container").appendChild(skinViewer.canvas);
                skinViewer.loadSkin("{self.current_skin_url}");
                skinViewer.animations.add(skinview3d.WalkingAnimation);
                skinViewer.autoRotate = true;
            </script>
        </body>
        </html>
        '''
        
        # 创建临时HTML文件
        temp_path = 'temp_preview.html'
        with open(temp_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # 在默认浏览器中打开
        webbrowser.open(temp_path)

    def clear_image(self):
        self.image_label.configure(image="")
        self.image_label.image = None
        self.current_skin_url = None
        self.download_button.configure(state=tk.DISABLED)
        self.preview_button.configure(state=tk.DISABLED)

class MinecraftSkin:
    def __init__(self):
        self.api_uuid = "https://api.mojang.com/users/profiles/minecraft/{username}"
        self.api_profile = "https://sessionserver.mojang.com/session/minecraft/profile/{uuid}"

    def get_player_uuid(self, username: str) -> Optional[str]:
        """
        获取玩家的UUID
        
        Args:
            username: Minecraft 玩家名
            
        Returns:
            成功返回UUID字符串，失败返回None
        """
        try:
            response = requests.get(self.api_uuid.format(username=username))
            if response.status_code == 200:
                return response.json()['id']
            return None
        except Exception as e:
            print(f"获取UUID时出错: {e}")
            return None

    def get_skin_data(self, uuid: str) -> Optional[Dict[str, Any]]:
        """
        获取玩家的皮肤数据
        
        Args:
            uuid: 玩家的UUID
            
        Returns:
            包含皮肤信息的字典，失败返回None
        """
        try:
            response = requests.get(self.api_profile.format(uuid=uuid))
            if response.status_code == 200:
                data = response.json()
                if not data.get('properties'):
                    print(f"API返回数据缺少properties字段: {data}")
                    return None
                    
                properties = data['properties'][0]
                try:
                    decoded_value = base64.b64decode(properties['value'])
                    return json.loads(decoded_value)
                except Exception as e:
                    print(f"解码皮肤数据失败: {e}")
                    print(f"原始数据: {properties['value']}")
                    return None
            else:
                print(f"API请求失败，状态码: {response.status_code}")
                print(f"响应内容: {response.text}")
                return None
        except Exception as e:
            print(f"获取皮肤数据时出错: {e}")
            return None

    def get_skin_url(self, username: str) -> Optional[str]:
        """
        获取玩家的皮肤URL
        
        Args:
            username: Minecraft 玩家名
            
        Returns:
            皮肤的URL，失败返回None
        """
        uuid = self.get_player_uuid(username)
        if not uuid:
            print(f"无法获取玩家 {username} 的UUID")
            return None
            
        print(f"获取到UUID: {uuid}")  # 调试信息
        
        skin_data = self.get_skin_data(uuid)
        if not skin_data:
            return None
            
        textures = skin_data.get('textures', {})
        if 'SKIN' in textures:
            return textures['SKIN']['url']
        else:
            print(f"皮肤数据中没有SKIN字段: {skin_data}")
            return None

def main():
    root = tk.Tk()
    app = MinecraftSkinGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
