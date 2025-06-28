import os
import numpy as np
import logging
from pyntcloud import PyntCloud
import open3d as o3d

# 设置日志记录
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def print_ply_info(file):
    """
    打印 .ply 文件的所有数据信息
    """
    try:
        logging.info(f"Reading file: {file}")
        cloud = PyntCloud.from_file(file)

        # 打印文件头部信息
        logging.info("PLY file header information:")
        print(cloud.points.head())  # 打印前几行数据

        # 打印所有列名
        logging.info("Columns in the point cloud:")
        print(cloud.points.columns)

        # 打印所有点的数据
        logging.info("All point cloud data:")
        print(cloud.points)

        # 打印顶点坐标
        logging.info("Vertex coordinates (x, y, z):")
        vertices = cloud.points[['x', 'y', 'z']].values
        print(vertices)

        # 打印统计数据
        logging.info("Point cloud statistics:")
        print(cloud.points.describe())

    except Exception as e:
        logging.error(f"Error reading {file}: {e}")

def compare_point_clouds(file1, file2):
    """
    比较两个点云文件的基本属性
    """
    # 读取点云文件
    cloud1 = PyntCloud.from_file(file1)
    cloud2 = PyntCloud.from_file(file2)

    # 获取点云数据
    points1 = cloud1.points[['x', 'y', 'z']].values
    points2 = cloud2.points[['x', 'y', 'z']].values

    # 比较点云大小
    logging.info(f"Point cloud 1 size: {len(points1)}")
    logging.info(f"Point cloud 2 size: {len(points2)}")

    # 比较点云范围
    min1, max1 = np.min(points1, axis=0), np.max(points1, axis=0)
    min2, max2 = np.min(points2, axis=0), np.max(points2, axis=0)
    logging.info(f"Point cloud 1 range - min: {min1}, max: {max1}")
    logging.info(f"Point cloud 2 range - min: {min2}, max: {max2}")

    # 检查无效点
    invalid1 = np.isnan(points1).any() or np.isinf(points1).any()
    invalid2 = np.isnan(points2).any() or np.isinf(points2).any()
    logging.info(f"Point cloud 1 has invalid points: {invalid1}")
    logging.info(f"Point cloud 2 has invalid points: {invalid2}")

def visualize_point_cloud(file, z_threshold=0):
    """
    可视化点云，只显示z坐标大于阈值的点
    """
    try:
        # 读取点云文件
        cloud = o3d.io.read_point_cloud(file)
        
        # 获取点云数据
        points = np.asarray(cloud.points)
        
        # 筛选z坐标大于阈值的点
        filtered_points = points[points[:, 2] > z_threshold]
        
        # 创建新的点云对象
        filtered_cloud = o3d.geometry.PointCloud()
        filtered_cloud.points = o3d.utility.Vector3dVector(filtered_points)
        
        # 保持原始颜色（如果有）
        if cloud.has_colors():
            colors = np.asarray(cloud.colors)
            filtered_colors = colors[points[:, 2] > z_threshold]
            filtered_cloud.colors = o3d.utility.Vector3dVector(filtered_colors)
        
        logging.info(f"Visualizing point cloud: {file} (only points with z > {z_threshold})")
        logging.info(f"Original points: {len(points)}, Filtered points: {len(filtered_points)}")
        
        o3d.visualization.draw_geometries([filtered_cloud])
        
    except Exception as e:
        logging.error(f"Error visualizing {file}: {e}")

def main(file1, file2):
    """
    主函数：综合比较两个点云文件
    """
    # 检查文件是否存在
    if not os.path.exists(file1) or not os.path.exists(file2):
        logging.error("One or both files do not exist.")
        return

    # 打印 .ply 文件的所有数据信息
    logging.info("Printing PLY file information...")
    print_ply_info(file1)
    print_ply_info(file2)

    # 比较点云文件
    logging.info("Comparing point clouds...")
    compare_point_clouds(file1, file2)

    # 可视化点云（只显示z>1的点）
    logging.info("Visualizing point clouds (only z > 5)...")
    visualize_point_cloud(file1)
    visualize_point_cloud(file2)

if __name__ == "__main__":
    # 指定两个点云文件路径
    file1 = "zhuzi1.ply"  # 替换为你的文件路径
    file2 = "pointcloud-unity-total.ply"  # 替换为你的文件路径

    # 运行主函数
    main(file1, file2)
