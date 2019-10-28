import speech_recognition as sr
import keyboard
import time
import pickle
import os

from voice_processing import VoiceProcess

r = sr.Recognizer()
commands = {} # Format: 'voice command string': [[actionType, value(key or duration)],
# [actionType, value(key or duration)], ...]


def generate_key():
    while True:
        repeat = 1
        command = ''
        # print("Input your desired phrase time limit (-1 for none)")
        # timeLimit = int(input())
        with sr.Microphone() as source:
            print("Please speak your voice command queue.")
            r.adjust_for_ambient_noise(source=source,duration=1)
            # if timeLimit > 0:
            #     audio = r.listen(source, phrase_time_limit=timeLimit)
            # else:
            audio = r.listen(source)
            try:
                text = r.recognize_google(audio)
                command = text
                print("Your voice command queue is '" + command + "'. Would you like to retry?\n [1]. Yes\n [2]. No")
                repeat = int(input())
            except:
                print("Your voice command queue was not detected, please try again.\n [1]. Yes\n [2]. No")
                repeat = int(input())

            if repeat == 2:
                break

    return command


def generate_actions():
    actionList = []
    while True:
        print(
            "What type of action would you like to add?\n [1]. Key Press\n [2]. Key Release\n "
            "[3]. Key Press and Key Release\n [4]. Delay\n")
        acttype = int(input())

        if acttype == 1 or acttype == 2 or acttype == 3:
            print("Press the hotkey you would like to press/release?")
            time.sleep(0.3)
            singleAction = [acttype, keyboard.read_hotkey(suppress=False)]

        elif acttype == 4:
            print("How long would the delay be (in milliseconds)?")
            delay = float(input())
            singleAction = [acttype, delay]

        print("Your current action is: ")
        print(singleAction)
        print("Are you sure you want to add this to the action string? [1. Yes, 2. No]")

        addAction = int(input())
        if addAction == 1:
            actionList.append(singleAction)
            print("Action has successfully been added to the list")

        print("Would you like to add another action?\n [1]. Yes\n [2]. No")
        repeat = int(input())

        if repeat == 2:
            return actionList


def create_command():
    command = generate_key()
    command = command.lower()
    actionList = generate_actions()
    commands[command] = actionList
    print("The voice command '" + command + "' now relates to:")
    print(actionList)


def execute_command(voiceString):
    try:
        commandArray = commands[voiceString]
        for i in commandArray:
            if i[0] == 1:
                keyboard.press(i[1])
            elif i[0] == 2:
                keyboard.release(i[1])
            elif i[0] == 3:
                keyboard.press_and_release(i[1])
            elif i[0] == 4:
                time.sleep(i[1])
    except KeyError:
        pass


def main():
    push_to_talk_key = settings[0]
    VoiceProcess.lexer_sensitivity = settings[1]
    print("W E L C O M E   T O   V O I C E   M A C R O   V E R S I O N   1 . 3 \n")
    while True:
        print("MAIN MENU\n [1]. Create Commands\n [2]. View Commands\n [3]. Start Voice Macro\n [4]. Settings\n "
              "[5]. EXIT")
        main_menu = int(input())
        if main_menu == 1:
            create_command()
        elif main_menu == 2:
            commands_keys = []
            counter = 1

            print("List of commands: ")
            for i in commands.keys():
                print("[" + str(counter) + "]. " + i)
                commands_keys.append(i)
                counter += 1

            print("Which command would you like to access? (-1 to return)")
            view_options = int(input())

            if view_options < 0:
                pass
            else:
                chosen_command = commands_keys[view_options-1]
                print("Command String: '" + chosen_command + "', Action String: " + str(commands.get(chosen_command)))
                print("What would you like to do with this command?\n [1]. Delete\n "
                      "[2]. Edit Key\n [3]. Edit key Values")
                view_options = int(input())

                if view_options == 1:
                    del commands[chosen_command]
                    print("Command '" + chosen_command + "' has been deleted.")

                elif view_options == 2:
                    new_command = generate_key()
                    if new_command != '':
                        commands[new_command] = commands.pop(chosen_command)
                elif view_options == 3:
                    new_command = generate_actions()
                    commands.update({str(chosen_command):new_command})

        elif main_menu == 3:
            print("Hold the '[" + push_to_talk_key + "]' to talk, and release to execute the command. Say 'Exit Macro' to end the Voice Macro")
            while True:
                command = ''
                while keyboard.is_pressed(push_to_talk_key):
                    with sr.Microphone() as source:
                        r.adjust_for_ambient_noise(source=source, duration=1)
                        audio = r.listen(source)

                        try:
                            text = r.recognize_google(audio)
                            command = text
                            command = command.lower()
                            print('You said : {}'.format(text))
                            voice_process = VoiceProcess(command, commands)
                            command = voice_process.command_validator()
                        except:
                            command = "cannot be identified"

                if command == "exit macro":
                    break

                execute_command(command)

        elif main_menu == 4:
            print("What would you like to do ?\n [1]. Push to talk button\n [2]. Lexemizer tolerance\n "
                  "[3]. Delete all macros")
            view_options=int(input())
            if view_options==1:
                print("Press the new key you want to choose")
                time.sleep(0.3)
                newkey=keyboard.read_hotkey(suppress=False)
                print("\nThe key that you pressed is ["+newkey+"] Are you sure ?\n [1] Yes \n [2] No")
                checker = int(input())
                if checker==1:
                    push_to_talk_key=newkey
                    print("Push to talk button has successfully been changed into [" + push_to_talk_key + "].")
                    settings[0]=push_to_talk_key
                    print(push_to_talk_key)
                else:
                    print("Push to talk button change aborted, the previous button [" + push_to_talk_key +
                          "] is still used.")
            elif view_options==2:
                print("TOLERANCE OPTION:\n [1]. Set Tolerance\n [2]. Reset to Default")
                input_choice = int(input())
                if input_choice == 1:
                    print("Please input the new tolerance level")
                    lexer_sensitivity = int(input())
                    settings[1] = lexer_sensitivity
                    VoiceProcess.lexer_sensitivity = settings[1]
                elif input_choice == 2:
                    settings[1] = 45
                    VoiceProcess.lexer_sensitivity = settings[1]
            elif view_options==3:
                commands.clear()
                print("All macros deleted")

        elif main_menu == 5:
            pickle_output=open("usermacro.pickle","wb")
            pickle.dump(commands,pickle_output)
            pickle_output.close()
            pickle_output = open("settings.pickle", "wb")
            pickle.dump(settings, pickle_output)
            pickle_output.close()
            break


settings=["`",""]
filename="usermacro.pickle"
if os.path.exists("usermacro.pickle"):
    pickle_input = open("usermacro.pickle", "rb")
    commands = pickle.load(pickle_input)
    pickle_input.close()
if os.path.exists("settings.pickle"):
    pickle_input = open("settings.pickle", "rb")
    settings=pickle.load(pickle_input)
    pickle_input.close()

main()