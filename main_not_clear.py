from pprint import pprint

import cv2
import time
from typing import  List


data_folder = "./KZSP/data/"


def resize_frame(frame):
    # Получите текущие размеры кадра
    height, width, _ = frame.shape

    max_canvas_width = 400
    max_canvas_height = 300

    # Рассчитайте соотношение масштабирования для ширины и высоты
    width_ratio = max_canvas_width / width
    height_ratio = max_canvas_height / height

    # Используйте минимальное значение из обоих коэффициентов масштабирования, чтобы сохранить пропорции
    scale_ratio = min(width_ratio, height_ratio)

    # Примените масштабирование
    resized_frame = cv2.resize(frame, (int(width * scale_ratio), int(height * scale_ratio)))

    return resized_frame

def read_annotations(file_path):
    with open(file_path, 'r') as file:
        annotations = [float(line.strip()) for line in file]
    return annotations

def get_frame_with_min_timestamp(annotation_list: list, current_timestamp: int) -> int:
    # if current_frame < 10: current_frame = 10
    # if current_frame > min(len(i) for i in l) - 11: current_frame = min(len(i) for i in l) - 11

    # Выборка меток среди которых будем искать ближайшую
    # cut_l = l[num_of_annotation][current_frame - 10: current_frame + 10]
    # Выборка отдалений от нужной нам метки из cut_l
    cut_l_difference = [abs(current_timestamp - t) for t in annotation_list]

    # d_diff = {l[num_of_annotation][l[num_of_annotation].index(
    #     cut_l[
    #         cut_l_difference.index(i)
    #     ]
    # )]: i for i in cut_l_difference}
    #
    #
    # pprint(d_diff)


    return annotation_list.index(annotation_list[cut_l_difference.index(min(cut_l_difference))])


def play_multiple_videos(video_paths):
    # Создаем объекты VideoCapture для каждого видео
    cap1 = cv2.VideoCapture(video_paths[0])
    cap2 = cv2.VideoCapture(video_paths[1])
    cap3 = cv2.VideoCapture(video_paths[2])
    cap4 = cv2.VideoCapture(video_paths[3])

    list_annotations = [1, 2, 3, 4]

    list_annotations[0], list_annotations[1], list_annotations[2], list_annotations[3] = (
        read_annotations(annotation) for annotation in annotation_paths)


    current_time = min(list_annotations[i][0] for i in range(0, 4))

    while True:



        frame_indexes = [get_frame_with_min_timestamp(list_annotations[i], current_time) for i in range(0, 4)]

        if max(frame_indexes) >= min(len(i) - 1 for i in list_annotations):
            break

        print(f"\n\n{current_time=}\n\n")
        print(f"\n\n{frame_indexes=}\n\n")


        cap1.set(cv2.CAP_PROP_POS_FRAMES, frame_indexes[0])
        cap2.set(cv2.CAP_PROP_POS_FRAMES, frame_indexes[1])
        cap3.set(cv2.CAP_PROP_POS_FRAMES, frame_indexes[2])
        cap4.set(cv2.CAP_PROP_POS_FRAMES, frame_indexes[3])

        # Чтение кадров из каждого видео
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()
        ret3, frame3 = cap3.read()
        ret4, frame4 = cap4.read()

        frame1, frame2, frame3, frame4 = (resize_frame(frame) for frame in [frame1, frame2, frame3, frame4])

        # Проверка на конец видео
        if not ret1 or not ret2 or not ret3 or not ret4:
            break

        # Объединение кадров
        top_row = cv2.hconcat([frame4, frame1])
        bottom_row = cv2.hconcat([frame2, frame3])
        full_frame = cv2.vconcat([top_row, bottom_row])

        # создание окна
        cv2.imshow('Four Videos', full_frame)

        # time.sleep(1/6)

        current_time += 0.200

        # Прерывание воспроизведения на q
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break


    # Освобождение ресурсов
    cap1.release()
    cap2.release()
    cap3.release()
    cap4.release()


    cv2.destroyAllWindows()




video_paths = [data_folder + f"{i}.avi" for i in range(1, 5)]
annotation_paths = [data_folder + f"{i}.txt" for i in range(1, 5)]

# Воспроизведение
play_multiple_videos(video_paths)