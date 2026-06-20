# 隐藏测试 · 练习 2.4A · quap_globe（学生勿看）
import numpy as np
m, s = quap_globe(6, 9)
assert np.ndim(m) == 0 and np.ndim(s) == 0, "应返回两个标量 (map_p, sd)"
assert abs(m - 6/9) < 0.01, "MAP 应≈6/9≈0.667"
assert abs(s - 0.157) < 0.01, "SD 应≈0.157（书 p55 为 0.16）"
m2, s2 = quap_globe(12, 18)
assert abs(m2 - 6/9) < 0.01, "同比例数据 MAP 不变"
assert s2 < s, "数据翻倍后 SD 应更小（后验更窄）"
assert abs(quap_globe(3, 9)[0] - 1/3) < 0.01, "MAP 应等于 W/N（=MLE/解析众数）"
print("（隐藏测试：6 项断言）")
