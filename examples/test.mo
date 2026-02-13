# 语句导入（当前解析器会消费该语句）
using snaps

# 强制类型声明
int i = 1
float f = 2.0
bool t = False

# 字面量
name = "morethon"
flag = True

# 算术与括号
sum = 1 + 2 * 3
mix = (1 + 2) * (3 + 4)

# 列表与索引
arr = [1, 2, 3, 4]
item = arr[2]
nested = [1, [2, 3], 4]

# 函数定义与调用（柯里化）
power x y = x ^ y
powv = power 2 3

double x = x + x
four = double 2

# 大括号表达式
inblock = { (1 + 2) * 5 }

# 综合列表
last = [i, item, powv]
