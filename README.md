# morethon

`morethon` 是一个实验性的脚本语言解释器（Python 实现）。

## 安装

```bash
pip install morethon
```

## 命令行用法

```bash
# 执行脚本
mo examples/test.mo
```

> 当前实现会输出“最后一个表达式/变量”的值。

---

## 当前版本语法（按解释器实现）

下面是**当前可用语法**的完整示例集合（可直接作为参考模板）：

```mo
# 1) using 语句（当前会被解析并消费，但不导入外部模块能力）
using snaps tools

# 2) 注释
# 单行注释以 # 开头

# 3) 字面量
i = 1            # INT
f = 2.5          # FLOAT
t = True         # BOOL
u = False        # BOOL
s = "hello"      # STR

# 4) 显式类型约束（强制类型）
int i2 = 10
float f2 = 3
bool b2 = False
str s2 = "morethon"

# 5) 表达式与运算符（左结合）
add = 1 + 2
sub = 7 - 3
mul = 2 * 4
div = 7 / 2
pow = 2 ^ 3
mix = (1 + 2) * (3 + 4)

# 6) 列表
empty = []
arr = [1, 2, 3]
nested = [1, [2, 3], 4]

# 7) 列表索引
x = arr[0]
y = nested[1][0]

# 8) 函数定义（柯里化）
# 单参数函数
inc x = x + 1
v1 = inc 41

# 多参数函数（实质是连续单参数调用）
power x y = x ^ y
v2 = power 2 5

# 9) 函数实参可为：变量 / 字面量 / 括号表达式 / 大括号块 / 列表
id x = x
v3 = id i
v4 = id "ok"
v5 = id (1 + 2)
v6 = id { 
     a = 1
     b = a + 1
     b 
}
v7 = id [7, 8, 9]

# 10) 大括号块（局部作用域，返回块内最后一个值）
blk = {
  a = 10
  b = a + 2
  b
}

# 11) 组合示例
final = power (inc 2) 3
```

---

## 语法说明（实现细节）

- 变量不可重复定义（同一作用域内二次赋值会报错）。
- 函数调用使用空格分隔参数，例如 `power 2 3`。
- 列表索引支持链式形式，例如 `nested[1][0]`。
- 支持的算术运算符：`+ - * / ^`。
- 当前仓库中的 `using` 语句仅语法上可通过，尚未实现真实模块导入行为。

## 项目地址

- GitHub: https://github.com/Chitaoji/morethon/
- PyPI: https://pypi.org/project/morethon/

## License

BSD 3-Clause License.
