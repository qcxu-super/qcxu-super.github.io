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

## 3.1 顺序控制

## 3.2 分支控制

### 单分支

```scala
import scala.io._

val age = StdIn.readInt()
if (age > 18) {
    println("未成年")
}
```

### 双分支

- if ... else ...

```scala
val age = 7
if (age > 18) {
    println("未成年")
} else {
    println("成年")
}
```

- if else 仅一行
```scala
var res = if (a > b) a else b
```

### 多分支

```scala
val  score = StdIn.readDouble()
if (score == 100) {
    println("奖励一辆车")
} else if (score > 80) {
    println("奖励iphone")
} else {
    println("没有任何奖励")
}
```

### switch模式匹配

match-case

## 3.3 循环控制

### for循环

- to：前闭后闭

```scala
for (i <- 1 to 3) {
    println(i+"") //1,2,3
}

var list = List("hello",10,30,"tom")
for (item <- list) {
    println("item = "+item)
}
```

- until：前闭后开

```scala
for (i <- 1 until 3) {
    println(i+"") //1,2
}
```

- 循环守卫，类似于continue

```scala
for (i <- 1 to 3 if i != 2) {
    println(i+"") //1,3
}

for (i <- 1 to 3) {
    if (i != 2) {
        println(i+"") //1,3
    }
}
```

- 引入变量

```scala
for (i <- 1 to 3; j = 4 - i) {
    println(j+"") //3,2,1
}

for (i <- 1 to 3) {
    j = 4 - i
    println(j+"") //3,2,1
}
```

- 嵌套循环

```scala
for (i <- 1 to 3; j <- 1 to 3) {
    println("i = " + i + ", j = " + j)
}

for (i <- 1 to 3) {
    for (j <- 1 to 3) {
        println("i = " + i + ", j = " + j)
    }
}


for {i <- 1 to 3
     j <- 1 to 3} {
         println("i = " + i + ", j = " + j)
     }
```

- 循环返回值

```scala
val res = for (i <- 1 to 3) yield i * 2
println(res) //Vector(2,4,6)

val res = for (i <- 1 to 4) yield {
    if (i % 2 == 0) {
        i
    } else {
        -1
    }
}
println(res) //-1,2,-1,4
```

- 控制步长

```scala
for (i <- Range(1,5,2)) {
    println(i+"") //1,3
}

for (i <- 1 to 5; i % 2 == 1) {
    println(i+"") //1,3
}
```

### 循环中断

breakable 是个高阶函数，就是说，可以接受函数(op)的函数。breakable()，小括号变大括号

```scala
import util.control.Breaks._
var n = 10
breakable {
    while (n <= 20) {
        n += 1
        if (n == 18) {
            break() //break函数化
        }
    }
}
```


# 4. 集合,数据结构

```scala
import scala.collection.immutable //不可变集合，长度不可变，内容可变
import scala.collection.mutable //可变集合，如ArrayList
```

seq, set, map

## 4.1 Array 定长数组

### 固定类型

```scala
val arr01 = new Array[Int](4)
println(arr01.length) //4

arr01(1) = 8
println(arr01(1)) //8

for (x <- arr01) {
    println(x) //0,8,0,0
}
```

### object.Array.apply()

```scala
var arr02 = Array(1,3,"tom")
for (x <- arr02) {
    println(x)
}
for (index <- 0 until arr02.length) {
    printf("arr02[%d]=%s",index,arr02(index)+"\t")
}
```

## 4.2 ArrayBuffer 变长数组

```scala
import scala.collection.mutable.ArrayBuffer
```

### 创建

```scala
val arr2 = ArrayBuffer[Int]() //不带值，空的
val arr01 = ArrayBuffer[Any](3,2,5) //带值
```

### 查询

```scala
println(arr01(1)) //2
for (i <- arr01) {
    println(i) //3,2,5
}
println(arr01.length) //3
println(arr01.hashcode()) //110266112
```

### 添加 append

```scala
arr01.append(90.0,13) //3,2,5,90.0,13
println(arr01.hashcode()) //-70025354,可变
```

### 修改

```scala
arr01(1) = 89
for (i <- arr01) {
    println(i)
}
```

### 删除 remove

```scala
arr01.remove(0)
for (i <- arr01) {
    println(i)
}
println(arr01.length)
```

## 4.3 Map

- 散列表：数组+链表
- 不可变的Map是有序的，可变的Map是无序的（一般都用可变的, scala.collection.mutable.Map）

```
import scala.collection.mutable.Map
```

### 创建

```scala
// 默认map是不可变的 immutable.Map，有序
val map1 = Map("Alice"->10, "Bob"->20, "Kotlin"->"北京")

// 构造可变map，无序
val map2 = mutable.Map("Alice"->10, "Bob"->20, "Kotlin"->"北京")

// 创建空映射
val map3 = new scala.collection.mutable.HashMap[String,Int]

// 对偶元组
val map4 = mutable.Map(("Alice",10),("Bob",20),("Kotlin","北京"))
```

### 取数

```scala
// key不存在时，会抛出异常
val value1 = map4("Alice")

// 用if防止异常
if (map4.contains("A")) {
    println(map4("A"))
} else {
    println("key not exists")
}

// map.get(key) --> Some(value)/None
// Some(value).get --> value
// None就不能get了
println(map4.get("Alice")) //Some(10)
println(map4.get("Alice").get) //10
map4.get("Alice") match {
    case Some(x) => x
    case None =>
}

// map.getOrElse
println(map4.getOrElse("Alice","default_value")) //10
println(map4.getOrElse("A","default_value")) //default_value

```

### 更新

```scala
map4("AA") = 20
map4 += ("D"->4) //如果添加的key已存在，则更新value
map4 += ("EE"->1, "FF"->3)
map4 -= ("AA") //key不存在不会报错
map4 -= ("A","B")
```

### 遍历

```scala
val map6 = mutable.Map(("A",1),("B","beijing"),("C",3))

for ((k,v) <- map6) println(k + " is mapping to " + v) //A is mapping to 1, ...

for (k <- map6.keys) println(k) //A,C,B

for (v <- map6.values) println(v) //1,3,beijing

for (v <- map6) println(v + "key=" + v._1 + ", val=" + v._2) //(A,1) key=A, val=1 ,....
```

# 5. Map映射操作：集合元素映射处理

### 传统方法

```scala
val list1 = List(3,5,7)
val list2 = List[Int]()
for (item <- list1) {
    list2 = list2 :+ item * 2
}
println(list2) //List(6,10,14)
```

### 高阶函数，函数的函数

```scala
// f(n1)，输入是Double，输出是Double。test是高阶函数

def test(f: Double => Double, n1: Double) = {
    f(n1)
}
def sum2(d: Double): Double = {
    d + d
}
test(sum2(3.5)) //7
```

```scala
def test2(f:() => Unit) = {
    f()
}
def sayOk() = {
    println("sayOKKK")
}
test2(sayOk) //sayOKKKK
```

### Map

```scala
val list1 = List(3,5,7)
def f1(n1: Int): Int = {
    2 * n1
}
val list2 = list1.map(f1)
println(list2) //6,10,14
```

map机制

```scala
def map(f: Int => Int): List[Int] = {
    for (item <- this.list1) {
        list2 = list2 :+ f(item)
    }
}
```

# 6. 模式匹配

```scala
val n1 = 20
val n2 = 10
val res = 0

var oper = '#'

oper match {
    case '+' => res = n1 + n2
    case '-' => res = n1 - n2
    case '*' => res = n1 * n2
    case '/' => res = n1 / n2
    case _ => println('oper error') //oper error
}

println("res = " + res) //0
```

```scala
oper = '+'

oper match {
    case '+' => {
        res = n1 + n2 //30
        println("ok") //ok
    }
    case _ if oper=='/' => n1 / n2
    case _ println("others")
}
```

```scala
val res = oper match {
    case '+' => n1 + n2 //取匹配到的最后一个值
    case _ => println("others")
}
println(res) //20
```