import math
import matplotlib.pyplot as plt
import numpy as np


eps = np.float64(10**(-5))		#См. в методичке стр 12

def error_estimation_func(W, V, p):  # Оценка погрешности (В методичке S)
    return abs((W - V)) / (-1 + 2 ** 4 )


def double_calc(f, x, y, h, param_a, param_b, param_c):  # Двойной подсчет методом РК*
    k1, k2, k3, k4 = calc_coeff(f, x, y, h / 2, param_a, param_b, param_c)
    tmp_x = x + h / 2
    tmp_y = y + (k1 + k2 + k2 + k3 + k3 + k4) / 6
    k1, k2, k3, k4 = calc_coeff(f, tmp_x, tmp_y, h / 2, param_a, param_b, param_c)
    tmp_y = tmp_y + (k1 + k2 + k2 + k3 + k3 + k4) / 6
    return tmp_y


def split_step(S, p, eps):  # p - порядок метода
    tmp = eps / (2**(p+1))
    if abs(S) > eps:
        return 3
    elif tmp <= abs(S) and abs(S) <= eps:
        return 1
    elif abs(S) < tmp:
        return 2


def calc_coeff(f, x, y, h, param_a, param_b, param_c):  # Подсчет коэффициентов РК*
    k1 = h * f(x, y, param_a, param_b, param_c)
    k2 = h * f(x + 0.5 * h, y + 0.5 * k1, param_a, param_b, param_c)
    k3 = h * f(x + 0.5 * h, y + 0.5 * k2, param_a, param_b, param_c)
    k4 = h * f(x + h, y + k3, param_a, param_b, param_c)
    return k1, k2, k3, k4


def check(x, x0, y0, param_a, param_b, param_c):  # Точное решение
    c = math.log(math.exp(param_a * x0 / param_c) * y0 / (y0 * param_b + param_a)) / param_a
    res = -param_a * math.exp(param_a * c) / (param_b * math.exp(param_a * c) - math.exp(param_a * x / param_c))
    return res


def rk4(f, x0, y0, x1, h, n, param_a, param_b, param_c):  # Минимальный метод(Без наворотов)
    vx = [0] * (n + 1)
    vy = [0] * (n + 1)
    vx[0] = x = x0
    vy[0] = y = y0
    for i in range(1, n + 1):
        k1, k2, k3, k4 = calc_coeff(f, x, y, h, param_a, param_b, param_c)
        vx[i] = x = x0 + i * h
        vy[i] = y = y + (k1 + 2*k2 + 2*k3 + k4) / 6.
    return vx, vy


def rk4_v2(f, x0, y0, x1, h, max_n, param_a, param_b, param_c, eps_bord, flag_inc_step, flag_deg_step, eps):
    info = dict.fromkeys(
        ['n', 'inc', 'deg', 'max err est', 'X on max err est', 'min err est', 'X on min err est', 'x1', 'eps',
         'eps_bord', 'a', 'b', 'c'])  # err est - оценка погрешности
    table = dict.fromkeys(
        ['X', 'Y', 'H', 'W', 'W-V', 'S', 'inc_count', 'deg_count', 'local'])  # См. Методичу страница 13
    info['n'] = 0
    info['inc'] = 0
    info['deg'] = 0
    info['max err est'] = np.float64(0)
    info['min err est'] = np.float64(999)
    info['x1'] = x1
    info['eps'] = eps
    info['eps_bord'] = eps_bord
    info['a'] = param_a
    info['b'] = param_b
    info['c'] = param_c
    # Выделение памяти

    table['W-V'] = [0] * (max_n + 1)
    vx = [0] * (max_n + 1)  # Значение x для каждого шага
    vy = [0] * (max_n + 1)  # Значение y для каждого шага
    vh = [0] * (max_n + 1)  # Значение h для каждого шага
    vw = [0] * (max_n + 1)  # Значение w для каждого шага
    v_ic = [0] * (max_n + 1)  # Значение inc_count для каждого шага
    v_dc = [0] * (max_n + 1)  # Значение deg_count для каждого шага
    vs = [0] * (max_n + 1)  # Значение s для каждого шага
    vx[0] = x = x0
    vy[0] = y = y0
    i = 1
    vh[0] = h
    ccc = 0
    while (i) < max_n:
        v_ic[i] = info['inc']
        v_dc[i] = info['deg']
        # Проверка выхода за границу
        if x + h > x1:
            h = h / 2
            v_dc[i] = info['deg'] = info['deg'] + 1
            continue
        k1, k2, k3, k4 = calc_coeff(f, x, y, h, param_a, param_b, param_c)  # Подсчет коэффициентов для метода РК*
        w = double_calc(f, x, y, h, param_a, param_b, param_c)
        vx[i] = x = (x + h)
        vs[i] = err_est = error_estimation_func(w, y + (k1 + k2 + k2 + k3 + k3 + k4) / 6, 4)

        # Выбор максимальной и минимальной оценки погрешности

        if abs(info['max err est']) < abs(err_est):
            info['max err est'] = abs(err_est)
            info['X on max err est'] = x
        if abs(info['min err est']) > abs(err_est):
            info['min err est'] = abs(err_est)  # Добавить условие чтобы сюда не ставил ошибку из начальной точки
            info['X on min err est'] = x  # Подсчет следующей точки с двойной точностью

        # Изменение шага
        if flag_deg_step != 0:
            if split_step(err_est, 4, eps) == 3:  # Третий случай
                x = x - h
                h /= 2
                # v_dc[i] = info['deg'] = info['deg']+1
                info['deg'] = info['deg'] + 1
                continue  # Прераваем текущую итерацию цикла т.е. не увидичиваем i уменьшаем шаг
        if flag_inc_step != 0:
            if split_step(err_est, 4, eps) == 2:  # Второй случай
                h = h * 2
                # v_ic[i] = info['inc'] = info['inc']+1
                info['inc'] = info['inc'] + 1

        vy[i] = y = y + (k1 + k2 + k2 + k3 + k3 + k4) / 6
        vw[i] = w
        # vy[i] = y = w
        table['W-V'][i] = abs(w-y)

        vh[i] = h
        v_ic[i] = info['inc']
        v_dc[i] = info['deg']
        i += 1
        if (x > x1 - eps_bord) and (x <= x1):
            break

    info['n'] = i
    # Удаление "лишнего хвоста"
    for j in range(max_n - i + 1):
        vx.pop()
        vy.pop()
        vh.pop()
        vw.pop()
        vs.pop()
        v_ic.pop()
        v_dc.pop()
        table['W-V'].pop()
    table['X'] = vx
    table['Y'] = vy
    table['H'] = vh
    table['W'] = vw
    table['S'] = vs
    table['local'] = vs*16
    table['inc_count'] = v_ic
    table['deg_count'] = v_dc
    # return vx, vy, info
    return table, info
