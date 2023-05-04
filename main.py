import math
import random
import itertools
import time

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# 计算三维坐标系下的两点间距离公式
def distance(a, b):
    dis = ((a[0][1] - b[0][1]) ** 2 + (a[0][2] - b[0][2])
           ** 2 + (a[0][3] - b[0][3]) ** 2) ** 0.5
    return dis


# 偏好排序结果
def order(i, rb_pre):
    pl = [0 for _ in range(n)]
    od = [0 for _ in range(n)]
    for j in range(n):
        pl[j] = rb_pre[i][j]
    min_index = 0
    for i in range(n):
        min_num = pl[0]
        for j in range(n):
            if pl[j] <= min_num:
                min_num = pl[j]
                min_index = j
        pl[min_index] = 10000
        od[i] = min_index
    return od


# 判断匹配是否稳定
def judge_stable(pair, b_cho, r_cho):
    for j in range(n):
        # 对于本次排列的蓝方来说，匹配为pair[j],更喜欢的在b_like_more_r
        target_r = pair[j]
        b_like_more_r = []
        for k in range(n):
            if b_cho[j][k] != target_r:
                b_like_more_r.append(b_cho[j][k])
            else:
                break
        # 判断蓝方更想要得到的匹配中的红方，比起它是否有b更喜欢的
        for q in b_like_more_r:
            for a in range(n):
                if pair[a] == q:
                    target_b = a
            for b in range(n):
                if r_cho[q][b] == j:
                    return 0
                if r_cho[q][b] == target_b:
                    break
    return 1


# 任务分配函数
def task_assign(num_uav):
    print('输入了' + str(num_uav) + '无人机')
    # 定义以及初始化存储无人机速度数组，r代表红方，为防守方，b代表蓝方，为攻击方
    # 速度范围在13-15m/s之间
    r_v = [random.uniform(13, 15) for _ in range(n)]
    b_v = [random.uniform(13, 15) for _ in range(n)]
    for i in range(n):
        r_v[i] = round(r_v[i], 1)
        b_v[i] = round(b_v[i], 1)
    print('速度：')
    print(r_v)
    print(b_v)

    # 定义双方无人机的航向角，红方的航向角范围是（0，pi），蓝方的是（pai，2*pi）
    r_a = [random.uniform(0, 1) * math.pi for _ in range(n)]
    b_a = [random.uniform(1, 2) * math.pi for _ in range(n)]
    for i in range(n):
        r_a[i] = round(r_a[i], 2)
        b_a[i] = round(b_a[i], 2)
    print('航向角')
    print(r_a)
    print(b_a)

    # 双方无人机的初始位置（三维）
    r_pos = [[0] * 3 for _ in range(n)]
    b_pos = [[0] * 3 for _ in range(n)]
    for i in range(n):
        for j in range(3):
            # 设置 x 的范围在0-1000之间
            if j == 0:
                r_pos[i][j] = random.randint(0, 1000)
                b_pos[i][j] = random.randint(0, 1000)
            # 设置 y 的范围，防守方在0-50之间，攻击方在950-1000之间
            if j == 1:
                r_pos[i][j] = random.randint(0, 50)
                b_pos[i][j] = random.randint(950, 1000)
            # 设置高度的范围在50-100m之间
            if j == 2:
                r_pos[i][j] = random.randint(50, 100)
                b_pos[i][j] = random.randint(50, 100)
    print('双方无人机的位置')
    print(r_pos)
    print(b_pos)

    # 偏好选择依据计算，分别为无人机的飞行时间t，航向角α，高度优势h,无人机间距离表示为rb_s
    rb_s = [[0.0] * n for _ in range(n)]
    rb_t = [[0.0] * n for _ in range(n)]
    br_t = [[0.0] * n for _ in range(n)]
    rb_a = [[0.0] * n for _ in range(n)]
    rb_h = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            rb_s[i][j] = ((r_pos[i][0] - b_pos[j][0]) ** 2 + (r_pos[i][1] -
                                                              b_pos[j][1]) ** 2 + (
                                  r_pos[i][2] - b_pos[j][2]) ** 2) ** 0.5
            rb_t[i][j] = rb_s[i][j] / r_v[i]
            br_t[j][i] = rb_s[i][j] / b_v[j]
            rb_h[i][j] = abs(r_pos[i][2] - b_pos[j][2])
            rb_a[i][j] = abs(round((abs(r_a[i] - b_a[j]) - math.pi), 2))
    print('红蓝双方距离矩阵：')
    print(rb_s)

    # 匹配之后的飞行总时间矩阵（对比算法用）
    rb_total = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            rb_total[i][j] = rb_a[i][j] + rb_s[i][j] / (b_v[j] + r_v[i])
    print('飞行总时间矩阵（对比用）')
    print(rb_total)

    print('飞行航向角矩阵（对比用）')
    print(rb_a)

    print('飞行高度差（对比用）：')
    print(rb_h)

    # 红方（防守方）的偏好选择总和
    rb_pre = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            rb_pre[i][j] = round(
                0.3 *
                rb_t[i][j] +
                0.3 *
                rb_h[i][j] +
                0.4 *
                rb_a[i][j],
                3)
    print('红色偏好选择')
    print(rb_pre)

    # 蓝方（攻击方）的偏好选择总和
    br_pre = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            br_pre[i][j] = round(
                0.3 *
                br_t[i][j] +
                0.3 *
                rb_h[i][j] +
                0.4 *
                rb_a[i][j],
                3)
    print('蓝色偏好选择')
    print(br_pre)

    # 红方偏好列表
    r_cho = [[0] * n for _ in range(n)]
    for i in range(n):
        m_pre = order(i, rb_pre)
        for j in range(n):
            r_cho[i][j] = m_pre[j]
    print('红方偏好选择列表')
    print(r_cho)

    # 蓝方偏好列表
    b_cho = [[0] * n for _ in range(n)]
    for i in range(n):
        n_pre = order(i, br_pre)
        for j in range(n):
            b_cho[i][n - 1 - j] = n_pre[j]
    print('蓝方偏好选择列表')
    print(b_cho)

    # 根据偏好选择列表找到所有稳定的匹配
    start = time.time()
    stable_pairs = []
    # p = [0] * n
    t = [0] * n
    for i in range(n):
        t[i] = i
    # pair_all = [[0]*3 for _ in range(math.factorial(num))]
    # pair_all = list(itertools.permutations(t, n))  # 所有的匹配集合
    # for i in range(math.factorial(n)):
    #     if judge_stable(pair_all[i], b_cho, r_cho):
    #         stable_pairs.append(pair_all[i])
    for i in list(itertools.permutations(t, n)):
        if judge_stable(i, b_cho, r_cho):
            stable_pairs.append(i)
    # print(math.factorial(n))
    # print(pair_all)

    # 结果中蓝方是0-n，对应的stable_pairs[i]是红方
    print('稳定匹配：')
    print(stable_pairs)
    print('稳定匹配长度')
    print(len(stable_pairs))

    # 计算所有稳定匹配的总代价
    if len(stable_pairs) == 1:
        final_pair.append(stable_pairs[0])
        sum_s = 0.0
        sum_t = 0.0
        sum_a = 0.0
        sum_h = 0.0
        std_eve = 0.0
        p = final_pair[0]
        for i in range(n):
            sum_s = sum_s + rb_s[p[i]][i]
        for j in range(n):
            sum_t = sum_t + rb_a[p[j]][j] + rb_s[p[j]][j] / (b_v[j] + r_v[p[j]])
        for k in range(n):
            sum_a = sum_a + rb_a[p[k]][k]
        for k in range(n):
            sum_h = sum_h + rb_h[p[k]][k]
        avg_h = sum_h / n
        # for i in range(n):
        #     std_eve = std_eve + (rb_h[p[i]][i] - avg_h) ** 2
        std_h = avg_h / 50
        total_cost = 0.33 * sum_s / n + 0.33 * sum_t / n + 0.34 * std_h


        print('一个稳定匹配时的总长度')
        print(sum_s/n)
        print('一个稳定匹配时的总飞行时间')
        print(sum_t/n)
        print('一个稳定匹配时的总航向角')
        print(sum_a / (n * math.pi))
        print(sum_a)
        print('一个稳定匹配时的总高度变化')
        print(std_h)
        print(sum_h)
        print('一个稳定匹配时的总花费')
        print(total_cost)
    else:
        total_cost = [0.0] * len(stable_pairs)
        sum_srb = [0.0] * len(stable_pairs)
        sum_trb = [0.0] * len(stable_pairs)
        sum_arb = [0.0] * len(stable_pairs)
        sum_hrb = [0.0] * len(stable_pairs)
        std_hrb = [0.0] * len(stable_pairs)
        for i in range(len(stable_pairs)):
            p = stable_pairs[i]
            std_eve = 0.0
            sum_h = 0.0
            std_h = 0.0
            # 计算高度总代价
            for j in range(n):
                sum_h = sum_h + rb_h[p[j]][j]
            avg_h = sum_h / n
            # std得到的是高度的总代价
            std_h = avg_h / 50

            # 计算得到总航程的平均值
            sum_s = 0.0
            for j in range(n):
                sum_s = sum_s + rb_s[p[j]][j]
            avg_s = sum_s / n

            # 计算飞行的总时间的平均值
            sum_t = 0.0
            for j in range(n):
                sum_t = sum_t + rb_a[p[j]][j] + \
                        rb_s[p[j]][j] / (b_v[j] + r_v[p[j]])
            avg_t = sum_t / n

            # 计算飞行的总航向角
            sum_a = 0.0
            for j in range(n):
                sum_a = sum_a + rb_a[p[j]][j]
            # 计算每个方案的总代价
            total_cost[i] = 0.33 * avg_s + 0.33 * avg_t + 0.34 * std_h
            sum_srb[i] = sum_s
            sum_trb[i] = sum_t
            sum_arb[i] = sum_a
            sum_hrb[i] = sum_h
            std_hrb[i] = std_h
        min_index = total_cost.index(min(total_cost))
        final_pair.append(stable_pairs[min_index])
    end = time.time()
    print(end - start)


if __name__ == '__main__':
    n = int(input('请输入对战的无人机的数量:'))
    final_pair = []
    if n == 0:
        print('请输入正确的无人机数量：')
    task_assign(n)
    print('最终的匹配对：')
    print(final_pair)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
