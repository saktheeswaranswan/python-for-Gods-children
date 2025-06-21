import os
import time
import cv2
import numpy as np
import pyautogui
import keyboard

# --- CONFIGURE THIS ---
BASE_FOLDER = r"C:\Users\RITS\Desktop\flowchart-ai-9\new-softwaregods-children-version-2"
# Map your Flowgorithm filenames (must match actual PNG names in BASE_FOLDER)
IMAGES = {
    1: "assign-tb.png",
    2: "assign-variable-tb-expression.png",
    3: "assign-variable-tb.png",
    4: "calltb.png",
    5: "declare-tb-option.png",
    6: "declare-tb.png",
    7: "do-looptb.png",
    8: "filereadtb.png",
    9: "forcheckbox.png",
    10: "forendvalue.png",
    11: "forstarttb.png",
    12: "forstartvalue.png",
    13: "forstepby.png",
    14: "fortb.png",
    15: "forvartb.png",
    16: "iftb.png",
    17: "input-tb.png",
    18: "ok-cancel.png",      # OK/CANCEL button
    19: "output-tb.png",
    20: "while-tb.png"
}
THRESHOLD = 0.9
REGION_SIZE = 200

def clamp(v, lo, hi):
    return max(lo, min(v, hi))

def load_gray_template(fname):
    path = os.path.join(BASE_FOLDER, fname)
    tpl = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if tpl is None:
        raise FileNotFoundError(f"Cannot load template: {path}")
    return tpl

def grab_gray_region(region):
    img = pyautogui.screenshot(region=region)
    arr = np.array(img)
    return cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)

def find_and_click(template):
    sw, sh = pyautogui.size()
    start = time.time()
    while True:
        # define search region around current mouse
        mx, my = pyautogui.position()
        left = clamp(mx - REGION_SIZE//2, 0, sw)
        top  = clamp(my - REGION_SIZE//2, 0, sh)
        w = clamp(REGION_SIZE, 0, sw - left)
        h = clamp(REGION_SIZE, 0, sh - top)
        hay = grab_gray_region((left, top, w, h))
        res = cv2.matchTemplate(hay, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if max_val >= THRESHOLD:
            ty, tx = max_loc
            th, tw = template.shape
            click_x = left + tx + tw//2
            click_y = top  + ty + th//2
            pyautogui.moveTo(click_x, click_y, duration=0.1)
            pyautogui.click()
            return True
        if time.time() - start > 10:
            print("⚠️  Timeout: template not found.")
            return False
        time.sleep(0.05)

def main():
    print("\n🟢 Flowgorithm Macro – grayscale‑only template matching")
    print(f"   Templates loaded from: {BASE_FOLDER}")
    print("   After clicking any ‘-tb’ textbox, type your text, then press ALT to confirm.\n")

    # preload all templates
    templates = {}
    for num, fname in IMAGES.items():
        try:
            templates[num] = load_gray_template(fname)
        except FileNotFoundError as e:
            print("⚠️", e)

    if 18 not in templates:
        print("❌ Missing ok-cancel.png; cannot proceed.")
        return

    while True:
        choice = input(f"Enter block number {sorted(templates)} or ‘q’ to quit: ").strip().lower()
        if choice == 'q':
            break
        if not choice.isdigit() or int(choice) not in templates:
            print("❌ Invalid choice.")
            continue

        num = int(choice)
        tpl = templates[num]
        print(f"\n🔍 Looking for '{IMAGES[num]}'…")
        found = find_and_click(tpl)
        if not found:
            continue

        # if this is a "textbox" template (ends with '-tb.png'), wait for ALT then click OK/CANCEL
        if IMAGES[num].endswith('-tb.png'):
            print("✏️  Type your text now. Then press ALT when done…")
            keyboard.wait('alt')
            print("🔍 Now looking for OK/CANCEL button…")
            find_and_click(templates[18])
            print("✅ OK/CANCEL clicked.\n")
        else:
            print("✅ Clicked.\n")

    print("🛑 Macro ended. Goodbye!")

if __name__ == "__main__":
    main()
