# DriveScenarioDiff

> Catch regressions before they hit the road.  
> 在上路前，先抓住每一次退化。

DriveScenarioDiff is a lightweight open-source tool for **autonomous driving regression analysis**.
It compares two run results (baseline vs candidate), aligns scenarios, computes metric deltas, and generates a simple report for quick debugging.

DriveScenarioDiff 是一个轻量开源工具，用于**自动驾驶回归分析**。
它比较两个版本的运行结果（基线 vs 新版），对齐场景，计算指标差异，并生成报告帮助快速定位问题。

---

## ✨ Features / 功能

- Scenario-level alignment (`scenario_id`) / 场景级对齐
- Delta metrics between two runs / 两次运行的指标差异计算
- Regression detection (pass -> fail) / 退化检测（通过->失败）
- Top-K worst scenarios ranking / 最差场景 Top-K 排序
- JSON summary output / JSON 汇总输出
- CI-friendly regression gate / 可用于 CI 回归卡口

---

## 📦 Installation / 安装

```bash
# Python 3.9+
pip install -e .
```

---

## 🚀 Quick Start / 快速开始

```bash
drivediff compare examples/runA_sample.json examples/runB_sample.json -o outputs
```

Output:
- `outputs/summary.json`
- terminal summary

---

## 📄 Input Format / 输入格式

Each run file is a JSON with scenario records:

```json
{
  "run_id": "v1.0.0",
  "timestamp": "2026-05-06T12:00:00Z",
  "scenarios": [
    {
      "scenario_id": "scene_001",
      "passed": true,
      "metrics": {
        "collision_count": 0,
        "min_ttc": 2.3,
        "max_lateral_error": 0.22,
        "comfort_jerk_rms": 1.15
      },
      "tags": ["urban", "pedestrian_crossing"]
    }
  ]
}
```

See `docs/schema.json` for full schema.

---

## 🧠 Regression Rule (v0)

A scenario is considered **regressed** when:
- baseline `passed=true` and candidate `passed=false`, OR
- optional thresholds are crossed (`--thresholds` config)

Use CI gate:

```bash
drivediff compare examples/runA_sample.json examples/runB_sample.json --fail-on-regression
```

If regressions are found, exit code is `2`.

---

## 🛣️ Roadmap / 路线图

- [ ] HTML report
- [ ] Metric plugin system
- [ ] ROS bag adapter
- [ ] CARLA result adapter
- [ ] GitHub PR comment bot

---

## 🤝 Contributing / 贡献指南

Issues and PRs are welcome!  
欢迎提交 Issue 和 PR。

Please include:
- sample input
- expected output
- reproducible command

---

## ⚖️ License / 许可证

MIT (recommended) or Apache-2.0.
