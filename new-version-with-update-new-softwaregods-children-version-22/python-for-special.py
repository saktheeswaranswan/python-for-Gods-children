import pyautogui
import cv2
import numpy as np
import time
import os

# Map numbers to your Flowgorithm icon filenames
IMAGES = {
    1: "assign.png",
    2: "output.png",
    3: "input.png",
    4: "for-loop.png",
    5: "while-loop.png",
    6: "doloop.png",
    7: "call.png",
    8: "comment.png",
    9: "control-if.png",
    10: "declare.png",
    11: "file-close.png",
    12: "file-open.png",
    13: "file-read.png",
    14: "file-write.png",
    15: "break-point.png",
    16: "arrow.png"
}

def clamp(v, lo, hi):
    return max(lo, min(v, hi))

def load_gray_template(path):
    tpl = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if tpl is None:
        raise FileNotFoundError(f"Template not found: {path}")
    return tpl

def grab_gray_region(region):
    """Screenshot region, return grayscale numpy array."""
    img = pyautogui.screenshot(region=region)
    arr = np.array(img)
    # Convert from RGB to grayscale
    return cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)

def find_template(template, region, threshold):
    """
    Grayscale template-match in region.
    Returns center (x,y) if match ≥ threshold.
    """
    hay = grab_gray_region(region)
    res = cv2.matchTemplate(hay, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    if max_val >= threshold:
        ty, tx = max_loc
        h, w = template.shape
        return (region[0] + tx + w//2, region[1] + ty + h//2)
    return None

def wait_and_click(template, threshold=0.9, region_size=200):
    sw, sh = pyautogui.size()
    print("🖱  Hover over the icon now…")
    start = time.time()
    while True:
        mx, my = pyautogui.position()
        l = clamp(mx - region_size//2, 0, sw)
        t = clamp(my - region_size//2, 0, sh)
        w = clamp(region_size, 0, sw - l)
        h = clamp(region_size, 0, sh - t)
        region = (l, t, w, h)

        match = find_template(template, region, threshold)
        if match:
            pyautogui.moveTo(*match, duration=0.1)
            pyautogui.click()
            time.sleep(0.1)
            pyautogui.doubleClick()
            print(f"✅ Matched & clicked at {match} (search took {time.time()-start:.2f}s)")
            return
        # Feedback every 0.3s
        if time.time() - start > 0 and int((time.time()-start)*10) % 3 == 0:
            print(f"…searching near ({mx},{my})")
        time.sleep(0.05)

def main():
    print("🟢 Flowgorithm Macro – fast, grayscale template‑match mode.")
    print("🎯 Bring Flowgorithm to front. Type a block number when ready.\n")
    time.sleep(1)

    # Preload grayscale templates
    templates = {}
    for num, fname in IMAGES.items():
        if os.path.isfile(fname):
            templates[num] = load_gray_template(fname)
        else:
            print(f"⚠️ Missing '{fname}', skipping #{num}")

    if not templates:
        print("❌ No templates loaded. Place your PNGs in this folder first.")
        return

    while True:
        choice = input("Enter block number (1–16), or 'q' to quit: ").strip().lower()
        if choice == 'q':
            break
        if not choice.isdigit() or int(choice) not in templates:
            print("❌ Invalid. Choose from:", ", ".join(map(str, templates.keys())))
            continue

        num = int(choice)
        print(f"\n🔍 Searching for '{IMAGES[num]}' (threshold=0.9)…")
        wait_and_click(templates[num])

    print("🛑 Macro ended. Goodbye!")

if __name__ == "__main__":
    main()
