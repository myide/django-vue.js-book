
<style>
    .test1 {
        color:red
    }

</style>

<template>
  <div>
    <Button type="primary" @click="showmodal('edit')">修改</Button>
    <Button type="warning" @click="showmodal('delete')" style="float:right">删除</Button>

    <Modal
        v-model="modal1"
        :title="title"
        @on-ok="ok"
        @on-cancel="cancel">

        <div>
            <!-- dom点击事件的写法： @click="clickEvent($event)" -->
            <Button v-for="(item,index) in checksous" :key="index" :class="{'test1':active == item.ids}" v-if="item.nodes==1" :itemtype="item.autotype" @click="clkbtn($event)" :id="item.ids" style="margin-left:20px">{{item.title}}</Button>
            <Button v-else :itemtype='item.autotype' :class="{'test1':active == item.ids}" @click="clkbtn($event)" :id="item.ids" style="margin-left:20px">{{item.autotype}}（{{item.nodes}}）</Button>
        </div>
        </br>
        <div>
            <Row>
                <component v-bind:is="currentView" :action='action' :targetids='targetids' :itemtype='itemtype'>  <!-- 使用动态组件 -->
                </component>
            </Row>
        </div>

    </Modal>

  </div>
</template>

<script>
import all from './all'
import idc from './idc'
import rack from './rack'
import deletecmdb from './delete'
import blank from './blank'

export default {
  components: {all, idc, rack},

  props: ['items'],  // 从父组件获取items

  data () {
      return {
          active: 0,
          modal1: false,
          title:'',
          checksous: {},
          currentView:'',
          // 
          action:'',
          targetids:[],
          itemtype:'',
      }
  },

  methods: {

    // 点击节点
    clkbtn (e) {
        console.log('----: ', e)
        // 获取按钮的id（勾选的节点id集合），根据id的数量，itemtype的类型，action类型；渲染不同的模态框：单个的，批量的
        let id = e.target.id

        if (id == ''){ // 点击的是按钮的文字内容区域
            id = e.target.parentElement.id
            var itemtype = e.target.parentElement.attributes.itemtype.nodeValue
        } else {
            var itemtype = e.target.attributes.itemtype.nodeValue
        }
        var objtitle = e.target.innerText  // 按钮的名字
        if (this.action == 'edit'){
            if (itemtype == 'IDC') {
                this.currentView = all
            } else if (itemtype == 'idc') {
                this.currentView = idc
            } else if (itemtype == 'rack') {
                this.currentView = rack
            }

        } else {
            this.currentView = deletecmdb
            console.log(this.action)
        }
        this.active = id
        this.targetids = id.split(',')
        this.itemtype = itemtype
        console.log(111, this.action, this.targetids, itemtype, e)
    },

    ok () {
        this.$Message.info('Clicked ok');
    },

    cancel () {
        this.$Message.info('Clicked cancel');
    },

    // 点击 修改 或 删除
    showmodal (action) {
        console.log(action)
        this.active = 0  // 防止打开模态框后 显示还是上次点击的
        if (action == 'edit'){
            this.title = '修改资源'
        } else if (action == 'delete'){
            this.title = '删除资源'
        }
        this.action = action

        var sous = {}
        var items = this.items  // 判断items，作不同的渲染
        var res = []
        // items.forEach(item => { 
        for (let i in items){
            let item = items[i]
            var id = item.id
            var title = item.title
            var autotype = item.autotype
            var tag = 0
            if (res != []){
                for (let j in res){
                    let sou = res[j]
                    if (sou.autotype == autotype){
                        sou.nodes += 1
                        sou.ids.push(id)
                        var tag = 1
                        break
                    }
                }
            }

            if (tag == 0){
                res.push({autotype:autotype, nodes:1, ids:[id], title:title})
            }

        }
        this.modal1 = true
        this.checksous = res
        this.currentView = blank  // 点击修改或删除后，用一个空的组件去替代 点击某资源按钮后出现的组件
    }

  }
}
</script>
