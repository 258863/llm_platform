# Contributing to LLM Platform

感谢您对LLM Platform项目的关注！我们欢迎任何形式的贡献，包括但不限于：

- 提交bug报告
- 提出新功能建议
- 改进文档
- 提交代码修复
- 优化性能
- 添加测试用例

## 开发环境设置

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/llm_platform.git
cd llm_platform
```

2. 创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
pip install -e .
```

## 开发流程

1. 创建新的分支：
```bash
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/your-fix-name
```

2. 进行修改并提交：
```bash
git add .
git commit -m "描述你的修改"
```

3. 推送到远程仓库：
```bash
git push origin feature/your-feature-name
```

4. 创建Pull Request

## 代码规范

- 使用Python 3.8+语法
- 遵循PEP 8规范
- 使用类型注解
- 编写详细的文档字符串
- 添加单元测试

### 代码格式化

我们使用以下工具来保持代码质量：

```bash
# 格式化代码
make format

# 类型检查
make type-check

# 代码检查
make lint

# 运行测试
make test
```

## 提交信息规范

提交信息应该遵循以下格式：

```
<type>(<scope>): <subject>

<body>

<footer>
```

类型（type）：
- feat: 新功能
- fix: 修复bug
- docs: 文档更新
- style: 代码格式修改
- refactor: 代码重构
- test: 测试相关
- chore: 构建过程或辅助工具的变动

示例：
```
feat(api): add new endpoint for model management

- Add POST /api/v1/models endpoint
- Add model validation
- Add error handling

Closes #123
```

## 测试

- 为新功能编写单元测试
- 确保所有测试通过
- 保持测试覆盖率

运行测试：
```bash
make test
```

## 文档

- 更新README.md
- 添加/更新API文档
- 添加/更新注释
- 更新CHANGELOG.md

## 发布流程

1. 更新版本号
2. 更新CHANGELOG.md
3. 创建发布标签
4. 构建并发布Docker镜像

## 问题反馈

如果您发现任何问题或有改进建议，请：

1. 检查是否已有相关issue
2. 如果没有，创建新的issue
3. 提供详细的描述和复现步骤
4. 添加相关的日志和截图

## 行为准则

请遵循我们的行为准则，保持专业和友善的交流环境。

## 许可证

通过提交代码，您同意将您的贡献按照项目的许可证进行授权。 