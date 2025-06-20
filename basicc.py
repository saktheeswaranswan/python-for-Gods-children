import pyautogui
import time
import cv2
import os

# List of required Flowgorithm icons
images = [
    "arrow.png", "assign.png", "output.png", "input.png",
    "for-loop.png", "while-loop.png", "doloop.png",
    "call.png", "comment.png", "control-if.png", "declare.png",
    "file-close.png", "file-open.png", "file-read.png", "file-write.png",
    "break-point.png"
]

pyautogui.FAILSAFE = True
confidence = 0.9

def check_images_exist():
    missing = []
    for img in images:
        if not os.path.exists(img):
            missing.append(img)
    return missing

def locate_and_click(image_name, right_click=False, move_offset=(0, 0)):
    try:
        location = pyautogui.locateCenterOnScreen(image_name, confidence=confidence)
        if location:
            x, y = location
            pyautogui.moveTo(x + move_offset[0], y + move_offset[1], duration=0.2)
            if right_click:
                pyautogui.rightClick()
            else:
                pyautogui.click()
            time.sleep(1)
            return True
        else:
            print(f"❌ Image not found: {image_name}")
            return False
    except Exception as e:
        print(f"⚠️ Error with {image_name}: {e}")
        return False

def create_variable():
    if locate_and_click("arrow.png", right_click=True):
        pyautogui.move(0, 60)  # Move down to "Create Variable"
        pyautogui.click()
        time.sleep(1)

def insert_assign_block():
    if locate_and_click("assign.png"):
        pyautogui.click()
        time.sleep(1)
        pyautogui.typewrite("num1 = 10\nnum2 = 5\n", interval=0.05)
        pyautogui.typewrite("sum = num1 + num2\n", interval=0.05)
        pyautogui.typewrite("diff = num1 - num2\n", interval=0.05)
        pyautogui.typewrite("prod = num1 * num2\n", interval=0.05)
        pyautogui.typewrite("quot = num1 / num2\n", interval=0.05)
        pyautogui.typewrite("mod = num1 % num2\n", interval=0.05)

def insert_output_block():
    if locate_and_click("output.png"):
        pyautogui.click()
        time.sleep(1)
        pyautogui.typewrite('print("Sum =", sum)\n', interval=0.05)
        pyautogui.typewrite('print("Diff =", diff)\n', interval=0.05)
        pyautogui.typewrite('print("Prod =", prod)\n', interval=0.05)
        pyautogui.typewrite('print("Quot =", quot)\n', interval=0.05)
        pyautogui.typewrite('print("Mod =", mod)\n', interval=0.05)

def run_program():
    print("⏳ Starting automation... Please focus Flowgorithm window.")
    time.sleep(5)

    create_variable()
    insert_assign_block()
    insert_output_block()

    print("✅ Done. Arithmetic logic inserted!")

def show_menu():
    print("\n📋 Flowgorithm Automation Options")
    print("1. Insert First Arithmetic Program (num1, num2, + - * / %)")
    print("2. Show Missing Images")
    print("3. Exit")

while True:
    show_menu()
    choice = input("👉 Select an option [1-3]: ")

    if choice == "1":
        run_program()
    elif choice == "2":
        missing = check_images_exist()
        if missing:
            print("❌ Missing image files:")
            for img in missing:
                print(f"   - {img}")
        else:
            print("✅ All required image files are present.")
    elif choice == "3":
        print("👋 Exiting.")
        break
    else:
        print("⚠️ Invalid choice. Try again.")
