from processor import *
from moviepy.editor import VideoFileClip

fname= 'project_video'
input = f'test_videos/{fname}.mp4'
output = f'output_videos/{fname}.mp4'
video= VideoProcess()

input_clip = VideoFileClip(input)
output_clip = input_clip.fl_image(video.pipeline)
output_clip.write_videofile(output, audio=False)
