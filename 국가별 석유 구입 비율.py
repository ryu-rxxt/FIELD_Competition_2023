import numpy as np

# 국가별 통계치
countries = ['미국', '러시아', '사우디']

# 전쟁 전
means = np.array([420475.23, 357491.76, 356314.27])
std_devs = np.array([10369.74, 3634.47, 2842.34])

# 전쟁 후
means = np.array([649673.63, 765365.8, 583478.36])
std_devs = np.array([27885.15, 56427.13, 22296.42])

# 확률 계산 함수
def calculate_ratios(means):
    inverse_squared_means = 1 / means**2
    normalized_inverse_means = inverse_squared_means / inverse_squared_means.sum()
    return normalized_inverse_means

# 결과 출력
ratios = calculate_ratios(means)
for country, ratio in zip(countries, ratios):
    print(f'{country}로부터의 비율: {ratio:.3f}')
