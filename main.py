import time

from mutagen.easyid3 import EasyID3
from mutagen import File
from os import listdir


path = input(r"Insert path to directory of ONLY music files (e.g. C:\Path\To\Your\Dir): ")
path = rf"\\?\{path}"
files = listdir(path)

tracklist = []
for file in files:
    f = File(path + "\\" + file, easy=True)
    if f:
        tn = f.get("tracknumber", ["0"])[0]
        num = int(tn.split("/")[0]) if tn.split("/")[0].isdigit() else 0
        title = f.get("title", [""])[0]
        tracklist.append([num, file, title])

tracklist.sort(key=lambda x: x[0])
album_count = len(tracklist)

counter = 0

for track in tracklist:
    print(str(track[0]) + " - " + str(track[1]) + " (" + str(track[2]) + ")")
    counter+=1
    track.append(counter)

input("Press enter to start applying changes (and turn directory into album)")
for track in tracklist:
    audio = EasyID3(path + "\\" + track[1])
    audio["tracknumber"] = f"{track[3]}/{album_count}"
    audio.save()

value = input("Insert album name (insert nothing to skip): ")
if value != '' and value is not None:
    for track in tracklist:
        audio = EasyID3(path + "\\" + track[1])
        audio["album"] = value
        audio.save()

value = input("Insert album artist (insert nothing to skip): ")
if value != '' and value is not None:
    for track in tracklist:
        audio = EasyID3(path + "\\" + track[1])
        audio["artist"] = value
        audio.save()

value = input("Insert album date (insert nothing to skip): ")
if value != '' and value is not None:
    for track in tracklist:
        audio = EasyID3(path + "\\" + track[1])
        audio["date"] = value
        audio.save()

value = input("Insert album genre (insert nothing to skip): ")
if value != '' and value is not None:
    for track in tracklist:
        audio = EasyID3(path + "\\" + track[1])
        audio["genre"] = value
        audio.save()

while True:
    print("---")
    for track in tracklist:
        print(str(track[3]) + " - " + str(track[1]) + " (" + str(track[2]) + ")")

    while True:
        select = int(input("Insert track number to edit the file: "))
        print("---\n" + str(tracklist[select - 1][1]) + " selected:")
        print("1 - Change title")
        print("2 - Swap track number (recommended)")
        print("3 - Change track number")
        print("4 - Change track artist")
        print("5 - Return")
        value = int(input("Insert option: "))

        if value == 1:
            value = input("Insert track name (insert nothing to skip): ")
            if value != '' and value is not None:
                audio = EasyID3(path + "\\" + tracklist[select - 1][1])
                audio["title"] = value
                audio.save()
                tracklist[select - 1][2] = value
            break

        if value == 2:
            value = int(input("Insert track number (insert nothing to skip): "))
            if value != '' and value is not None:
                audio = EasyID3(path + "\\" + tracklist[value - 1][1])
                audio["tracknumber"] = f"{select}/{album_count}"
                tracklist[value - 1][0] = select
                tracklist[value - 1][3] = select
                audio.save()
                audio = EasyID3(path + "\\" + tracklist[select - 1][1])
                audio["tracknumber"] = f"{value}/{album_count}"
                tracklist[select - 1][0] = value
                tracklist[select - 1][3] = value
                audio.save()
            tracklist.sort(key=lambda x: x[0])
            break

        if value == 3:
            value = int(input("Insert track number (insert nothing to skip): "))
            if value != '' and value is not None:
                audio = EasyID3(path + "\\" + tracklist[select - 1][1])
                audio["tracknumber"] = f"{value}/{album_count}"
                audio.save()
                tracklist[select - 1][0] = value
                tracklist[select - 1][3] = value
            break

        if value == 4:
            value = input("Insert track artist (insert nothing to skip): ")
            if value != '' and value is not None:
                audio = EasyID3(path + "\\" + tracklist[select - 1][1])
                audio["artist"] = value
                audio.save()
            break

        if value == 5:
            break



