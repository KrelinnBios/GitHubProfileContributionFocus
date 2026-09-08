# AGENTS.md

本文件适用于整个仓库，作为 AI 编码代理修改本项目时的项目规范。除非用户另有要求，使用中文回复和说明。

## 项目概览

GitHub Profile Contribution Focus 是一个基于 Python 标准库实现的 composite GitHub Action，用于读取 GitHub 个人主页「Last year」范围内的可见贡献，按仓库和月份生成主题自适应 SVG 时间带，并维护 README 中的版本化图片引用。

- `action.yml`：Action 输入、输出和执行入口。
- `src/generate.py`：命令行入口与整体生成流程。
- `src/contribution_focus/github.py`：GitHub GraphQL API 查询与贡献数据读取。
- `src/contribution_focus/dates.py`：统计区间和月份切分。
- `src/contribution_focus/aggregate.py`：仓库贡献汇总、排序和 `Other` 归并。
- `src/contribution_focus/config.py`：配置加载与默认值。
- `src/contribution_focus/chart.py`：SVG 时间带布局与渲染。
- `src/contribution_focus/colors.py`：行颜色与主题颜色规则。
- `src/contribution_focus/output.py`：版本化文件名、README 引用更新与旧图清理。
- `tests/`：日期、聚合、图表、配置和输出行为测试。
- `examples/`：配置、工作流和预览示例。

项目不依赖第三方 Python 包，保持可直接运行于 GitHub 托管 runner 的轻量实现。

## 开始任务前

- 先读取与任务直接相关的模块、测试和示例，不根据 README 描述或文件名猜测实际实现。
- 修改 Action 输入、输出或默认值时，同时检查 `action.yml`、配置模块、示例工作流和三种语言 README。
- 修改统计区间、GraphQL 查询、归属规则或 `Other` 逻辑时，先核对 GitHub「Last year」口径和现有测试。
- 修改 SVG 布局、主题或颜色时，先检查 `chart.py`、`colors.py` 和预览示例。
- 优先做最小、可验证的改动，不为了局部需求引入第三方依赖、框架或无关重构。

## 修改原则

- 保持 Python 标准库实现，除非用户明确要求改变依赖策略。
- 统计范围继续以 GitHub `contributionsCollection` 的默认起止时间为基准，保持与个人主页「Last year」口径一致；不要自行改成固定 12 个完整自然月。
- Commit、Issue、Pull Request、Review 和仓库创建等可安全归属到仓库的贡献进入对应仓库；无法安全归属的贡献进入 `Other`。
- 不泄露不可见私有仓库名称。私有或其他无法安全归属的数据只能按允许的聚合口径进入 `Other`。
- 排名继续按整个统计范围内的总贡献量决定，默认展示贡献最高的 5 个仓库，其余仓库逐月归并为 `Other`。
- 图中的 `Contrib` 是本项目定义的贡献类型汇总，不等同于仓库首页 commits 总数；不要混用两种口径。
- 月度查询和聚合必须避免因分页或日期边界导致漏计、重复计数或跨月错位。
- SVG 必须继续通过 `prefers-color-scheme` 适配 GitHub 浅色与深色模式。
- 不提交 Token、GraphQL 原始响应、私有仓库信息或其他敏感调试数据。

## 输出与缓存约束

- 生成文件使用内容摘要形成版本化文件名，以绕过 GitHub 对同名图片的缓存。
- `output.py` 负责更新 README 图片引用并清理旧版本文件；修改输出逻辑时必须保证新 SVG 路径、README 引用和旧图清理一致。
- 数据和配置没有变化时，应保持幂等，避免无意义地生成新文件或让 `changed` 变为 `true`。
- 首次运行仍需兼容 README 中未版本化的占位路径，例如 `./contribution-focus.svg`。
- `action.yml` 的 `image` 与 `changed` 输出语义不得与实际生成逻辑漂移。

## 验证

代码修改至少运行：

```bash
python -m unittest discover -s tests -v
```

修改图表、日期或聚合逻辑时，额外运行：

```bash
python examples/generate_preview.py
```

并确认：

- 统计区间与 GitHub「Last year」范围一致，首尾不完整月份不会被错误补齐或截断。
- 前 5 个仓库的排序基于整个统计周期总贡献量。
- 其他仓库与无法安全归属的贡献按月进入 `Other`。
- 月份顺序、贡献总数和色块强度没有错位。
- 浅色与深色主题文字、轨道和色块均可辨认。
- README 引用、版本化文件名和旧图清理符合预期。

纯文档修改无需运行测试，但应检查三种语言 README 的事实是否仍一致。

## 文档同步

- `README.md`、`README.zh-TW.md` 和 `README.en.md` 面向使用者；`AGENTS.md` 只记录编码代理修改项目时需要遵守的规则。
- 三种语言 README 的结构、Action 输入输出、配置字段、统计口径、隐私说明和使用步骤保持一致。
- 修改 `action.yml`、GraphQL 统计口径、配置字段、仓库归并规则、颜色规则、版本化文件行为或隐私边界时，检查三种语言 README 和 `examples/` 是否需要同步。
- 不把实现无法保证的贡献归属、私有数据可见性或 GitHub 内部统计细节写成确定事实。

## 提交约定

- 一个提交聚焦一个明确主题。
- 提交信息简短说明实际结果。
- 不提交测试临时文件、GraphQL 响应、令牌、私有仓库数据、本地配置或与任务无关的生成物。
- 工作区已有其他修改时，只处理并提交本次任务涉及的内容。