// Version 1.0
// Time: Wed Dec 10,16:20
// frontend

import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

// Bingtian Qiao: 创建 Vue 应用实例并注入根组件 App
const app = createApp(App)

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}

// Bingtian Qiao: 将 Element Plus 插件挂载到应用实例
app.use(ElementPlus)
app.mount('#app')
