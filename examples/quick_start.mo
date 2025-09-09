# 模块引用
using snaps

# 变量不可变，不可重复声明，类型自动推导
a = 1 # int 
b = [1, 2, 3] # [int]
c = "foo" # str

# 强制类型
int f = 1.0 # int

# 定义函数
power x y = x ^ y # (num a, b) => a -> b -> a $ b
unsigned f = {
    g: x, y = f(abs(x), y)
    g
} # (num a) => (a -> b -> c) -> a -> b -> c

# 基本类型
# - function
# - str
# - type
# - num:
#   - bool
#   - int
#   - float
# a $ b表示两种类型的最小共同父类，如num $ int = num