# SubFormator

## Description
You downloaded a video with subtitles that don’t match the ones you want to use, so you downloaded subtitles in the language you want to use, except that, unfortunately, they don’t connect with the speech. Well this script offers you a solution. Using the reference subtitle file designed for the video, you will now be able to adapt your external subtitle files. The program adjusts the speaking time to the source file. You can also use the default style or apply only the default style without changing the speaking time.
 
## Features
- Allows the adaptation of a subtitle file to the reference format
- Use a default style for an ASS subtitle file

## Requirements
- [Python](https://www.python.org/downloads/) 3+

## Information
 - Ne prend en charge que les fichier de sous titre de format ASS (SubStation Alpha)
 - Do not add extension when declaring files (do not put .ass)
 - Based on the time of the first dialogue of the reference file
 - If the time does not match, try to disable time scaling with the "--ignore"

## Commands
| Command | Description | Format |
| ------ | ------ | ------ |
| --reference | Define the reference sub-title file | Without extension |
| --input | Define the subtitle file to be modified | Without extension |
| --default | Use the default style | No argument |
| --ignore | Ignore Time Scale | No argument |
| --title | Define the title | Text |
| --author | Define the author | Text |
| --play_res | Set the image size | Width**x**Hight |

## Examples

Creation of subtitles using the style of the input file
```
SubFormator.py --reference "REFERENCE_SUBTITLES" --input "INPUT_SUBTITLES"
```

Creating subtitles using the default style
```
SubFormator.py --reference "REFERENCE_SUBTITLES" --input "INPUT_SUBTITLES" --default
```

-----------------
*This script was created by the [__Nashi Team__](https://sites.google.com/view/kamyroll/home).  
Find us on [discord](https://discord.com/invite/g6JzYbh) for more information on projects in development.*
