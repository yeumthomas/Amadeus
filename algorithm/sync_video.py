import ffmpeg
import os
from scipy.io.wavfile import read, write

# helpful link to figure out os paths: https://stackoverflow.com/questions/18114081/ffmpeg-cannot-detect-file-while-os-can
print(os.getcwd())
rel_root = os.getcwd() # gets current working directory (ludwig-2.0 apparently)
bg = ffmpeg.input(rel_root + '/algorithm/public/REAL-1920x1080.jpg')
main = ffmpeg.input(rel_root + '/algorithm/public/lastMoments.mov')
logo = ffmpeg.input(rel_root + '/algorithm/public/teethareuspic.jpg')
input2 = ffmpeg.input(rel_root + '/algorithm/public/test-input2.mov')
input3 = ffmpeg.input(rel_root + '/algorithm/public/input3.mov')
aud = input3.audio
input3 = input3.video

# AUDIO OPERATIONS
def extract_audio(alist):
    """
    extracts audio from .audio ffmpeg streams into .WAV files
    Inputs:
        - alist: list of streams
    Outputs:
        - wav_alist: list of wav files
    """
    file_path = rel_root + "/algorithm/public/audio_extracts/"
    wav_alist = []
    a_tracker = 0
    for a in alist:
        name = file_path + str(a_tracker) + '.wav'
        wav_alist.append(a.output(name, audio_bitrate="160k").run())
    print('stuff in wav ', wav_alist[0])
    return wav_alist

def generate_mixed_audio(alist):
    sf, data = read(alist[0])
    print(data)
    print(sf)

extract_audio([aud])

# VIDEO OPERATIONS (all files included assumed to exclude audio)
def trim_vids(untrimmed_vlist):
    pass

def generate_mosaic(vlist):
    """
    Generates a r x c mosaic video output
    Inputs:
        - vlist: list of lists where each of the x nested lists is a row with x videos
    Returns:
        - rxc mosaic workflow
    """
    hstack_lst = []
    for row in vlist:
        hstack_lst.append(ffmpeg.filter(row, 'hstack', len(row)))
    return ffmpeg.filter(hstack_lst, 'vstack', len(vlist))

def compress_v(in_vid, num_r_c):
    """
    Compresses video to match how many rows, cols it contains
    Inputs:
        - in_vid: video object inputted
        - num_r_c: integer representing number of both rows and columns of final vid (row = col here)
    Return:
        - new video artifact with compression added to workflow
    """
    w, h = 1920, 1080
    res_dict = {
        1: [w, h],
        2: [w/2, h/2],
        3: [w/3, h/3],
        4: [w/4, h/4],
        5: [w/5, h/5],
        6: [w/6, h/6],
        7: [w/7, h/7] # not currently sure if breaks since not perfectly divisible
    }
    return ffmpeg.filter(in_vid, 'scale', width=res_dict[num_r_c][0], height=res_dict[num_r_c][1]) # allows x.0 for input w, h

# input22 = compress_v(input2, 2).split()
# input2main = compress_v(main, 2).split()
# input23 = compress_v(input3, 2).split()
# generate_mosaic([[input22[0], input22[1]], [input23[0], input23[1]]]).output(aud, "test_again_3.10.mp4").run()


"""
NOTES
- h/v/xstack HELLA important: https://stackoverflow.com/questions/11552565/vertically-or-horizontally-stack-mosaic-several-videos-using-ffmpeg

- ffmpeg.trim i think i will need this later on in the future
# left_half = (
#     ffmpeg
#     .crop(main)
# )

- use .SPLIT() to create split upstream, call children by x[0], x[1]...

- use .compile() for any more complicated operations


# THIS IS POSSIBLE
# in0 = ffmpeg.input('input0').filter('crop', ...)
# in1 = ffmpeg.input('input1').filter('crop', ...)
# out = ffmpeg.filter([in0, in1], 'hstack').output('output')

- WORKING WITH VID AND AUDIO TOGETHER
- https://github.com/kkroening/ffmpeg-python/issues/208


- MAKING BLANK SPOTS IN MOSAIC BLACK
- https://stackoverflow.com/questions/63429206/ffmpeg-xstack-mutiple-inputs-for-mosaic-video-output-extra-output-blank-scre
"""


"""
LOG 
# 12/23 it works! the hstack 4-way was successful, now gotta see if i can compress the videos
# todo:
#   - compression works with scaling!
#   - xstack

# 12/27
SUCCESSES
- manual xstack works
- successfully scaling
- learned how to control bitrate
- extract audio and video separately

# 12/28
SUCCESSES
- converted audio ffmpeg streams to .WAV files

QUESTIONS
- how to store the audio ffmpeg streams

THINGS TO CONSIDER FOR CONFIGURABILITY
- dimensions of videos
- frame rate of videos
- video file types
"""