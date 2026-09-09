<template>

    <div class="file-manager">

        <!-- =========================
             顶部
        ========================== -->

        <div class="manager-header">

            <div class="manager-title-row">

                <div>

                    <div class="manager-title">
                        知识库文档
                    </div>

                    <div class="manager-desc">
                        管理用于 AI 检索的企业文档
                    </div>

                </div>


                <div class="file-count">
                    {{ files.length }}
                </div>

            </div>


            <el-upload
                action="#"
                :auto-upload="false"
                :show-file-list="false"
                accept=".pdf"
                :on-change="handleUpload"
                :disabled="uploading"
            >

                <el-button
                    type="primary"
                    class="upload-button"
                    :loading="uploading"
                >
                    {{ uploading ? "上传中..." : "上传 PDF" }}
                </el-button>

            </el-upload>

        </div>


        <div class="section-divider"></div>


        <!-- =========================
             文件列表
        ========================== -->

        <div class="file-list">

            <div
                v-if="files.length > 0"
                class="file-items"
            >

                <div
                    v-for="file in files"
                    :key="file.filename"
                    class="file-item"
                >

                    <div class="file-icon">
                        PDF
                    </div>


                    <div class="file-info">

                        <div
                            class="file-name"
                            :title="file.filename"
                        >
                            {{ file.filename }}
                        </div>


                        <div class="file-status">

                            <span class="status-dot"></span>

                            已加入知识库

                        </div>

                    </div>


                    <el-button
                        class="delete-button"
                        text
                        :loading="deletingFile === file.filename"
                        :disabled="deletingFile !== ''"
                        @click="handleDelete(file.filename)"
                    >
                        删除
                    </el-button>

                </div>

            </div>


            <!-- =========================
                 空状态
            ========================== -->

            <div
                v-else
                class="empty-state"
            >

                <div class="empty-icon">
                    <span>＋</span>
                </div>

                <div class="empty-title">
                    暂无知识库文档
                </div>

                <div class="empty-desc">
                    上传 PDF 文档后即可开始智能问答
                </div>

            </div>

        </div>


        <!-- =========================
             底部
        ========================== -->

        <div
            v-if="files.length > 0"
            class="manager-footer"
        >

            <span class="footer-dot"></span>

            <span>
                共 {{ files.length }} 个文档已接入
            </span>

        </div>

    </div>

</template>


<script setup>

import {
    ref,
    onMounted
} from "vue"


import {
    getFiles,
    uploadFile,
    deleteFile
} from "../api/rag"


const files = ref([])


const uploading = ref(false)


const deletingFile = ref("")


async function loadFiles() {

    try {

        const res = await getFiles()

        files.value = res.data

    }

    catch (error) {

        console.error(
            "获取文件列表失败：",
            error
        )

    }

}


async function handleUpload(file) {

    if (
        !file ||
        !file.raw
    ) {

        return

    }


    if (
        file.raw.type !== "application/pdf"
    ) {

        console.warn(
            "目前只支持 PDF 文件"
        )

        return

    }


    try {

        uploading.value = true


        await uploadFile(
            file.raw
        )


        await loadFiles()

    }

    catch (error) {

        console.error(
            "文件上传失败：",
            error
        )

    }

    finally {

        uploading.value = false

    }

}


async function handleDelete(filename) {

    if (!filename) {

        return

    }


    try {

        deletingFile.value = filename


        await deleteFile(
            filename
        )


        await loadFiles()

    }

    catch (error) {

        console.error(
            "文件删除失败：",
            error
        )

    }

    finally {

        deletingFile.value = ""

    }

}


onMounted(() => {

    loadFiles()

})

</script>


<style scoped>

.file-manager {

    height: 100%;

    display: flex;

    flex-direction: column;

    background: #ffffff;

}


/* =========================
   Header
========================= */

.manager-header {

    padding: 16px 16px 14px;

}


.manager-title-row {

    display: flex;

    align-items: flex-start;

    justify-content: space-between;

}


.manager-title {

    font-size: 14px;

    font-weight: 600;

    color: #303133;

}


.manager-desc {

    margin-top: 4px;

    font-size: 10px;

    line-height: 1.5;

    color: #a0a4ab;

}


.file-count {

    min-width: 23px;

    height: 23px;

    padding: 0 6px;

    display: flex;

    align-items: center;

    justify-content: center;

    border-radius: 7px;

    background: #f0f7ff;

    color: #409eff;

    font-size: 10px;

    font-weight: 600;

}


.el-upload {

    display: block;

    width: 100%;

    margin-top: 12px;

}


.upload-button {

    width: 100%;

    height: 32px;

    border-radius: 7px;

    font-size: 11px;

    font-weight: 500;

}


.section-divider {

    height: 1px;

    background: #ebeef5;

}


/* =========================
   File list
========================= */

.file-list {

    flex: 1;

    min-height: 0;

    overflow-y: auto;

    padding: 9px;

}


.file-list::-webkit-scrollbar {

    width: 5px;

}


.file-list::-webkit-scrollbar-thumb {

    border-radius: 10px;

    background: #dcdfe6;

}


.file-list::-webkit-scrollbar-track {

    background: transparent;

}


.file-items {

    display: flex;

    flex-direction: column;

    gap: 5px;

}


/* =========================
   File item
========================= */

.file-item {

    display: flex;

    align-items: center;

    min-height: 55px;

    padding: 8px 7px;

    border: 1px solid transparent;

    border-radius: 8px;

    transition:
        background 0.18s ease,
        border-color 0.18s ease;

}


.file-item:hover {

    background: #f7f9fc;

    border-color: #ebeef5;

}


.file-icon {

    width: 32px;

    height: 35px;

    flex-shrink: 0;

    display: flex;

    align-items: center;

    justify-content: center;

    border-radius: 6px;

    background: #fff1f0;

    color: #f56c6c;

    font-size: 8px;

    font-weight: 700;

    letter-spacing: 0.2px;

}


.file-info {

    flex: 1;

    min-width: 0;

    margin-left: 9px;

}


.file-name {

    overflow: hidden;

    white-space: nowrap;

    text-overflow: ellipsis;

    font-size: 11px;

    line-height: 1.5;

    color: #303133;

}


.file-status {

    display: flex;

    align-items: center;

    gap: 4px;

    margin-top: 2px;

    font-size: 9px;

    color: #a0a4ab;

}


.status-dot {

    width: 5px;

    height: 5px;

    flex-shrink: 0;

    border-radius: 50%;

    background: #67c23a;

}


.delete-button {

    flex-shrink: 0;

    margin-left: 4px;

    padding: 3px 4px;

    color: #a0a4ab;

    font-size: 10px;

}


.delete-button:hover {

    color: #f56c6c;

}


/* =========================
   Empty state
========================= */

.empty-state {

    height: 100%;

    display: flex;

    flex-direction: column;

    align-items: center;

    justify-content: center;

    padding: 25px 12px;

    text-align: center;

}


.empty-icon {

    width: 42px;

    height: 42px;

    display: flex;

    align-items: center;

    justify-content: center;

    border-radius: 11px;

    background: #f5f7fa;

    color: #c0c4cc;

    font-size: 23px;

}


.empty-title {

    margin-top: 10px;

    font-size: 11px;

    font-weight: 500;

    color: #606266;

}


.empty-desc {

    max-width: 180px;

    margin-top: 5px;

    font-size: 9px;

    line-height: 1.6;

    color: #b1b3b8;

}


/* =========================
   Footer
========================= */

.manager-footer {

    display: flex;

    align-items: center;

    gap: 5px;

    padding: 9px 13px;

    border-top: 1px solid #ebeef5;

    background: #fafbfc;

    font-size: 9px;

    color: #a0a4ab;

}


.footer-dot {

    width: 5px;

    height: 5px;

    border-radius: 50%;

    background: #67c23a;

}

</style>