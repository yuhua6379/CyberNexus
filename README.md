# CyberNexus

我们在构建一个虚拟世界，借助大语言模型的“自然语言处理能力”和有限的"推理能力"来驱动整个世界中角色们的运作。

角色被赋予了思考、记忆的能力，可以和世界中的其他角色进行交流。你可以在 [这个聊天记录](./showcase/sample_conversation.md)
中看到基础的角色之间是如何“活过来”为了自己的目的进行交流的。

# 运作原理

## 关键机制 (toDo)

角色：

1. 规划
2. 交互
2. 记忆
2. 反思

世界：

1. 底层循环
2. 大循环
3. 资源管理

## 运转逻辑

![运转逻辑](./showcase/howitworks.png)

# 技术架构 (toDo)
1.Bot的模块结构，下面这张图解释了机器人的模块结构
![模块结构](D:\PycharmProjects\CyberNexus\showcase\modules.png)

2.记忆的处理方法，下面这张图解释了机器人的记忆模块是如何运作的
![记忆处理](D:\PycharmProjects\CyberNexus\showcase\memory.png)

3.如何构建一个能感知世界且实时自驱动的机器人？
![自驱动机器人](D:\PycharmProjects\CyberNexus\showcase\selfdrive_bot.png)

# 功能清单

- [x] 世界的基础运转能力
- [x] 创建角色，以及对应的 bot
- [x] 角色的记忆和反省能力
- [x] 与角色聊天
- [x] 两个角色之间互动聊天
- [ ] 角色察觉周围环境的能力 (Tools)
- [ ] 角色思考决策的能力
- [ ] 虚拟社区构建，社区资源设置和管理
- [ ] 社区角色之间的沟通交互，世界运作
- [ ] 可视化：角色交互和资源使用
- [ ] 角色的虚拟形象
