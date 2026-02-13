# morethon
Interpreter for morethon language.

## Installation
```sh
$ pip install morethon
```

## Requirements
```txt
click
```
### Usage
```py
mo # 激活morethon环境
```
### Morethon语法定义
```mo
require snaps # 引用模块
snaps::open # 用::调用模块中的变量

using snaps # 直接引用模块内全部变量

# 变量不可变，不可重复声明
# 变量名可以包含字母、数字、下划线（_）、点（.），必须以字母或下划线开头

# 类型自动推导
avg = （1.0 + 2.0 + 4.0） / 2 # float
mid = 2 # int

# 强制类型转换
int a = 1.0 # int
float b = 1 # float

# 类型：
# int, float, bool, num, str
# num 包含 float, int两类，int包含 bool
# a & b 为类型的最小父集，如 int & int is int，int & float is num, num & int is num


# 定义函数类型（没有实际作用，相当于注释）
abs x := (num a) => a -> a 

# 定义函数
power: x, y = x ^ y # (num a, b) => a -> b -> a & b 
unsigned: f = {
     g: x, y = f(abs(x), y)
     g
} ＃ (num a, b, c) => (a -> b -> c) -> (a -> b -> c)
c = unsigned power a b

```
## See Also
### Github repository
* https://github.com/Chitaoji/morethon/

### PyPI project
* https://pypi.org/project/morethon/

## License
This project falls under the BSD 3-Clause License.

## History
### v0.0.0
* Initial release.