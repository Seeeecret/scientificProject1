import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 读取数据
# 假设附件2为销售数据，附件3为批发价格数据
sales_data = pd.read_excel('/mnt/data/附件2.xlsx')
wholesale_data = pd.read_excel('/mnt/data/附件3.xlsx')

# 数据预览
print(sales_data.head())
print(wholesale_data.head())

# 数据基本统计信息
print(sales_data.describe())
print(wholesale_data.describe())

# 数据缺失值检查
print(sales_data.isnull().sum())
print(wholesale_data.isnull().sum())

# 销售数据按日期聚合，查看总销售量的时间趋势
sales_data['日期'] = pd.to_datetime(sales_data['日期'])  # 将日期字段转换为日期格式
daily_sales = sales_data.groupby('日期')['销售量'].sum().reset_index()

# 绘制销售量随时间的变化图
plt.figure(figsize=(14, 7))
plt.plot(daily_sales['日期'], daily_sales['销售量'], label='Daily Sales Volume')
plt.title('Daily Sales Volume Over Time')
plt.xlabel('Date')
plt.ylabel('Sales Volume')
plt.legend()
plt.grid(True)
plt.show()

# 各品类的销售量统计
category_sales = sales_data.groupby('品类')['销售量'].sum().reset_index()

# 绘制不同品类的销售量分布
plt.figure(figsize=(10, 6))
sns.barplot(x='品类', y='销售量', data=category_sales)
plt.title('Sales Volume by Category')
plt.xlabel('Category')
plt.ylabel('Total Sales Volume')
plt.xticks(rotation=45)
plt.show()

# 相关性分析：计算不同品类/单品之间的销售量相关系数
sales_corr = sales_data.pivot_table(index='日期', columns='品类', values='销售量', aggfunc='sum')
corr_matrix = sales_corr.corr()

# 绘制相关性热图
plt.figure(figsize=(12, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix of Sales Volume between Categories')
plt.show()

# 批发价格和销售量的关联分析
# 合并销售数据和批发价格数据，假设两者均有'日期'和'品类'作为共同列
merged_data = pd.merge(sales_data, wholesale_data, on=['日期', '品类'])

# 批发价格与销售量的散点图
plt.figure(figsize=(10, 6))
sns.scatterplot(x='批发价格', y='销售量', hue='品类', data=merged_data)
plt.title('Sales Volume vs. Wholesale Price')
plt.xlabel('Wholesale Price')
plt.ylabel('Sales Volume')
plt.grid(True)
plt.show()
