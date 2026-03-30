# CPS Skills — 臨床問題解決技能 (Claude Code)

[![Claude Code](https://img.shields.io/badge/Claude_Code-Skill-blueviolet?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZD0iTTEyIDJDNi40OCAyIDIgNi40OCAyIDEyczQuNDggMTAgMTAgMTAgMTAtNC40OCAxMC0xMFMxNy41MiAyIDEyIDJ6IiBmaWxsPSJ3aGl0ZSIvPjwvc3ZnPg==)](https://claude.ai/claude-code)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://python.org)
[![License: Educational](https://img.shields.io/badge/License-Educational-green)](references.bib)
[![Chapters](https://img.shields.io/badge/章節-33%2F33_含LR-success)](.claude/skills/cps/references/chapters/)
[![Cases Tested](https://img.shields.io/badge/測試案例-2-informational)](case/)

> [!NOTE]
> [English](README.md) | [繁體中文](README.zh-TW.md)

一個 [Claude Code](https://claude.ai/claude-code) 技能，模擬 [NEJM 臨床問題解決](https://www.nejm.org/clinical-problem-solving) 的格式。給定病人情境，透過多角色診斷回合與貝氏似然比推理，結合教科書證據與文獻搜尋，產出結構化的最終診斷。

## 運作方式

```mermaid
graph LR
    A[SCENARIO.md] --> B[症狀對應]
    B --> C[第一回合：主治醫師]
    C --> D[第二回合：放射科 + 病理科]
    D --> E[第三回合：次專科]
    E --> F[第四回合：實證醫學]
    F --> G[第五回合：診斷會議]
    G --> H[FINAL_DX.md]

    style A fill:#e1f5fe
    style H fill:#c8e6c9
```

| 階段 | 角色 | 執行內容 |
|------|------|---------|
| 1 | 主治醫師（內科） | 問題描述、初步 Top 10 鑑別診斷與前測機率 |
| 2 | 放射科 + 病理科 | 影像與檢驗判讀，套用似然比 |
| 3 | 次專科（自動選擇） | 心臟/神經/感染/胸腔科深度分析 |
| 4 | 實證醫學專家 | WebSearch 搜尋當前證據、指引、統合分析 |
| 5 | 診斷會議 | 共識整合、貝氏機率表、最終診斷 |

每個回合套用 **似然比 (Likelihood Ratio)** 更新疾病機率：

```
後測勝算 = 前測勝算 x LR
```

## 快速開始

```bash
# 建立病人情境
mkdir -p case/my-case
cat > case/my-case/SCENARIO.md << 'EOF'
# 65 歲男性急性胸痛
## 主訴
胸骨下壓迫性胸痛，放射至左臂，持續 2 小時
## 生命徵象
HR 110, BP 90/60, SpO2 94%
EOF

# 在 Claude Code 中執行
/cps case/my-case/SCENARIO.md
```

**產出：**
```
case/my-case/
├── SCENARIO.md           # 病人呈現
├── round-1.md            # 主治醫師評估
├── round-2.md            # 放射科與病理科
├── round-3.md            # 次專科會診
├── round-4.md            # 證據整合
├── round-5.md            # 診斷會議
├── probability-table.md  # 貝氏機率瀑布表
└── FINAL_DX.md           # 最終診斷與推理鏈
```

## 特色功能

### 8 個醫學角色

| 角色 | 職責 | 啟動條件 |
|------|------|----------|
| 主治醫師（內科） | 病史摘要、初步鑑別診斷 | 每次啟動 |
| 放射科醫師 | 影像判讀 | 有影像資料 |
| 病理科醫師 | 檢驗/切片判讀 | 有檢驗資料 |
| 心臟科醫師 | 心電圖、心臟超音波、心導管 | 胸痛、呼吸困難、昏厥 |
| 胸腔科醫師 | 肺功能、血液氣體分析 | 咳嗽、呼吸困難、喘鳴 |
| 感染科醫師 | 培養、血清學 | 發燒、免疫低下 |
| 神經科醫師 | 神經學檢查、腦部影像 | 頭痛、頭暈、譫妄 |
| 實證醫學專家 | 文獻搜尋 | 每次啟動 |

### 33 個教科書章節參考

根據原始文獻整理的臨床診斷資料，每章 60-120 行，包含：
- 鑑別診斷架構與關鍵轉折點
- 似然比表格（LR+/LR-）
- 診斷演算法與臨床決策規則
- 不可遺漏的診斷與危險信號

### 貝氏 LR 計算器

```bash
echo '{"diagnoses": [{"name": "ACS", "prior": 0.25, "must_not_miss": true,
  "findings": [{"name": "Troponin+", "lr": 11.0, "present": true}]}]}' \
  | python3 .claude/skills/cps/scripts/lr_calculator.py
```

### 安全檢查機制

來自真實案例回顧中技能初次失敗的經驗：

| 檢查 | 觸發條件 | 執行內容 |
|------|---------|---------|
| 紅旗病史 | 異常過去病史（如 <40 歲心梗） | 先釐清病因再做鑑別 |
| 症候群篩檢 | 年輕患者、病因不明 | 完整皮膚/眼/血管檢查 |
| 罕見病因搜尋 | 發現與常見鑑別不符 | WebSearch 搜尋完整病因清單 |
| 假說空間稽核 | 每回合結束後 | 「有沒有 Top 10 以外的診斷？」 |
| 遺傳模式辨識 | AD 家族史 + 血管疾病 | 篩查遺傳性血管病變 |
| 假說謙遜原則 | 永遠 | 鑑別診斷永不封閉 |

## 範例案例

### 案例一：76 歲女性 呼吸困難 + 漸進性肌無力

> 6 個月漸進性近端肌無力、雙側眼瞼下垂、反射消失、呼吸衰竭

| 發現 | LR | 機率 |
|------|-----|------|
| 近端肌無力 + 反射消失 | x5.0 | 35% -> 72.9% |
| 低振幅/消失 CMAPs | x8.0 | -> 95.6% |
| SIADH（自主神經功能異常） | x3.0 | -> 98.5% |
| MG 治療無效 | x4.0 | -> **99.6%** |

**最終診斷：乳突-伊頓肌無力症候群 (LEMS)**，副腫瘤性，來自小細胞肺癌

### 案例二：38 歲女性 突發胸痛 — 5 次診斷轉折

> 郵差，有心肌梗塞病史，突發胸痛，硝化甘油無效

| 轉折 | 新資料 | 主要診斷 | 機率 |
|------|--------|---------|------|
| 1 | 年輕女性 + 先前心梗 | SCAD | 97.5% |
| 2 | 多血管區域心梗 + 貧血 | APS | 94.7% |
| 3 | 三血管冠狀動脈瘤 | 川崎病 | 90% |
| 4 | 皮膚丘疹 | KD / 類肉瘤 / NF1 | 50% / 25% / 10% |
| 5 | 咖啡牛奶斑 + 腋窩雀斑 + 神經纖維瘤 | **NF1** | **>95%** |

**最終診斷：第一型神經纖維瘤病 (NF1) 血管病變**，瀰漫性冠狀動脈瘤

**關鍵啟示**：貝氏推理只能在你定義的假說空間內運作。NF1 不在最初的 Top 10 中。

## 指令

| 指令 | 說明 |
|------|------|
| `/cps SCENARIO.md` | 完整 7 階段診斷工作流程 |
| `/cps discover [主題]` | 搜尋 NEJM CPC、BMJ 困難案例 |
| `/cps round [案例目錄] N` | 新增額外的診斷回合 |
| `/cps review [案例目錄]` | 檢視並更新現有案例 |

## 專案結構

```
cps-skills/
├── .claude/skills/cps/
│   ├── SKILL.md                    # 主要技能指令 (303 行)
│   ├── references/
│   │   ├── chapters/              # 33 個精煉章節參考
│   │   ├── personas.md            # 8 個角色定義
│   │   ├── bayesian-reasoning.md  # LR 公式 + 臨床 LR 表
│   │   ├── ddx-framework.md       # VINDICATE + 不可遺漏清單
│   │   ├── rare-causes.md         # NF1、KD、SCAD、PXE、Fabry...
│   │   └── ...
│   └── scripts/
│       ├── init_case.py           # 案例目錄建立
│       ├── lr_calculator.py       # 貝氏機率計算器
│       └── extract_chapter.py     # Epub 章節提取（選用）
├── case/                          # 案例輸出（僅教學案例）
├── .env.example                   # 文獻搜尋 API 金鑰
├── references.bib                 # BibTeX 臨床資料引用來源
└── CLAUDE.md                      # Claude Code 專案指令
```

## 選用：文獻搜尋

設定 [robust-lit-review](https://github.com/htlin222/robust-lit-review) 的 API 金鑰：

```bash
cp .env.example .env
# 填入：SCOPUS_API_KEY, PUBMED_API_KEY, EMBASE_API_KEY 等
```

未設定 `.env` 時，技能僅使用 WebSearch。

## 隱私聲明

> [!CAUTION]
> **絕對不要提交真實病患資料。** 本儲存庫中所有案例皆為去識別化的教學情境。`.gitignore` 已排除常見的病患資料檔案格式。建立自己的案例時，請僅使用虛構或完全去識別化的資料。

## 參考文獻

章節參考檔案中的臨床資料來自同儕審查文獻。所有引用使用 pandoc 格式 `[@key]`，條目收錄於 [`references.bib`](references.bib)。主要來源包括 JAMA Rational Clinical Examination 系列 [@simel2009]、實證理學檢查文獻 [@mcgee2018]，以及臨床決策規則的原始驗證研究。

## 授權

供教育及臨床推理研究用途。
