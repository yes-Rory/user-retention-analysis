import pandas as pd
import matplotlib.pyplot as plt

# 绘制留存热力图
# read data 读取csv时会自动生成默认索引列，所以使用index_col指定某一列作为dataframe的索引
retention_rate = pd.read_csv(
    "Retention-Analysis/retention_rate.csv",
    index_col=0
)
print(retention_rate)

# step1 :准备画布
plt.figure(figsize=(8,4))
# step2 :绘制热力图
plt.imshow(
    # 二维数字矩阵
    retention_rate.values,
    cmap="Blues",
    # 控制格子的形状
    aspect="auto"
)
# step3 :调整坐标轴刻度
plt.xticks(
    range(len(retention_rate.columns)),
    retention_rate.columns
)
plt.yticks(
    range(len(retention_rate.index)),
    retention_rate.index
)
# 颜色说明书
plt.colorbar(
    label="Retention Rate(%)"
)
# step3 :保存并显示图片
plt.savefig(
    "Retention-Analysis/retention_heatmap.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()