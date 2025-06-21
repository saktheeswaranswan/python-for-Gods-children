import threading
import subprocess
import os

# Paths to your scripts (adjust if needed)
SCRIPT_DIR = r"C:\Users\RITS\Desktop\flowchart-ai-9\new-softwaregods-children-version-2"
FIRST_SCRIPT = os.path.join(SCRIPT_DIR, "python-for-special.py")
SECOND_SCRIPT = os.path.join(SCRIPT_DIR, "pyautoguitytextin.py")

# Event to signal when first script has started its input prompt
first_ready = threading.Event()


def run_first():
    """
    Run the first script and signal when it prompts for input.
    """
    # Start the first script as a subprocess
    proc = subprocess.Popen(
        ["python", FIRST_SCRIPT],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    # Read its stdout line by line, forward to console,
    # detect when it asks for input (e.g. contains 'Enter' or other prompt).
    for line in proc.stdout:
        print(line, end="")
        if "Enter" in line or "input" in line.lower():
            # Signal that first script is ready for input
            first_ready.set()
            # Send actual user input to first script
            user_input = input()
            proc.stdin.write(user_input + "\n")
            proc.stdin.flush()

    proc.wait()


def run_second():
    """
    Wait for first_ready, then run the second script.
    """
    first_ready.wait()
    proc = subprocess.Popen(
        ["python", SECOND_SCRIPT],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    # Forward output and detect its input prompt
    for line in proc.stdout:
        print(line, end="")
        if "Enter" in line or "input" in line.lower():
            user_input = input()
            proc.stdin.write(user_input + "\n")
            proc.stdin.flush()

    proc.wait()


def main():
    t1 = threading.Thread(target=run_first, daemon=True)
    t2 = threading.Thread(target=run_second, daemon=True)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("\n✅ Both scripts completed.")


if __name__ == "__main__":
    main()
