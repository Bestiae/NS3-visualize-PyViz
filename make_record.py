# import modules
# import numpy as np
# import pyvips
# import svgwrite
import cv2
import glob
from pdf2image import convert_from_path
from moviepy.editor import *
import argh
import tempfile

# главная функция, которая и делает основную логику моего задания, то есть сохранение записи симуляции в
# 2-х видео форматах(.avi, .mp4), и гиф.
#?? функция принимает 2 аргумента: input_dir, output_file
# ?_ ?_
def make(input_dir, output_file):
    # output_file = '/home/bestiae/ns-3/test_petro/Unnamed.avi'


    # this variable format is function, so we add at the end of the variable underscore(_)
    format_ = output_file.split('.')[-1]

    #?? это arr который нужен для???
    # для того чтобы в него записать конвертированые с .pdf в .jpg фотографии симуляции
    # который в дальнейшем используется для конвертации этих фото в видео и гиф
    img_array = []
    # это цикл, который (sorted)достает файлы с input_dir(tmp папки) и делает конвертацию c PDF в JPEG,
    # после чего записывает все сконвентированые фотографии в img_arr.
    # для порядка последовательности файлов из input_dir
    for filename in sorted(glob.glob(f'{input_dir}/*.pdf')):
        #?? filename is is __[tmp?] path with ".pdf"?
        # Store Pdf with convert_from_path function
        images = convert_from_path(filename)

        # этим записом мы не должны закрывать файл который создаем, он сам закрывается
        # после выолнения инструкций и окончания блока with
        # create a temporary file using a context manager
        with tempfile.NamedTemporaryFile() as fp:
            # images[0].save(f'{new_filename}.jpg', 'JPEG')
            # img = cv2.imread(f"{new_filename}.jpg")
            # pdf файлы с которых мы делаем JPEG, это файлы с 1 страницой, потому мы записываем images[0],
            # выбирая только первую страницу файла PDF
            images[0].save(fp.name, 'JPEG')
            # print(images[0])

            # cv2.imread() method loads an image from the specified file.
            img = cv2.imread(fp.name)

        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)

    len_arr = len(img_array)
    print("this is len of photo jpg. ", len_arr)

    if format_ == 'mp4':
        # out = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'MJPG'), 3, size)
        out = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'mp4v'), 3, size)
        for i in range(len(img_array)):
            out.write(img_array[i])
        out.release()
        cap = cv2.VideoCapture(output_file)
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        # fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
        print("this is lenght for mp4: ", length)
        # print("this is fps for mp4: ", fps)
        print(f"Video .mp4 is saved on: {output_file}")
    elif format_ == 'avi':
        out = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'DIVX'), 3, size)
        for i in range(len(img_array)):
            out.write(img_array[i])
        out.release()
        print(f"Video .avi is saved on: {output_file}")
    elif format_ == 'gif':
        with tempfile.NamedTemporaryFile() as fp:

            out = cv2.VideoWriter(f'{fp.name}.avi', cv2.VideoWriter_fourcc(*'DIVX'), 3, size)
            for i in range(len(img_array)):
                out.write(img_array[i])
            out.release()
            clip = (VideoFileClip(f'{fp.name}.avi'))
            clip.write_gif(output_file)
        print(f"Gif .gif is saved on: {output_file}")

"""
этот иф нужен для того, чтобы запустить нашу программу с аргументами, которые мы передаем с core.py
"""
if __name__ == '__main__':
    # make('/home/bestiae/ns-3/old_photo', '/home/bestiae/ns-3/test_petro/Unnamed.avi')
    argh.dispatch_command(make)
