<style>
</style>

<template>
    <div>
        <Row>
            
            <Col span="4"> 
                <Card>
                    <Row>
                        <!-- 使用动态组件: 父组件需要在组件和data里设置属性，子组件需要在props里获取这些属性 -->
                        <component v-bind:is="currentView" :items="items">
                        </component>
                    </Row>
                    <div>
                        <Tree :data="data1" @on-select-change="nodeinfo" @on-check-change="nodelist" show-checkbox></Tree> 
                    </div>
                </Card>
            </Col> 

            <Col span="20"> 
                <Card>
                    <div> {{nodecontent}}</div> 
                    <div> ------------------------------------------------ </div>
                    <div v-for="item in items" :key="item.title">
                        {{ item.title }}
                    </div>
                </Card>
            </Col>
        </Row>
    </div>
</template>

<script>
import Vue from 'vue'
//import {Card, Row, Col, Tree, Icon, Button} from 'iview';
import search from './dcomps/search'
import editdeletebtn from './dcomps/editdeletebtn'

export default {
    //components:{Card, Row, Col, Tree, Icon, Button, search, editdeletebtn},
    data () {
        return {
            nodecontent:'',
            data1:[],
            items:[],
            currentView:search,
        }
    },

    methods: {
        nodeinfo (data){
            console.log(data)
            let self = data[0]
            this.nodecontent = self.autotype + '_' + self.title
        },

        nodelist (data){
            console.log(data)
            this.items = data
            if (data.length > 0){  // 有选中的节点，用编辑删除组件
                this.currentView = editdeletebtn
            } else {  // 无选中的节点，用搜索组件
                this.currentView = search
            }
        },

        getTree(tree = []) {
            let arr = [];
            if (!!tree && tree.length !== 0) {
                tree.forEach(item => {
                    let obj = {};
                    obj.id = item.id
                    obj.title = item.title;
                    obj.autotype = item.autotype; // 其他你想要添加的属性
                    obj.expand = false;
                    obj.selected = false;
                    obj.children = this.getTree(item.children); // 递归调用
                    arr.push(obj);
                });
            }
            return arr;
        },

        getdata () {
            const path = this.util.ajax.defaults.baseURL + this.backendsapi.idc
            this.ajax({
                method: 'get',
                url: path,
                data: {}, 
            })

            .then(response => {
                this.data1 = this.getTree(response.data.data)
                console.log(this.data1)
            })

            .catch(error => {
                console.log(error)
            })

        },

    },

    created () {
        //this.data6 = this.getTree(this.data5)
        this.getdata()
    },

}
</script>

