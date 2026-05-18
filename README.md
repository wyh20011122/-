技术方案：基于 PRD 的自动化测试与缺陷生成插件
1. 项目目标
本项目旨在开发一个自动化测试插件，使其能够从 PRD 文档出发，自动完成需求分析、测试用例设计、测试执行、测试报告生成以及缺陷记录生成。当前阶段先实现一个最小可运行 Demo，以 React + Flask 登录注册系统作为被测系统，通过故意保留用户名长度校验缺失的问题，验证插件从 PRD 到 bug 发现的完整闭环。
2. 当前 Demo 技术架构
当前 Demo 采用前后端分离结构：
login-demo/
├── PRD.md
├── backend/
│   └── app.py
├── frontend/
│   └── src/
└── test_report.md
后端使用 Flask 提供注册和登录接口。前端使用 React 构建简单登录注册页面。PRD.md 作为独立需求文档，描述系统应满足的业务规则，例如“用户名长度必须大于 6 位”。自动化测试脚本读取 PRD，并根据规则生成测试用例，然后调用后端接口进行验证。
当前故意植入的 bug 是：PRD 要求用户名长度必须大于 6 位，但 Flask 后端没有实现用户名长度校验，导致短用户名仍然可以注册成功。
3. 核心流程设计
整体流程如下：
PRD 文档输入
    ↓
需求规则提取
    ↓
测试点识别
    ↓
测试用例生成
    ↓
接口测试执行
    ↓
实际结果与预期结果对比
    ↓
生成测试报告
    ↓
自动生成 bug 信息
在当前 Demo 中，插件雏形已经完成以下能力：
读取 PRD.md
生成用户名长度测试用例
调用 /register 接口
判断 expected status 与 actual status
生成 test_report.md
输出 bug title、severity、description、expected result、actual result
4. 当前实现说明
当前系统中，PRD 规定：
Username length must be greater than 6 characters.
测试脚本生成负向测试用例：
{
  "username": "abc123",
  "password": "12345678"
}
根据 PRD，用户名 abc123 长度不大于 6，因此注册应失败，预期返回状态码为 400。
但实际接口返回：
{
  "message": "Register success"
}
状态码为 200，因此系统自动判断该测试失败，并生成 bug：
Bug Title: Registration allows username shorter than required length
Severity: High
Expected Result: Registration should fail
Actual Result: Registration succeeded
5. 后续插件模块规划
5.1 PRD 解析模块
该模块负责读取并理解 PRD 文档内容。后续可以支持 Markdown、Word、PDF 等格式。核心功能包括：
提取功能点
提取业务规则
识别输入字段
识别校验条件
识别异常场景
识别接口行为
后续可接入 LLM，使插件能够自动从自然语言需求中提取结构化规则，例如：
{
  "field": "username",
  "rule": "length > 6",
  "scenario": "registration",
  "expected_behavior": "reject invalid input"
}
5.2 需求分析模块
该模块将 PRD 中的自然语言需求转换成可测试的需求点。比如：
用户名不能为空
用户名长度必须大于 6 位
密码长度必须大于 6 位
登录成功后返回欢迎信息
会被转换成：
注册-用户名为空-应失败
注册-用户名长度不足-应失败
注册-密码长度不足-应失败
登录-正确账号密码-应成功
5.3 测试用例生成模块
该模块根据需求点自动生成测试用例，包括正向用例和负向用例。
例如用户名长度规则可以生成：
用户名为空
用户名长度小于等于 6
用户名长度大于 6
用户名重复
每条用例包含：
case_id
case_title
input_data
expected_status
expected_response
priority
test_type
5.4 测试执行模块
该模块负责执行测试用例。当前 Demo 主要通过 Python requests 调用 Flask 接口。后续可以扩展为：
API 测试
UI 自动化测试
数据库校验
Mock 数据测试
端到端测试
对于 API 测试，可支持 GET、POST、PUT、DELETE 等请求方法，并支持 header、body、query params 等配置。
5.5 结果比对模块
该模块负责将实际结果与预期结果进行比较。当前主要比较 HTTP status code，后续需要增强为：
状态码比对
返回字段比对
错误信息比对
数据类型比对
业务语义比对
数据库状态比对
这样可以避免“假通过”问题。例如返回 400 不一定代表测试通过，还要判断错误原因是否与 PRD 一致。
5.6 测试报告模块
该模块负责生成测试报告。报告内容包括：
测试时间
PRD 来源
测试用例总数
通过数量
失败数量
失败原因
接口响应
自动生成的 bug 信息
后续可以支持多种格式：
Markdown
HTML
JSON
PDF
Excel
5.7 Bug 生成模块
当前 Demo 已经可以自动生成 bug 文本。后续如果接入公司系统，可以自动调用 Jira、禅道、飞书项目、GitHub Issues 等平台接口创建 bug。
bug 信息包括：
Bug Title
Severity
Priority
Environment
Steps to Reproduce
Expected Result
Actual Result
Related PRD Rule
Related Test Case
5.8 插件交互模块
后续如果做成 VSCode 插件，可以提供以下功能：
选择 PRD 文件
选择被测接口配置
一键生成测试用例
一键执行测试
查看测试报告
查看自动生成 bug
导出测试结果
VSCode 插件界面可以包括：
PRD Analyzer
Test Case Generator
Test Runner
Report Viewer
Bug List
6. 后续迭代路线
第一阶段：最小可运行 Demo
React + Flask 登录注册系统
PRD.md
手动规则测试脚本
自动生成 test_report.md
自动输出 bug
当前已完成。
第二阶段：规则自动提取
使用 LLM 从 PRD 中提取规则
自动生成结构化需求
自动生成多条测试用例
减少人工写死逻辑
第三阶段：测试能力增强
支持多个接口
支持正向和负向测试
支持响应内容校验
支持测试数据自动生成
支持测试前清理数据
第四阶段：报告与 bug 系统对接
生成 HTML / PDF 报告
自动创建 bug
支持 Jira / GitHub Issues / 禅道
记录测试历史
第五阶段：VSCode 插件化
开发 VSCode 插件界面
支持选择 PRD
支持一键运行测试
支持报告预览
支持 bug 列表展示
7. 当前阶段总结
当前 Demo 已经完成了一个基础闭环：
PRD → 测试用例 → 测试执行 → 测试报告 → bug 生成
虽然当前版本仍是规则写死的原型，但它已经验证了核心可行性。后续重点是将 PRD 解析和测试用例生成从人工规则升级为 LLM 驱动，使插件能够真正自动理解需求并发现实现与需求之间的不一致。
## 当前 Demo 已完成流程

[x] PRD 文档读取

[x] 规则抽取

[x] 自动测试用例生成

[x] 测试执行

[x] 缺陷自动识别

[ ] 测试报告自动生成

[ ] Bug 自动创建

[ ] UI 自动测试

[ ] LLM 需求分析

[ ] VSCode 插件化
