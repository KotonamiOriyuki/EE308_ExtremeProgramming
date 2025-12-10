<!-- Version 1.0
Time: Wed Dec 10,17:02
frontend -->

<template>
  <el-dialog
      :model-value="visible"
      :title="isEdit ? '编辑联系人' : '新建联系人'"
      @close="$emit('update:visible', false)"
      width="600px"
  >
    <el-form :model="form" label-width="80px">
      <el-form-item label="姓名">
        <el-input v-model="form.name" placeholder="请输入姓名" />
      </el-form-item>

      <div v-for="(field, key) in dynamicFields" :key="key" class="field-section">
        <div class="section-header">
          <span>{{ field.title }}</span>
          <el-button link type="primary" @click="addItem(key)">+ 添加</el-button>
        </div>
        <div v-for="(item, index) in form[key]" :key="index" class="dynamic-row">
          <el-input v-model="item.label" placeholder="标签" style="width: 100px" />
          <el-input v-model="item.value" placeholder="内容" style="flex: 1" />
          <el-button type="danger" link @click="removeItem(key, index)">
            <el-icon><Delete /></el-icon>
          </el-button>
        </div>
      </div>
    </el-form>

    <template #footer>
      <el-button @click="$emit('update:visible', false)">取消</el-button>
      <el-button type="primary" @click="save">保存</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, watch } from 'vue';

const props = defineProps(['visible', 'data']);
const emit = defineEmits(['update:visible', 'submit']);

const isEdit = ref(false);
const form = ref({ name: '', phones: [], emails: [], addresses: [], socials: [] });

const dynamicFields = {
  phones: { title: '电话号码' },
  emails: { title: '电子邮箱' },
  addresses: { title: '地址' },
  socials: { title: '社交账号' }
};

// Bingtian Qiao:监听/初始化
watch(() => props.visible, (val) => {
  if (val) {
    if (props.data) {
      form.value = JSON.parse(JSON.stringify(props.data));
      isEdit.value = true;
    } else {
      form.value = { name: '', phones: [], emails: [], addresses: [], socials: [] };
      isEdit.value = false;
    }
  }
});

// Bingtian Qiao:增删保存
const addItem = (key) => form.value[key].push({ label: '', value: '' });
const removeItem = (key, index) => form.value[key].splice(index, 1);
const save = () => emit('submit', form.value);
</script>

<style scoped>
.field-section { margin-bottom: 20px; padding: 10px; background: #f1f5f9; border-radius: 6px; }
.section-header { display: flex; justify-content: space-between; margin-bottom: 10px; font-weight: bold; color: #475569; font-size: 0.9em; }
.dynamic-row { display: flex; gap: 10px; margin-bottom: 8px; }
</style>