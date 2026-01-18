#!/usr/bin/env python3
"""
GitHub用户配置切换器
用法: python git_switch.py [用户名]
"""

import os
import sys
import json
from pathlib import Path

class GitUserSwitcher:
    def __init__(self):
        self.config_file = Path.home() / '.git_users.json'
        self.default_config = {
            "users": {
                "Oxygen": {
                    "name": "Oxyconsumo",
                    "email": "Oxyconsumo@colchicum.moe"
                }
            },
            "current": "mstouk57g"
        }
        self.load_config()

    def load_config(self):
        """加载配置文件"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            except:
                self.config = self.default_config
        else:
            self.config = self.default_config
            self.save_config()

    def save_config(self):
        """保存配置文件"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)

    def add_user(self, alias, name, email):
        """添加新用户"""
        self.config["users"][alias] = {"name": name, "email": email}
        self.save_config()
        print(f"✅ 已添加用户 '{alias}'")

    def list_users(self):
        """列出所有用户"""
        print("\n📋 已保存的用户配置:")
        print("-" * 40)
        for alias, info in self.config["users"].items():
            status = " (当前)" if alias == self.config.get("current") else ""
            print(f"  {alias}{status}:")
            print(f"    姓名: {info['name']}")
            print(f"    邮箱: {info['email']}")
        print("-" * 40)

    def switch_user(self, alias, scope="global"):
        """切换到指定用户"""
        if alias not in self.config["users"]:
            print(f"❌ 用户 '{alias}' 不存在")
            self.list_users()
            return False

        user = self.config["users"][alias]

        # 设置Git配置
        if scope == "global":
            os.system(f'git config --global user.name "{user["name"]}"')
            os.system(f'git config --global user.email "{user["email"]}"')
            print(f"🌍 已全局切换到用户 '{alias}'")
        elif scope == "local":
            # 获取当前目录是否为Git仓库
            if not os.path.exists('.git'):
                print("❌ 当前目录不是Git仓库")
                return False
            os.system(f'git config user.name "{user["name"]}"')
            os.system(f'git config user.email "{user["email"]}"')
            print(f"📁 已本地切换到用户 '{alias}'")

        # 更新当前用户
        self.config["current"] = alias
        self.save_config()

        # 显示当前配置
        self.show_current()
        return True

    def show_current(self):
        """显示当前用户配置"""
        print("\n🔍 当前Git配置:")
        print("-" * 40)
        os.system('git config --global user.name')
        os.system('git config --global user.email')
        print("-" * 40)

    def get_current_user(self):
        """获取当前用户"""
        return self.config.get("current", "personal")

    def remove_user(self, alias):
        """删除用户"""
        if alias in self.config["users"]:
            del self.config["users"][alias]
            if self.config.get("current") == alias:
                self.config["current"] = list(self.config["users"].keys())[0] if self.config["users"] else None
            self.save_config()
            print(f"✅ 已删除用户 '{alias}'")
        else:
            print(f"❌ 用户 '{alias}' 不存在")

def main():
    switcher = GitUserSwitcher()

    if len(sys.argv) == 1:
        # 无参数时显示帮助
        print("""
GitHub用户切换工具 v1.0
========================

用法:
  python git_switch.py [命令] [参数]

命令:
  list                    列出所有用户
  switch <别名>           切换到指定用户（全局）
  local <别名>            切换到指定用户（仅当前仓库）
  add <别名> <姓名> <邮箱> 添加新用户配置
  remove <别名>           删除用户配置
  current                 显示当前用户
  show                    显示当前Git配置
  help                    显示此帮助信息

示例:
  python git_switch.py list
  python git_switch.py switch personal
  python git_switch.py add work "张三" "zhangsan@company.com"
        """)
        switcher.list_users()
        return

    command = sys.argv[1]

    if command == "list":
        switcher.list_users()

    elif command == "switch" and len(sys.argv) >= 3:
        switcher.switch_user(sys.argv[2], "global")

    elif command == "local" and len(sys.argv) >= 3:
        switcher.switch_user(sys.argv[2], "local")

    elif command == "add" and len(sys.argv) >= 5:
        alias = sys.argv[2]
        name = sys.argv[3]
        email = sys.argv[4]
        switcher.add_user(alias, name, email)

    elif command == "remove" and len(sys.argv) >= 3:
        switcher.remove_user(sys.argv[2])

    elif command == "current":
        current = switcher.get_current_user()
        print(f"当前用户: {current}")

    elif command == "show":
        switcher.show_current()

    elif command == "help":
        main()

    else:
        print("❌ 无效命令或参数不足")
        print("使用 'python git_switch.py help' 查看帮助")

if __name__ == "__main__":
    main()