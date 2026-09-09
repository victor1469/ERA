<template>

    <div class="chat-container">

        <!-- =========================
             Chat Header
        ========================== -->

        <div class="chat-header">

            <div class="chat-header-main">

                <div class="chat-header-icon">
                    ✦
                </div>

                <div>

                    <div class="chat-title">
                        AI智能文档助手
                    </div>

                    <div class="chat-subtitle">
                        基于企业知识库的智能问答
                    </div>

                </div>

            </div>


            <div class="chat-header-status">

                <span class="chat-status-dot"></span>

                在线

            </div>

        </div>


        <!-- =========================
             消息区域
        ========================== -->

        <div class="chat-messages">

            <!-- 空状态 -->

            <div
                v-if="messages.length === 0"
                class="empty-message"
            >

                <div class="welcome-icon">
                    ✦
                </div>


                <div class="empty-title">
                    AI 智能文档助手
                </div>


                <div class="empty-text">
                    基于企业知识库的智能检索与问答
                </div>


                <div class="feature-list">

                    <div class="feature-card">

                        <div class="feature-icon">
                            📄
                        </div>

                        <div class="feature-content">

                            <div class="feature-title">
                                文档理解
                            </div>

                            <div class="feature-desc">
                                快速理解企业文档内容
                            </div>

                        </div>

                    </div>


                    <div class="feature-card">

                        <div class="feature-icon">
                            🔍
                        </div>

                        <div class="feature-content">

                            <div class="feature-title">
                                智能检索
                            </div>

                            <div class="feature-desc">
                                从知识库精准检索相关内容
                            </div>

                        </div>

                    </div>


                    <div class="feature-card">

                        <div class="feature-icon">
                            ✨
                        </div>

                        <div class="feature-content">

                            <div class="feature-title">
                                AI 问答
                            </div>

                            <div class="feature-desc">
                                基于文档内容生成智能回答
                            </div>

                        </div>

                    </div>

                </div>


                <div class="example-title">
                    你可以这样问
                </div>


                <div class="example-list">

                    <div class="example-item">
                        “这个文档主要讲了什么？”
                    </div>

                    <div class="example-item">
                        “文档中有哪些重要内容？”
                    </div>

                    <div class="example-item">
                        “请总结一下这份文档。”
                    </div>

                </div>

            </div>


            <!-- =========================
                 消息
            ========================== -->

            <div
                v-for="(message, index) in messages"
                :key="index"
                class="message"
                :class="[
                    message.role,
                    {
                        'message-error': message.isError
                    }
                ]"
            >

                <div class="message-avatar">

                    <span v-if="message.role === 'user'">
                        👤
                    </span>

                    <span v-else>
                        ✦
                    </span>

                </div>


                <div class="message-content">

                    <div class="message-name">

                        <span v-if="message.role === 'user'">
                            你
                        </span>

                        <span v-else>
                            AI助手
                        </span>

                    </div>


                    <!-- AI回答 -->

                    <div
                        v-if="message.role === 'assistant'"
                        class="markdown-body"
                        v-html="renderMarkdown(message.content)"
                    ></div>


                    <!-- 来源 -->

                    <div
                        v-if="
                            message.role === 'assistant' &&
                            message.sources &&
                            message.sources.length
                        "
                        class="sources-section"
                    >

                        <div class="sources-title">

                            <span class="sources-icon">
                                📚
                            </span>

                            参考来源

                            <span class="sources-count">
                                {{ message.sources.length }}
                            </span>

                        </div>


                        <div
                            v-for="(source, sourceIndex) in message.sources"
                            :key="sourceIndex"
                            class="source-item"
                        >

                            <div class="source-number">
                                {{ sourceIndex + 1 }}
                            </div>


                            <div class="source-content">

                                <div class="source-header">

                                    <div
                                        class="source-filename"
                                        :title="getSourceFilename(source)"
                                    >
                                        {{ getSourceFilename(source) }}
                                    </div>


                                    <div
                                        v-if="
                                            source.score !== null &&
                                            source.score !== undefined
                                        "
                                        class="source-score"
                                    >
                                        相似度 {{ formatScore(source.score) }}
                                    </div>

                                </div>


                                <div class="source-text">
                                    {{ getSourceText(source) }}
                                </div>

                            </div>

                        </div>

                    </div>


                    <!-- 用户消息 -->

                    <div
                        v-else
                        class="user-message"
                    >
                        {{ message.content }}
                    </div>

                </div>


                <!-- Loading -->

                <div
                    v-if="loading"
                    class="loading-container"
                >

                    <div class="loading-spinner"></div>

                    <div class="loading-content">

                        <div class="loading-title">
                            {{ loadingStatus }}
                        </div>

                        <div
                            v-if="loadingCount > 0"
                            class="loading-subtitle"
                        >
                            已检索 {{ loadingCount }} 条相关资料
                        </div>

                    </div>

                </div>

            </div>

        </div>


        <!-- =========================
             输入区域
        ========================== -->

        <div class="chat-input-area">

            <el-input
                v-model="question"
                :disabled="loading"
                type="textarea"
                :rows="3"
                resize="none"
                placeholder="请输入关于文档的问题，例如：这个文档主要讲什么？"
                @keydown.enter.exact.prevent="sendQuestion"
            />


            <div class="input-footer">

                <div class="input-tip">

                    <span class="tip-key">
                        Enter
                    </span>

                    发送

                </div>


                <el-button
                    type="primary"
                    class="send-button"
                    :loading="loading"
                    :disabled="loading || !question.trim()"
                    @click="sendQuestion"
                >
                    {{ loading ? "处理中..." : "发送" }}
                </el-button>

            </div>

        </div>

    </div>

</template>


<script setup>

import {
    ref
} from "vue"


import {
    marked
} from "marked"


import DOMPurify from "dompurify"


import {
    chat
} from "../api/rag"



const question = ref("")


const loading = ref(false)

const loadingStatus = ref("")

const loadingCount = ref(0)


const messages = ref([])



function renderMarkdown(content) {

    const html = marked.parse(
        content || ""
    )

    return DOMPurify.sanitize(
        html
    )

}


function getSourceFilename(source) {

    if (
        source &&
        typeof source === "object" &&
        source.filename
    ) {

        return source.filename

    }


    return "知识库文档"

}


function formatScore(score) {

    if (
        score === null ||
        score === undefined
    ) {

        return ""

    }


    return `${Math.round(score * 100)}%`

}


function getSourceText(source) {

    if (
        typeof source === "string"
    ) {

        return source

    }


    if (
        source &&
        typeof source === "object" &&
        source.content
    ) {

        return source.content

    }


    if (
        source &&
        typeof source === "object" &&
        source.text
    ) {

        return source.text

    }


    if (
        source &&
        typeof source === "object" &&
        source.document
    ) {

        return source.document

    }


    return String(source || "")

}


async function sendQuestion() {

    const text = question.value.trim()


    // 防止空问题

    if (!text) {

        return

    }


    // 防止重复点击

    if (loading.value) {

        return

    }


    // 添加用户消息

    messages.value.push({

        role: "user",

        content: text

    })


    // 清空输入框

    question.value = ""


    // 开始加载

    loading.value = true

    loadingStatus.value = "正在检索知识库..."

    loadingCount.value = 0


    try {

        /*
         * 第一步：
         * 调用后端 /chat
         *
         * 后端内部：
         *
         * 用户问题
         * ↓
         * Embedding
         * ↓
         * Chroma
         * ↓
         * 检索相关文档
         * ↓
         * Ollama / Qwen
         */

        const res = await chat(text)


        if (
            !res ||
            !res.data
        ) {

            throw new Error(
                "服务器返回数据为空"
            )

        }


        const answer = res.data.answer


        if (
            !answer ||
            !answer.trim()
        ) {

            throw new Error(
                "AI没有返回有效回答"
            )

        }


        const sources =
            res.data.sources || []


        loadingCount.value =
            sources.length


        loadingStatus.value =
            `找到 ${sources.length} 条相关资料`


        await new Promise(
            resolve =>
                setTimeout(
                    resolve,
                    300
                )
        )


        loadingStatus.value =
            "Qwen 正在生成回答..."


        await new Promise(
            resolve =>
                setTimeout(
                    resolve,
                    300
                )
        )


        messages.value.push({

            role: "assistant",

            content: answer,

            sources: sources

        })


    }

    catch (error) {

        console.error(
            "Chat error:",
            error
        )


        let errorMessage =
            "抱歉，系统暂时无法完成回答。"


        if (
            error.response
        ) {

            const status =
                error.response.status


            if (
                status === 404
            ) {

                errorMessage =
                    "后端接口不存在，请检查 FastAPI 服务。"

            }

            else if (
                status >= 500
            ) {

                errorMessage =
                    "服务器内部发生错误，请检查 FastAPI 或 Ollama。"

            }

            else if (
                status === 422
            ) {

                errorMessage =
                    "请求参数格式错误，请检查输入内容。"

            }

        }

        else if (
            error.request
        ) {

            errorMessage =
                "无法连接后端服务器，请确认 FastAPI 正在运行。"

        }

        else if (
            error.message
        ) {

            if (
                error.message.includes(
                    "timeout"
                )
            ) {

                errorMessage =
                    "AI响应超时，请稍后重试。"

            }

        }


        messages.value.push({

            role: "assistant",

            content: errorMessage,

            sources: [],

            isError: true

        })

    }

    finally {

        loading.value = false

        loadingStatus.value = ""

        loadingCount.value = 0

    }

}

</script>


<style scoped>

/* =========================
   Chat 容器
========================= */

.chat-container {

    height: 100%;

    min-height: 0;

    display: flex;

    flex-direction: column;

    background: #ffffff;

    border-radius: 12px;

    border: 1px solid #e5e7eb;

    overflow: hidden;

    box-shadow:
        0 1px 3px rgba(0, 0, 0, 0.025);

}


/* =========================
   Chat Header
========================= */

.chat-header {

    min-height: 62px;

    padding: 13px 20px;

    display: flex;

    align-items: center;

    justify-content: space-between;

    border-bottom: 1px solid #ebeef5;

    background: #ffffff;

}


.chat-header-main {

    display: flex;

    align-items: center;

    gap: 10px;

}


.chat-header-icon {

    width: 32px;

    height: 32px;

    flex-shrink: 0;

    display: flex;

    align-items: center;

    justify-content: center;

    border-radius: 8px;

    background: #f0f7ff;

    color: #409eff;

    font-size: 16px;

    font-weight: 600;

}


.chat-title {

    font-size: 15px;

    line-height: 1.4;

    font-weight: 600;

    color: #303133;

}


.chat-subtitle {

    margin-top: 2px;

    font-size: 10px;

    line-height: 1.4;

    color: #a0a4ab;

}


.chat-header-status {

    display: flex;

    align-items: center;

    gap: 5px;

    padding: 4px 8px;

    border-radius: 6px;

    background: #f0f9eb;

    color: #67c23a;

    font-size: 10px;

}


.chat-status-dot {

    width: 5px;

    height: 5px;

    border-radius: 50%;

    background: #67c23a;

}


/* =========================
   消息区域
========================= */

.chat-messages {

    flex: 1;

    min-height: 0;

    overflow-y: auto;

    padding: 22px 24px;

    scroll-behavior: smooth;

}


.chat-messages::-webkit-scrollbar {

    width: 6px;

}


.chat-messages::-webkit-scrollbar-thumb {

    border-radius: 10px;

    background: #dcdfe6;

}


.chat-messages::-webkit-scrollbar-track {

    background: transparent;

}


/* =========================
   空状态
========================= */

.empty-message {

    min-height: 100%;

    display: flex;

    flex-direction: column;

    align-items: center;

    justify-content: center;

    color: #909399;

    padding: 30px 20px;

}


.welcome-icon {

    width: 58px;

    height: 58px;

    display: flex;

    align-items: center;

    justify-content: center;

    border-radius: 16px;

    background: #409eff;

    color: #ffffff;

    font-size: 27px;

    font-weight: 600;

    margin-bottom: 15px;

    box-shadow:
        0 7px 20px rgba(64, 158, 255, 0.18);

}


.empty-title {

    font-size: 21px;

    line-height: 1.4;

    color: #303133;

    font-weight: 600;

    letter-spacing: 0.1px;

}


.empty-text {

    margin-top: 6px;

    font-size: 12px;

    line-height: 1.6;

    color: #909399;

}


/* =========================
   功能卡片
========================= */

.feature-list {

    display: flex;

    gap: 10px;

    margin-top: 24px;

    max-width: 680px;

    width: 100%;

    justify-content: center;

}


.feature-card {

    flex: 1;

    max-width: 215px;

    min-height: 78px;

    display: flex;

    align-items: center;

    gap: 10px;

    padding: 12px 14px;

    background: #ffffff;

    border: 1px solid #ebeef5;

    border-radius: 9px;

    text-align: left;

    transition:
        border-color 0.2s ease,
        box-shadow 0.2s ease,
        transform 0.2s ease;

}


.feature-card:hover {

    border-color: #d9ecff;

    box-shadow:
        0 4px 14px rgba(64, 158, 255, 0.07);

    transform: translateY(-1px);

}


.feature-icon {

    width: 34px;

    height: 34px;

    flex-shrink: 0;

    display: flex;

    align-items: center;

    justify-content: center;

    border-radius: 8px;

    background: #f2f6fc;

    font-size: 16px;

}


.feature-content {

    min-width: 0;

}


.feature-title {

    font-size: 12px;

    font-weight: 600;

    color: #303133;

}


.feature-desc {

    margin-top: 3px;

    font-size: 10px;

    line-height: 1.5;

    color: #909399;

}


/* =========================
   示例问题
========================= */

.example-title {

    margin-top: 23px;

    margin-bottom: 8px;

    font-size: 11px;

    color: #a0a4ab;

}


.example-list {

    display: flex;

    flex-wrap: wrap;

    justify-content: center;

    gap: 6px;

}


.example-item {

    padding: 5px 10px;

    border-radius: 6px;

    background: #f7f8fa;

    color: #606266;

    font-size: 10px;

    border: 1px solid transparent;

    transition:
        background 0.2s ease,
        border-color 0.2s ease;

}


.example-item:hover {

    background: #f0f7ff;

    border-color: #d9ecff;

    color: #409eff;

}


/* =========================
   消息
========================= */

.message {

    display: flex;

    align-items: flex-start;

    gap: 10px;

    margin-bottom: 20px;

}


.message-avatar {

    width: 32px;

    height: 32px;

    border-radius: 9px;

    display: flex;

    align-items: center;

    justify-content: center;

    flex-shrink: 0;

    background: #f2f6fc;

    font-size: 15px;

}


.message-content {

    max-width: min(78%, 820px);

    min-width: 0;

}


.message-name {

    font-size: 10px;

    color: #a0a4ab;

    margin-bottom: 5px;

}


.user-message {

    background: #409eff;

    color: #ffffff;

    padding: 9px 13px;

    border-radius: 9px 9px 3px 9px;

    line-height: 1.65;

    font-size: 13px;

    white-space: pre-wrap;

    box-shadow:
        0 2px 6px rgba(64, 158, 255, 0.10);

}


.message.user {

    flex-direction: row-reverse;

}


.message.user .message-content {

    display: flex;

    flex-direction: column;

    align-items: flex-end;

}


/* =========================
   Markdown
========================= */

.markdown-body {

    padding: 11px 14px;

    border: 1px solid #ebeef5;

    border-radius: 3px 9px 9px 9px;

    background: #ffffff;

    line-height: 1.75;

    color: #303133;

    font-size: 13px;

}


.markdown-body :deep(h1),
.markdown-body :deep(h2),
.markdown-body :deep(h3) {

    margin-top: 15px;

    margin-bottom: 8px;

    color: #303133;

}


.markdown-body :deep(h1:first-child),
.markdown-body :deep(h2:first-child),
.markdown-body :deep(h3:first-child) {

    margin-top: 0;

}


.markdown-body :deep(p) {

    margin: 7px 0;

}


.markdown-body :deep(p:first-child) {

    margin-top: 0;

}


.markdown-body :deep(p:last-child) {

    margin-bottom: 0;

}


.markdown-body :deep(ul),
.markdown-body :deep(ol) {

    padding-left: 22px;

}


.markdown-body :deep(li) {

    margin: 3px 0;

}


.markdown-body :deep(code) {

    background: #f5f7fa;

    padding: 2px 5px;

    border-radius: 4px;

    color: #606266;

    font-size: 12px;

}


.markdown-body :deep(pre) {

    margin: 10px 0;

    background: #282c34;

    color: #ffffff;

    padding: 13px;

    border-radius: 7px;

    overflow-x: auto;

}


.markdown-body :deep(pre code) {

    background: transparent;

    color: inherit;

    padding: 0;

}


/* =========================
   来源
========================= */

.sources-section {

    margin-top: 14px;

    padding-top: 12px;

    border-top: 1px solid #ebeef5;

}


.sources-title {

    display: flex;

    align-items: center;

    gap: 5px;

    font-size: 11px;

    font-weight: 600;

    color: #606266;

    margin-bottom: 8px;

}


.sources-icon {

    font-size: 12px;

}


.sources-count {

    min-width: 17px;

    height: 17px;

    display: inline-flex;

    align-items: center;

    justify-content: center;

    padding: 0 4px;

    border-radius: 5px;

    background: #f2f6fc;

    color: #409eff;

    font-size: 9px;

    font-weight: 500;

}


.source-item {

    display: flex;

    gap: 9px;

    padding: 9px 10px;

    margin-bottom: 6px;

    background: #f8f9fb;

    border: 1px solid #ebeef5;

    border-radius: 7px;

    transition:
        border-color 0.2s ease,
        background 0.2s ease;

}


.source-item:hover {

    background: #f5f8fc;

    border-color: #dfe8f3;

}


.source-number {

    width: 20px;

    height: 20px;

    flex-shrink: 0;

    display: flex;

    align-items: center;

    justify-content: center;

    border-radius: 6px;

    background: #409eff;

    color: #ffffff;

    font-size: 10px;

}


.source-content {

    min-width: 0;

    flex: 1;

}


.source-header {

    display: flex;

    align-items: center;

    justify-content: space-between;

    gap: 10px;

    margin-bottom: 3px;

}


.source-filename {

    min-width: 0;

    overflow: hidden;

    white-space: nowrap;

    text-overflow: ellipsis;

    font-size: 11px;

    font-weight: 600;

    color: #303133;

}


.source-score {

    flex-shrink: 0;

    padding: 2px 5px;

    border-radius: 4px;

    background: #f0f9eb;

    color: #67c23a;

    font-size: 9px;

}


.source-text {

    font-size: 10px;

    line-height: 1.6;

    color: #606266;

    word-break: break-word;

    display: -webkit-box;

    -webkit-line-clamp: 3;

    -webkit-box-orient: vertical;

    overflow: hidden;

}


/* =========================
   Loading
========================= */

.loading-container {

    display: flex;

    align-items: center;

    gap: 10px;

    margin: 10px 0 16px 42px;

    padding: 10px 12px;

    max-width: 330px;

    background: #f7f8fa;

    border: 1px solid #ebeef5;

    border-radius: 8px;

}


.loading-spinner {

    width: 17px;

    height: 17px;

    border: 2px solid #dcdfe6;

    border-top-color: #409eff;

    border-radius: 50%;

    animation:
        loading-spin
        0.8s linear infinite;

    flex-shrink: 0;

}


.loading-content {

    min-width: 0;

}


.loading-title {

    font-size: 11px;

    color: #303133;

    line-height: 1.5;

}


.loading-subtitle {

    margin-top: 2px;

    font-size: 9px;

    color: #909399;

}


@keyframes loading-spin {

    from {

        transform: rotate(0deg);

    }

    to {

        transform: rotate(360deg);

    }

}


/* =========================
   Error
========================= */

.message-error .markdown-body {

    border-color: #fbc4c4;

    background: #fef0f0;

    color: #f56c6c;

}


.message-error .message-avatar {

    background: #fef0f0;

}


/* =========================
   输入区域
========================= */

.chat-input-area {

    padding: 13px 18px 14px;

    border-top: 1px solid #ebeef5;

    background: #ffffff;

}


.chat-input-area :deep(.el-textarea__inner) {

    min-height: 72px !important;

    padding: 10px 12px;

    border-radius: 8px;

    border-color: #dcdfe6;

    box-shadow: none;

    font-size: 12px;

    line-height: 1.6;

    transition:
        border-color 0.2s ease,
        box-shadow 0.2s ease;

}


.chat-input-area :deep(.el-textarea__inner:focus) {

    border-color: #409eff;

    box-shadow:
        0 0 0 2px rgba(64, 158, 255, 0.08);

}


.input-footer {

    display: flex;

    align-items: center;

    justify-content: space-between;

    margin-top: 8px;

}


.input-tip {

    display: flex;

    align-items: center;

    gap: 5px;

    color: #a0a4ab;

    font-size: 10px;

}


.tip-key {

    padding: 2px 5px;

    border: 1px solid #dcdfe6;

    border-radius: 4px;

    background: #fafafa;

    color: #909399;

    font-size: 9px;

}


.send-button {

    min-width: 68px;

    height: 32px;

    border-radius: 7px;

    font-size: 11px;

}


/* =========================
   Responsive
========================= */

@media (max-width: 900px) {

    .chat-messages {

        padding: 18px;

    }


    .feature-list {

        max-width: 600px;

    }


    .message-content {

        max-width: 84%;

    }

}


@media (max-width: 600px) {

    .chat-header {

        padding: 12px 14px;

    }


    .chat-header-status {

        display: none;

    }


    .chat-messages {

        padding: 15px;

    }


    .empty-message {

        padding: 20px 10px;

    }


    .feature-list {

        flex-direction: column;

        align-items: stretch;

        max-width: 300px;

    }


    .feature-card {

        max-width: none;

    }


    .example-list {

        flex-direction: column;

    }


    .message-content {

        max-width: 88%;

    }


    .chat-input-area {

        padding: 11px 12px;

    }


    .source-header {

        align-items: flex-start;

    }

}

</style>