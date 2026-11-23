
"""
学生成绩管理系统
综合运用：循环/选择结构、列表/字典、输入输出、面向对象、文件处理、第三方模块、异常处理
需安装第三方库：matplotlib
安装命令：pip install matplotlib
"""

import json
import matplotlib.pyplot as plt
import os

# ---------- 学生类 ----------
class Student:
    """学生实体类"""
    def __init__(self, stu_id, name, score):
        self.stu_id = stu_id      # 学号 (字符串，便于通用)
        self.name = name          # 姓名
        self.score = score        # 期末总成绩(0-100)

    def to_dict(self):
        """将学生对象转换为字典，用于JSON序列化"""
        return {"stu_id": self.stu_id, "name": self.name, "score": self.score}

    @staticmethod
    def from_dict(data):
        """从字典创建学生对象"""
        return Student(data["stu_id"], data["name"], data["score"])

    def __str__(self):
        return f"{self.stu_id}\t{self.name}\t{self.score}"


# ---------- 管理系统类 ----------
class StudentManager:
    """学生管理类，封装核心功能"""
    DATA_FILE = "students.json"

    def __init__(self):
        self.students = []          # 存储Student对象的列表
        self.load_data()            # 初始化时自动加载文件

    def save_data(self):
        """将学生列表保存到JSON文件"""
        try:
            with open(self.DATA_FILE, "w", encoding="utf-8") as f:
                # 将每个学生对象转为字典，再保存列表
                json.dump([stu.to_dict() for stu in self.students], f, ensure_ascii=False, indent=2)
            print("数据保存成功。")
        except Exception as e:
            print(f"保存文件时出错：{e}")

    def load_data(self):
        """从JSON文件加载数据，若文件不存在则创建空列表"""
        if not os.path.exists(self.DATA_FILE):
            self.students = []
            print("未找到数据文件，已初始化空列表。")
            return
        try:
            with open(self.DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.students = [Student.from_dict(item) for item in data]
            print(f"成功加载 {len(self.students)} 条学生记录。")
        except json.JSONDecodeError:
            print("文件格式损坏，将使用空数据。")
            self.students = []
        except Exception as e:
            print(f"加载文件时出错：{e}，将使用空数据。")
            self.students = []

    def add_student(self, stu_id, name, score):
        """添加学生，包含学号重复检查"""
        # 检查学号是否已存在
        for stu in self.students:
            if stu.stu_id == stu_id:
                raise ValueError(f"学号 {stu_id} 已存在，不能重复添加。")
        if not (0 <= score <= 100):
            raise ValueError("成绩必须在0~100之间。")
        new_stu = Student(stu_id, name, score)
        self.students.append(new_stu)
        self.save_data()
        print(f"学生 {name}({stu_id}) 添加成功。")

    def delete_student(self, stu_id):
        """根据学号删除学生"""
        for i, stu in enumerate(self.students):
            if stu.stu_id == stu_id:
                del self.students[i]
                self.save_data()
                print(f"学号 {stu_id} 已删除。")
                return True
        print(f"未找到学号为 {stu_id} 的学生。")
        return False

    def update_score(self, stu_id, new_score):
        """修改学生成绩"""
        if not (0 <= new_score <= 100):
            raise ValueError("成绩必须在0~100之间。")
        for stu in self.students:
            if stu.stu_id == stu_id:
                old_score = stu.score
                stu.score = new_score
                self.save_data()
                print(f"学号 {stu_id} 成绩由 {old_score} 修改为 {new_score}。")
                return True
        print(f"未找到学号为 {stu_id} 的学生。")
        return False

    def search_by_id(self, stu_id):
        """按学号查询并返回学生对象，若不存在返回None"""
        for stu in self.students:
            if stu.stu_id == stu_id:
                return stu
        return None

    def get_all_students_sorted(self, reverse=True):
        """返回按成绩排序后的学生列表（默认降序）"""
        return sorted(self.students, key=lambda s: s.score, reverse=reverse)

    def show_statistics(self):
        """显示统计信息：平均分、最高最低分、各分数段统计"""
        if not self.students:
            print("暂无学生数据，请先添加。")
            return
        scores = [s.score for s in self.students]
        avg = sum(scores) / len(scores)
        max_score = max(scores)
        min_score = min(scores)

        print("\n========== 成绩统计 ==========")
        print(f"总人数：{len(self.students)}")
        print(f"平均分：{avg:.2f}")
        print(f"最高分：{max_score}")
        print(f"最低分：{min_score}")

        # 分数段统计 (A:>=90, B:>=80, C:>=70, D:>=60, F:<60)
        grades = {"A(≥90)": 0, "B(80-89)": 0, "C(70-79)": 0, "D(60-69)": 0, "F(<60)": 0}
        for s in scores:
            if s >= 90:
                grades["A(≥90)"] += 1
            elif s >= 80:
                grades["B(80-89)"] += 1
            elif s >= 70:
                grades["C(70-79)"] += 1
            elif s >= 60:
                grades["D(60-69)"] += 1
            else:
                grades["F(<60)"] += 1

        print("\n分数段分布：")
        for grade, count in grades.items():
            percent = count / len(self.students) * 100
            bar = "#" * int(percent // 2)   # 简单进度条，每2%一个#号
            print(f"{grade:10} : {count:2}人 ({percent:5.1f}%) {bar}")

    def plot_score_histogram(self):
        """使用matplotlib绘制成绩分布直方图"""
        if not self.students:
            print("没有数据，无法绘图。")
            return
        scores = [s.score for s in self.students]
        plt.figure(figsize=(8, 5))
        plt.hist(scores, bins=10, color='skyblue', edgecolor='black', alpha=0.7)
        plt.title("学生成绩分布直方图")
        plt.xlabel("分数")
        plt.ylabel("人数")
        plt.grid(axis='y', linestyle='--', alpha=0.5)
        # 在柱顶显示具体人数
        n, bins, patches = plt.hist(scores, bins=10, color='skyblue', edgecolor='black', alpha=0.7)
        for i in range(len(n)):
            if n[i] > 0:
                plt.text((bins[i] + bins[i+1])/2, n[i] + 0.2, int(n[i]), ha='center')
        plt.show()


# ---------- 主程序（菜单交互）----------
def main():
    manager = StudentManager()
    while True:
        print("\n========== 学生成绩管理系统 ==========")
        print("1. 添加学生")
        print("2. 删除学生")
        print("3. 修改成绩")
        print("4. 按学号查询")
        print("5. 显示所有学生（按成绩降序）")
        print("6. 统计信息")
        print("7. 绘制成绩分布图")
        print("0. 退出")
        choice = input("请输入操作编号：").strip()

        # 选择结构
        if choice == '1':
            try:
                stu_id = input("学号：").strip()
                name = input("姓名：").strip()
                score_str = input("成绩(0-100)：").strip()
                score = float(score_str)
                manager.add_student(stu_id, name, score)
            except ValueError as e:
                print(f"输入错误：{e}")
            except Exception as e:
                print(f"未知错误：{e}")

        elif choice == '2':
            stu_id = input("请输入要删除的学号：").strip()
            manager.delete_student(stu_id)

        elif choice == '3':
            try:
                stu_id = input("学号：").strip()
                new_score_str = input("新成绩(0-100)：").strip()
                new_score = float(new_score_str)
                manager.update_score(stu_id, new_score)
            except ValueError as e:
                print(f"输入错误：{e}")

        elif choice == '4':
            stu_id = input("学号：").strip()
            stu = manager.search_by_id(stu_id)
            if stu:
                print(f"查询结果：{stu}")
            else:
                print("未找到该学生。")

        elif choice == '5':
            students_sorted = manager.get_all_students_sorted(reverse=True)
            if not students_sorted:
                print("暂无学生数据。")
            else:
                print("\n学号\t姓名\t成绩")
                print("-" * 20)
                for stu in students_sorted:
                    print(stu)

        elif choice == '6':
            manager.show_statistics()

        elif choice == '7':
            try:
                manager.plot_score_histogram()
            except ImportError:
                print("绘图失败，请确保已安装matplotlib库 (pip install matplotlib)")
            except Exception as e:
                print(f"绘图时发生错误：{e}")

        elif choice == '0':
            print("感谢使用，再见！")
            break

        else:
            print("无效选项，请重新输入。")


if __name__ == "__main__":
    main()