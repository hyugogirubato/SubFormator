from datetime import datetime
import io
import argparse
import sys
import os


def main():
    global src_ref, src_inp, is_default, author, title, play_res_X, play_res_Y, is_ignore

    src_ref = ""
    src_inp = ""
    is_default = False
    is_ignore = False
    author = ""
    title = ""
    play_res_X = "640"
    play_res_Y = "360"

    parser = argparse.ArgumentParser()
    parser.add_argument('--reference')
    parser.add_argument('--input')
    parser.add_argument('--ignore', action="store_true")
    parser.add_argument('--default', action="store_true")
    parser.add_argument('--title')
    parser.add_argument('--author')
    parser.add_argument('--play_res')
    args = parser.parse_args()

    if args.reference and args.input:
        src_ref = args.reference
        src_inp = args.input
        is_default = args.default
        is_ignore = args.ignore

        if is_default:
            if args.title:
                title = args.title
            if args.author:
                author = args.author
            if args.play_res:
                try:
                    play_res = args.play_res
                    play_res_X = play_res.split("x")[1].strip()
                    play_res_Y = play_res.split("x")[0].strip()
                except:
                    print("ERROR: Video format invalid.")
                    sys.exit(0)

        create_subtitles()
    else:
        print("ERROR: Reference file and an input file is required.")
        sys.exit(0)


def create_subtitles():
    check_file()
    file = io.open("{} [Edit].ass".format(os.path.basename(src_ref)), mode="w", encoding="utf-8")
    create_header(file)

    ref_dialogue = get_dialogue(get_lines(src_ref))
    inp_dialogue = get_dialogue(get_lines(src_inp))

    time_delta = get_delta_time(ref_dialogue, inp_dialogue)

    for dialogue in inp_dialogue:
        items = dialogue.split(",")

        if subtract:
            time_start = datetime.strptime(items[1], "%H:%M:%S.%f") - time_delta
        else:
            time_start = datetime.strptime(items[1], "%H:%M:%S.%f") + time_delta

        time_end = datetime.strptime(items[2], "%H:%M:%S.%f") - datetime.strptime(items[1], "%H:%M:%S.%f") + time_start

        items[1] = get_time(str(time_start))
        items[2] = get_time(str(time_end))

        if is_default:
            items[3] = "Default"
            items[4] = ""
            items[5] = "0000"
            items[6] = "0000"
            items[7] = "0000"
            # line = get_line(items)
            line = ",".join(items)
        else:
            line = ",".join(items)

        file.write(line)
    file.close()
    print("[debug] The subtitles have been edited")
    sys.exit(0)


def get_line(items):
    line = ",".join(items[9:len(items)])

    if "{\i1}" in line:
        items[3] = "Italics"
        dialog = line.split("{\i1}")[1].split("{\i0}")[0].strip()
    elif "{\\b1}" in line:
        items[3] = "B1"
        dialog = line.split("{\\b1}")[1].split("{\\b1}")[0].strip()
    else:
        dialog = line.strip()

    return ",".join(items[0:9]) + dialog + "\n"


def get_time(time):
    if " " in time:
        time = time.split(" ")[1]

    if time.startswith("00:"):
        time = time[1:11]
    else:
        time = time[0:10]

    if "." in time:
        return time
    else:
        return time + ".00"


def get_delta_time(ref, inp):
    global subtract
    items = ref[0].split(",")
    time_ref = items[1]

    items = inp[0].split(",")
    time_inp = items[1]

    if datetime.strptime(time_ref, "%H:%M:%S.%f") > datetime.strptime(time_inp, "%H:%M:%S.%f"):
        subtract = False
        time = datetime.strptime(time_ref, "%H:%M:%S.%f") - datetime.strptime(time_inp, "%H:%M:%S.%f")
    else:
        subtract = True
        time = datetime.strptime(time_inp, "%H:%M:%S.%f") - datetime.strptime(time_ref, "%H:%M:%S.%f")

    if is_ignore:
        time = datetime.strptime("00:00:00.00", "%H:%M:%S.%f")
        print("[debug] Delta time ignored")
    else:
        print("[debug] Delta time: {}".format(time))

    return time


def check_file():
    if not os.path.isfile("{}.ass".format(src_ref)):
        print("ERROR: Reference file does not exist.")
        sys.exit(0)
    elif not os.path.isfile("{}.ass".format(src_inp)):
        print("ERROR: Input file does not exist.")
        sys.exit(0)


def get_lines(src):
    file = io.open("{}.ass".format(src), mode="r", encoding="utf-8")
    lines = file.readlines()
    file.close()
    return lines


def get_dialogue(lines):
    dialogue = list()
    for line in lines:
        if "Dialogue:" in line:
            dialogue.append(line)
    return dialogue


def create_header(file):
    if is_default:
        file.write("[Script Info]\n")
        file.write("Title: {}\n".format(title))
        file.write("Original Script: {}\n".format(author))
        file.write("Original Translation:\n")
        file.write("Original Editing:\n")
        file.write("Original Timing:\n")
        file.write("Synch Point:\n")
        file.write("Script Updated By:\n")
        file.write("Update Details:\n")
        file.write("ScriptType: v4.00+\n")
        file.write("Collisions: Normal\n")
        file.write("PlayResX: {}\n".format(play_res_X))
        file.write("PlayResY: {}\n".format(play_res_Y))
        file.write("Timer: 0.0000\n")
        file.write("WrapStyle: 0\n")
        file.write("\n")
        file.write("[V4+ Styles]\n")
        file.write(
            "Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,Strikeout,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding\n")
        file.write(
            "Style: Default,Arial,20,&H00FFFFFF,&H0000FFFF,&H00000000,&H7F404040,-1,0,0,0,100,100,0,0,1,2,1,2,0020,0020,0022,0\n")
        file.write(
            "Style: B1,Arial,32,&H00FFFFFF,&H0000FFFF,&H00000000,&H7F404040,-1,0,0,0,100,100,0,0,1,2,1,2,0070,0070,0030,0\n")
        file.write(
            "Style: OS,Arial,18,&H00FFFFFF,&H0000FFFF,&H00000000,&H7F404040,-1,0,0,0,100,100,0,0,1,2,1,8,0001,0001,0015,0\n")
        file.write(
            "Style: Italics,Arial,20,&H00FFFFFF,&H0000FFFF,&H00000000,&H7F404040,-1,-1,0,0,100,100,0,0,1,2,1,2,0020,0020,0022,0\n")
        file.write(
            "Style: Ep Title,Arial,18,&H00FFFFFF,&H0000FFFF,&H00000000,&H7F404040,-1,0,0,0,100,100,0,0,1,2,1,3,0170,0070,0020,0\n")
        file.write(
            "Style: Copy of Ep Title,Arial,18,&H00FFFFFF,&H0000FFFF,&H00000000,&H7F404040,-1,0,0,0,100,100,0,0,1,2,1,3,0070,0226,0065,0\n")
        file.write(
            "Style: On Top,Arial,20,&H00FFFFFF,&H0000FFFF,&H00000000,&H7F404040,-1,0,0,0,100,100,0,0,1,2,1,8,0020,0020,0022,0\n")
        file.write(
            "Style: Copy of OS,Arial,18,&H00FFFFFF,&H0000FFFF,&H00000000,&H7F404040,-1,0,0,0,100,100,0,0,1,2,1,9,0020,0020,0020,0\n")
        file.write(
            "Style: DefaultLow,Arial,20,&H00FFFFFF,&H0000FFFF,&H00000000,&H7F404040,-1,0,0,0,100,100,0,0,1,2,1,2,0020,0020,0010,0\n")
        file.write("\n")
        file.write("[Events]\n")
        file.write("Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text\n")
    else:
        lines = get_lines(src_inp)
        for line in lines:
            if not "Dialogue:" in line:
                file.write(line)


if __name__ == '__main__':
    main()
