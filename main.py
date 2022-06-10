import numpy as np
import time as tm
import threading as thread
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d


# 直接插入排序
def insert_sort(a):
    a = np.append(np.array([0]), a)
    for i in range(2, a.size):
        j = i - 1
        a[0] = a[i]
        if a[i] < a[j]:
            a[0], a[i] = a[i], a[j]
            j = i - 2
            while a[0] < a[j]:
                a[j + 1] = a[j]
                j -= 1
            a[j + 1] = a[0]
    return a[1:]


# 折半插入排序
def b_insert_sort(a):
    for i in range(1, a.size):
        tou = 0
        wei = i - 1
        zhong = (tou + wei) // 2
        while tou <= wei:
            if a[zhong] == a[i]:
                break
            elif a[zhong] > a[i]:
                wei = zhong - 1
            elif a[zhong] < a[i]:
                tou = zhong + 1
            zhong = (tou + wei) // 2
        b = a[i]
        for j in range(zhong + 1, i)[::-1]:
            a[j + 1] = a[j]
        a[zhong + 1] = b
    return a


# 快速排序
def quick_sort(a, low=0, lang=10000):
    if low >= lang:
        return
    if lang == 10000:
        lang = a.size - 1
    old_low = low
    old_lang = lang
    b = a[low]
    while low < lang:
        while low < lang and b <= a[lang]:
            lang -= 1
        a[low] = a[lang]
        while low < lang and b > a[low]:
            low += 1
        a[lang] = a[low]
    a[low] = b
    quick_sort(a, old_low, low - 1)
    quick_sort(a, lang + 1, old_lang)
    return a


# 直接选择排序
def select_sort(a):
    for i in range(a.size):
        a_min = i
        for j in range(i, a.size):
            if a[a_min] > a[j]:
                a_min, j = j, a_min
        a[i], a[a_min] = a[a_min], a[i]
    return a


# 堆排序
def heap_sort(a):
    def creat_heap(lang=a.size - 1, b=0):
        c = a[b]
        j = 2 * b
        while j <= lang:
            if j < lang and a[j] < a[j + 1]:
                j += 1
            if c >= a[j]:
                break
            a[b], b = a[j], j
            j *= 2
        a[b] = c

    for i in range(a.size // 2)[::-1]:
        creat_heap(a.size - 1, i)
    for i in range(1, a.size)[::-1]:
        a[0], a[i] = a[i], a[0]
        creat_heap(i - 1)
    return a


# 二路归并排序
def merge_sort(a, low=0, lang=99999):
    if lang == 99999:
        lang = a.size - 1
    if lang - low > 1:
        zhong = (lang + low) // 2
        a1 = merge_sort(a, low, zhong)
        a2 = merge_sort(a, zhong + 1, lang)
        b = np.zeros(a1.size + a2.size, dtype=int)
        len1 = 0
        len2 = 0
        for i in range(b.size):
            if len1 < a1.size or len2 < a2.size:
                if len1 >= a1.size:
                    b[i] = a2[len2]
                    len2 += 1
                elif len2 >= a2.size or a1[len1] <= a2[len2]:
                    b[i] = a1[len1]
                    len1 += 1
                else:
                    b[i] = a2[len2]
                    len2 += 1
        return b
    else:
        if a[low] > a[lang]:
            a[low], a[lang] = a[lang], a[low]
        if low == lang:
            return np.array([a[low]])
        return np.array([a[low], a[lang]])


# 猴子排序
# ps：不要试太多的数列，这玩意看脸，这是python，跑的很慢的
def monkey_sort(a):
    while True:
        for i in range(a.size - 1):
            if a[i] > a[i + 1]:
                break
        else:
            return a
        np.random.shuffle(a)


# 睡眠排序
# ps：试着优化了一下，但还是不要试太大、太小、太离散的数列
def sleep_sort(a, b=np.array([])):
    for i in range(a.size):
        def sleep_add():
            nonlocal b
            tm.sleep(a[i] / 100)
            b = np.append(b, a[i])

        thread.Thread(target=sleep_add).start()
    return b


# 性能分析
def performance_analysis(a):
    time = []
    size = []
    for i in range(100, 1010, 10):
        size.append(i)
        times = 0.0
        for j in range(1):
            c = np.random.random_integers(0, 100, i)
            t1 = tm.time()
            a(c)
            times += tm.time() - t1
        time.append(times)
    return gaussian_filter1d(time, sigma=5), size


def main():
    functions = {
        insert_sort: "直接插入排序",
        b_insert_sort: "折半插入排序",
        select_sort: "直接选择排序",
        quick_sort: "快速排序",
        heap_sort: "堆排序",
        merge_sort: "二分归并排序"
    }
    key = [
        insert_sort,  # 直接插入排序
        b_insert_sort,  # 折半插入排序
        select_sort,  # 直接选择排序
        quick_sort,  # 快速排序
        heap_sort,  # 堆排序
        merge_sort  # 二分归并排序
    ]
    plt.rcParams['font.sans-serif'] = ['SimHei']
    for function in key:
        time, size = performance_analysis(function)
        plt.plot(size, time, label=functions[function])
    plt.xlabel("数据长度")
    plt.ylabel("平均运行时长")
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
