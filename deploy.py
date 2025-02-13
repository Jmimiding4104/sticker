import subprocess

def run_command(command):
    """執行 shell 指令，並捕獲輸出"""
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    
    if result.returncode != 0:
        print(f"❌ 指令失敗：{command}")
        print(f"🔴 錯誤輸出：{result.stderr.strip()}")
    else:
        print(f"✅ 指令成功：{command}")
        print(f"🟢 輸出：{result.stdout.strip()}")

def main():
    """執行部署流程"""
    print("🚀 開始部署...")
    
    run_command("cd dist")
    
    run_command("git init")
    
    run_command("git add -A")
    
    run_command("git commit -m 'deploy'")
    
    run_command("git push -f https://github.com/Jmimiding4104/sticker.git master:master-program")
    
    print("🎉 部署完成！")

if __name__ == "__main__":
    main()
