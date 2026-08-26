# China Robotics Insider — 上线 + 谷歌收录 + AdSense 变现 行动手册

> 你的英文网站源码已全部就绪，就在 `china-robotics-site/` 目录。按本手册操作，即可把它变成一个能被 Google 收录、能接 AdSense 挣钱的真实网站。

---

## 一、网站现状速览

| 项 | 内容 |
|---|---|
| 网站定位 | 面向全球读者的中国机器人产业英文内容站 |
| 站点名 | **China Robotics Insider** |
| 已建页面 | 首页、历史、人物、公司、产品、关于、隐私政策（7 个页面） |
| 技术栈 | 纯静态 HTML + CSS + JS（对谷歌收录与广告最友好） |
| SEO 已内置 | 每页 title/description/canonical、Open Graph、JSON-LD 结构化数据、语义化标签 |
| SEO 文件 | `sitemap.xml`、`robots.txt` 已生成 |
| 内容量 | 7 页原创英文内容，约 5,500+ 英文词 |

**目录结构：**
```
china-robotics-site/
├── index.html        # 首页（产业概览+数据+栏目入口）
├── history.html      # 发展历史（时间线）
├── people.html       # 人物（17位创业者/企业家/大牛）
├── companies.html    # 公司（5大类20+家）
├── products.html     # 前沿产品
├── about.html        # 关于与编辑标准
├── privacy.html      # 隐私政策（AdSense 必需）
├── css/style.css     # 样式
├── js/main.js        # 交互
├── sitemap.xml       # 站点地图
├── robots.txt        # 爬虫规则
└── assets/           # 素材目录（后续放图）
```

---

## 二、域名（已完成 ✅）

你已在 Porkbun 购买 **`robotichina.com`**，全站文件里的域名也已统一替换为 `www.robotichina.com`，无需再做任何替换。

> 小提醒：`robotichina.com` 与行业门户 `robotchina.com` 只差一个字母，海外读者可能拼错。建议在 About 页和首屏反复强化站名 "China Robotics Insider"（品牌名保持这个），降低混淆影响。

---

## 三、第 1 步：部署上线（3 选 1，推荐 GitHub Pages，免费）

### 方案 A：GitHub Pages（免费，推荐起步）
1. 注册 GitHub，新建仓库，名字随便（如 `chinarobotics-site`）。
2. 把 `china-robotics-site/` 里**所有文件**（含 css、js 子目录）上传到仓库根目录。
3. 进入仓库 `Settings → Pages`，Source 选 `main` 分支，保存。
4. 等 1-2 分钟，你的网站就在 `https://你的用户名.github.io/chinarobotics-site/` 上线了。

### 方案 B：Netlify（免费，可绑定自己的域名）
1. 注册 netlify.com → `Add new site → Deploy manually`。
2. 把 `china-robotics-site/` 整个文件夹拖进去，秒上线。
3. `Domain settings` 里绑定你已购买的 `robotichina.com`（Netlify 提供免费 HTTPS）。

### 方案 C：Vercel / Cloudflare Pages（同样免费）
操作与 Netlify 类似，都是"拖文件夹→上线→绑域名"。

> **无论哪种方案，绑好自有域名后，用 `www.你的域名.com` 能正常访问即可进入下一步。**

---

## 四、第 2 步：Google Search Console 收录（免费）

1. 打开 https://search.google.com/search-console ，用 Google 账号登录。
2. 添加资源 → 选"网域" → 输入你的域名（如 `robotichina.com`）。
3. 按提示在域名服务商处添加 DNS 记录完成验证（或选"网址前缀"方式，用 HTML 文件验证）。
4. 验证通过后，在左侧"站点地图"提交：`https://你的域名/sitemap.xml`。
5. **关键：点左侧"网址检查"，输入你的首页 URL，点"请求编入索引"。**
6. 之后 1-2 周内谷歌会开始收录。新页面（以后新增的）会自动被 sitemap 抓到。

> 收录是滚雪球：内容越多、更新越勤，谷歌爬得越频繁。网站刚上线前几周收录慢是正常的。

---

## 五、第 3 步：申请 Google AdSense（开始挣钱）

### 申请门槛（务必先满足）
- ✅ 网站有**自己的域名**（robotichina.com，已完成）
- ✅ 有**足够原创内容**（你现在 7 页英文原创内容，建议再新增 3-5 页后再申请，胜率更高）
- ✅ 网站有**基本导航**（已有）和**隐私政策页**（已有 privacy.html）
- ✅ 网站运行 **2-4 周以上**，且有少量自然流量

### 申请流程
1. 打开 https://adsense.google.com → 用 Google 账号登录。
2. 填入你的网站 URL → 提交申请。
3. 审核通常 2 天 - 2 周。期间**不要改动站名/域名/大幅改版**。
4. 通过后，AdSense 会给一段代码，粘贴到每个页面的 `<head>` 里（本网站每个 HTML 顶部都预留了 `<head>` 区域，很好加）。
5. 之后在 AdSense 后台"自动广告"一键开启，谷歌会自动选择广告位。

### 收入预期（现实一点）
- 机器人/科技类 CPC（单次点击单价）较高，约 $0.5-3/点击。
- 初期流量小，可能前几个月只有几十美元/月。
- **真正的收入增长来自持续更新内容 + SEO 排名上升**（见第六步）。

---

## 六、第 4 步：内容策略（决定你能挣多少）

AdSense 收入 = 流量 × 点击率 × 单价。流量靠内容。

### 1. 起步期：加厚"内容地基"（未来 1 个月）
建议每周新增 2-3 个页面，优先这些高搜索意图主题：
- 单公司深度页：`Unitree G1 vs Agibot A2 comparison`、`Best Chinese humanoid robots 2026`
- 人物故事页：把 people.html 里 17 位人物**逐个拆成独立页面**（`/people/wang-xingxing-unitree.html`）——长尾词来源
- 指南类：`How to buy a robot dog from China`、`Chinese robot companies list`
- 你公众号里已有的每篇特稿（赵同阳、秦深涛、刘松铭等）都可以英文化后做成独立文章页

### 2. 关键词思路（长尾优先，竞争小）
- 英文搜索习惯是具体问题：`"unitree go2 price"`、`"agibot stock"`、`"walker s factory"`、`"china humanoid robot companies"`
- 每篇文章 title 用一个具体关键词，description 包含完整问题。

### 3. E-E-A-T（谷歌给内容打分）
- 在 about.html 里补充作者信息、行业背景（你是机器人领域自媒体，这就是优势）。
- 每个页面底部加"最后更新时间"。
- 关键数据标注来源（现在部分页面已标注口径，继续保持）。

### 4. 内链
- 新增文章页时，记得互相链接（如人物页↔公司页↔产品页），本网站已为你做好了内链骨架。

---

## 七、变现路径全景（不止 AdSense）

| 阶段 | 方式 | 说明 |
|---|---|---|
| 0-3 个月 | **AdSense** | 主要收入，门槛低、被动 |
| 3-6 个月 | **联盟营销（Affiliate）** | 在"产品"类文章里挂 Amazon/品牌联盟链接（如机器人周边、开发板），转化比广告高 |
| 6 个月+ | **Newsletter + 付费内容** | 建立邮件订阅（Buttondown/Substack 免费），沉淀读者 |
| 品牌合作 | **赞助/软文** | 流量起来后，中国机器人公司出海宣传需求大，可接赞助 |

---

## 八、常见问题

**Q：为什么我的网站还没被谷歌收录？**
A：新站 1-4 周收录都是正常的。确保：① Search Console 验证成功 ② sitemap 提交成功 ③ 主动"请求编入索引" ④ 别频繁改域名/站名。

**Q：AdSense 被拒怎么办？**
A：常见原因是内容不足或网站太新。补 3-5 页原创内容、运行满 1 个月再申请。不要买流量，不要加"点击广告"字样。

**Q：能用免费子域名先跑吗？**
A：能测试，但 AdSense 必须自有域名。建议一步到位买域名。

**Q：图片素材从哪来？**
A：本网站目前用图标/配色，无版权风险。后续加真实产品图建议用公司官网公开图 + 注明来源，或自己拍摄/生成（注意版权）。

---

## 九、本站后续可直接迭代的方向

1. **拆分人物页**：people.html 里每个人单独建页（量大，SEO 价值最高）。
2. **加博客/资讯栏**：复用你公众号"机器人精英圈"的内容，英文化后每周更新。
3. **多语言版**：英文站跑通后，可加中文版/日语版，扩大流量池。
4. **数据可视化**：加"中国机器人融资地图"等交互页面，增强外链吸引力。

---

*准备好后随时找我：我可以帮你批量把公众号特稿英文化、拆分成独立页面、继续扩站。*
