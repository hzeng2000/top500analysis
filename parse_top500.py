import pandas as pd


def parse_country_architecture_stats(df):
    # 按国别统计MPP和Cluster
    country_architecture_stats = df.groupby(['Country', 'Architecture']).size().unstack(fill_value=0)
    country_architecture_stats = country_architecture_stats.reset_index()
    country_architecture_stats.columns = ['国家', 'MPP', 'Cluster']
    country_architecture_stats['Total'] = country_architecture_stats['MPP'] + country_architecture_stats['Cluster']

    # 按Total列进行降序排序
    country_architecture_stats = country_architecture_stats.sort_values(by='Total', ascending=False)
    # 输出按国别统计的结果
    print("按国别统计TOP500中体系结构分类：")
    print(country_architecture_stats)
    return country_architecture_stats
    
def parse_top10_processors(df):
    # 获取排名前十的系统信息
    top10 = df.head(10)
    top10_processors = top10[['Rank', 'Name', 'Processor', 'Processor Technology', 'Processor Speed (MHz)', 'Accelerator/Co-Processor']]

    # 输出排名前十系统的处理器信息
    print("\nTOP500中排名前十系统的处理器信息：")
    print(top10_processors)
    return top10_processors
def parse_top10_interconnect(df):
    # 获取排名前十的系统信息
    top10 = df.head(10)
    # 获取排名前十系统的互连网络信息
    top10_interconnect = top10[['Rank', 'Name', 'Country', 'Interconnect Family', 'Interconnect']]

    # 输出排名前十系统的互连网络信息
    print("\nTOP500中排名前十系统的互连网络信息：")
    print(top10_interconnect)

    return top10_interconnect

def parse_china_top500_green500(df_top500, df_green500):
    # 筛选中国的系统
    china_systems_top500 = df_top500[df_top500['Country'] == 'China']
    china_systems_top500 = china_systems_top500.dropna(subset=['Name'])
    
    # 提取所需字段
    china_top500 = china_systems_top500[['Rank', 'Name', 'Rmax [TFlop/s]', 'Rpeak [TFlop/s]', 'Power (kW)', 'Energy Efficiency [GFlops/Watts]']]
    china_top500.columns = ['TOP500 排名', '机器', 'HPL 性能 (TFlop/s)', '峰值性能 (TFlop/s)', '功耗 (kW)', '性能功耗比 (GFlops/瓦)_x']
    
    # 在 GREEN500 中查找对应的中国系统
    china_green500 = df_green500[df_green500['Name'].isin(china_top500['机器'])]
    
    # 提取所需字段
    china_green500 = china_green500[['Name', 'Rank', 'Energy Efficiency [GFlops/Watts]']]
    china_green500.columns = ['机器', 'GREEN500 排名', '性能功耗比 (GFlops/瓦)_y']
    
    # 合并 TOP500 和 GREEN500 数据
    china_top500_green500 = pd.merge(china_top500, china_green500, on='机器', how='left')
    
    # 输出中国的 TOP500 与 GREEN500 排名对比
    print("\n我国高性能计算机的 TOP500 与 GREEN500 排名对比：")
    print(china_top500_green500)
    
    return china_top500_green500
def analyze_top500(top500_file_path, green500_file_path):
    # 读取Excel文件
    top500_df = pd.read_excel(top500_file_path, sheet_name=0)
    green500_df = pd.read_excel(green500_file_path, sheet_name=0)

    country_architecture_stats = parse_country_architecture_stats(top500_df)
    top10_processors = parse_top10_processors(top500_df)
    top10_interconnect = parse_top10_interconnect(top500_df)
    china_top500_green500 = parse_china_top500_green500(top500_df, green500_df)
    return country_architecture_stats, top10_processors, top10_interconnect, china_top500_green500

# 调用函数并传入Excel文件路径
top500_file_path = '/home/hzeng/prj/top500analysis/TOP500_202411.xlsx'
green500_file_path = '/home/hzeng/prj/top500analysis/green500_top_202411.xlsx'
country_architecture_stats, top10_processors, top10_interconnect, china_top500_green500 = analyze_top500(top500_file_path, green500_file_path)

# 将结果保存到Excel文件
with pd.ExcelWriter('top500_analysis_results.xlsx') as writer:
    country_architecture_stats.to_excel(writer, sheet_name='Country_Architecture', index=False)
    top10_processors.to_excel(writer, sheet_name='Top10_Processors', index=False)
    top10_interconnect.to_excel(writer, sheet_name='Top10_Interconnect', index=False)
    china_top500_green500.to_excel(writer, sheet_name='China_Top500_Green500', index=False)

print("\n分析结果已保存到 top500_analysis_results.xlsx 文件中。")