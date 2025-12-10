<!-- Version 1.0
Time: Wed Dec 10,17:20
frontend -->

<template>
  <div class="list-container">
    <!-- Bingtian Qiao: 工具栏 -->
    <div class="toolbar">
      <el-button type="primary" @click="openCreate">
        <el-icon><Plus /></el-icon> 新建联系人
      </el-button>
      <div class="right-tools">
        <el-upload
            class="upload-demo" action="#"
            :http-request="handleImport"
            :show-file-list="false" accept=".xlsx"
        >
          <el-button>导入 Excel</el-button>
        </el-upload>
        <el-button @click="handleExport">导出 Excel</el-button>
      </div>
    </div>

    <el-table :data="tableData" style="width: 100%" v-loading="loading" row-key="_id">
      <!-- Bingtian Qiao: 收藏列 -->
      <el-table-column width="60" align="center">
        <template #default="scope">
          <el-icon
              class="star-icon"
              :class="{ active: scope.row.is_favorite }"
              @click="toggleFavorite(scope.row)"
          >
            <StarFilled v-if="scope.row.is_favorite" />
            <Star v-else />
          </el-icon>
        </template>
      </el-table-column>

      <el-table-column prop="name" label="姓名" width="120" show-overflow-tooltip />

      <!-- Bingtian Qiao: 联系方式列表 -->
      <el-table-column label="电话" min-width="160">
        <template #default="scope">
          <div v-if="scope.row.phones && scope.row.phones.length">
            <div v-for="(item, i) in scope.row.phones" :key="i" class="info-row">
              <span class="tag-label">[{{ item.label }}]</span> {{ item.value }}
            </div>
          </div>
          <span v-else class="empty-text">(空)</span>
        </template>
      </el-table-column>

      <el-table-column label="邮箱" min-width="160">
        <template #default="scope">
          <div v-if="scope.row.emails && scope.row.emails.length">
            <div v-for="(item, i) in scope.row.emails" :key="i" class="info-row">
              <span class="tag-label">[{{ item.label }}]</span> {{ item.value }}
            </div>
          </div>
          <span v-else class="empty-text">(空)</span>
        </template>
      </el-table-column>

      <el-table-column label="地址" min-width="180">
        <template #default="scope">
          <div v-if="scope.row.addresses && scope.row.addresses.length">
            <div v-for="(item, i) in scope.row.addresses" :key="i" class="info-row">
              <span class="tag-label">[{{ item.label }}]</span> {{ item.value }}
            </div>
          </div>
          <span v-else class="empty-text">(空)</span>
        </template>
      </el-table-column>

      <!-- Bingtian Qiao: 操作列 -->
      <el-table-column label="操作" width="150" align="right" fixed="right">
        <template #default="scope">
          <el-button size="small" link type="primary" @click="openEdit(scope.row)">编辑</el-button>
          <el-button size="small" link type="danger" @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <ContactForm v-model:visible="dialogVisible" :data="currentContact" @submit="handleSave" />
  </div>
</template>

<script setup>
// Bingtian Qiao: 组件状态与方法
import { ref, onMounted } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import api from '../api';
import ContactForm from './ContactForm.vue';

const tableData = ref([]);
const loading = ref(false);
const dialogVisible = ref(false);
const currentContact = ref(null);

const loadData = async () => {
  loading.value = true;
  try {
    const res = await api.getAll();
    tableData.value = res.data;
  } catch (e) { ElMessage.error('加载失败'); }
  loading.value = false;
};

const toggleFavorite = async (row) => {
  try {
    await api.update(row._id, { is_favorite: !row.is_favorite });
    row.is_favorite = !row.is_favorite;
    loadData();
  } catch (e) { ElMessage.error('操作失败'); }
};

const openCreate = () => { currentContact.value = null; dialogVisible.value = true; };
const openEdit = (row) => { currentContact.value = row; dialogVisible.value = true; };

const handleSave = async (formData) => {
  try {
    if (currentContact.value) {
      await api.update(currentContact.value._id, formData);
      ElMessage.success('更新成功');
    } else {
      await api.create(formData);
      ElMessage.success('创建成功');
    }
    dialogVisible.value = false;
    loadData();
  } catch (e) { ElMessage.error('保存失败'); }
};

const handleDelete = (row) => {
  ElMessageBox.confirm('确认删除?', '提示', { type: 'warning' }).then(async () => {
    await api.delete(row._id);
    loadData();
    ElMessage.success('已删除');
  });
};

const handleImport = async (options) => {
  const formData = new FormData();
  formData.append('file', options.file);
  try {
    await api.import(formData);
    ElMessage.success('导入成功');
    loadData();
  } catch (e) { ElMessage.error('导入失败'); }
};

const handleExport = async () => {
  try {
    const res = await api.export();
    const url = window.URL.createObjectURL(new Blob([res.data]));
    const link = document.createElement('a');
    link.href = url;
    link.download = 'contacts.xlsx';
    document.body.appendChild(link);
    link.click();
  } catch (e) { ElMessage.error('导出失败'); }
};

onMounted(loadData);
</script>

<style scoped>
.toolbar { display: flex; justify-content: space-between; margin-bottom: 20px; padding: 15px; background: white; border-radius: 8px; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }
.right-tools { display: flex; gap: 10px; }
.star-icon { cursor: pointer; color: #cbd5e1; font-size: 1.2rem; transition: all 0.3s; }
.star-icon.active { color: #f59e0b; transform: scale(1.1); }
.info-row { font-size: 13px; margin-bottom: 4px; line-height: 1.4; color: #334155; }
.tag-label { color: #64748b; font-size: 12px; margin-right: 4px; background: #f1f5f9; padding: 1px 4px; border-radius: 4px; }
.empty-text { color: #cbd5e1; font-size: 12px; font-style: italic; }
</style>