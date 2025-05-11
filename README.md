# 中共二大互动历史游戏项目（Visual Novel）

本项目是一个基于 Vue 3 + Pinia 的网页互动视觉小说，用户可与中共二大历史人物进行对话，结合大模型接口和语音朗读功能，增强党史学习的沉浸体验。

---

## 📁 项目结构

| 路径              | 说明                      |
|------------------|---------------------------|
| `src/`           | 项目源码目录              |
| `src/scenes/`    | 各个游戏场景组件（如主场景、开场动画等） |
| `src/components/`| 公用组件（按钮、转场、粒子背景） |
| `src/stores/`    | 状态管理（Pinia）         |
| `public/`        | 静态资源目录（图片、视频） |

---

## 🧱 环境准备

### ✅ 必须工具

- **Node.js**：建议版本 v18+

---

## 🚀 本地运行步骤

### 1. 克隆项目

```bash
git clone https://github.com/你的用户名/SecondCongressVisualNovels.git
cd SecondCongressVisualNovels
```

### 2. 安装依赖

```bash
npm install
```

### 3. 启动开发环境

```bash
npm run dev
```

打开浏览器访问： [http://localhost:5173](http://localhost:5173)

---

## 🧪 开发建议

- 开发环境使用 [Vite](https://vitejs.dev/) 构建，热更新快
- 所有角色立绘图片放在 `public/characters/` 目录
- 背景图、视频等放在 `public/backgrounds/`

---

## ⚠️ 注意事项

- `.env` 环境变量未包含在版本控制中，请根据需要添加
- `.gitignore` 忽略了 `node_modules/`、`dist/` 等构建产物
- 请自行准备美术资源（立绘、背景图等），或使用占位图开发

---

## 📝 License

MIT License - 可用于学习、非商业性项目。
