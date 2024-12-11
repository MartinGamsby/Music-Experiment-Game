# Was originally adapted from jxmorris12/synthviz. Thanks!
# I changed:
# - removed timidity
# - optimized the video creating process with imageio, creating from RAM instead of writing every frame on disk
# - support multiple tracks with multiple colors.
# - Removed the 1s buffer, because there's sometimes some issues with creating a video, and then adding audio, and the sound gets choppy, maybe a Windows issue... (I'm just copying video and audio together right now)

import os
import subprocess

import pretty_midi
import PIL
import PIL.Image
import numpy as np
import tqdm

from pathlib import Path
from time import sleep

# Only used in the print-out of the notes; not relevant to the video:
ACCIDENTAL_NOTES = "flat"

WHITE_NOTES = {0: "C", 2: "D", 4: "E", 5: "F", 7: "G", 9: "A", 11: "B"}
SHARP_NOTES = {1: "C#", 3: "D#", 6: "F#", 8: "G#", 10: "A#"}
FLAT_NOTES    = {1: "Bb", 3: "Eb", 6: "Gb", 8: "Ab", 10: "Bb"}

WHITE_NOTES_SCALE = {0: 0, 2: 1, 4: 2, 5: 3, 7: 4, 9: 5, 11: 6}

print_notes_to_stdout = False

VIDEO_FROM_CACHE = True
ADD_ONE_SECOND_BUFFER = False # TODO: to test with VIDEO_FROM_CACHE, makes some really small videos sometimes... (1s?)

#------------------------------------------------------------------------------
def note_breakdown(midi_note):
    note_in_chromatic_scale = midi_note % 12
    octave = round((midi_note - note_in_chromatic_scale) / 12 - 1)
    
    return [note_in_chromatic_scale, octave]

#------------------------------------------------------------------------------
def is_white_key(note):
    return (note % 12) in WHITE_NOTES

#------------------------------------------------------------------------------
def pixel_range(midi_note, image_width):
    # Returns the min and max x-values for a piano key, in pixels.
    
    width_per_white_key = image_width / 52
    
    if is_white_key(midi_note):
        [in_scale, octave] = note_breakdown(midi_note)
        offset = 0
        width = 1
    else:
        [in_scale, octave] = note_breakdown(midi_note - 1)
        offset = 0.5
        width = 0.5
    
    white_note_n = WHITE_NOTES_SCALE[in_scale] + 7*octave - 5
    
    start_pixel = round(width_per_white_key*(white_note_n + offset)) + 1
    end_pixel     = round(width_per_white_key*(white_note_n + 1 + offset)) - 1
    
    if width != 1:
        mid_pixel = round(0.5*(start_pixel + end_pixel))
        half_pixel_width = 0.5*width_per_white_key
        half_pixel_width *= width
        
        start_pixel = round(mid_pixel - half_pixel_width)
        end_pixel     = round(mid_pixel + half_pixel_width)
    
    return [start_pixel, end_pixel]
   
#------------------------------------------------------------------------------
def split_in_colors(names_list, multiplier=1):
    import colorsys
    
    while '' in names_list:
        names_list.remove('')
        
    N = len(names_list)
    HSV_tuples = [(x*1.0/N, 0.5, 0.5) for x in range(N)]
    RGB_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)
    
    ret = []
    for rgb in RGB_tuples:
        ret.append([int(rgb[0]*255*multiplier), int(rgb[1]*255*multiplier), int(rgb[2]*255*multiplier)])
    return ret
    
#------------------------------------------------------------------------------
def save_image(im_frame, folder, idx, writer):    
    if VIDEO_FROM_CACHE:
        import imageio
        writer.append_data(im_frame)
    else:
        img = PIL.Image.fromarray(im_frame)#, mode="RGB")
        
        #https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#jpeg
        # 100 disables portions of the JPEG compression algorithm, and results in large files with hardly any gain in image quality. 
        #img.save("{}/frame{:05d}.jpg".format(folder, idx), quality=85)#Default 75, 95 best
        #ZLIB compression level, a number between 0 and 9: 1 gives best speed, 9 gives best compression, 0 gives no compression at all. Default is 6
        img.save("{}/frame{:05d}.png".format(folder, idx), compress_level=0)
    
#------------------------------------------------------------------------------
def create_video(input_midi: str,
        input_mp3: str,
        image_width    = 1280,
        image_height = 720,
        black_key_height = 2/3,
        vertical_speed = 1/4, # Speed in main-image-heights per second
        fps = 20, 
        video_filename = "output.mp4",
    ):
    frames_folder = os.path.join(Path.cwd(), "video_frames")
    piano_height = round(image_height/6)
    main_height = image_height - piano_height
    time_per_pixel = 1/(main_height*vertical_speed)
    pixels_per_frame = main_height*vertical_speed / fps # (pix/image) * (images/s) / (frames / s) = 

    note_names = {}

    for note in range(21, 109):
        [note_in_chromatic_scale, octave] = note_breakdown(note)
        
        if note_in_chromatic_scale in WHITE_NOTES:
            note_names[note] = "{}{:d}".format(
                WHITE_NOTES[note_in_chromatic_scale], octave)
        else:
            if ACCIDENTAL_NOTES == "flat":
                note_names[note] = "{}{:d}".format(
                    FLAT_NOTES[note_in_chromatic_scale], octave)
            else:
                note_names[note] = "{}{:d}".format(
                    SHARP_NOTES[note_in_chromatic_scale], octave)

    # The 'notes' list will store each note played, with start and end
    # times in seconds.
    print("Loading MIDI file:", input_midi)
    midi_data = pretty_midi.PrettyMIDI(input_midi)
    
    tracks = []
    for i in range(len(midi_data.instruments)):
        tracks.append([
            { "note": n.pitch, "start": n.start, "end": n.end}
            for n in midi_data.instruments[i].notes
        ])
        print(f"Loaded {len(tracks[-1])} notes from MIDI file track #{i+1}")
    colors = split_in_colors(tracks, 2)
    dark_colors = split_in_colors(tracks)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ~ The rest of the code is about making the video. ~
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
    if not os.path.isdir(frames_folder):
        os.mkdir(frames_folder)
        
    # Delete all previous image frames:
    for f in os.listdir(frames_folder):
        os.remove("{}/{}".format(frames_folder, f))

    im_base = np.zeros((image_height, image_width, 3), dtype=np.uint8)

    # Draw the piano, and the grey lines next to the C's for the main area:
    key_start = image_height - piano_height
    white_key_end = image_height - 1
    black_key_end = round(image_height - (1-black_key_height)*piano_height)

    im_lines = im_base.copy()

    for i in range(21, 109):
        # draw white keys
        if is_white_key(i):
            [x0, x1] = pixel_range(i, image_width)
            im_base[key_start:white_key_end, x0:x1] = [255, 255, 255]
        
        # draw lines separating octaves
        if i % 12 == 0:
            im_lines[0:(key_start-1), (x0-2):(x0-1)] = [20, 20, 20]

    for i in range(21, 109):
        # draw black keys
        if not is_white_key(i):
            [x0, x1] = pixel_range(i, image_width)
            im_base[key_start:black_key_end, x0:x1] = [0, 0, 0]

    im_piano = im_base[key_start:white_key_end, :]

    im_frame = im_base.copy()
    im_frame += im_lines

    end_t = 0
    for notes in tracks:
        end_t = max(end_t, max(note["end"] for note in notes) + 1)

    frame_start = end_t
    for notes in tracks:
        if ADD_ONE_SECOND_BUFFER:
            frame_start = min(frame_start, notes[0]["start"] - 1)
        else:
            frame_start = min(frame_start, notes[0]["start"])
    
    # First frame:
    # TODO for multi tracks?
    for track_id, notes in enumerate(tracks):
        for j in range(main_height):
            im_j = main_height - j - 1
            t = frame_start + time_per_pixel*j
            for note in notes:
                if note["start"] <= t <= note["end"]:
                    [x0, x1] = pixel_range(note["note"], image_width)
                    im_frame[im_j, x0:x1] = colors[track_id]#falling_note_color
    
    if VIDEO_FROM_CACHE:
        import imageio
        # TODO: better temp name
        temp_mp4_no_audio = video_filename+".mp4"
        writer = imageio.get_writer(temp_mp4_no_audio, format='FFMPEG', mode='I', fps=fps, codec='libx264')
    else:
        writer = None
            
    save_image(im_frame, frames_folder, 0, writer)


    # Rest of video:
    finished = False
    frame_ct = 0
    pixel_start = 0
    pixel_start_rounded = 0

    print("Generating video frames from notes")

    pbar = tqdm.tqdm(total=end_t, desc='Creating video')
    while not finished:
    
        frame_start += 1/fps
        
        frame_ct += 1
        
        prev_pixel_start_rounded = pixel_start_rounded
        pixel_start += pixels_per_frame
        pixel_start_rounded = round(pixel_start)
        
        pixel_increment = pixel_start_rounded - prev_pixel_start_rounded
        
        pbar.update(1/fps)

        pbar.set_description(f'Creating video [Frame count = {frame_ct}]')
        
        # Copy most of the previous frame into the new frame:
        im_frame[pixel_increment:main_height, :] = im_frame[0:(main_height - pixel_increment), :]
        im_frame[0:pixel_increment, :] = im_lines[0:pixel_increment, :]
        im_frame[key_start:white_key_end, :] = im_piano
        
        for track_id, notes in enumerate(tracks):
            # Which keys need to be colored?
            keys_to_color = []
            for note in notes:
                if note["start"] <= frame_start <= note["end"]:
                    keys_to_color.append(note["note"])
            
            # Draw the new pixels at the top of the frame:
            for j in range(pixel_increment):
                t = frame_start + time_per_pixel*(main_height - j - 1)
                
                for note in notes:
                    if note["start"] <= t <= note["end"]:
                        [x0, x1] = pixel_range(note["note"], image_width)
                        im_frame[j, x0:x1] = colors[track_id]#falling_note_color
            
            # First color the white keys (this will cover some black-key pixels),
            # then re-draw the black keys either side,
            # then color the black keys.
            for note in keys_to_color:
                if is_white_key(note):
                    [x0, x1] = pixel_range(note, image_width)
                    im_frame[key_start:white_key_end, x0:x1] = dark_colors[track_id]#pressed_key_color
            
            for note in keys_to_color:
                if is_white_key(note):
                    if (not is_white_key(note - 1)) and (note > 21):
                        [x0, x1] = pixel_range(note - 1, image_width)
                        im_frame[key_start:black_key_end, x0:x1] = [0,0,0]
                    
                    if (not is_white_key(note + 1)) and (note < 108):
                        [x0, x1] = pixel_range(note + 1, image_width)
                        im_frame[key_start:black_key_end, x0:x1] = [0,0,0]
            
            for note in keys_to_color:
                if not is_white_key(note):
                    [x0, x1] = pixel_range(note, image_width)
                    im_frame[key_start:black_key_end, x0:x1] = dark_colors[track_id]#pressed_key_color
            
        
        
        save_image(im_frame, frames_folder, frame_ct, writer)
        if frame_start >= end_t:
            finished = True

    pbar.close()
    
    sound_file = input_mp3
    if VIDEO_FROM_CACHE:
        writer.close()
        
        if ADD_ONE_SECOND_BUFFER:
            sleep(0.5)# Too fast to write, need to wait until the OS wakes up??
            subprocess.call(f"ffmpeg -i {temp_mp4_no_audio} -i {sound_file} -f lavfi -t 0.1 -i anullsrc -filter_complex [1]adelay=1000|1000[aud];[2][aud]amix -vcodec copy -y {video_filename}".split())
        else:
            codec = "copy"
            subprocess.call(f"ffmpeg -i {temp_mp4_no_audio} -i {sound_file} -c {codec} {video_filename}".split())
        os.remove(temp_mp4_no_audio)
    else:    
        sleep(0.5)# Too fast to write, need to wait until the OS wakes up?? (for jpeg I guess)

        print("Rendering full video with ffmpeg")
        if ADD_ONE_SECOND_BUFFER:
            ffmpeg_cmd = f"ffmpeg -framerate {fps} -i {frames_folder}/frame%05d.png -i {sound_file} -f lavfi -t 0.1 -i anullsrc -filter_complex [1]adelay=1000|1000[aud];[2][aud]amix -vcodec libx264 -preset fast -qmin 25 -y {video_filename}"
        else:
            ffmpeg_cmd = f"ffmpeg -framerate {fps} -i {frames_folder}/frame%05d.png -i {sound_file} -vcodec libx264 -preset fast -qmin 25 -y {video_filename}"

        print("> ffmpeg_cmd: ", ffmpeg_cmd)

        subprocess.call(ffmpeg_cmd.split())
