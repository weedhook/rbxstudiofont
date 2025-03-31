import os
import shutil
import subprocess
import sys
import time

def list(path): return [f for f in os.listdir(path) if f.endswith('.ttf')]

def replace(path, num, new_font):
    fonts = list(path)
    if not (1 <= num <= len(fonts)): return print("invalid index")
    original = fonts[num - 1]
    new = os.path.join(os.path.dirname(__file__), 'fonts', f'{new_font}.ttf')
    if not os.path.exists(new): return print(f"font '{new_font}.ttf' wasn't found.")
    os.remove(os.path.join(path, original))
    shutil.copy(new, os.path.join(path, original))
    print(f"replaced '{original}' w/ '{new_font}.ttf'.")
    restart()

def findroblox():
    versions = r"C:\Program Files (x86)\Roblox\Versions"
    for folder in os.listdir(versions):
        path = os.path.join(versions, folder)
        if os.path.isdir(path) and os.path.exists(os.path.join(path, "RobloxStudioBeta.exe")) and os.path.exists(os.path.join(path, "content", "fonts")):
            return path
    return None

def restart():
    print("restarting/loading robloxstudio")
    time.sleep(2)
    subprocess.run(["taskkill", "/F", "/IM", "RobloxStudioBeta.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)
    subprocess.Popen([os.path.join(rblx_path, 'RobloxStudioBeta.exe')], shell=True)

if __name__ == "__main__":
    rblx_path = findroblox()
    if not rblx_path: sys.exit("failed to fetch roblox studio.")

    fonts_path = os.path.join(rblx_path, 'content', 'fonts')
    rblx_fonts = list(fonts_path)
    print(f"loaded {len(rblx_fonts)} fonts from 'content/fonts'.\n")
    for idx, font in enumerate(rblx_fonts, 1): print(f"[{idx}] {font}")

    while True:
        cmd = input().strip()
        if cmd.lower() == "exit": break
        if cmd.lower().startswith("replace "):
            parts = cmd.split(' ', 2)
            if len(parts) == 3: replace(fonts_path, int(parts[1]), parts[2].strip('"'))
            else: print("replace <index> \"font_name\"")
