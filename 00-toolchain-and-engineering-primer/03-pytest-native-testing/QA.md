# 大厂高频面试题精讲 (03-pytest-native-testing)

---

### Q1: 为什么生产项目普遍选用 pytest 而非标准库自带的 unittest？assert 语句重写机制底层是如何工作的？

#### 🎯 面试官考点
- 测试工程化演进、Python 导入钩子（Import Hook）与 AST 字节码重写（Bytecode Instrumentation）。

#### 💡 满分回答模板
1. **编程范式与开发体验代差**：
   - `unittest` 是 Java JUnit 的历史移植产物，强制使用类继承，必须调用 `self.assertEqual` 等繁琐 API，样板代码极多；
   - `pytest` 推崇纯函数与 Pythonic 的原生 `assert` 语法，支持模块化插件生态，代码行数精简 50% 以上。
2. **AST 重写核心机制（The Magic Behind `assert`）**：
   - 如果直接在普通 Python 代码中运行 `assert a == b`，一旦失败只会抛出干瘪的 `AssertionError`，不带任何上下文值；
   - `pytest` 在运行时注册了一个 **PEP 302 模块导入钩子（Import Hook）**。当加载测试文件时，它动态解析源码的 AST 抽象语法树；
   - 它将原始的 `assert a == b` **重写为带有中间求值追踪的复杂 AST 分支代码**。当断言失败时，能精准分解并格式化打印出操作数 `a` 的当前值、`b` 的当前值以及详细的结构化差异比较（Diff）。

---

### Q2: 请详述 pytest 中的 fixture 机制。其作用域（Scope）有哪些？如何利用 yield 实现 Setup 与 Teardown？

#### 🎯 面试官考点
- 控制反转与依赖注入设计模式、测试生命周期控制与上下文清理保障。

#### 💡 满分回答模板
1. **核心定位：声明式依赖注入图**：
   - Fixture 彻底打破了传统面向对象中 `setUp` 必须和测试用例绑死在一个类中的缺陷，允许以函数形式定义可拔插、可复用的上下文资源。
2. **五大作用域生命周期（Scope）**：
   - **`function`（默认）**：每个测试函数执行前均创建一次，测试后立即销毁；
   - **`class`**：每个测试类仅实例化一次；
   - **`module`**：每个测试模块（`.py` 文件）共享一次；
   - **`package`**：跨子包共享一次；
   - **`session`**：整个测试套件生命周期只初始化一次（如：全局数据库容器、网络 Mock 服务）。
3. **基于 `yield` 的生成器优雅清理**：
   - Fixture 函数以 `yield` 语句为分水岭：
     ```python
     @pytest.fixture
     def db_conn():
         conn = connect_db()  # Setup: 初始化资源
         yield conn  # 注入测试用例供其使用
         conn.close()  # Teardown: 测试完毕后执行安全析构
     ```
   - 即使测试用例运行中途抛出异常崩溃，pytest 也会安全捕获并保证 `yield` 后方的代码必然得到执行。

---

### Q3: 在单元测试中，什么是 Mock？为什么应该尽量优先使用依赖注入而非猴子补丁（Monkey Patching）？

#### 🎯 面试官考点
- 测试金字塔、测试隔离原则、Monkey Patching 的隐蔽副作用与面向接口设计。

#### 💡 满分回答模板
1. **Mock 的核心定义**：
   - 模拟真实对象的行为，用预设好返回值或状态的假对象替代昂贵、不稳定或副作用不可逆的外部依赖（如：发送短信、调用支付接口、操作真实生产数据库）。
2. **为什么应警惕全局猴子补丁（Monkey Patching）**：
   - 猴子补丁通过直接在运行时动态篡改全局模块属性（如 `unittest.mock.patch('os.remove')`）；
   - **致命隐患**：如果测试用例中途崩溃且未正确恢复现场，全局被篡改的方法会污染后续所有测试用例，引发极难排查的幽灵连锁误报；且静态分析工具和 IDE 无法追踪动态补丁。
3. **推崇显式依赖注入（Dependency Injection via Protocols/Classes）**：
   - 业务代码设计为接收服务实例参数（如 `def send_receipt(mailer: MailerProtocol)`）；
   - 测试中只需直接构造一个内存版的 Fake/Mock 实例传参即可，无需污染全局命名空间，代码内聚性与可测性极高。
