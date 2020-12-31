import ffmpeg
import os
from scipy.io.wavfile import read, write
import matplotlib.pyplot as plt
import numpy as numpy
import cv2

# helpful link to figure out os paths: https://stackoverflow.com/questions/18114081/ffmpeg-cannot-detect-file-while-os-can
REL_ROOT = os.getcwd() # gets current working directory (ludwig-2.0 apparently)
V_OUTPUT_PATH = REL_ROOT + '/algorithm/public/video_extracts/'
A_OUTPUT_PATH = REL_ROOT + '/algorithm/public/audio_extracts/'
A_TRIMMED_PATH = REL_ROOT + '/algorithm/public/audio_trimmed/'
A_MERGED_PATH = REL_ROOT + '/algorithm/public/audio_merged/'

# INPUTS
bg = ffmpeg.input(REL_ROOT + '/algorithm/public/REAL-1920x1080.jpg')
main = ffmpeg.input(REL_ROOT + '/algorithm/public/lastMoments.mov')
logo = ffmpeg.input(REL_ROOT + '/algorithm/public/teethareuspic.jpg')
input2 = ffmpeg.input(REL_ROOT + '/algorithm/public/test-input2.mov')
input3 = ffmpeg.input(REL_ROOT + '/algorithm/public/input3.mov')
aud = input3.audio
input3 = input3.video

in1 = ffmpeg.input(REL_ROOT + '/algorithm/public/1.mov')
in2 = ffmpeg.input(REL_ROOT + '/algorithm/public/2.mov')
in3 = ffmpeg.input(REL_ROOT + '/algorithm/public/3.mov')
in4 = ffmpeg.input(REL_ROOT + '/algorithm/public/4.mov')
# claptest = ffmpeg.input(REL_ROOT + '/algorithm/public/claptest.mov').audio


# ENTIRE HANDLER
def editor(files):
    """
    handles all functions
    """

    merged_audio_path, cut_off_time = audio_handler([files[0].audio, files[1].audio, files[2].audio, files[3].audio])
    audio = ffmpeg.input(merged_audio_path)
    
    trimmed_vids = trim_vids(files, cut_off_time)

    ### DETERMINE VIDEO LAYOUT HERE ###

    compressed_vids = []
    for video in trimmed_vids:
        compressed_vids.append(compress_v(video, 2))

    video = generate_mosaic([[compressed_vids[0], compressed_vids[1]], [compressed_vids[2], compressed_vids[3]]])

    out = ffmpeg.output(video, audio, "COMPLETED.mp4", vcodec='h264', acodec='aac', strict='experimental')
    out.run()


# AUDIO OPERATIONS
def audio_handler(alist):
    """
    Synchronizes and mixes all individual audio files into single audio file.
    Inputs:
        - alist: list of paths to audio files
    Outputs:
        - path to single mixed audio file
        - time of cut-offs (to be sync'd with videos)
    """

    # creates and gets file paths for indvidiual wav files
    file_path_list = extract_audio(alist)

    trimmed_path_list = []
    cut_off_time = []
    for ind in range(len(file_path_list)):

        # finds cut-off time on claps
        (cut_off, sample_rate, data) = find_clap(file_path_list[ind])
        
        # creates and gets file paths for trimmed wav files
        delay = 1
        trimmed_path_list.append(trim_audio(data, cut_off, sample_rate, ind, delay))

        cut_off_time.append(cut_off / float(sample_rate) + delay)

    # merges all files into one
    return sync_audio(trimmed_path_list), cut_off_time

def extract_audio(alist):
    """
    extracts audio from .audio ffmpeg streams into .WAV files
    (called by generate_mixed_audio)
    Inputs:
        - alist: list of .audio streams
    Outputs:
        - wav_alist: list of paths to wav files in audio_extracts
    """
    wav_alist = []
    a_tracker = 0 # names files incrementing by 1

    for a in alist:
        name = A_OUTPUT_PATH + str(a_tracker) + '.wav'
        a.output(name, audio_bitrate="160k").run()
        a_tracker += 1
    for file in os.scandir(A_OUTPUT_PATH):
        wav_alist.append(file.path)

    return wav_alist

# ERROR HANDLING INCOMPLETE
def find_clap(afile):
    """
    Finds location of first clap
    Inputs:
        - afile: audio file inputted
    Return:
        - frame of first clap
        - sample rate
    """
    # break down files into numpy arrays
    CLAP_TIMER = 60
    THRESH_CAP = .4 
    sample_rate, data = read(afile)
    
    if data.ndim == 1:
        modified_data = list(map(abs, data[:CLAP_TIMER * sample_rate]))
    else:
        modified_data = list(map(abs, data[:CLAP_TIMER * sample_rate, 0]))
    
    # graph_audio(modified_data)

    threshold = max(modified_data) * THRESH_CAP # gets max loudness of data and sets 40% loudness as a clap

    print("")   
    print("Threshold: ", threshold)
    print("Maximum Freq: ", max(modified_data))
    print("")

    for i in range(int(len(modified_data))):
        if modified_data[i] >= threshold:
            return (i, sample_rate, data)
        
    print("ERROR FINDING CLAP")

def trim_audio(afile, cut_off, sample_rate, index, delay=1):
    """
    trims audio 1 seconds after clap.
    Inputs:
        - afile: audio file to be trimmed
        - cut_off: location in seconds of clap
        - sample_rate: sample rate of audio file
        - index: index of audio file in main list of audio files
        - number of seconds after cut_off to trim video
    Return:
        - path to trimmed audio file
    """
    trimmed_clip = afile[(cut_off + sample_rate * delay):]
    trimmed_file_name = A_TRIMMED_PATH + str(index) + ".wav"
    write(trimmed_file_name, sample_rate, trimmed_clip)

    return trimmed_file_name

def sync_audio(trimmed_path_list):
    """
    synchronize all audio into a single wav file
    Inputs:
        - trimmed_path_list: paths to all trimmed audio files
    Output:
        - path to final wav file
    """
    merged_path = A_MERGED_PATH + 'merged.wav'
    a_inputs = [ffmpeg.input(path) for path in trimmed_path_list]

    while len(a_inputs) > 1:
        print(len(a_inputs))
        a_inputs.append(ffmpeg.filter([a_inputs.pop(0), a_inputs.pop(0)], 'amix'))
    
    merged_data = a_inputs[0]
    ffmpeg.output(merged_data, merged_path).run()
    return merged_path

def graph_audio(data):
    """
    Graph shape of audio
    """
    plt.figure(1)
    plt.title("Abs(data) over Time (samples)")
    plt.plot(data)
    plt.show()



def trim_vids(vlist, cut_off_time):
    """
    trims videos to match trimmed audio
    Inputs:
        - vlist: list of video ffmpeg inputs
        - cut_off_time: time in seconds of when to start each video
    Outputs:
        - trimmed video objects
    """
    trimmed_vlist = []

    for ind, video in enumerate(vlist):
        cap=cv2.VideoCapture(video)
        fps = cap.get(cv2.CAP_PROP_FPS)
        trimmed_vlist.append(ffmpeg.trim(video, start_frame=cut_off_time[ind] * fps).setpts('PTS-STARTPTS'))

    return trimmed_vlist

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
# generate_mosaic([[input22[0], input22[1]], [input23[0], input23[1]]]).output(aud, V_OUTPUT_PATH + "test_again_3.10.mp4").run()

editor([in1, in2, in3, in4])

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

# 12/29
SUCCESSES
- GOT A BOOTLEG VIDEO FINISHED

QUESTIONS/GOALS FOR TMR
- compress_v take in a list of video files rather than 1
- trimming video is not exact, maybe fix decimal (find framerate of vid and go by frames)

THINGS TO CONSIDER FOR CONFIGURABILITY
- dimensions of videos
- frame rate of videos
- video file types
"""