import time
from typing import List

import cv2
import numpy as np

data_folder = "./KZSP/data/"


def resize_frame(frame: np.ndarray) -> np.ndarray:
    """
    Изменение размера фрейма.

    Args:
        frame (np.array): Входной фрейм.

    Returns:
        np.array: Фрейм с измененным размером.
    """
    height, width, _ = frame.shape

    max_canvas_width = 400
    max_canvas_height = 300
    width_ratio = max_canvas_width / width
    height_ratio = max_canvas_height / height
    scale_ratio = min(width_ratio, height_ratio)
    resized_frame = cv2.resize(frame, (int(width * scale_ratio), int(height * scale_ratio)))

    return resized_frame


def read_annotations(file_path: str) -> List[float]:
    """
    Чтение аннотаций с файла и запись в список.

    Args:
        file_path (str): Путь к файлу с аннотациями.

    Returns:
        List[float]: Список аннотаций из файла.
    """
    with open(file_path, 'r') as file:
        annotations = [float(line.strip()) for line in file]
    return annotations


def get_frame_with_min_timestamp(annotation_list: List[float], current_timestamp: float) -> int:
    """
    Возвращает индекс элемента в списке аннотаций с ближайшим timestamp к текущему временному моменту.

    Args:
        annotation_list (List[float]): Список аннотаций из timestamp-ов.
        current_timestamp (float): Timestamp, к которому нужно найти ближайший.

    Returns:
        int: Индекс ближайшего элемента в списке.
    """
    cut_l_difference = [abs(current_timestamp - t) for t in annotation_list]
    return annotation_list.index(annotation_list[cut_l_difference.index(min(cut_l_difference))])


def play_multiple_videos(v_paths: List[str], a_paths: List[str]) -> None:
    """
    Основная функция воспроизведения

    Args:
        v_paths (List[str]): Пути до видеофайлов.
        a_paths (List[str]): Пути до аннотационных файлов.
    """

    # Создаем объекты VideoCapture для каждого видео
    cap1 = cv2.VideoCapture(v_paths[0])
    cap2 = cv2.VideoCapture(v_paths[1])
    cap3 = cv2.VideoCapture(v_paths[2])
    cap4 = cv2.VideoCapture(v_paths[3])

    # Читаем аннотации
    list_annotations = [read_annotations(annotation) for annotation in a_paths]

    # Выясняем время, от которого будем отталкиваться
    current_time = min(list_annotations[i][0] for i in range(4))

    while True:
        frame_indexes = [get_frame_with_min_timestamp(list_annotations[i], current_time) for i in range(4)]

        if max(frame_indexes) >= min(len(i) - 1 for i in list_annotations):
            break

        # Устанавливаем текущий кадр для каждого видео
        for cap, frame_index in zip([cap1, cap2, cap3, cap4], frame_indexes):
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)

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

        # Создание окна
        cv2.imshow('Four Videos', full_frame)

        current_time += 0.200

        # Прерывание воспроизведения на 'q'
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # Освобождение ресурсов
    cap1.release()
    cap2.release()
    cap3.release()
    cap4.release()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    video_paths = [data_folder + f"{i}.avi" for i in range(1, 5)]
    annotation_paths = [data_folder + f"{i}.txt" for i in range(1, 5)]

    # Воспроизведение
    play_multiple_videos(video_paths, annotation_paths)
