# Web Test Project

基于 Playwright + pytest 的 Web 自动化测试项目

## 技术栈

- Python 3.12
- Playwright
- pytest

## 项目结构

```
web_test_project/
├── data/           # 测试数据
├── tests/          # 测试代码
│   └── pages/      # Page Object
├── conftest.py     # pytest 配置
├── pytest.ini      # 配置文件
└── requirements.txt
```

## 运行测试

```bash
# 运行所有测试
pytest

# 可视化运行
pytest --headed

# 运行指定测试
pytest tests/test_day4.py -v
```

## 学习进度

### Day 1-3：基础入门
- [x] 环境搭建
- [x] 元素定位
- [x] expect 断言

### Day 4-6：核心技能
- [x] Page Object Model (POM)
- [x] 数据驱动测试
- [x] 高级交互（多窗口）

### Day 7：项目优化
- [x] 项目结构整理
- [x] 配置文件完善
- [ ] README 完善
