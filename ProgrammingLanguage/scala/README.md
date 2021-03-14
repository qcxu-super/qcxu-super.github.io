# 1. 变量

## 1.1 基本数据类型

```scala
var age: Int = 10 // default
var sal: Double = 10.9 // default
var name: String = "Tom"
var ispass: Boolean = true
var score: Float = 70.9f
println(s"${age} ${ispass}")
println(age.isInstanceOf[Int]) // true
```

## 1.2 var & val

var是可变变量，val不可变

```scala
// var: can change
var age = 10
age = 30

// val: cannot change
val num = 30
num = 40 // error
```

## 1.3 Nothing

常用于异常值判断，无正常返回值

```scala
def sayHello: Nothing {
	throw new Exception('error')
}
```


## 1.4 数据类型转换

```
// AnyVal
var num: Int = 10
num.toString

// 数据类型强制：可转换为容量更小的数据类型
var num: Int = 2.7.toInt

// toString
var d1 = 1.2
var s1 = d1 + ""

// string to others
s1.toInt
s1.toFloat
```

# 2. 运算符

## 2.1 算数运算符

- 除法

```scala
var r1: Int = 10/3  //3
var r2: Double = 10/3 //3.0
var r3: Double = 10.0/3 //3.33333
```

- mod

```scala
println(10%3) //1
println(-10%3) //(-10)-(-3)*3=-1
println(-10%-3) //(-10)-(3)*(-3)=-1
```

- ++ and --

```scala
var num1 = 10
num1 += 1
num1 -= 1
```

## 2.2 赋值运算符

```scala
C = A + B
C += A
```

## 2.3 比较运算符

```scala
println(a > b)
println(a != b)
var flag: Boolean = a==b //true or false
var res = if(a > b) a else b
```

## 2.4 逻辑运算符

```scala
A && B
A || B
!(A && B)
```

## 2.5 位运算符

```scala
a & b
a | b
a ^ b
```

# 3. 流程控制