from pynput import keyboard
import time
import json

# If multiple keys are held and released or held and pass a timeout, will write the letter for that combination

kb = keyboard.Controller()

with open("key_map.json", encoding="utf8") as f:
    key_map = json.load(f)

other_keys = {
                "bks": keyboard.Key.backspace,
                "ent": keyboard.Key.enter,
                "del": keyboard.Key.delete,
                "tab": keyboard.Key.tab,
                "spc": keyboard.Key.space,
                "lft": keyboard.Key.left,
                "rgt": keyboard.Key.right,
                "up": keyboard.Key.up,
                "dwn": keyboard.Key.down,
                "ctl": keyboard.Key.ctrl,
                "alt": keyboard.Key.alt,
                "sft": keyboard.Key.shift,
                "spr": keyboard.Key.cmd
}


combin_keys = []

for k in key_map:
    for c in k:
        if c not in combin_keys:
            combin_keys.append(c)


combin = []
t0 = None
timeout = 1

actions = []

def key_name(key):
    return str(key).strip("'")

def reset():
    global combin, t0
    combin = []
    t0 = None

last = None
def on_press(key):
    global t0, combin, combin_keys, last, actions

    if key != last:
        print(f"sys press {key}")

    last = key

    if key_name(key) in combin_keys:
        if key not in combin:
            combin.append(key)
            t0 = time.time()
            return
        else:
            return
    else:
        actions.append((key, "press"))
        return

def on_release(key):
    global actions, a_combin, ignore

    print("sys release", key)

    if key in ignore:
        ignore.remove(key)
        return

    if len(combin) == 1:
        actions.append((combin[0], "tap"))
    elif len(combin) > 1:
        actions.append((combin, "combin"))
        ignore = combin[:]
        ignore.remove(key)
    else:
        actions += (key, "release")

def press_key(key, press_type="press"):
    global listener, kb

    assert press_type in ("type", "press", "release", "tap", "combin")

    listener.stop()

    print(key, press_type)

    if press_type == "type":
        assert type(key) == str
        kb.type(key)
    elif press_type == "press":
        assert type(key) in (keyboard.Key,keyboard.KeyCode)
        kb.press(key)
    elif press_type == "release":
        assert type(key) in (keyboard.Key, keyboard.KeyCode)
        kb.release(key)
    elif press_type == "tap":
        assert type(key) in (keyboard.Key, keyboard.KeyCode)
        kb.tap(key)
    elif press_type == "combin":
        assert type(key) == list and len(key) > 1

        parsed = "".join(sorted([key_name(k) for k in key]))
        try:
            mapped_combin = key_map[parsed]
            if mapped_combin in other_keys:
                if mapped_combin in other_keys:
                    kb.tap(other_keys[mapped_combin])
            else:
                for c in mapped_combin:
                    kb.tap(c)
            print("Mapped", mapped_combin)
        except:
            for c in parsed:
                kb.tap(c)

    # Restart listener
    listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release,
        suppress=True)

    listener.start()

    reset()


listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release,
    suppress=True)
listener.start()


while True:
    while actions:
        press_key(*actions.pop(0))

    if t0 and time.time() > t0 + timeout:
        assert len(combin) > 0

        if len(combin) > 1:
            press_key(*(combin, "combin"))
        else:
            press_key(*(combin[0], "press"))

    time.sleep(0.001)