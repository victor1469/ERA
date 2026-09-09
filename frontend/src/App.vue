<template>

    <div class="app">

        <!-- =========================
             顶部 Header
        ========================== -->

        <header class="header">

            <div class="brand">

                <div class="brand-icon">
                    ✦
                </div>

                <div class="brand-text">

                    <div class="brand-name">
                        AI智能文档助手
                    </div>

                    <div class="brand-desc">
                        Enterprise RAG Knowledge Assistant
                    </div>

                </div>

            </div>


            <div class="header-right">

                <div class="tech-tag">
                    Local Qwen
                </div>

                <div class="tech-tag">
                    RAG
                </div>

                <div class="status">

                    <span class="status-dot"></span>

                    AI服务运行中

                </div>

            </div>

        </header>


        <!-- =========================
             主体
        ========================== -->

        <main class="main">

            <!-- =========================
                 左侧知识库
            ========================== -->

            <aside class="sidebar">

                <div class="sidebar-header">

                    <div class="sidebar-title">
                        知识库
                    </div>

                    <div class="sidebar-subtitle">
                        企业文档管理
                    </div>

                </div>


                <div class="file-manager-wrapper">

                    <FileManager />

                </div>


                <div class="sidebar-footer">

                    <div class="system-info">

                        <span class="info-dot"></span>

                        <span>
                            本地知识库已连接
                        </span>

                    </div>

                </div>

            </aside>


            <!-- =========================
                 右侧聊天
            ========================== -->

            <section class="content">

                <div class="content-header">

                    <div>

                        <div class="content-title">
                            智能问答
                        </div>

                        <div class="content-desc">
                            基于已上传文档进行智能检索与问答
                        </div>

                    </div>


                    <div class="content-badge">

                        <span class="badge-dot"></span>

                        RAG 已启用

                    </div>

                </div>


                <div class="chat-wrapper">

                    <ChatBox />

                </div>

            </section>

        </main>

    </div>

</template>


<script setup>

import FileManager from "./components/FileManager.vue"

import ChatBox from "./components/ChatBox.vue"

</script>


<style>

* {
    box-sizing: border-box;
}


html,
body,
#app {
    margin: 0;
    width: 100%;
    min-height: 100%;
}


body {

    font-family:
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        "Microsoft YaHei",
        sans-serif;

    background: #f5f7fa;

    color: #303133;

    -webkit-font-smoothing: antialiased;

}


button,
input,
textarea {

    font-family: inherit;

}


.app {

    min-height: 100vh;

    background: #f5f7fa;

}


/* =========================
   Header
========================= */

.header {

    height: 68px;

    background: #ffffff;

    border-bottom: 1px solid #e8eaed;

    display: flex;

    align-items: center;

    justify-content: space-between;

    padding: 0 30px;

}


.brand {

    display: flex;

    align-items: center;

    gap: 11px;

}


.brand-icon {

    width: 38px;

    height: 38px;

    border-radius: 10px;

    background: #409eff;

    color: #ffffff;

    display: flex;

    align-items: center;

    justify-content: center;

    font-size: 20px;

    font-weight: 600;

    box-shadow:
        0 4px 12px rgba(64, 158, 255, 0.18);

}


.brand-text {

    display: flex;

    flex-direction: column;

}


.brand-name {

    font-size: 16px;

    line-height: 1.4;

    font-weight: 650;

    color: #303133;

}


.brand-desc {

    margin-top: 2px;

    font-size: 10px;

    letter-spacing: 0.35px;

    color: #a0a4ab;

}


.header-right {

    display: flex;

    align-items: center;

    gap: 7px;

}


.tech-tag {

    padding: 4px 9px;

    border-radius: 6px;

    background: #f2f6fc;

    color: #409eff;

    font-size: 10px;

    font-weight: 500;

}


.status {

    display: flex;

    align-items: center;

    gap: 7px;

    margin-left: 8px;

    padding-left: 13px;

    border-left: 1px solid #ebeef5;

    color: #67c23a;

    font-size: 11px;

}


.status-dot {

    width: 6px;

    height: 6px;

    border-radius: 50%;

    background: #67c23a;

    box-shadow:
        0 0 0 3px rgba(103, 194, 58, 0.09);

}


/* =========================
   Main
========================= */

.main {

    display: flex;

    height: calc(100vh - 68px);

    padding: 18px 22px 22px;

    gap: 18px;

}


/* =========================
   Sidebar
========================= */

.sidebar {

    width: 312px;

    flex-shrink: 0;

    display: flex;

    flex-direction: column;

    background: #ffffff;

    border: 1px solid #e5e7eb;

    border-radius: 12px;

    overflow: hidden;

    box-shadow:
        0 1px 3px rgba(0, 0, 0, 0.025);

}


.sidebar-header {

    padding: 17px 18px 15px;

    border-bottom: 1px solid #ebeef5;

}


.sidebar-title {

    font-size: 15px;

    font-weight: 600;

    color: #303133;

}


.sidebar-subtitle {

    margin-top: 4px;

    font-size: 11px;

    color: #909399;

}


.file-manager-wrapper {

    flex: 1;

    min-height: 0;

    overflow: hidden;

}


.sidebar-footer {

    padding: 11px 15px;

    border-top: 1px solid #ebeef5;

    background: #fafbfc;

}


.system-info {

    display: flex;

    align-items: center;

    gap: 7px;

    color: #909399;

    font-size: 10px;

}


.info-dot {

    width: 6px;

    height: 6px;

    border-radius: 50%;

    background: #67c23a;

}


/* =========================
   Content
========================= */

.content {

    flex: 1;

    min-width: 0;

    display: flex;

    flex-direction: column;

}


.content-header {

    height: 56px;

    display: flex;

    align-items: flex-start;

    justify-content: space-between;

    padding: 1px 3px 11px;

}


.content-title {

    font-size: 17px;

    font-weight: 600;

    color: #303133;

}


.content-desc {

    margin-top: 4px;

    font-size: 11px;

    color: #909399;

}


.content-badge {

    display: flex;

    align-items: center;

    gap: 6px;

    padding: 5px 9px;

    border-radius: 7px;

    background: #f0f9eb;

    color: #67c23a;

    font-size: 10px;

}


.badge-dot {

    width: 6px;

    height: 6px;

    border-radius: 50%;

    background: #67c23a;

}


.chat-wrapper {

    flex: 1;

    min-height: 0;

}


/* =========================
   Responsive
========================= */

@media (max-width: 1100px) {

    .sidebar {

        width: 280px;

    }

}


@media (max-width: 900px) {

    .header {

        padding: 0 18px;

    }


    .header-right {

        display: none;

    }


    .main {

        flex-direction: column;

        height: auto;

        min-height: calc(100vh - 68px);

        padding: 14px;

        gap: 14px;

    }


    .sidebar {

        width: 100%;

        height: 360px;

        max-height: 360px;

    }


    .content {

        min-height: 680px;

    }


    .content-header {

        height: 52px;

    }

}


@media (max-width: 600px) {

    .header {

        height: 62px;

    }


    .brand-desc {

        display: none;

    }


    .main {

        min-height: calc(100vh - 62px);

        padding: 10px;

    }


    .sidebar {

        height: 320px;

        max-height: 320px;

    }

}

</style>