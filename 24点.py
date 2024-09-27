import random
import operator
import itertools
import re  # 用于从输入中提取数字

# 定义运算符
ops = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
}

# 优先级比较函数，决定是否需要添加括号
def needs_parentheses(prev_op, current_op):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    return precedence[current_op] > precedence[prev_op]

# 将数字和运算符转化为带括号的表达式
def format_expression(operators, nums):
    expression = str(nums[0])
    for i in range(1, len(nums)):
        if i > 1 and needs_parentheses(operators[i-2], operators[i-1]):
            expression = f"({expression})"
        expression += f" {operators[i-1]} {nums[i]}"
    return expression

# 生成随机数字
def generate_numbers(count, min_number, max_number):
    return [random.randint(min_number, max_number) for _ in range(count)]

# 根据运算符生成表达式并检查是否满足等式，确保数字不重复使用
def find_solution(nums):
    num_operators = len(nums) - 1
    for operators in itertools.product(ops.keys(), repeat=num_operators):
        # 生成所有可能的数字排列，确保每个数字只使用一次
        for perm_nums in itertools.permutations(nums):
            try:
                # 构造完整的表达式，保证每个数字只用一次
                expression = str(perm_nums[0])
                for i in range(len(operators)):
                    expression += f" {operators[i]} {perm_nums[i + 1]}"
                
                # 计算表达式结果
                if eval(expression):  # 如果表达式有效
                    return expression
            except ZeroDivisionError:
                continue  # 避免除以0的情况
            except:
                continue  # 忽略其他异常

    return None

# 确保生成的数字集合有解，且每个数字只能用一次
def generate_valid_numbers(count, min_number, max_number):
    while True:
        numbers = generate_numbers(count, min_number, max_number)
        solution = find_solution(numbers)
        if solution:
            return numbers, solution

# 从用户输入中提取使用的数字（包括括号和运算符）
def extract_numbers_from_input(user_input):
    # 使用正则表达式提取所有数字，支持负数和浮点数
    return [float(num) for num in re.findall(r'-?\d+\.?\d*', user_input)]

# 游戏主循环
def main():
    print("欢迎来到互动数学计算游戏！")

    play_again = True
    while play_again:
        # 获取用户输入的数字数量
        try:
            num_count = int(input("请输入生成的数字个数 (例如，4): "))
            if num_count < 2:
                raise ValueError("数字个数至少为2。")
        except ValueError as e:
            print(f"输入错误: {e}")
            continue

        # 获取用户输入的数字范围
        try:
            min_number = int(input("请输入数字范围的最小值: "))
            max_number = int(input("请输入数字范围的最大值: "))
            if min_number > max_number:
                raise ValueError("最小值不能大于最大值。")
        except ValueError as e:
            print(f"输入错误: {e}")
            continue

        # 生成数字和对应的解
        numbers, solution = generate_valid_numbers(num_count, min_number, max_number)
        print("\n生成的数字是:", numbers)
        print("\n你可以使用以下运算符:")
        print(" '+' 进行加法")
        print(" '-' 进行减法")
        print(" '*' 进行乘法")
        print(" '/' 进行除法")
        print(" '==' 来判断两边是否相等 (例如，'3 + 2 == 5')\n")

        # 提供尝试次数
        attempts = 0
        max_attempts = 3
        while attempts < max_attempts:
            # 获取用户输入的等式
            user_equation = input("请输入你使用给定数字和运算符的等式: ")

            # 检查用户是否使用了所有生成的数字
            user_numbers = extract_numbers_from_input(user_equation)
            if sorted(user_numbers) != sorted(numbers):
                print(f"你必须使用所有生成的数字: {numbers}。请重试。")
                continue

            # 检查用户输入的等式是否正确
            try:
                if eval(user_equation):
                    print("恭喜你，等式正确！")
                    break
                else:
                    print("等式不正确，请重试。")
            except Exception as e:
                print(f"等式错误: {e}。请重试。")

            attempts += 1
            if attempts == max_attempts:
                show_hint = input("你想要提示或答案吗？ (yes/no): ").strip().lower()
                if show_hint == 'yes':
                    print(f"正确的等式是: {solution}")

        # 询问用户是否继续游戏
        play_again_input = input("\n你想再玩一次吗？ (yes/no): ").strip().lower()
        play_again = play_again_input == 'yes'

if __name__ == "__main__":
    main()