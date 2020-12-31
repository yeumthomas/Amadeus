import ffmpeg
import os
from scipy.io.wavfile import read, write
import matplotlib.pyplot as plt
import numpy
import math

"""
FINAL VIDEO DESCRIPTION
- audio: 4410 sr
- video: .mp4, fr: 25 fps
- codec: h.264
"""

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


def editor(folder_path, work_num, output_file_name, output_file_type):
    """
    Handles all functions.
    Input:
        - folder_path: path to folder housing all video files ordered in order to be shown in video.
        - work_num: main number address for client
        - output_file_name: name of final video file
        - output_file_type: type of video file for final video
    Output:
        - path to final video
    """
    ffmpeg_v_list = []
    for file in os.scandir(folder_path):
        ffmpeg_v_list.append(ffmpeg.input(file.path))
    
    # GENERATE FOLDER FOR WORKSPACE
    workspace = generate_dir(os.getcwd() + '/algorithm/assets/', work_num)

    # AUDIO
    ffmpeg_a_list = [video.audio for video in ffmpeg_v_list]
    merged_audio_path, cut_off_time = audio_handler(ffmpeg_a_list, workspace)
    audio = ffmpeg.input(merged_audio_path)
    
    # VIDEO
    trimmed_vids = trim_vids(ffmpeg_v_list, cut_off_time)
    video = generate_mosaic(trimmed_vids)
    
    # MERGE AV
    finished_file_path = workspace + output_file_name + output_file_type
    out = ffmpeg.output(video, audio, finished_file_path, vcodec='h264', acodec='aac', strict='experimental')
    out.run()

    return finished_file_path

def generate_dir(path, name):
    """
    creates new directory
    Inputs:
        - path: address to new directory
        - name: name of directory
    Outputs:
        - path to new directory
    """
    dir_path = os.path.join(path, name)
    os.mkdir(dir_path)
    dir_path = dir_path + '/'
    return dir_path

# AUDIO OPERATIONS
def audio_handler(alist, workspace):
    """
    Synchronizes and mixes all individual audio files into single audio file.
    Inputs:
        - alist: list of paths to audio files
        - workspace: path to workspace folder
    Outputs:
        - path to single mixed audio file
        - time of cut-offs (to be sync'd with videos)
    """

    # creates and gets file paths for indvidiual wav files
    file_path_list = extract_audio(alist, workspace)

    trimmed_path_list = []
    cut_off_time = []
    audio_trimmed_path = generate_dir(workspace, "audio_trimmed")
    for ind in range(len(file_path_list)):

        # finds cut-off time on claps
        (cut_off, sample_rate, data) = find_clap(file_path_list[ind])

        # creates and gets file paths for trimmed wav files
        delay = 1
        trimmed_path_list.append(trim_audio(data, cut_off, sample_rate, ind, audio_trimmed_path, delay))
        cut_off_time.append(cut_off / float(sample_rate) + delay)

    # merges all files into one
    return sync_audio(trimmed_path_list, workspace), cut_off_time

def extract_audio(alist, workspace):
    """
    extracts audio from .audio ffmpeg streams into .WAV files
    (called by generate_mixed_audio)
    Inputs:
        - alist: list of .audio streams
        - workspace: path to workspace folder
    Outputs:
        - wav_alist: list of paths to wav files in audio_extracts
    """
    wav_alist = []
    a_tracker = 0 # names files incrementing by 1

    audio_extracts_path = generate_dir(workspace, "audio_extracts")
    for a in alist:
        name = audio_extracts_path + str(a_tracker) + '.wav'
        a.output(name, audio_bitrate="160k").run()
        a_tracker += 1
    for file in os.scandir(audio_extracts_path):
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

def trim_audio(afile, cut_off, sample_rate, index, audio_trimmed_path, delay=1):
    """
    trims audio 1 seconds after clap.
    Inputs:
        - afile: audio file to be trimmed
        - cut_off: location in seconds of clap
        - sample_rate: sample rate of audio file
        - index: index of audio file in main list of audio files
        - audio_trimmed_path: file path to workspace directory
        - delay: number of seconds after cut_off to trim video
    Return:
        - path to trimmed audio file
    """

    trimmed_clip = afile[(cut_off + sample_rate * delay):]
    trimmed_file_name = audio_trimmed_path + str(index) + ".wav"
    write(trimmed_file_name, sample_rate, trimmed_clip)

    return trimmed_file_name

def sync_audio(trimmed_path_list, workspace):
    """
    synchronize all audio into a single wav file
    Inputs:
        - trimmed_path_list: paths to all trimmed audio files
        - workspace: path to workspace directory
    Output:
        - path to final wav file
    """
    merged_path = workspace + 'merged.wav'
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



# VIDEO OPERATIONS
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
    FPS_FINAL = 25
    for ind, video in enumerate(vlist):
        stream = ffmpeg.filter(video, 'fps', fps=FPS_FINAL, round='up')
        trimmed_vlist.append(ffmpeg.trim(stream, start_frame=cut_off_time[ind] * FPS_FINAL).setpts('PTS-STARTPTS'))

    return trimmed_vlist

def generate_mosaic(vlist):
    """
    Generates the mosaic-style for final video and compresses files accordingly.
    Inputs:
        - vlist: list of ffmpeg video objects
    Output:
        - path to final video
    """
    def propose_mosaic(vlist):
        """
        creates a proposed mosaic for videos
        Inputs:
            - vlist: list of videos
        Returns:
            - proposed video format (ex: [4, 5, 5] for 14 videos, 3 rows, 5 videos each row except 1st)
        """
        vnum = len(vlist)
        lower_square = math.floor(math.sqrt(vnum))
        check = False

        while not check:
            mosaic_form = []
            rows = lower_square
            remainder = vnum % rows
            cols = vnum // rows

            for dummy in range(rows):
                mosaic_form.append(cols)

            print(mosaic_form)
            if remainder:
                rev_ind = len(mosaic_form) - 1
                for dummy in range(remainder):
                    mosaic_form[rev_ind] = mosaic_form[rev_ind] + 1
                    rev_ind -= 1
                    print(mosaic_form)
            
            check = check_dims(len(mosaic_form), mosaic_form[-1])
            lower_square += 1

        return mosaic_form

    def check_dims(r, c):
        """
        Checks to see if width of videos are greater than height (we want horizontal videos in mosaic)
        Inputs:
            - r: # of rows in proposed mosaic
            - c: # of cols in row with most columns in proposed mosaic
        Outputs:   
            - True, if mosaic passes this check
            - False, if otherwise
        """
        if 1920 / c > 1080 / r:
            return True
        else:   
            return False

    def compress_v(video, rows, cols):
        """
        Compresses video to match how many rows, cols it contains
        Inputs:
            - video: video path
            - rows: number of rows
            - cols: number of cols for row video is in
        Outputs:
            - new video artifact with compression added to workflow
        """
        w, h = 1920, 1080
        return ffmpeg.filter(video, 'scale', width=w/cols, height=h/rows)

    mosaic_form = propose_mosaic(vlist)

    # Compress each individual video by their dimensions in mosaic.
    total_rows = len(mosaic_form)
    mosaic_matrix = [[] for dummy in range(total_rows)]
    curr_vid = 0
    for row, total_cols in enumerate(mosaic_form, start=0):
        for v_index in range(total_cols):
            print("")
            print("row: ", row)
            print("v_index: ", v_index)
            print("curr_vid: ", curr_vid)
            print("total_rows: ", total_rows)
            print("total_cols: ", total_cols)
            print("")

            mosaic_matrix[row].append(compress_v(vlist[curr_vid], total_rows, total_cols))
            curr_vid += 1
    
    print("MOSAIC_MATRIX: ", mosaic_matrix)
    # Prepare ffmpeg xstack.
    hstack_lst = []
    for row in mosaic_matrix:
        hstack_lst.append(ffmpeg.filter(row, 'hstack', len(row)))
    return ffmpeg.filter(hstack_lst, 'vstack', len(hstack_lst))


editor(os.getcwd() + '/algorithm/assets/me_singing', "DEMO PROJECT", "acapella", ".mp4")

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

# 12/30
- AUDIO / VIDEO IS SYNCHRONIZED PERFECTLY
THINGS TO CONSIDER FOR CONFIGURABILITY
- dimensions of videos
- frame rate of videos
- video file types
"""