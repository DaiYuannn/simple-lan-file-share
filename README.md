# SimpleFileShare

一个基于 Django 的精简局域网文件分享系统，只需在主机上运行一个后端服务，局域网内其他设备通过浏览器访问网页即可上传 / 下载文件。

## 功能概览

- 主页展示“公共文件库”列表（文件名、上传时间、下载链接）。
- 主页提供上传表单：选择文件并可填写可选名称。
- 上传的文件保存在服务器本地 `media/uploads/` 目录。
- 不需要登录，适合小范围、可信局域网环境快速共享文件。

## 项目结构

项目根目录：

```text
fileshare/
  manage.py
  venv/                      # Python 虚拟环境
  db.sqlite3                 # SQLite 数据库（迁移后生成）
  main/
    settings.py              # Django 配置（含静态/媒体目录配置）
    urls.py                  # 根 URL 配置，挂载 fileshare
    ...
  fileshare/                 # Django app
    models.py                # SharedFile 模型
    views.py                 # index 视图（列表 + 上传）
    urls.py                  # app 路由（`"" -> index`）
    migrations/              # 数据库迁移
    templates/
      fileshare/
        index.html           # 主页面模板
    static/
      fileshare/
        main.css             # 简单页面样式
        main.js              # 预留前端脚本
```

## 环境准备

建议使用 Python 3.10+。

### 1. 创建虚拟环境并安装依赖

如果你是从零开始，而没有 `venv`：

```powershell
cd C:\Users\DaiYuan\Desktop\fileshare
python -m venv venv
.\venv\Scripts\activate
pip install django
```

（本仓库中已经完成了上述步骤，仅在重新部署到其他机器时需要重新执行。）

### 2. 生成依赖清单（可选）

```powershell
pip freeze > requirements.txt
```

在新环境中可以用：

```powershell
pip install -r requirements.txt
```

## 数据库迁移

在 `src` 目录下执行（首次或模型变更后需要）：

```powershell
cd C:\Users\DaiYuan\Desktop\fileshare
.\venv\Scripts\activate
python manage.py makemigrations
python manage.py migrate
```

迁移成功后会在 `src` 下生成 `db.sqlite3`。

## 启动服务

### 本机/局域网开发运行

在 `src` 目录下：

```powershell
cd C:\Users\DaiYuan\Desktop\fileshare
.\venv\Scripts\activate
python manage.py runserver 0.0.0.0:8000
```

- `0.0.0.0`：监听所有网卡，允许局域网其他设备访问。
- `8000`：HTTP 端口，可按需修改（如 `8080`）。

### 访问方式

1. 本机浏览器访问：

   - `http://127.0.0.1:8000/`

2. 局域网其他设备访问：

   - 在服务端机器上查看 IP：

     ```powershell
     ipconfig
     ```

   - 例如 IP 是 `192.168.1.10`，则在其他设备上访问：

     - `http://192.168.1.10:8000/`

## 使用说明

1. 打开主页：
   - 页面顶部显示“局域网文件分享”标题和说明。
2. 上传文件：
   - 在“上传文件”区域选择文件；
   - 可选填写“文件名称”，用于更友好的显示（不填则使用文件名）；
   - 点击“上传”按钮，上传成功后自动返回主页，列表中会出现新文件。
3. 下载文件：
   - 在“公共文件库”列表中，点击某一行的“下载”链接即可下载对应文件。

## 配置细节

- `ALLOWED_HOSTS = ["*"]`：
  - 为方便局域网内访问，在开发/内网环境中放宽限制。
  - 若用于更严格环境，可改为仅允许具体 IP 或域名。
- 静态文件：
  - `STATIC_URL = "static/"`
  - `STATICFILES_DIRS = [BASE_DIR / "fileshare" / "static"]`
- 媒体文件（上传文件）：
  - `MEDIA_URL = "media/"`
  - `MEDIA_ROOT = BASE_DIR / "media"`
  - `SharedFile.file` 使用 `upload_to="uploads/"`，实际存储路径为：`media/uploads/`。

## 模型与视图简述

- 模型 `fileshare.models.SharedFile`：
  - `name`：`CharField(max_length=255, blank=True)`；
  - `file`：`FileField(upload_to="uploads/")`；
  - `uploaded_at`：`DateTimeField(auto_now_add=True)`。

- 视图 `fileshare.views.index`：
  - `GET`：查询 `SharedFile`，按 `uploaded_at` 倒序显示；
  - `POST`：从表单读取 `name` 和 `file`，保存后使用 `redirect("fileshare:index")` 返回主页。
  