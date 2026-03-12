import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'

// Vant组件库
import 'vant/lib/index.css'
import { 
  Button, 
  Field, 
  Form, 
  Uploader, 
  Progress, 
  Toast, 
  Dialog,
  NavBar,
  Tabbar,
  TabbarItem,
  Cell,
  CellGroup,
  Radio,
  RadioGroup,
  Loading,
  Empty
} from 'vant'

const app = createApp(App)
const pinia = createPinia()

// 注册Vant组件
app.use(Button)
app.use(Field)
app.use(Form)
app.use(Uploader)
app.use(Progress)
app.use(Toast)
app.use(Dialog)
app.use(NavBar)
app.use(Tabbar)
app.use(TabbarItem)
app.use(Cell)
app.use(CellGroup)
app.use(Radio)
app.use(RadioGroup)
app.use(Loading)
app.use(Empty)

app.use(pinia)
app.use(router)
app.mount('#app')
